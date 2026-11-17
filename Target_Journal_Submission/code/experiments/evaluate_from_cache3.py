"""v3 evaluation stage (review cycle 1): every method for every (dataset, seed) from cached model outputs.

Changes relative to evaluate_from_cache.py (v2), all decided in response to review cycle 1:
  * location-scale noise density g: RobustLSDensity (KDE + 1% Student-t2 defensive component) fitted to
    CROSS-FITTED standardised residuals (results/raw_contexts_v3, experiments/refit_scales.py);
  * harmonised scale floor max(1e-3 sd(y), 0.05 median|r_oof|) for every method that uses sigma-hat;
  * stratum-exact set geometry (src/methods/ls_exact3.py); half-open stratum pieces for interval methods;
  * domain D intersected with [0, inf) for non-negative targets;
  * new variants: S-NCP-hull, S-NCP-floor, BCCP-floor, SDLC-N (Gaussian-noise ablation);
  * new evaluation strata (top/bottom 1%, deciles of sigma-hat), stratum-wise tilted coverage, effective
    sample sizes, a positive-control shift that re-weights whole strata, infinite-threshold counts.
Writes results/raw_eval_v3/<did>_<seed>.jsonl.
"""
from __future__ import annotations

import json
import os
import sys
import time
import traceback
from multiprocessing import Pool
from pathlib import Path

import numpy as np
from scipy.stats import norm

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from experiments.run_benchmark import CFG, run_methods, split  # noqa: E402
from src.data.openml_ctr23 import load  # noqa: E402
from src.evaluation.metrics import evaluate, wsc  # noqa: E402
from src.methods import conformal as C  # noqa: E402
from src.methods import ls_exact3 as L3  # noqa: E402
from src.methods.strata import ALL_STRATA_SCHEMES, make_partition  # noqa: E402
from src.models import density as D  # noqa: E402

TOP = ROOT.parent
CACHE = Path(os.environ.get("TSCP_CACHE_DIR", TOP / "results" / "raw_contexts"))
CACHE3 = Path(os.environ.get("TSCP_CACHE3_DIR", TOP / "results" / "raw_contexts_v3"))
OUT = Path(os.environ.get("TSCP_EVAL_DIR", TOP / "results" / "raw_eval_v3"))
CORE_LS = ("SDLC-LS", "S-HPD-LS", "DLS-M-LS", "SDLC-LS2", "SDLC-N")


def build_context(c, c3, part, alphas):
    fl = float(c3["floor_new"])
    f = lambda v: np.maximum(np.asarray(v, float), fl)
    hd = D.HistogramDensity(part, CFG["n_coarse"])
    ctx = dict(yc=c["yc"], yt=c["yt"], mu_c=c["mu_c"].astype(float), mu_t=c["mu_t"].astype(float),
               sg_c=f(c["sg_c"]), sg_t=f(c["sg_t"]),
               q_c={a: (c[f"qlo_c_{a}"].astype(float), c[f"qhi_c_{a}"].astype(float)) for a in alphas},
               q_t={a: (c[f"qlo_t_{a}"].astype(float), c[f"qhi_t_{a}"].astype(float)) for a in alphas},
               F_c_H=hd.cells(c["P_c_H"].astype(float)), F_t_H=hd.cells(c["P_t_H"].astype(float)),
               density_tags=("H",), yhat_edges=c["yhat_edges"].astype(float))
    tables = {"LS": L3.LSTable3(D.RobustLSDensity(c3["z_LS_cf"].astype(float))),
              "LS2": L3.LSTable3(D.RobustLSDensity(c3["z_LS2_cf"].astype(float))),
              "N": L3.LSTable3(D.GaussianNoiseDensity())}
    scales = {"LS": (ctx["sg_c"], ctx["sg_c"], ctx["sg_t"], ctx["sg_t"]),
              "N": (ctx["sg_c"], ctx["sg_c"], ctx["sg_t"], ctx["sg_t"]),
              "LS2": (f(c["sm_c"]), f(c["sp_c"]), f(c["sm_t"]), f(c["sp_t"]))}
    return ctx, tables, scales


def interval_extras(ctx, alpha, part, sl):
    """Additional stratified interval variants requested by reviewers."""
    yc = ctx["yc"][sl]
    st_c = part.stratum(yc)
    res_c = np.abs(yc - ctx["mu_c"][sl])
    nres_c = res_c / ctx["sg_c"][sl]
    beta = min(2 * alpha, 0.5)
    out = {}
    sncp = C.interval_method(nres_c, ctx["mu_t"], alpha, part, kind="nres", scale_test=ctx["sg_t"], strata_cal=st_c)
    out["S-NCP-hull"] = C.to_hull(sncp, part)
    out["S-NCP-floor"] = C.interval_method(nres_c, ctx["mu_t"], alpha, part, kind="nres", scale_test=ctx["sg_t"],
                                           strata_cal=st_c, floor_beta=beta)
    out["S-Res-floor"] = C.interval_method(res_c, ctx["mu_t"], alpha, part, kind="res", strata_cal=st_c,
                                           floor_beta=beta)
    return out


def all_sets(ctx, tables, scales, alpha, part, cal_idx=None, which="all", only=None):
    sl = slice(None) if cal_idx is None else cal_idx
    sets = run_methods(ctx, alpha, part, cal_idx=cal_idx, which=which)
    if which == "all":
        sets.update(interval_extras(ctx, alpha, part, sl))
    yc = ctx["yc"][sl]
    st_c = part.stratum(yc)
    for tag in ("LS", "LS2", "N"):
        want_full = which == "all" and tag != "N"
        if only is not None and not any(m.endswith(tag) or f"-{tag}-" in m for m in only):
            continue
        smc, spc, smt, spt = scales[tag]
        sets.update(L3.ls_methods(tables[tag], tag, ctx["mu_c"][sl], smc[sl], spc[sl], yc, ctx["mu_t"], smt, spt,
                                  ctx["yt"], alpha, part, st_c, full=want_full, hpd=(tag == "LS")))
    if only is not None:
        sets = {m: S for m, S in sets.items() if m in only}
    return sets


def eval_strata3(part, yt, sg_t):
    ytr = part.y_train
    dec = np.searchsorted(np.quantile(ytr, np.arange(1, 10) / 10), yt, side="right")
    ext = np.searchsorted(np.quantile(ytr, [0.05, 0.95]), yt, side="right")
    ext1 = np.searchsorted(np.quantile(ytr, [0.01, 0.99]), yt, side="right")
    sig = np.searchsorted(np.quantile(sg_t, np.arange(1, 10) / 10), sg_t, side="right")
    return {"cal": part.stratum(yt), "dec": dec, "ext": ext, "ext1": ext1, "sig": sig}


def shift_weights3(part, yt):
    ytr = np.sort(part.y_train)
    u = (np.searchsorted(ytr, yt, side="right") + 0.5) / (len(ytr) + 1)
    z = norm.ppf(np.clip(u, 1e-4, 1 - 1e-4))
    st = part.stratum(yt)
    pc = np.ones_like(z)
    pc[st == part.K - 1] = 5.0
    pc[st == 0] = 0.5
    return {"up1": np.exp(z), "up2": np.exp(2 * z), "tails1": np.exp(np.abs(z)), "down1": np.exp(-z), "pc": pc}


def n_inf(nk, a):
    return int(sum(int(np.ceil((n + 1) * (1 - a))) > n for n in nk))


def eval_one(did, seed):
    out = OUT / f"{did}_{seed}.jsonl"
    if out.exists():
        return str(out), "skip"
    t0 = time.perf_counter()
    c = dict(np.load(CACHE / f"{did}_{seed}.npz"))
    c3 = dict(np.load(CACHE3 / f"{did}_{seed}.npz"))
    X, y, meta = load(did)
    tr, ca, te = split(len(y), seed)
    assert np.allclose(y[te], c["yt"]) and np.allclose(y[tr], c["y_train"]), "cache/split mismatch"
    Xt = X[te]
    part = make_partition(c["y_train"], n_fine=CFG["n_fine"], n_coarse=CFG["n_coarse"], nonneg=True)
    alphas = CFG["alphas"]
    ctx, tables, scales = build_context(c, c3, part, alphas)
    yt = ctx["yt"]
    es, W = eval_strata3(part, yt, ctx["sg_t"]), shift_weights3(part, yt)
    nk = np.bincount(part.stratum(ctx["yc"]), minlength=part.K)
    base = dict(did=did, dataset=meta["name"], seed=seed, n=meta["n"], p=meta["p"], n_cal=len(ctx["yc"]),
                n_test=len(yt), K=part.K, y_train_sd=float(part.y_train.std()), version="v3",
                test_rmse=float(np.sqrt(np.mean((yt - ctx["mu_t"]) ** 2))),
                frac_test_out_domain=float((~part.in_domain(yt)).mean()), ncal_strata=nk.tolist(),
                ncal_min_stratum=int(nk.min()), floor_new=float(c3["floor_new"]),
                train_stratum_mass=(np.bincount(part.stratum(part.y_train), minlength=part.K)
                                    / len(part.y_train)).round(4).tolist(),
                z_sd_cf=float(np.std(c3["z_LS_cf"])), z_sd_insample=float(np.std(c3["z_LS_insample"])),
                **{f"ess_{k}": float(w.sum() ** 2 / (w ** 2).sum()) for k, w in W.items()})
    for tag in ("LS", "LS2"):
        smt, spt = scales[tag][2], scales[tag][3]
        z, s = L3.zside(yt, ctx["mu_t"], smt, spt)
        base[f"test_nll_{tag}"] = float(-np.mean(np.log(np.maximum(tables[tag].g_at(z) / s, 1e-300))))
    rng = np.random.default_rng(10_000 + seed)
    rows = []
    for a in alphas:
        for m, S in all_sets(ctx, tables, scales, a, part).items():
            r, cov = evaluate(S, yt, part, a, es, W)
            if a == 0.1:
                r["wsc"] = wsc(Xt, cov, seed)
            rows.append({**base, "alpha": a, "scheme": "S5", "cal_frac": 1.0, "method": m,
                         "n_strata_inf": n_inf(nk, a), **r})
        if a != 0.1:
            continue
        for sch in ("S3", "S10"):
            p2 = part.with_strata(ALL_STRATA_SCHEMES[sch])
            nk2 = np.bincount(p2.stratum(ctx["yc"]), minlength=p2.K)
            only = {"S-Res", "S-NCP", "S-CQR", *CORE_LS}
            for m, S in all_sets(ctx, tables, scales, a, p2, which="core", only=only).items():
                r, _ = evaluate(S, yt, p2, a, {**es, "cal": p2.stratum(yt)}, W)
                rows.append({**base, "K": p2.K, "alpha": a, "scheme": sch, "cal_frac": 1.0, "method": m,
                             "n_strata_inf": n_inf(nk2, a), **r})
        for frac in CFG["cal_fracs"]:
            sub = np.sort(rng.choice(len(ctx["yc"]), int(round(frac * len(ctx["yc"]))), replace=False))
            nks = np.bincount(part.stratum(ctx["yc"][sub]), minlength=part.K)
            only = set(CFG["cal_frac_methods"]) | {"SDLC-N"}
            for m, S in all_sets(ctx, tables, scales, a, part, cal_idx=sub, which="all", only=only).items():
                r, _ = evaluate(S, yt, part, a, es, W)
                rows.append({**base, "alpha": a, "scheme": "S5", "cal_frac": frac, "method": m,
                             "n_strata_inf": n_inf(nks, a), **r})
    tmp = out.with_suffix(".tmp")
    with open(tmp, "w") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")
    os.replace(tmp, out)
    return str(out), f"ok {time.perf_counter() - t0:.1f}s"


def _star(a):
    try:
        return eval_one(*a)
    except Exception as e:
        return f"{a}", "FAILED " + repr(e) + traceback.format_exc()[-1500:]


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    workers = int(sys.argv[1]) if len(sys.argv) > 1 else CFG["workers"]
    tasks = sorted({tuple(int(v) for v in p.name.split(".")[0].split("_")) for p in CACHE3.glob("*.npz")
                    if not p.name.endswith(".tmp.npz")})
    with Pool(workers) as pool:
        for name, status in pool.imap_unordered(_star, tasks):
            print(name, status, flush=True)

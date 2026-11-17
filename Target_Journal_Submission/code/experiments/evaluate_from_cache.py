"""Evaluation stage (fit once, evaluate many): recompute EVERY method for every (dataset, seed)
from the cached model outputs written by run_benchmark.py (results/raw_contexts/*.npz).

* interval methods (SCP, NCP, CQR, Mondrian-yhat, S-SCP/BCCP, BCCP-hull, S-NCP, S-CQR): from cached mu,
  sigma and quantile predictions (identical code path as the benchmark);
* histogram-density methods: from cached class probabilities (grid-based, as the estimator is binned);
* location-scale-family methods (DLS, SDLC, S-HPD, HPD-split, DCP, SDLC-floor, SDLC-hull, for LS and
  the exploratory LS2): GRID-FREE exact implementation (src/methods/ls_exact.py).
Writes results/raw_eval/<did>_<seed>.jsonl. Worst-slab coverage re-uses the test covariates rebuilt
from the deterministic split.
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

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from experiments.run_benchmark import CFG, eval_strata_for, run_methods, shift_weights, split  # noqa: E402
from src.data.openml_ctr23 import load  # noqa: E402
from src.evaluation.metrics import evaluate, wsc  # noqa: E402
from src.methods import ls_exact as LX  # noqa: E402
from src.methods.strata import ALL_STRATA_SCHEMES, make_partition  # noqa: E402
from src.models import density as D  # noqa: E402

TOP = ROOT.parent
import os  # noqa: E402
CACHE = Path(os.environ.get("TSCP_CACHE_DIR", TOP / "results" / "raw_contexts"))
OUT = Path(os.environ.get("TSCP_EVAL_DIR", TOP / "results" / "raw_eval"))


def context_from_cache(c, part, alphas):
    hd = D.HistogramDensity(part, CFG["n_coarse"])
    ctx = dict(yc=c["yc"], yt=c["yt"], mu_c=c["mu_c"].astype(float), mu_t=c["mu_t"].astype(float),
               sg_c=c["sg_c"].astype(float), sg_t=c["sg_t"].astype(float),
               q_c={a: (c[f"qlo_c_{a}"].astype(float), c[f"qhi_c_{a}"].astype(float)) for a in alphas},
               q_t={a: (c[f"qlo_t_{a}"].astype(float), c[f"qhi_t_{a}"].astype(float)) for a in alphas},
               F_c_H=hd.cells(c["P_c_H"].astype(float)), F_t_H=hd.cells(c["P_t_H"].astype(float)),
               density_tags=("H",), yhat_edges=c["yhat_edges"].astype(float))
    tables = {"LS": LX.LSTable(D.LocationScaleDensity(part, c["z_LS"].astype(float))),
              "LS2": LX.LSTable(D.LocationScaleDensity(part, c["z_LS2"].astype(float)))}
    scales = {"LS": (c["sg_c"].astype(float), c["sg_c"].astype(float), c["sg_t"].astype(float), c["sg_t"].astype(float)),
              "LS2": (c["sm_c"].astype(float), c["sp_c"].astype(float), c["sm_t"].astype(float), c["sp_t"].astype(float))}
    return ctx, tables, scales


def all_sets(ctx, tables, scales, alpha, part, cal_idx=None, which="all"):
    sets = run_methods(ctx, alpha, part, cal_idx=cal_idx, which=which)
    sl = slice(None) if cal_idx is None else cal_idx
    yc = ctx["yc"][sl]
    st_c = part.stratum(yc)
    for tag in ("LS", "LS2"):
        smc, spc, smt, spt = scales[tag]
        sets.update(LX.ls_methods(tables[tag], tag, ctx["mu_c"][sl], smc[sl], spc[sl], yc, ctx["mu_t"], smt, spt,
                                  ctx["yt"], alpha, part, st_c, full=(which == "all")))
    return sets


def eval_one(did, seed):
    out = OUT / f"{did}_{seed}.jsonl"
    if out.exists():
        return str(out), "skip"
    t0 = time.perf_counter()
    c = dict(np.load(CACHE / f"{did}_{seed}.npz"))
    X, y, meta = load(did)
    tr, ca, te = split(len(y), seed)
    assert np.allclose(y[te], c["yt"]) and np.allclose(y[tr], c["y_train"]), "cache/split mismatch"
    Xt = X[te]
    part = make_partition(c["y_train"], n_fine=CFG["n_fine"], n_coarse=CFG["n_coarse"])
    alphas = CFG["alphas"]
    ctx, tables, scales = context_from_cache(c, part, alphas)
    yt = ctx["yt"]
    es, W = eval_strata_for(part, yt), shift_weights(part, yt)
    base = dict(did=did, dataset=meta["name"], seed=seed, n=meta["n"], p=meta["p"], n_cal=len(ctx["yc"]),
                n_test=len(yt), K=part.K, y_train_sd=float(part.y_train.std()),
                test_rmse=float(np.sqrt(np.mean((yt - ctx["mu_t"]) ** 2))),
                frac_test_out_domain=float((~part.in_domain(yt)).mean()))
    # calibration counts per stratum and how often a stratum threshold is +inf (n_k < 1/alpha - 1)
    nk = np.bincount(part.stratum(ctx["yc"]), minlength=part.K)
    base["ncal_min_stratum"] = int(nk.min())
    base["ncal_strata"] = nk.tolist()
    for a in alphas:
        base[f"n_strata_inf_a{a}"] = int(sum(int(np.ceil((n + 1) * (1 - a))) > n for n in nk))
    base["train_stratum_mass"] = (np.bincount(part.stratum(part.y_train), minlength=part.K) / len(part.y_train)).round(4).tolist()
    for tag in ("LS", "LS2"):
        smt, spt = scales[tag][2], scales[tag][3]
        z, s = LX._z(yt, ctx["mu_t"], smt, spt)
        base[f"test_nll_{tag}"] = float(-np.mean(np.log(np.maximum(tables[tag].g_at(z) / s, 1e-300))))
    base["test_nll_H"] = float(-np.mean(np.log(np.maximum(D.at(ctx["F_t_H"], yt, part), 1e-300))))
    rng = np.random.default_rng(10_000 + seed)
    rows = []
    for a in alphas:
        for m, S in all_sets(ctx, tables, scales, a, part).items():
            r, cov = evaluate(S, yt, part, a, es, W)
            if a == 0.1:
                r["wsc"] = wsc(Xt, cov, seed)
            rows.append({**base, "alpha": a, "scheme": "S5", "cal_frac": 1.0, "method": m, **r})
        if a != 0.1:
            continue
        for sch in ("S3", "S10"):
            p2 = part.with_strata(ALL_STRATA_SCHEMES[sch])
            for m, S in all_sets(ctx, tables, scales, a, p2, which="core").items():
                r, _ = evaluate(S, yt, p2, a, {**es, "cal": p2.stratum(yt)}, W)
                rows.append({**base, "K": p2.K, "alpha": a, "scheme": sch, "cal_frac": 1.0, "method": m, **r})
        for f in CFG["cal_fracs"]:
            sub = np.sort(rng.choice(len(ctx["yc"]), int(round(f * len(ctx["yc"]))), replace=False))
            for m, S in all_sets(ctx, tables, scales, a, part, cal_idx=sub, which="all").items():
                if m in CFG["cal_frac_methods"]:
                    r, _ = evaluate(S, yt, part, a, es, W)
                    rows.append({**base, "alpha": a, "scheme": "S5", "cal_frac": f, "method": m, **r})
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
    tasks = sorted({tuple(int(v) for v in p.stem.split("_")) for p in CACHE.glob("*.npz")})
    with Pool(workers) as pool:
        for name, status in pool.imap_unordered(_star, tasks):
            print(name, status, flush=True)

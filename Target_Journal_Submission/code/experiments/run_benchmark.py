"""Main benchmark: every conformal method on every (dataset, seed).

One JSON-lines file per (dataset, seed) is written to results/raw/ (checkpointing:
existing files are skipped, partial files are written atomically). All numbers in the
manuscript are computed from these files by scripts/analyze.py.
"""
from __future__ import annotations

import argparse
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

from src.data.openml_ctr23 import load  # noqa: E402
from src.evaluation.metrics import evaluate, wsc  # noqa: E402
from src.methods import conformal as C  # noqa: E402
from src.methods.strata import ALL_STRATA_SCHEMES, make_partition  # noqa: E402
from src.models import density as D  # noqa: E402
from src.models import learners as Lr  # noqa: E402

CFG = json.loads((ROOT / "config" / "benchmark.json").read_text())


def split(n, seed, fr=None):
    fr = fr or CFG["split"]
    rng = np.random.default_rng(seed)
    p = rng.permutation(n)
    a = int(round(fr[0] * n))
    b = a + int(round(fr[1] * n))
    return p[:a], p[a:b], p[b:]


# ----------------------------------------------------------------------------- model fitting
def fit_context(X, y, seed, alphas, n_fine, n_jobs, n_coarse=40, idx=None):
    tr, ca, te = idx if idx is not None else split(len(y), seed)
    Xtr, ytr, Xc, yc, Xt, yt = X[tr], y[tr], X[ca], y[ca], X[te], y[te]
    part = make_partition(ytr, n_fine=n_fine, n_coarse=n_coarse)
    timing = {}
    t0 = time.perf_counter()
    mu = Lr.fit_point(Xtr, ytr, seed, n_jobs)
    timing["point"] = time.perf_counter() - t0
    t0 = time.perf_counter()
    sg, oof = Lr.fit_scale(Xtr, ytr, seed, n_jobs, return_oof=True)
    timing["scale"] = time.perf_counter() - t0
    floor = 1e-3 * ytr.std() + 1e-12
    q_c, q_t = {}, {}
    timing["quantile"] = 0.0
    for a in alphas:
        t0 = time.perf_counter()
        ml = Lr.fit_quantile(Xtr, ytr, a / 2, seed, n_jobs)
        mh = Lr.fit_quantile(Xtr, ytr, 1 - a / 2, seed, n_jobs)
        timing["quantile"] += time.perf_counter() - t0
        q_c[a] = (ml.predict(Xc), mh.predict(Xc))
        q_t[a] = (ml.predict(Xt), mh.predict(Xt))
    # histogram density: multiclass GBDT over coarse equal-mass target bins
    t0 = time.perf_counter()
    hd = D.HistogramDensity(part, n_coarse)
    clf = Lr.fit_classifier(Xtr, hd.labels(ytr), hd.n_classes, seed, n_jobs)
    F_c_H = hd.cells(Lr.predict_proba_full(clf, Xc, hd.n_classes))
    F_t_H = hd.cells(Lr.predict_proba_full(clf, Xt, hd.n_classes))
    timing["density_H"] = time.perf_counter() - t0
    # location-scale density: re-uses mu, sigma; KDE of OOF standardised residuals
    t0 = time.perf_counter()
    sg_tr = np.maximum(sg.predict(Xtr), floor)
    lsd = D.LocationScaleDensity(part, (ytr - oof) / sg_tr)
    mu_c, mu_t = mu.predict(Xc), mu.predict(Xt)
    sg_c, sg_t = np.maximum(sg.predict(Xc), floor), np.maximum(sg.predict(Xt), floor)
    F_c_LS, F_t_LS = lsd.cells(mu_c, sg_c), lsd.cells(mu_t, sg_t)
    timing["density_LS"] = time.perf_counter() - t0
    nll = {t: float(-np.mean(np.log(np.maximum(D.at(F, yt, part), 1e-300))))
           for t, F in (("H", F_t_H), ("LS", F_t_LS))}
    ctx = dict(yc=yc, yt=yt, Xt=Xt, mu_c=mu_c, mu_t=mu_t, sg_c=sg_c, sg_t=sg_t,
               q_c=q_c, q_t=q_t, F_c_H=F_c_H, F_t_H=F_t_H, F_c_LS=F_c_LS, F_t_LS=F_t_LS,
               yhat_edges=np.quantile(mu.predict(Xtr), [0.2, 0.4, 0.6, 0.8]),
               test_nll_H=nll["H"], test_nll_LS=nll["LS"],
               n_iter_density=int(clf.best_iteration_ or 0),
               test_rmse=float(np.sqrt(np.mean((yt - mu_t) ** 2))))
    return ctx, part, timing


# ----------------------------------------------------------------------------- methods
def run_methods(ctx, alpha, part, cal_idx=None, which="all", timings=None):
    """Return {method: prediction set}. which='core' -> only the stratification-sensitive
    subset used in the strata-scheme sensitivity analysis."""
    sl = slice(None) if cal_idx is None else cal_idx
    yc = ctx["yc"][sl]
    mu_c, mu_t = ctx["mu_c"][sl], ctx["mu_t"]
    sg_c, sg_t = ctx["sg_c"][sl], ctx["sg_t"]
    has_q = bool(ctx.get("q_c"))
    has_h = "F_c_H" in ctx
    if has_q:
        qlo_c, qhi_c = ctx["q_c"][alpha][0][sl], ctx["q_c"][alpha][1][sl]
        qlo_t, qhi_t = ctx["q_t"][alpha]
    st_c = part.stratum(yc)
    res_c = np.abs(yc - mu_c)
    nres_c = res_c / sg_c
    cqr_c = np.maximum(qlo_c - yc, yc - qhi_c) if has_q else None
    full = which == "all"
    out = {}
    tm = timings if timings is not None else {}

    def put(name, fn):
        t0 = time.perf_counter()
        out[name] = fn()
        tm[name] = time.perf_counter() - t0

    if full:
        put("SCP", lambda: C.interval_method(res_c, mu_t, alpha, part, kind="res"))
        put("NCP", lambda: C.interval_method(nres_c, mu_t, alpha, part, kind="nres", scale_test=sg_t))
        if has_q:
            put("CQR", lambda: C.interval_method(cqr_c, (qlo_t, qhi_t), alpha, part, kind="cqr"))

        def mcp():  # Mondrian conformal regressor on bins of the point prediction
            yb = ctx["yhat_edges"]
            b_c, b_t = np.searchsorted(yb, mu_c), np.searchsorted(yb, mu_t)
            lo, hi = np.empty(len(mu_t)), np.empty(len(mu_t))
            for k in np.unique(b_t):
                t = C.conformal_quantile(res_c[b_c == k], alpha)
                lo[b_t == k], hi[b_t == k] = mu_t[b_t == k] - t, mu_t[b_t == k] + t
            return ("int", np.maximum(lo, part.lo)[:, None], np.minimum(hi, part.hi)[:, None])
        put("MCP-yhat", mcp)
        put("S-NCP", lambda: C.interval_method(nres_c, mu_t, alpha, part, kind="nres",
                                               scale_test=sg_t, strata_cal=st_c))
        if has_q:
            put("S-CQR", lambda: C.interval_method(cqr_c, (qlo_t, qhi_t), alpha, part, kind="cqr",
                                                   strata_cal=st_c))
    put("S-Res", lambda: C.interval_method(res_c, mu_t, alpha, part, kind="res", strata_cal=st_c))
    for tag in (("H", "LS") if has_h else ("LS",)):
        Fc, Ft = ctx[f"F_c_{tag}"][sl], ctx[f"F_t_{tag}"]
        f_c = D.at(Fc, yc, part)
        put(f"DLS-M-{tag}", lambda: C.mask_method(-f_c, Ft, alpha, part))
        put(f"SDLC-{tag}", lambda: C.mask_method(-f_c, Ft, alpha, part, strata_cal=st_c))
        if full:
            def hpd(strat):
                Hc = D.at(D.hpd_value(Fc, part), yc, part)
                return C.mask_method(-Hc, D.hpd_value(Ft, part), alpha, part,
                                     strata_cal=st_c if strat else None)
            put(f"HPD-split-{tag}", lambda: hpd(False))
            put(f"S-HPD-{tag}", lambda: hpd(True))
            put(f"DCP-{tag}", lambda: C.dcp_method(Fc, yc, Ft, alpha, part))
            put(f"SDLC-{tag}-floor", lambda: C.mask_method(-f_c, Ft, alpha, part, strata_cal=st_c,
                                                           floor_beta=min(2 * alpha, 0.5)))
            put(f"SDLC-{tag}-hull", lambda: C.to_hull(out[f"SDLC-{tag}"], part))
    return out


# ----------------------------------------------------------------------------- evaluation helpers
def eval_strata_for(part, yt):
    ytr = part.y_train
    dec = np.searchsorted(np.quantile(ytr, np.arange(1, 10) / 10), yt, side="right")
    ext = np.searchsorted(np.quantile(ytr, [0.05, 0.95]), yt, side="right")
    return {"cal": part.stratum(yt), "dec": dec, "ext": ext}


def shift_weights(part, yt):
    """Importance weights emulating target (label) shift of the test distribution:
    exponential tilting in the normal-score of y under the training distribution."""
    ytr = np.sort(part.y_train)
    u = (np.searchsorted(ytr, yt, side="right") + 0.5) / (len(ytr) + 1)
    z = norm.ppf(np.clip(u, 1e-4, 1 - 1e-4))
    return {"up1": np.exp(1.0 * z), "up2": np.exp(2.0 * z),
            "tails1": np.exp(1.0 * np.abs(z)), "down1": np.exp(-1.0 * z)}


def run_one(did, seed, out_dir, mode):
    out = Path(out_dir) / f"{did}_{seed}.jsonl"
    if out.exists():
        return str(out), "skip"
    X, y, meta = load(did)
    alphas = CFG["alphas"] if mode == "full" else [0.1]
    t_start = time.perf_counter()
    ctx, part, timing = fit_context(X, y, seed, alphas, CFG["n_fine"], CFG["n_jobs_per_task"],
                                    CFG["n_coarse"])
    base = dict(did=did, dataset=meta["name"], seed=seed, n=meta["n"], p=meta["p"],
                n_cal=len(ctx["yc"]), n_test=len(ctx["yt"]), M=part.M, K=part.K,
                test_nll_H=ctx["test_nll_H"], test_nll_LS=ctx["test_nll_LS"],
                test_rmse=ctx["test_rmse"], y_train_sd=float(part.y_train.std()),
                n_iter_density=ctx["n_iter_density"],
                frac_test_out_domain=float((~part.in_domain(ctx["yt"])).mean()),
                **{f"t_fit_{k}": v for k, v in timing.items()})
    yt = ctx["yt"]
    es = eval_strata_for(part, yt)
    W = shift_weights(part, yt)
    rng = np.random.default_rng(10_000 + seed)
    rows = []
    for a in alphas:
        tm = {}
        sets = run_methods(ctx, a, part, which="all", timings=tm)
        for m, S in sets.items():
            r, cov = evaluate(S, yt, part, a, es, W)
            if a == 0.1:
                r["wsc"] = wsc(ctx["Xt"], cov, seed)
            rows.append({**base, "alpha": a, "scheme": "S5", "cal_frac": 1.0, "method": m,
                         "t_calib_predict": tm.get(m, np.nan), **r})
        if a != 0.1:
            continue
        for sch in ("S3", "S10"):   # stratification sensitivity (shared density models)
            p2 = part.with_strata(ALL_STRATA_SCHEMES[sch])
            for m, S in run_methods(ctx, a, p2, which="core").items():
                r, _ = evaluate(S, yt, p2, a, {**es, "cal": p2.stratum(yt)}, W)
                rows.append({**base, "K": p2.K, "alpha": a, "scheme": sch, "cal_frac": 1.0,
                             "method": m, **r})
        for f in CFG["cal_fracs"]:  # calibration-size sensitivity
            sub = np.sort(rng.choice(len(ctx["yc"]), int(round(f * len(ctx["yc"]))), replace=False))
            for m, S in run_methods(ctx, a, part, cal_idx=sub, which="all").items():
                if m in CFG["cal_frac_methods"]:
                    r, _ = evaluate(S, yt, part, a, es, W)
                    rows.append({**base, "alpha": a, "scheme": "S5", "cal_frac": f, "method": m, **r})
    total = time.perf_counter() - t_start
    for r in rows:
        r["t_total_task"] = total
    tmp = out.with_suffix(".tmp")
    with open(tmp, "w") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")
    os.replace(tmp, out)
    return str(out), f"ok {total:.1f}s"


def _star(a):
    try:
        return run_one(*a)
    except Exception as e:  # failures are reported, never hidden
        return f"{a[0]}_{a[1]}", "FAILED " + repr(e) + traceback.format_exc()[-1500:]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", default="full", choices=["quick", "full"])
    ap.add_argument("--datasets", nargs="*", type=int)
    ap.add_argument("--seeds", nargs="*", type=int)
    ap.add_argument("--workers", type=int, default=CFG["workers"])
    ap.add_argument("--out", default=str(ROOT.parent / "results" / "raw"))
    a = ap.parse_args()
    dids = a.datasets or (CFG["quick_datasets"] if a.mode == "quick" else CFG["datasets"])
    seeds = a.seeds if a.seeds else (CFG["seeds"] if a.mode == "full" else [0])
    out = Path(a.out if a.mode == "full" else a.out + "_quick")
    out.mkdir(parents=True, exist_ok=True)
    # largest datasets first for better load balancing
    sizes = {d: load(d)[2]["n"] for d in dids}
    tasks = [(d, s, str(out), a.mode) for s in seeds for d in sorted(dids, key=lambda d: -sizes[d])]
    with Pool(a.workers) as pool:
        for name, status in pool.imap_unordered(_star, tasks):
            print(name, status, flush=True)


if __name__ == "__main__":
    main()

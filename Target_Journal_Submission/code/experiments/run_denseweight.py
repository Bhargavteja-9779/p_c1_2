"""Imbalance-aware learner study (review cycle 1, C1-23): DenseWeight sample weighting
(Steininger, Kobs, Davidson, Krause & Hotho, 2021): w(y) = max(1 - a * p'(y), eps), p' = min-max
normalised KDE density of the TRAINING targets, a = 1, eps = 1e-6, weights rescaled to mean 1.
Mean, quantile and scale models are refitted with these weights; the conformal layer is unchanged (v3).
Question: does imbalance-aware point learning remove the tail under-coverage of marginal conformal
methods, and how does it interact with stratified calibration? 31 datasets x seeds 0-2, alpha = 0.1.
Writes results/raw_denseweight/."""
from __future__ import annotations

import json
import os
import sys
import time
import traceback
from multiprocessing import Pool
from pathlib import Path

import numpy as np
from scipy.stats import gaussian_kde
from sklearn.model_selection import KFold

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from experiments.evaluate_from_cache3 import eval_strata3, interval_extras, shift_weights3  # noqa: E402
from experiments.run_benchmark import CFG, run_methods, split  # noqa: E402
from src.data.openml_ctr23 import load  # noqa: E402
from src.evaluation.metrics import evaluate  # noqa: E402
from src.methods import ls_exact3 as L3  # noqa: E402
from src.methods.strata import make_partition  # noqa: E402
from src.models import density as D  # noqa: E402
from src.models import learners as Lr  # noqa: E402

OUT = ROOT.parent / "results" / "raw_denseweight"
A_DW, EPS_DW = 1.0, 1e-6


def denseweight(y):
    sub = y if len(y) <= 5000 else np.random.default_rng(0).choice(y, 5000, replace=False)
    p = gaussian_kde(sub)(y)
    pn = (p - p.min()) / (p.max() - p.min() + 1e-300)
    w = np.maximum(1 - A_DW * pn, EPS_DW)
    return w / w.mean()


def reg(X, y, seed, w, objective=None, q=None):
    kw = dict(objective="quantile", alpha=q) if objective == "quantile" else {}
    return Lr._fit(Lr.lgb.LGBMRegressor(n_estimators=Lr.MAX_ROUNDS, **kw, **Lr.LGB_PARAMS), X, y, seed, 1,
                   sample_weight=w)


def run_one(did, seed):
    out = OUT / f"{did}_{seed}.jsonl"
    if out.exists():
        return str(out), "skip"
    X, y, meta = load(did)
    tr, ca, te = split(len(y), seed)
    Xtr, ytr, Xc, yc, Xt, yt = X[tr], y[tr], X[ca], y[ca], X[te], y[te]
    part = make_partition(ytr, n_fine=CFG["n_fine"], n_coarse=CFG["n_coarse"], nonneg=True)
    t0 = time.perf_counter()
    w = denseweight(ytr)
    mu = reg(Xtr, ytr, seed, w)
    folds = list(KFold(3, shuffle=True, random_state=seed).split(Xtr))
    oof = np.zeros_like(ytr)
    for k, (a, b) in enumerate(folds):
        oof[b] = reg(Xtr[a], ytr[a], seed + 100 + k, w[a]).predict(Xtr[b])
    r = ytr - oof
    floor = max(1e-3 * ytr.std(), 0.05 * float(np.median(np.abs(r)))) + 1e-12
    sg = reg(Xtr, np.abs(r), seed + 7, w)
    sig_cf = np.zeros_like(ytr)
    for k, (a, b) in enumerate(folds):
        sig_cf[b] = reg(Xtr[a], np.abs(r[a]), seed + 200 + k, w[a]).predict(Xtr[b])
    ql, qh = reg(Xtr, ytr, seed, w, "quantile", 0.05), reg(Xtr, ytr, seed, w, "quantile", 0.95)
    fl = lambda v: np.maximum(v, floor)
    T = L3.LSTable3(D.RobustLSDensity(r / fl(sig_cf)))
    t_fit = time.perf_counter() - t0
    mu_c, mu_t, sg_c, sg_t = mu.predict(Xc), mu.predict(Xt), fl(sg.predict(Xc)), fl(sg.predict(Xt))
    ctx = dict(yc=yc, yt=yt, Xt=Xt, mu_c=mu_c, mu_t=mu_t, sg_c=sg_c, sg_t=sg_t,
               q_c={0.1: (ql.predict(Xc), qh.predict(Xc))}, q_t={0.1: (ql.predict(Xt), qh.predict(Xt))},
               density_tags=(), yhat_edges=np.quantile(mu.predict(Xtr), [0.2, 0.4, 0.6, 0.8]))
    st = part.stratum(yc)
    sets = run_methods(ctx, 0.1, part, which="all")
    sets.update(interval_extras(ctx, 0.1, part, slice(None)))
    sets.update(L3.ls_methods(T, "LS", mu_c, sg_c, sg_c, yc, mu_t, sg_t, sg_t, yt, 0.1, part, st))
    es, W = eval_strata3(part, yt, sg_t), shift_weights3(part, yt)
    kt = part.stratum(yt)
    upper = kt == part.K - 1
    rows = []
    for m, S in sets.items():
        rr, _ = evaluate(S, yt, part, 0.1, es, W)
        rows.append(dict(did=did, dataset=meta["name"], seed=seed, learner="LightGBM+DenseWeight", alpha=0.1,
                         method=m, K=part.K, y_train_sd=float(ytr.std()), t_fit=t_fit,
                         test_rmse=float(np.sqrt(np.mean((yt - mu_t) ** 2))),
                         test_rmse_upper=float(np.sqrt(np.mean((yt[upper] - mu_t[upper]) ** 2))) if upper.any() else None,
                         **rr))
    tmp = out.with_suffix(".tmp")
    with open(tmp, "w") as fh:
        for r_ in rows:
            fh.write(json.dumps(r_) + "\n")
    os.replace(tmp, out)
    return str(out), f"ok {t_fit:.1f}s"


def _star(a):
    try:
        return run_one(*a)
    except Exception as e:
        return f"{a}", "FAILED " + repr(e) + traceback.format_exc()[-1200:]


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    sizes = {d: load(d)[2]["n"] for d in CFG["datasets"]}
    tasks = [(d, s) for s in (0, 1, 2) for d in sorted(CFG["datasets"], key=lambda d: -sizes[d])]
    with Pool(CFG["workers"]) as pool:
        for name, status in pool.imap_unordered(_star, tasks):
            print(name, status, flush=True)

"""Learner generality v3 (review cycle 1, C1-20): MLP mean and scale models with the SAME choices as the
main v3 pipeline: training-only median imputation plus missingness indicators, cross-fitted scale models
for the standardisation of residuals, harmonised scale floor max(1e-3 sd, 0.05 median|r_oof|), robust
KDE noise density and exact geometry. 31 datasets x seeds 0-4, alpha = 0.1, primary strata.
Writes results/raw_mlp_v3/."""
from __future__ import annotations

import json
import os
import sys
import time
import traceback
import warnings
from multiprocessing import Pool
from pathlib import Path

import numpy as np
from sklearn.exceptions import ConvergenceWarning
from sklearn.model_selection import KFold
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from experiments.evaluate_from_cache3 import eval_strata3, interval_extras, shift_weights3  # noqa: E402
from experiments.run_benchmark import CFG, run_methods, split  # noqa: E402
from src.data.openml_ctr23 import load  # noqa: E402
from src.evaluation.metrics import evaluate  # noqa: E402
from src.methods import ls_exact3 as L3  # noqa: E402
from src.methods.strata import make_partition  # noqa: E402
from src.models import density as D  # noqa: E402

warnings.filterwarnings("ignore", category=ConvergenceWarning)
OUT = ROOT.parent / "results" / "raw_mlp_v3"


def mlp(seed):
    return make_pipeline(StandardScaler(), MLPRegressor(hidden_layer_sizes=(128, 64), alpha=1e-4,
                         learning_rate_init=1e-3, batch_size=256, max_iter=200, early_stopping=True,
                         validation_fraction=0.1, n_iter_no_change=10, random_state=seed))


def fit_y(X, y, seed):
    m, s = y.mean(), y.std() + 1e-12
    est = mlp(seed).fit(X, (y - m) / s)
    return lambda Z: est.predict(Z) * s + m


def impute(Xtr, *others):
    med = np.nanmedian(Xtr, axis=0)
    med = np.where(np.isfinite(med), med, 0.0)
    miss = np.isnan(Xtr).any(0)

    def tf(X):
        ind = np.isnan(X[:, miss]).astype(float)
        return np.column_stack([np.where(np.isnan(X), med, X), ind])
    return [tf(Xtr)] + [tf(X) for X in others]


def run_one(did, seed):
    out = OUT / f"{did}_{seed}.jsonl"
    if out.exists():
        return str(out), "skip"
    X, y, meta = load(did)
    tr, ca, te = split(len(y), seed)
    Xtr, Xc, Xt = impute(X[tr], X[ca], X[te])
    ytr, yc, yt = y[tr], y[ca], y[te]
    part = make_partition(ytr, n_fine=CFG["n_fine"], n_coarse=CFG["n_coarse"], nonneg=True)
    t0 = time.perf_counter()
    mu = fit_y(Xtr, ytr, seed)
    folds = list(KFold(3, shuffle=True, random_state=seed).split(Xtr))
    oof = np.zeros_like(ytr)
    for k, (a, b) in enumerate(folds):
        oof[b] = fit_y(Xtr[a], ytr[a], seed + 100 + k)(Xtr[b])
    r = ytr - oof
    floor = max(1e-3 * ytr.std(), 0.05 * float(np.median(np.abs(r)))) + 1e-12
    sg = fit_y(Xtr, np.abs(r), seed + 7)
    sig_cf = np.zeros_like(ytr)
    for k, (a, b) in enumerate(folds):
        sig_cf[b] = fit_y(Xtr[a], np.abs(r[a]), seed + 200 + k)(Xtr[b])
    fl = lambda v: np.maximum(v, floor)
    T = L3.LSTable3(D.RobustLSDensity(r / fl(sig_cf)))
    TN = L3.LSTable3(D.GaussianNoiseDensity())
    mu_c, mu_t, sg_c, sg_t = mu(Xc), mu(Xt), fl(sg(Xc)), fl(sg(Xt))
    t_fit = time.perf_counter() - t0
    ctx = dict(yc=yc, yt=yt, Xt=Xt, mu_c=mu_c, mu_t=mu_t, sg_c=sg_c, sg_t=sg_t, q_c={}, q_t={},
               density_tags=(), yhat_edges=np.quantile(mu(Xtr), [0.2, 0.4, 0.6, 0.8]))
    st = part.stratum(yc)
    sets = run_methods(ctx, 0.1, part, which="all")
    sets.update(interval_extras(ctx, 0.1, part, slice(None)))
    sets.update(L3.ls_methods(T, "LS", mu_c, sg_c, sg_c, yc, mu_t, sg_t, sg_t, yt, 0.1, part, st))
    sets.update(L3.ls_methods(TN, "N", mu_c, sg_c, sg_c, yc, mu_t, sg_t, sg_t, yt, 0.1, part, st, full=False,
                              hpd=False))
    es, W = eval_strata3(part, yt, sg_t), shift_weights3(part, yt)
    rows = []
    for m, S in sets.items():
        rr, _ = evaluate(S, yt, part, 0.1, es, W)
        rows.append(dict(did=did, dataset=meta["name"], seed=seed, learner="MLP", version="v3", alpha=0.1, method=m,
                         K=part.K, n_cal=len(yc), y_train_sd=float(ytr.std()), floor=floor,
                         test_rmse=float(np.sqrt(np.mean((yt - mu_t) ** 2))),
                         scale_spearman_test=float(__import__("scipy").stats.spearmanr(sg_t, np.abs(yt - mu_t))[0]),
                         t_fit=t_fit, **rr))
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
    seeds = [int(s) for s in sys.argv[1:]] or [0, 1, 2, 3, 4]
    sizes = {d: load(d)[2]["n"] for d in CFG["datasets"]}
    tasks = [(d, s) for s in seeds for d in sorted(CFG["datasets"], key=lambda d: -sizes[d])]
    with Pool(CFG["workers"]) as pool:
        for name, status in pool.imap_unordered(_star, tasks):
            print(name, status, flush=True)

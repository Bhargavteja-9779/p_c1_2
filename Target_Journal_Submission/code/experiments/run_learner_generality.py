"""Learner-generality experiment: the same conformal procedures with a multilayer
perceptron (scikit-learn) instead of LightGBM for the mean and scale models.
CQR and the histogram density are omitted (they require quantile / multiclass models).
Pre-registered: all 31 datasets, seeds 0-4, alpha = 0.1, primary strata."""
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
from experiments.run_benchmark import CFG, eval_strata_for, run_methods, shift_weights, split  # noqa: E402
from src.data.openml_ctr23 import load  # noqa: E402
from src.evaluation.metrics import evaluate  # noqa: E402
from src.methods.strata import make_partition  # noqa: E402
from src.models import density as D  # noqa: E402

warnings.filterwarnings("ignore", category=ConvergenceWarning)
OUT = ROOT.parent / "results" / "raw_mlp"


def mlp(seed):
    return make_pipeline(StandardScaler(), MLPRegressor(hidden_layer_sizes=(128, 64), alpha=1e-4,
                         learning_rate_init=1e-3, batch_size=256, max_iter=200, early_stopping=True,
                         validation_fraction=0.1, n_iter_no_change=10, random_state=seed))


def fit_y(X, y, seed):
    m, s = y.mean(), y.std() + 1e-12
    est = mlp(seed).fit(X, (y - m) / s)
    return lambda Z: est.predict(Z) * s + m


def run_one(did, seed):
    out = OUT / f"{did}_{seed}.jsonl"
    if out.exists():
        return str(out), "skip"
    X, y, meta = load(did)
    X = np.nan_to_num(X, nan=0.0)
    tr, ca, te = split(len(y), seed)
    Xtr, ytr, Xc, yc, Xt, yt = X[tr], y[tr], X[ca], y[ca], X[te], y[te]
    part = make_partition(ytr, n_fine=CFG["n_fine"], n_coarse=CFG["n_coarse"])
    t0 = time.perf_counter()
    mu = fit_y(Xtr, ytr, seed)
    oof = np.zeros_like(ytr)
    for k, (a, b) in enumerate(KFold(3, shuffle=True, random_state=seed).split(Xtr)):
        oof[b] = fit_y(Xtr[a], ytr[a], seed + 100 + k)(Xtr[b])
    sg = fit_y(Xtr, np.abs(ytr - oof), seed + 7)
    floor = max(1e-3 * ytr.std(), 1e-12)
    sgf = lambda Z: np.maximum(sg(Z), max(floor, 0.05 * np.median(np.abs(ytr - oof))))
    lsd = D.LocationScaleDensity(part, (ytr - oof) / sgf(Xtr))
    mu_c, mu_t, sg_c, sg_t = mu(Xc), mu(Xt), sgf(Xc), sgf(Xt)
    ctx = dict(yc=yc, yt=yt, Xt=Xt, mu_c=mu_c, mu_t=mu_t, sg_c=sg_c, sg_t=sg_t, q_c={}, q_t={},
               F_c_LS=lsd.cells(mu_c, sg_c), F_t_LS=lsd.cells(mu_t, sg_t),
               yhat_edges=np.quantile(mu(Xtr), [0.2, 0.4, 0.6, 0.8]))
    t_fit = time.perf_counter() - t0
    es, W = eval_strata_for(part, yt), shift_weights(part, yt)
    rows = []
    for m, S in run_methods(ctx, 0.1, part, which="all").items():
        r, _ = evaluate(S, yt, part, 0.1, es, W)
        rows.append(dict(did=did, dataset=meta["name"], seed=seed, learner="MLP", alpha=0.1, method=m,
                         K=part.K, n_cal=len(yc), y_train_sd=float(ytr.std()),
                         test_rmse=float(np.sqrt(np.mean((yt - mu_t) ** 2))), t_fit=t_fit, **r))
    tmp = out.with_suffix(".tmp")
    with open(tmp, "w") as fh:
        for r in rows:
            fh.write(json.dumps(r) + "\n")
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
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    with Pool(CFG["workers"]) as pool:
        for name, status in pool.imap_unordered(_star, tasks):
            print(name, status, flush=True)

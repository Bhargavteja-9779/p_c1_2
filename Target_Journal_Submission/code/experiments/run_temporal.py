"""Temporal and time-blocked splits (review round 5, issue 6; C1-31(d)). Post hoc robustness check, alpha = 0.1,
primary strata, same models and evaluation as run_grouped.py.

  Moneyball (41021), feature f0 = season (1962-2012):
    forward   seasons in time order: earliest seasons -> proper training (about 50% of rows), next -> calibration
              (about 25%), latest -> test; calibration and test are NOT exchangeable (the split itself is the same
              for every seed; seeds vary the models);
    blocked   whole seasons assigned at random to training/calibration/test (50/25/25% of rows), seeds 0-4.
  Bike_Sharing_Demand (44142): the curated OpenML version keeps only month (f0) and hour as time features (no year
  or day), so a temporal order cannot be reconstructed; months are assigned at random as blocks (seeds 0-4).
Writes results/raw_temporal/<did>_<mode>_<seed>.jsonl.
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
from experiments.evaluate_from_cache3 import all_sets, build_context, eval_strata3, shift_weights3  # noqa: E402
from experiments.run_benchmark import CFG, fit_context  # noqa: E402
from experiments.run_grouped import KEEP, crossfit, group_split  # noqa: E402
from src.data.openml_ctr23 import load  # noqa: E402
from src.evaluation.metrics import evaluate  # noqa: E402
from src.methods.strata import make_partition  # noqa: E402
from src.models import learners as Lr  # noqa: E402

OUT = ROOT.parent / "results" / "raw_temporal"


def forward_split(t, fr=(0.5, 0.25)):
    order = np.argsort(t, kind="stable")
    ut = np.unique(t)
    cum = np.cumsum([np.sum(t == u) for u in ut]) / len(t)
    a = ut[cum <= fr[0] + 1e-9]
    b = ut[(cum > fr[0] + 1e-9) & (cum <= fr[0] + fr[1] + 1e-9)]
    tr, ca = np.flatnonzero(np.isin(t, a)), np.flatnonzero(np.isin(t, b))
    te = np.setdiff1d(order, np.concatenate([tr, ca]))
    rng = np.random.default_rng(0)
    return rng.permutation(tr), rng.permutation(ca), rng.permutation(te)


def run(did, mode, seed):
    out = OUT / f"{did}_{mode}_{seed}.jsonl"
    if out.exists():
        return str(out), "skip"
    t0 = time.perf_counter()
    X, y, meta = load(did)
    g = np.round(X[:, 0]).astype(int)            # season (Moneyball) or month (Bike)
    tr, ca, te = forward_split(g) if mode == "forward" else group_split(np.unique(g, return_inverse=True)[1], seed)
    ctx0, _, _ = fit_context(X, y, seed, [0.1], CFG["n_fine"], 1, CFG["n_coarse"], idx=(tr, ca, te))
    c = {k: (np.asarray(v, np.float64) if k.startswith("y") else np.asarray(v, np.float32)) for k, v in ctx0["cache"].items()}
    _, oof = Lr.fit_scale(X[tr], y[tr], seed, 1, return_oof=True)
    c3 = crossfit(X[tr], y[tr], oof, seed)
    part = make_partition(c["y_train"], n_fine=CFG["n_fine"], n_coarse=CFG["n_coarse"], nonneg=True)
    ctx, tables, scales = build_context(c, c3, part, [0.1])
    yt = ctx["yt"]
    es, W = eval_strata3(part, yt, ctx["sg_t"]), shift_weights3(part, yt)
    rows = []
    for m, S in all_sets(ctx, tables, scales, 0.1, part).items():
        if m not in KEEP:
            continue
        r, _ = evaluate(S, yt, part, 0.1, es, W)
        rows.append(dict(did=did, dataset=meta["name"], seed=seed, split=mode, n=len(y),
                         train_blocks=sorted(map(int, np.unique(g[tr]))), test_blocks=sorted(map(int, np.unique(g[te]))),
                         K=part.K, y_train_sd=float(part.y_train.std()), method=m, alpha=0.1, **r))
    tmp = out.with_suffix(".tmp")
    with open(tmp, "w") as fh:
        for r_ in rows:
            fh.write(json.dumps(r_) + "\n")
    os.replace(tmp, out)
    return str(out), f"ok {time.perf_counter() - t0:.1f}s"


def _star(a):
    try:
        return run(*a)
    except Exception as e:
        return f"{a}", "FAILED " + repr(e) + traceback.format_exc()[-1500:]


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    workers = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    tasks = [(41021, m, s) for m in ("forward", "blocked") for s in range(5)] + [(44142, "blocked", s) for s in range(5)]
    with Pool(workers) as pool:
        for name, status in pool.imap_unordered(_star, tasks):
            print(name, status, flush=True)

"""Robustness to repeated units (review cycle 1, C1-31): re-run the v3 pipeline with splits that keep
repeated units together.

  sarcos (44976)             exact duplicate rows removed (the original test set was appended to the
                             training set), then the usual random 50/25/25 split;
  video_transcoding (44974)  grouped by input video: the three columns that take exactly 1,099 distinct
                             values (the number of videos) jointly identify the input video;
  superconductivity (44964)  grouped by identical feature vector (40% of rows share one).
Groups are assigned at random to training (50% of rows), calibration (25%) and test (rest); seeds 0-4;
alpha = 0.1; primary strata. Fitting = run_benchmark.fit_context (same models), cross-fitted scales as in
refit_scales.py, evaluation = evaluate_from_cache3 (same methods and metrics).
Writes results/raw_grouped/<did>_<seed>.jsonl.
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
import pandas as pd
from sklearn.model_selection import KFold

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from experiments.evaluate_from_cache3 import all_sets, build_context, eval_strata3, shift_weights3  # noqa: E402
from experiments.run_benchmark import CFG, fit_context  # noqa: E402
from src.data.openml_ctr23 import load  # noqa: E402
from src.evaluation.metrics import evaluate  # noqa: E402
from src.methods.strata import make_partition  # noqa: E402
from src.models import learners as Lr  # noqa: E402

OUT = ROOT.parent / "results" / "raw_grouped"
KEEP = {"SCP", "NCP", "CQR", "HPD-split-LS", "DLS-M-LS", "S-Res", "S-NCP", "S-CQR", "S-HPD-LS", "SDLC-N", "SDLC-LS"}


def groups_for(did, X, y):
    if did == 44976:                                    # sarcos: drop exact duplicates, then rows are units
        key = pd.util.hash_pandas_object(pd.DataFrame(np.c_[X, y]), index=False).values
        _, first = np.unique(key, return_index=True)
        keep = np.sort(first)
        return keep, np.arange(len(keep)), "dedup"
    if did == 44974:                                    # video_transcoding: input-video identity
        nun = [len(np.unique(X[:, j])) for j in range(X.shape[1])]
        cols = [j for j, u in enumerate(nun) if u == 1099]
        assert len(cols) >= 2, nun
        key = pd.util.hash_pandas_object(pd.DataFrame(X[:, cols]), index=False).values
        return np.arange(len(y)), np.unique(key, return_inverse=True)[1], "by_video"
    if did == 44964:                                    # superconductivity: identical feature vectors
        key = pd.util.hash_pandas_object(pd.DataFrame(X), index=False).values
        return np.arange(len(y)), np.unique(key, return_inverse=True)[1], "by_features"
    raise ValueError(did)


def group_split(g, seed, fr=(0.5, 0.25)):
    rng = np.random.default_rng(5000 + seed)
    ug = rng.permutation(np.unique(g))
    sizes = np.bincount(g)[ug]
    cum = np.cumsum(sizes) / sizes.sum()
    a = ug[cum <= fr[0]]
    b = ug[(cum > fr[0]) & (cum <= fr[0] + fr[1])]
    tr, ca = np.flatnonzero(np.isin(g, a)), np.flatnonzero(np.isin(g, b))
    te = np.setdiff1d(np.arange(len(g)), np.concatenate([tr, ca]))
    return rng.permutation(tr), rng.permutation(ca), rng.permutation(te)


def crossfit(Xtr, ytr, mu_oof, seed, n_jobs=1):
    r = ytr - mu_oof
    floor_new = max(1e-3 * ytr.std(), 0.05 * float(np.median(np.abs(r)))) + 1e-12
    sig_cf, sm_cf, sp_cf = np.zeros_like(ytr), np.zeros_like(ytr), np.zeros_like(ytr)
    for k, (a, b) in enumerate(KFold(3, shuffle=True, random_state=seed).split(Xtr)):
        m = Lr._fit(Lr.lgb.LGBMRegressor(n_estimators=Lr.MAX_ROUNDS, **Lr.LGB_PARAMS), Xtr[a], np.abs(r[a]),
                    seed + 200 + k, n_jobs)
        sig_cf[b] = m.predict(Xtr[b])
        ra = r[a]
        neg, pos = ra < 0, ra > 0
        mm = Lr._fit(Lr.lgb.LGBMRegressor(n_estimators=Lr.MAX_ROUNDS, **Lr.LGB_PARAMS), Xtr[a][neg], -ra[neg],
                     seed + 211 + k, n_jobs)
        mp = Lr._fit(Lr.lgb.LGBMRegressor(n_estimators=Lr.MAX_ROUNDS, **Lr.LGB_PARAMS), Xtr[a][pos], ra[pos],
                     seed + 223 + k, n_jobs)
        sm_cf[b], sp_cf[b] = mm.predict(Xtr[b]), mp.predict(Xtr[b])
    fl = lambda v: np.maximum(v, floor_new)
    return dict(r_oof=r, z_LS_cf=r / fl(sig_cf), z_LS2_cf=np.where(r < 0, r / fl(sm_cf), r / fl(sp_cf)),
                floor_new=np.array(floor_new))


def run(did, seed):
    out = OUT / f"{did}_{seed}.jsonl"
    if out.exists():
        return str(out), "skip"
    t0 = time.perf_counter()
    X, y, meta = load(did)
    keep, g, how = groups_for(did, X, y)
    X, y = X[keep], y[keep]
    tr, ca, te = group_split(g, seed)
    ctx0, _, _ = fit_context(X, y, seed, [0.1], CFG["n_fine"], 1, CFG["n_coarse"], idx=(tr, ca, te))
    c = {k: (np.asarray(v, np.float64) if k.startswith("y") else np.asarray(v, np.float32)) for k, v in ctx0["cache"].items()}
    _, oof = Lr.fit_scale(X[tr], y[tr], seed, 1, return_oof=True)   # same OOF residuals as the main pipeline
    c3 = crossfit(X[tr], y[tr], oof, seed)
    part = make_partition(c["y_train"], n_fine=CFG["n_fine"], n_coarse=CFG["n_coarse"], nonneg=True)
    ctx, tables, scales = build_context(c, c3, part, [0.1])
    yt = ctx["yt"]
    es, W = eval_strata3(part, yt, ctx["sg_t"]), shift_weights3(part, yt)
    gt = g[te]
    rows = []
    for m, S in all_sets(ctx, tables, scales, 0.1, part).items():
        if m not in KEEP:
            continue
        r, _ = evaluate(S, yt, part, 0.1, es, W)
        rows.append(dict(did=did, dataset=meta["name"], seed=seed, split=how, n=len(y), n_groups=int(len(np.unique(g))),
                         test_groups_seen_in_train=float(np.isin(gt, g[tr]).mean()), K=part.K,
                         y_train_sd=float(part.y_train.std()), method=m, alpha=0.1, **r))
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
    workers = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    tasks = [(d, s) for d in (44964, 44976, 44974) for s in range(5)]
    with Pool(workers) as pool:
        for name, status in pool.imap_unordered(_star, tasks):
            print(name, status, flush=True)

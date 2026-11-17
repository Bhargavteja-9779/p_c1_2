"""v3 fitting stage for the scale models (review cycle 1, issues C1-05/C1-06/C1-20).

The noise density g of the location-scale model was previously fitted to out-of-fold residuals
divided by an IN-SAMPLE scale prediction, which shrinks their spread. This script recomputes, with the
same deterministic seeds as the original fitting run,
  * the out-of-fold residuals r_oof (3 folds) and the full-data scale model (checked against cache),
  * CROSS-FITTED scale predictions on the training set: for fold j, a scale model trained on |r_oof|
    of the other folds predicts fold j (symmetric and two-piece versions),
  * the harmonised scale floor max(1e-3 sd(y_tr), 0.05 median|r_oof|) used by every method,
and stores z_LS_cf = r_oof / sigma_cf and z_LS2_cf (side-wise) in results/raw_contexts_v3/.
"""
from __future__ import annotations

import os
import sys
import time
import traceback
from multiprocessing import Pool
from pathlib import Path

import numpy as np
from sklearn.model_selection import KFold

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from experiments.run_benchmark import CFG, split  # noqa: E402
from src.data.openml_ctr23 import load  # noqa: E402
from src.models import learners as Lr  # noqa: E402

TOP = ROOT.parent
CACHE = Path(os.environ.get("TSCP_CACHE_DIR", TOP / "results" / "raw_contexts"))
OUT = Path(os.environ.get("TSCP_CACHE3_DIR", TOP / "results" / "raw_contexts_v3"))


def refit_one(did, seed, n_jobs=1):
    out = OUT / f"{did}_{seed}.npz"
    if out.exists():
        return f"{did}_{seed}", "skip"
    t0 = time.perf_counter()
    X, y, _ = load(did)
    tr, ca, te = split(len(y), seed)
    Xtr, ytr, Xc = X[tr], y[tr], X[ca]
    c = np.load(CACHE / f"{did}_{seed}.npz")
    sg, oof = Lr.fit_scale(Xtr, ytr, seed, n_jobs, return_oof=True)
    floor_old = 1e-3 * ytr.std() + 1e-12
    chk = np.max(np.abs(np.maximum(sg.predict(Xc), floor_old) - c["sg_c"].astype(float)) /
                 (np.abs(c["sg_c"].astype(float)) + floor_old))
    r = ytr - oof
    floor_new = max(1e-3 * ytr.std(), 0.05 * float(np.median(np.abs(r)))) + 1e-12
    sig_cf = np.zeros_like(ytr)
    sm_cf, sp_cf = np.zeros_like(ytr), np.zeros_like(ytr)
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
    z_cf = r / fl(sig_cf)
    z2_cf = np.where(r < 0, r / fl(sm_cf), r / fl(sp_cf))
    sg_tr_in = np.maximum(sg.predict(Xtr), floor_old)
    tmp = out.with_suffix(".tmp.npz")
    np.savez_compressed(tmp, r_oof=r.astype(np.float32), z_LS_cf=z_cf.astype(np.float32),
                        z_LS2_cf=z2_cf.astype(np.float32), floor_new=np.array(floor_new),
                        z_LS_insample=(r / sg_tr_in).astype(np.float32), cache_check=np.array(chk))
    os.replace(tmp, out)
    return f"{did}_{seed}", f"ok {time.perf_counter() - t0:.1f}s check={chk:.2e}"


def _star(a):
    try:
        return refit_one(*a)
    except Exception as e:
        return f"{a}", "FAILED " + repr(e) + traceback.format_exc()[-1200:]


if __name__ == "__main__":
    OUT.mkdir(parents=True, exist_ok=True)
    workers = int(sys.argv[1]) if len(sys.argv) > 1 else CFG["workers"]
    sizes = {d: load(d)[2]["n"] for d in CFG["datasets"]}
    tasks = [(d, s) for s in CFG["seeds"] for d in sorted(CFG["datasets"], key=lambda d: -sizes[d])]
    with Pool(workers) as pool:
        for name, status in pool.imap_unordered(_star, tasks):
            print(name, status, flush=True)

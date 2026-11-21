"""Stratified methods with dedicated 1% tail strata (review round 8, issue 3; requested in review 01). Post hoc.

Scheme S7: stratum edges at the training-target quantiles 0.01, 0.10, 0.25, 0.75, 0.90, 0.99, so the outermost
strata are [q_0.99, inf) and (-inf, q_0.01): stratum-wise calibration then guarantees coverage of the top and bottom
1% of the target distribution directly, the target that RW-DLC addresses through relevance weighting. Uses the cached
model outputs of the held-out replication (no refits); methods BCCP (S-Res), S-NCP, S-HPD and SDLC, alpha = 0.1.
Run with the confirmatory environment variables, e.g.
  TSCP_CONFIG=confirmatory.json TSCP_NMAX=50000 TSCP_CACHE_DIR=../results/confirmatory/raw_contexts \
  TSCP_CACHE3_DIR=../results/confirmatory/raw_contexts_v3 python experiments/eval_tail1.py 3
Writes results/raw_tail1/<did>_<seed>.jsonl.
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
from experiments.evaluate_from_cache3 import (CACHE, CACHE3, all_sets, build_context, eval_strata3,  # noqa: E402
                                              n_inf, shift_weights3)
from experiments.run_benchmark import CFG, split  # noqa: E402
from src.data.openml_ctr23 import load  # noqa: E402
from src.evaluation.metrics import evaluate  # noqa: E402
from src.methods.strata import make_partition  # noqa: E402

OUT = ROOT.parent / "results" / "raw_tail1"
S7 = (0.01, 0.1, 0.25, 0.75, 0.9, 0.99)
ONLY = {"S-Res", "S-NCP", "S-HPD-LS", "SDLC-LS"}


def run(did, seed):
    out = OUT / f"{did}_{seed}.jsonl"
    if out.exists():
        return str(out), "skip"
    t0 = time.perf_counter()
    c = dict(np.load(CACHE / f"{did}_{seed}.npz"))
    c3 = dict(np.load(CACHE3 / f"{did}_{seed}.npz"))
    X, y, meta = load(did)
    tr, ca, te = split(len(y), seed)
    assert np.allclose(y[te], c["yt"]) and np.allclose(y[tr], c["y_train"]), "cache/split mismatch"
    part = make_partition(c["y_train"], n_fine=CFG["n_fine"], n_coarse=CFG["n_coarse"], nonneg=True)
    ctx, tables, scales = build_context(c, c3, part, [0.1])
    yt = ctx["yt"]
    es, W = eval_strata3(part, yt, ctx["sg_t"]), shift_weights3(part, yt)
    p7 = part.with_strata(S7)
    nk = np.bincount(p7.stratum(ctx["yc"]), minlength=p7.K)
    rows = []
    for m, S in all_sets(ctx, tables, scales, 0.1, p7, which="core", only=ONLY).items():
        r, _ = evaluate(S, yt, p7, 0.1, {**es, "cal": p7.stratum(yt)}, W)
        rows.append(dict(did=did, dataset=meta["name"], seed=seed, scheme="S7", K=p7.K, method=m, alpha=0.1,
                         y_train_sd=float(part.y_train.std()), ncal_strata=nk.tolist(),
                         n_strata_inf=n_inf(nk, 0.1), **r))
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
    workers = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    tasks = sorted({tuple(int(v) for v in p.name.split(".")[0].split("_")) for p in CACHE3.glob("*.npz")
                    if not p.name.endswith(".tmp.npz")})
    with Pool(workers) as pool:
        for name, status in pool.imap_unordered(_star, tasks):
            print(name, status, flush=True)

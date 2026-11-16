"""Computational cost of calibration + prediction for every method (Experiment 6).

For seed 0 of every dataset the cached model outputs are loaded and each method is timed
end-to-end (calibration scores, thresholds and prediction sets for the whole test set),
single process, no concurrent jobs, 3 repetitions. Fit times of the underlying models are
recorded separately by the fitting run (results/raw/*.jsonl).
Output: results/timing_methods.csv (dataset, method, repetition, seconds, n_cal, n_test).
"""
from __future__ import annotations

import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from experiments.evaluate_from_cache import CACHE, context_from_cache  # noqa: E402
from experiments.run_benchmark import CFG, run_methods  # noqa: E402
from src.data.openml_ctr23 import load  # noqa: E402
from src.methods import ls_exact as LX  # noqa: E402
from src.methods.conformal import conformal_quantile  # noqa: E402
from src.methods.strata import make_partition  # noqa: E402

OUT = ROOT.parent / "results" / "timing_methods.csv"


def ls_timed(T, tag, mu_c, smc, spc, yc, mu_t, smt, spt, yt, part, st_c, alpha=0.1):
    K = part.K
    out = {}

    def tm(name, fn):
        t0 = time.perf_counter()
        fn()
        out[name] = time.perf_counter() - t0

    def dls():
        sc = LX.scores("density", T, yc, mu_c, smc, spc, part)
        st = LX.scores("density", T, yt, mu_t, smt, spt, part)
        LX.build_sets("density", T, mu_t, smt, spt, np.full(K, conformal_quantile(sc, alpha)), part, yt, st)

    def sdlc():
        sc = LX.scores("density", T, yc, mu_c, smc, spc, part)
        st = LX.scores("density", T, yt, mu_t, smt, spt, part)
        q = np.array([conformal_quantile(sc[st_c == k], alpha) for k in range(K)])
        LX.build_sets("density", T, mu_t, smt, spt, q, part, yt, st)

    def hpd(strat):
        sc = LX.scores("hpd", T, yc, mu_c, smc, spc, part)
        st = LX.scores("hpd", T, yt, mu_t, smt, spt, part)
        q = (np.array([conformal_quantile(sc[st_c == k], alpha) for k in range(K)]) if strat
             else np.full(K, conformal_quantile(sc, alpha)))
        LX.build_sets("hpd", T, mu_t, smt, spt, q, part, yt, st)

    def dcp():
        LX.dcp_sets(T, mu_t, smt, spt, LX.scores("dcp", T, yc, mu_c, smc, spc, part), alpha, part, yt)

    tm(f"DLS-M-{tag}", dls)
    tm(f"SDLC-{tag}", sdlc)
    tm(f"S-HPD-{tag}", lambda: hpd(True))
    tm(f"HPD-split-{tag}", lambda: hpd(False))
    tm(f"DCP-{tag}", dcp)
    return out


def main(reps=3):
    rows = []
    for did in CFG["datasets"]:
        c = dict(np.load(CACHE / f"{did}_0.npz"))
        name = load(did)[2]["name"]
        part = make_partition(c["y_train"], n_fine=CFG["n_fine"], n_coarse=CFG["n_coarse"])
        ctx, tables, scales = context_from_cache(c, part, CFG["alphas"])
        st_c = part.stratum(ctx["yc"])
        for r in range(reps):
            tmd = {}
            run_methods(ctx, 0.1, part, which="all", timings=tmd)
            for tag in ("LS", "LS2"):
                smc, spc, smt, spt = scales[tag]
                tmd.update(ls_timed(tables[tag], tag, ctx["mu_c"], smc, spc, ctx["yc"], ctx["mu_t"], smt, spt,
                                    ctx["yt"], part, st_c))
            for m, sec in tmd.items():
                rows.append(dict(did=did, dataset=name, method=m, rep=r, seconds=sec,
                                 n_cal=len(ctx["yc"]), n_test=len(ctx["yt"])))
        print(name, "done", flush=True)
    pd.DataFrame(rows).to_csv(OUT, index=False)


if __name__ == "__main__":
    main()

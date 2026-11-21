"""Computational cost and grid accuracy of the relevance-weighted study (review round 6).

For seed 0 of every held-out dataset (stored contexts, one thread): set-up times of RW-DLC (relevance KDE, tau,
calibration), per-test-point time of building the sets of RW-DLC, RW-NCP, SDLC-grid and S-NCP on the same grid
implementation as experiments/run_rw.py (G = 4000), and the grid accuracy of RW-DLC (G = 4000 vs 16000: change of
the mean size, maximum relative change of individual sizes) and the peak traced memory of building the RW-DLC sets. Writes results/timing_rw.csv.
"""
import os

for v in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS"):
    os.environ[v] = "1"
import json  # noqa: E402
import sys  # noqa: E402
import time  # noqa: E402
import tracemalloc  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from scipy.stats import gaussian_kde  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from experiments import run_rw as R  # noqa: E402
from src.methods.strata import make_partition  # noqa: E402
from src.models.density import RobustLSDensity  # noqa: E402

OUT = ROOT.parent / "results" / "timing_rw.csv"


def med_time(fn, reps=3):
    fn()
    ts = []
    for _ in range(reps):
        t0 = time.perf_counter()
        fn()
        ts.append(time.perf_counter() - t0)
    return float(np.median(ts))


def one(did, seed=0):
    S = R.SUITES["confirmatory"]
    c, c3 = np.load(S["ctx"] / f"{did}_{seed}.npz"), np.load(S["ctx3"] / f"{did}_{seed}.npz")
    ytr, yc, yt = (c[k].astype(float) for k in ("y_train", "yc", "yt"))
    fl = float(c3["floor_new"])
    mu_c, mu_t = c["mu_c"].astype(float), c["mu_t"].astype(float)
    sg_c, sg_t = np.maximum(c["sg_c"].astype(float), fl), np.maximum(c["sg_t"].astype(float), fl)
    part = make_partition(ytr, nonneg=True)
    g = RobustLSDensity(c3["z_LS_cf"].astype(float))
    fh = lambda y, mu, sg: g.g_at((y - mu) / sg) / sg                                   # noqa: E731
    row = dict(did=did, n_train=len(ytr), n_cal=len(yc), n_test=len(yt))
    t0 = time.perf_counter()
    kde = gaussian_kde(ytr, bw_method="silverman")
    tau = R.TAU_REL * float(kde(ytr).max())
    row["t_relevance_fit_s"] = time.perf_counter() - t0
    pY = lambda y: np.maximum(kde(np.asarray(y, float)), tau)                          # noqa: E731
    ind_c, k_c = part.in_domain(yc), part.stratum(yc)
    t0 = time.perf_counter()
    p_c = pY(yc)
    f_c = fh(yc, mu_c, sg_c)
    s = -(1 / p_c) * f_c
    s[~ind_c] = np.inf
    W = R.WeightedThreshold(s, 1 / p_c)
    row["t_rw_calibration_s"] = time.perf_counter() - t0
    sN = np.abs(yc - mu_c) / sg_c
    sN[~ind_c] = np.inf
    WN = R.WeightedThreshold(sN, 1 / p_c)
    sd = -f_c.copy()
    sd[~ind_c] = np.inf
    q_sdlc = R.stratified_thresholds(sd, k_c, part.K)
    q_sncp = R.stratified_thresholds(sN, k_c, part.K)
    sizes = {}
    for G in (4000, 16000):
        yg = np.linspace(part.lo, part.hi, G)
        dy = yg[1] - yg[0]
        phg = 1 / pY(yg)
        qg, qgN, kg = W(phg), WN(phg), part.stratum(yg)

        def build(kind, store=False):
            out = np.empty(len(yt))
            for a in range(0, len(yt), R.CHUNK):
                b = slice(a, a + R.CHUNK)
                if kind in ("RW-DLC", "SDLC"):
                    Fg = fh(yg[None, :], mu_t[b, None], sg_t[b, None])
                    inc = (-phg[None, :] * Fg <= qg[None, :]) if kind == "RW-DLC" else (-Fg <= q_sdlc[kg][None, :])
                else:
                    Zg = np.abs(yg[None, :] - mu_t[b, None]) / sg_t[b, None]
                    inc = (Zg <= qgN[None, :]) if kind == "RW-NCP" else (Zg <= q_sncp[kg][None, :])
                out[b] = inc.sum(1) * dy
            if store:
                sizes[(kind, G)] = out
            return out
        if G == 4000:
            for kind in ("RW-DLC", "RW-NCP", "SDLC", "S-NCP"):
                row[f"us_per_point_{kind}_G4000"] = 1e6 * med_time(lambda: build(kind)) / len(yt)
        tracemalloc.start()                         # peak traced memory of the RW-DLC sets (chunks of R.CHUNK)
        build("RW-DLC")
        row[f"rw_peak_MB_G{G}"] = tracemalloc.get_traced_memory()[1] / 2 ** 20
        tracemalloc.stop()
        build("RW-DLC", store=True)
    a, b = sizes[("RW-DLC", 4000)], sizes[("RW-DLC", 16000)]
    nz = b > 0
    row["rw_mean_size_rel_change_G4000_vs_16000"] = float(abs(a.mean() / b.mean() - 1))
    row["rw_point_size_max_rel_change"] = float((np.abs(a - b)[nz] / b[nz]).max()) if nz.any() else 0.0
    row["rw_point_size_median_rel_change"] = float(np.median(np.abs(a - b)[nz] / b[nz])) if nz.any() else 0.0
    return row


def main():
    cfg = json.loads((ROOT / "config" / "confirmatory.json").read_text())
    dids = [d if isinstance(d, int) else d["did"] for d in cfg["datasets"]]
    rows = []
    for d in dids:
        r = one(d)
        rows.append(r)
        print(r, flush=True)
    pd.DataFrame(rows).to_csv(OUT, index=False)


if __name__ == "__main__":
    main()

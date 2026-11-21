"""Like-for-like timing of calibration and prediction (review round 6, issue 6).

Replaces the end-to-end timing of experiments/timing.py for the comparison of SDLC with S-NCP and BCCP.
Every method is timed with the same boundaries:
  (a) calibration: from the calibration labels and model outputs to the stratum thresholds
      (score computation + per-stratum conformal quantiles);
  (b) batch prediction: from mu_hat(x), the scale(s) and the thresholds to the prediction sets of the whole
      test set, without labels (SDLC: the piece end-points of the exact geometry; interval methods: one
      interval per stratum clipped to the stratum);
  (c) single-query latency: (b) for one test point at a time (200 random test points; p50 and p99).
Thread variables are set before numpy is imported and checked with threadpoolctl. Seed 0 of all 31 CTR23
datasets; one warm-up, median of 3 repetitions for (a) and (b). Hardware and versions are written to
results/timing_like_env.json. Output: results/timing_like.csv.
"""
import os

for v in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS"):
    os.environ[v] = "1"
import json  # noqa: E402
import platform  # noqa: E402
import sys  # noqa: E402
import time  # noqa: E402
from pathlib import Path  # noqa: E402

import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from threadpoolctl import threadpool_info  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from experiments.evaluate_from_cache3 import CACHE, CACHE3, build_context  # noqa: E402
from experiments.run_benchmark import CFG  # noqa: E402
from src.data.openml_ctr23 import load  # noqa: E402
from src.methods import ls_exact3 as LX  # noqa: E402
from src.methods.conformal import conformal_quantile  # noqa: E402
from src.methods.strata import make_partition  # noqa: E402

OUT = ROOT.parent / "results" / "timing_like.csv"
ENV = ROOT.parent / "results" / "timing_like_env.json"
ALPHA = 0.1


def med(fn, reps=3):
    fn()
    ts = []
    for _ in range(reps):
        t0 = time.perf_counter()
        fn()
        ts.append(time.perf_counter() - t0)
    return float(np.median(ts))


def lat(fn, idx):
    fn(idx[:1])
    ts = []
    for i in idx:
        one = np.array([i])
        t0 = time.perf_counter()
        fn(one)
        ts.append(time.perf_counter() - t0)
    return np.percentile(ts, 50), np.percentile(ts, 99)


def main():
    info = threadpool_info()
    env = {"python": platform.python_version(), "machine": platform.machine(), "processor": platform.processor(),
           "numpy": np.__version__, "pandas": pd.__version__,
           "threadpools": [{k: d.get(k) for k in ("internal_api", "num_threads")} for d in info]}
    try:
        cpu = [ln for ln in open("/proc/cpuinfo") if ln.startswith("model name")]
        env["cpu"] = cpu[0].split(":", 1)[1].strip() if cpu else ""
        env["n_cpu"] = os.cpu_count()
        env["loadavg_start"] = os.getloadavg()
    except OSError:
        pass
    assert all(d.get("num_threads") == 1 for d in info), info
    rows = []
    rng = np.random.default_rng(0)
    for did in CFG["datasets"]:
        c = dict(np.load(CACHE / f"{did}_0.npz"))
        c3 = dict(np.load(CACHE3 / f"{did}_0.npz"))
        name = load(did)[2]["name"]
        part = make_partition(c["y_train"], n_fine=CFG["n_fine"], n_coarse=CFG["n_coarse"], nonneg=True)
        ctx, tables, scales = build_context(c, c3, part, CFG["alphas"])
        T = tables["LS"]
        smc, spc, smt, spt = scales["LS"]
        yc, mu_c, sg_c = ctx["yc"], ctx["mu_c"], ctx["sg_c"]
        mu_t, sg_t = ctx["mu_t"], ctx["sg_t"]
        n, K = len(mu_t), part.K
        E = part.strata_edges.astype(float).copy()
        E[0], E[-1] = part.lo, part.hi
        st_c = part.stratum(yc)

        def thr(sc):
            return np.array([conformal_quantile(sc[st_c == k], ALPHA) for k in range(K)])

        cal = {"SDLC": lambda: thr(LX.scores("density", T, yc, mu_c, smc, spc, part)),
               "S-NCP": lambda: thr(np.abs(yc - mu_c) / sg_c),
               "BCCP": lambda: thr(np.abs(yc - mu_c))}
        q = {m: f() for m, f in cal.items()}
        zero = np.zeros(n)

        def pred_sdlc(i):
            return LX.build_sets("density", T, mu_t[i], smt[i], spt[i], q["SDLC"], part, mu_t[i], zero[i])

        def pred_int(i, m):
            t = q[m]
            s = sg_t[i][:, None] if m == "S-NCP" else 1.0
            lo = np.maximum(mu_t[i][:, None] - t[None, :] * s, E[None, :-1])
            hi = np.minimum(mu_t[i][:, None] + t[None, :] * s, E[None, 1:])
            return lo, np.where(hi > lo, hi, np.nan)

        pred = {"SDLC": pred_sdlc, "S-NCP": lambda i: pred_int(i, "S-NCP"), "BCCP": lambda i: pred_int(i, "BCCP")}
        all_i = np.arange(n)
        one = rng.choice(n, size=min(200, n), replace=False)
        for m in ("SDLC", "S-NCP", "BCCP"):
            p50, p99 = lat(pred[m], one)
            rows.append(dict(did=did, dataset=name, method=m, n_cal=len(yc), n_test=n, K=K,
                             cal_s=med(cal[m]), pred_us_per_point=1e6 * med(lambda: pred[m](all_i)) / n,
                             single_p50_us=1e6 * p50, single_p99_us=1e6 * p99))
        print(name, "done", flush=True)
    env["loadavg_end"] = os.getloadavg()
    pd.DataFrame(rows).to_csv(OUT, index=False)
    ENV.write_text(json.dumps(env, indent=1))


if __name__ == "__main__":
    main()

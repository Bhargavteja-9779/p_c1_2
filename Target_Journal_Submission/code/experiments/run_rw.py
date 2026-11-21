"""Relevance-weighted density-level conformal prediction (RW-DLC) study.

Implements exactly the plan in PREREGISTRATION_relevance_weighted.md (committed before any evaluation):
relevance functions phi_U = 1/max(p_Y, tau) and phi_H = max(p_Y, tau)^(-1/2) fitted on the proper-training targets,
weighted split-conformal calibration with the candidate's own weight placed at +infinity, scores
-phi(y) f(y|x) (RW-DLC), -f(y|x) (RW-DLS) and |y-mu|/sigma (RW-NCP), and comparators SCP, NCP, CQR, DLS-M, S-NCP
and SDLC recomputed on the same y-grid (G = 4000 points over the domain D). alpha = 0.1.

Usage:  python experiments/run_rw.py ctr23 [workers]        (31 datasets x seeds 0-9, contexts from raw_refit_contexts)
        python experiments/run_rw.py confirmatory [workers] (17 held-out datasets x seeds 0-4)
Writes results/rw/<suite>/<did>_<seed>.json (one record per method).
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
from scipy.stats import gaussian_kde

ROOT = Path(__file__).resolve().parents[1]
TOP = ROOT.parent
sys.path.insert(0, str(ROOT))
from src.methods.strata import make_partition  # noqa: E402
from src.models.density import RobustLSDensity  # noqa: E402

ALPHA, G, TAU_REL, CHUNK = 0.1, 4000, 0.01, 400
SUITES = {
    "ctr23": dict(ctx=Path(os.environ.get("TSCP_RW_CTX", TOP / "results" / ("raw_refit_contexts" if (TOP / "results" / "raw_refit_contexts").exists() else "raw_contexts"))),
                  ctx3=TOP / "results" / "raw_contexts_v3",
                  cfg=ROOT / "config" / "benchmark.json", seeds=range(10)),
    "confirmatory": dict(ctx=TOP / "results" / "confirmatory" / "raw_contexts",
                         ctx3=TOP / "results" / "confirmatory" / "raw_contexts_v3",
                         cfg=ROOT / "config" / "confirmatory.json", seeds=range(5)),
}
OUT = TOP / "results" / "rw"


# ----------------------------------------------------------------------------------------------- calibration
def split_threshold(scores, alpha=ALPHA):
    """Unweighted split-conformal threshold: ceil((n+1)(1-alpha))-th smallest score (+inf if rank > n)."""
    s = np.sort(scores)
    r = int(np.ceil((len(s) + 1) * (1 - alpha)))
    return s[r - 1] if r <= len(s) else np.inf


class WeightedThreshold:
    """q(y) = inf{s: sum_i w_i 1{S_i <= s} >= (1-alpha)(sum_i w_i + w(y))}, +inf if unattainable."""

    def __init__(self, scores, weights, alpha=ALPHA):
        o = np.argsort(scores, kind="stable")
        self.s, self.cw = scores[o], np.cumsum(weights[o])
        self.W, self.alpha = self.cw[-1], alpha

    def __call__(self, w_y):
        target = (1 - self.alpha) * (self.W + np.asarray(w_y, float))
        j = np.searchsorted(self.cw, target * (1 - 1e-12), side="left")
        out = np.full(j.shape, np.inf)
        ok = j < len(self.s)
        out[ok] = self.s[j[ok]]
        return out


def stratified_thresholds(scores, strata, K, alpha=ALPHA):
    return np.array([split_threshold(scores[strata == k], alpha) if (strata == k).any() else np.inf
                     for k in range(K)])


# ----------------------------------------------------------------------------------------------- one run
def run(suite, did, seed):
    S = SUITES[suite]
    out = OUT / suite / f"{did}_{seed}.json"
    if out.exists():
        return f"{did}_{seed}", "skip"
    t0 = time.perf_counter()
    c = np.load(S["ctx"] / f"{did}_{seed}.npz")
    c3 = np.load(S["ctx3"] / f"{did}_{seed}.npz")
    ytr, yc, yt = (c[k].astype(float) for k in ("y_train", "yc", "yt"))
    fl = float(c3["floor_new"])
    mu_c, mu_t = c["mu_c"].astype(float), c["mu_t"].astype(float)
    sg_c, sg_t = np.maximum(c["sg_c"].astype(float), fl), np.maximum(c["sg_t"].astype(float), fl)
    qlo_c, qhi_c = c["qlo_c_0.1"].astype(float), c["qhi_c_0.1"].astype(float)
    qlo_t, qhi_t = c["qlo_t_0.1"].astype(float), c["qhi_t_0.1"].astype(float)
    part = make_partition(ytr, nonneg=True)
    lo, hi, K = part.lo, part.hi, part.K
    g = RobustLSDensity(c3["z_LS_cf"].astype(float))
    fh = lambda y, mu, sg: g.g_at((y - mu) / sg) / sg                                  # noqa: E731

    # relevance functions (proper-training targets only)
    kde = gaussian_kde(ytr, bw_method="silverman")
    tau = TAU_REL * float(kde(ytr).max())
    pY = lambda y: np.maximum(kde(np.asarray(y, float)), tau)                       # noqa: E731
    yg = np.linspace(lo, hi, G)
    dy = yg[1] - yg[0]
    p_g, p_c, p_t = pY(yg), pY(yc), pY(yt)
    PHI = {"U": (1 / p_g, 1 / p_c, 1 / p_t), "H": (p_g ** -0.5, p_c ** -0.5, p_t ** -0.5)}
    ind_c, ind_t = part.in_domain(yc), part.in_domain(yt)
    k_c, k_t, k_g = part.stratum(yc), part.stratum(yt), part.stratum(yg)

    # calibration scores (+inf outside D)
    def cal(score):
        s = score.copy()
        s[~ind_c] = np.inf
        return s
    f_c = fh(yc, mu_c, sg_c)
    sc = {"SCP": cal(np.abs(yc - mu_c)), "NCP": cal(np.abs(yc - mu_c) / sg_c),
          "CQR": cal(np.maximum(qlo_c - yc, yc - qhi_c)), "DLS": cal(-f_c)}
    thr = {m: split_threshold(sc[m]) for m in ("SCP", "NCP", "CQR", "DLS")}
    thr_strat = {"S-NCP": stratified_thresholds(sc["NCP"], k_c, K), "SDLC": stratified_thresholds(sc["DLS"], k_c, K)}
    wt = {"RW-DLC-U": WeightedThreshold(cal(-PHI["U"][1] * f_c), PHI["U"][1]),
          "RW-DLS-U": WeightedThreshold(sc["DLS"], PHI["U"][1]),
          "RW-NCP-U": WeightedThreshold(sc["NCP"], PHI["U"][1]),
          "RW-DLC-H": WeightedThreshold(cal(-PHI["H"][1] * f_c), PHI["H"][1])}
    wphi = {"RW-DLC-U": "U", "RW-DLS-U": "U", "RW-NCP-U": "U", "RW-DLC-H": "H"}
    methods = ["SCP", "NCP", "CQR", "DLS-M", "S-NCP", "SDLC", "RW-NCP-U", "RW-DLS-U", "RW-DLC-U", "RW-DLC-H"]

    # test-target coverage by the exact rule
    f_t = fh(yt, mu_t, sg_t)
    r_t = np.abs(yt - mu_t)
    cov, inf_thr = {}, {}
    cov["SCP"] = r_t <= thr["SCP"]
    cov["NCP"] = r_t / sg_t <= thr["NCP"]
    cov["CQR"] = np.maximum(qlo_t - yt, yt - qhi_t) <= thr["CQR"]
    cov["DLS-M"] = -f_t <= thr["DLS"]
    cov["S-NCP"] = r_t / sg_t <= thr_strat["S-NCP"][k_t]
    cov["SDLC"] = -f_t <= thr_strat["SDLC"][k_t]
    for m, W in wt.items():
        ph_t = PHI[wphi[m]][2]
        s_t = {"RW-DLC-U": -PHI["U"][2] * f_t, "RW-DLS-U": -f_t, "RW-NCP-U": r_t / sg_t, "RW-DLC-H": -PHI["H"][2] * f_t}[m]
        q = W(ph_t)
        cov[m] = s_t <= q
        inf_thr[m] = float(np.isinf(q).mean())
    for m in methods:
        cov[m] = cov[m] & ind_t

    # set sizes on the y-grid
    size = {m: np.zeros(len(yt)) for m in methods}
    q_g = {m: W(PHI[wphi[m]][0]) for m, W in wt.items()}
    for a in range(0, len(yt), CHUNK):
        b = slice(a, a + CHUNK)
        Fg = fh(yg[None, :], mu_t[b, None], sg_t[b, None])
        Rg = np.abs(yg[None, :] - mu_t[b, None])
        Zg = Rg / sg_t[b, None]
        inc = {"SCP": Rg <= thr["SCP"], "NCP": Zg <= thr["NCP"],
               "CQR": np.maximum(qlo_t[b, None] - yg[None, :], yg[None, :] - qhi_t[b, None]) <= thr["CQR"],
               "DLS-M": -Fg <= thr["DLS"], "S-NCP": Zg <= thr_strat["S-NCP"][k_g][None, :],
               "SDLC": -Fg <= thr_strat["SDLC"][k_g][None, :],
               "RW-DLC-U": -PHI["U"][0][None, :] * Fg <= q_g["RW-DLC-U"][None, :],
               "RW-DLS-U": -Fg <= q_g["RW-DLS-U"][None, :],
               "RW-NCP-U": Zg <= q_g["RW-NCP-U"][None, :],
               "RW-DLC-H": -PHI["H"][0][None, :] * Fg <= q_g["RW-DLC-H"][None, :]}
        for m in methods:
            size[m][b] = inc[m].sum(1) * dy

    # metrics
    sd = float(ytr.std())
    dec = np.quantile(ytr, np.arange(1, 10) / 10)
    d_t = np.searchsorted(dec, yt, side="right")
    q01, q99 = np.quantile(ytr, [0.01, 0.99])
    top, bot = yt > q99, yt < q01
    # review 5 (issue 5): definition of the main pipeline (half-open groups: y >= q99, y < q01; evaluate_from_cache3)
    top_h, bot_h = yt >= q99, yt < q01
    ess = {k: float(PHI[k][1].sum() ** 2 / (PHI[k][1] ** 2).sum()) for k in PHI}
    rows = []
    for m in methods:
        cv = cov[m].astype(float)
        dcov = [float(cv[d_t == j].mean()) if (d_t == j).any() else np.nan for j in range(10)]
        rows.append(dict(did=did, seed=seed, suite=suite, method=m, n_cal=len(yc), n_test=len(yt),
                         coverage=float(cv.mean()),
                         cov_phiU=float((PHI["U"][2] * cv).sum() / PHI["U"][2].sum()),
                         cov_phiH=float((PHI["H"][2] * cv).sum() / PHI["H"][2].sum()),
                         decile_cov=dcov, macro_decile=float(np.nanmean(dcov)), worst_decile=float(np.nanmin(dcov)),
                         top1_cov=float(cv[top].mean()) if top.any() else np.nan, n_top1=int(top.sum()),
                         bot1_cov=float(cv[bot].mean()) if bot.any() else np.nan, n_bot1=int(bot.sum()),
                         top1h_cov=float(cv[top_h].mean()) if top_h.any() else np.nan, n_top1h=int(top_h.sum()),
                         bot1h_cov=float(cv[bot_h].mean()) if bot_h.any() else np.nan, n_bot1h=int(bot_h.sum()),
                         size=float(size[m].mean() / sd), empty=float((size[m] == 0).mean()),
                         ess_U=ess["U"], ess_H=ess["H"], inf_thr=inf_thr.get(m, np.nan), tau=tau,
                         grid_dy_over_sd=float(dy / sd), seconds=time.perf_counter() - t0))
    out.parent.mkdir(parents=True, exist_ok=True)
    tmp = out.with_suffix(".tmp")
    tmp.write_text(json.dumps(rows))
    os.replace(tmp, out)
    return f"{did}_{seed}", f"ok {time.perf_counter() - t0:.1f}s"


def _star(a):
    try:
        return run(*a)
    except Exception as e:  # failures are reported, never hidden
        return f"{a[1]}_{a[2]}", "FAILED " + repr(e) + traceback.format_exc()[-1200:]


def main():
    suite = sys.argv[1]
    workers = int(sys.argv[2]) if len(sys.argv) > 2 else 4
    S = SUITES[suite]
    cfg = json.loads(S["cfg"].read_text())
    dids = [d if isinstance(d, int) else d["did"] for d in cfg["datasets"]]
    tasks = [(suite, d, s) for s in S["seeds"] for d in dids if (S["ctx"] / f"{d}_{s}.npz").exists()]
    print(f"{len(tasks)} tasks", flush=True)
    with Pool(workers) as pool:
        for name, status in pool.imap_unordered(_star, tasks):
            print(name, status, flush=True)


if __name__ == "__main__":
    main()

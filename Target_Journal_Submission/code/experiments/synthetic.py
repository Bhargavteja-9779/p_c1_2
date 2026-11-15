"""Synthetic study with a KNOWN conditional density (verifies Theorem 1 and Proposition 1).

Y = mu(X) + sigma(X) * eps, X ~ U[-1,1]^5, eps = standardised Gamma(2) (right-skewed).
Oracle scores use the true mu, sigma, density; 'estimated' scores use the same LightGBM
pipeline as the benchmark. Each method is calibrated by split conformal.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from scipy.stats import gamma

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from experiments.run_benchmark import eval_strata_for, fit_context, run_methods  # noqa: E402
from src.evaluation.metrics import evaluate  # noqa: E402
from src.methods import conformal as C  # noqa: E402
from src.models import density as D  # noqa: E402
from src.methods import ls_exact as LX  # noqa: E402

K_SHAPE = 2.0
OUT = ROOT.parent / "results" / "synthetic.jsonl"


def g_pdf(z):
    return gamma.pdf(z * np.sqrt(K_SHAPE) + K_SHAPE, K_SHAPE) * np.sqrt(K_SHAPE)


def mu_f(X):
    return 2 * np.sin(np.pi * X[:, 0]) + 2 * X[:, 1] ** 2 + X[:, 2]


def sig_f(X):
    return 0.2 + 0.8 * np.abs(X[:, 3])


def sample(n, rng):
    X = rng.uniform(-1, 1, (n, 5))
    eps = (rng.gamma(K_SHAPE, 1.0, n) - K_SHAPE) / np.sqrt(K_SHAPE)
    return X, mu_f(X) + sig_f(X) * eps


def hdr_z(alpha):
    z = np.linspace(-np.sqrt(K_SHAPE) + 1e-9, 12, 200_001)
    g = g_pdf(z)
    o = np.argsort(-g)
    m = np.cumsum(g[o]) * (z[1] - z[0])
    sel = o[: np.searchsorted(m, 1 - alpha) + 1]
    return z[sel].min(), z[sel].max()


def run(seed, n_tr=5000, n_cal=5000, n_te=20000, alpha=0.1):
    rng = np.random.default_rng(seed)
    X, y = sample(n_tr + n_cal + n_te, rng)
    idx = (np.arange(n_tr), np.arange(n_tr, n_tr + n_cal), np.arange(n_tr + n_cal, len(y)))
    ctx, part, _ = fit_context(X, y, seed, [alpha], 200, 1, 40, idx=idx)
    Xc, Xt = X[idx[1]], X[idx[2]]
    yc, yt = ctx["yc"], ctx["yt"]
    es = eval_strata_for(part, yt)
    rows = []
    # estimated pipeline (same code as the final evaluation: grid-free location-scale family)
    c = ctx["cache"]
    ctx["density_tags"] = ("H",)
    est = run_methods(ctx, alpha, part, which="all")
    stc = part.stratum(yc)
    est.update(LX.ls_methods(LX.LSTable(D.LocationScaleDensity(part, c["z_LS"])), "LS", c["mu_c"], c["sg_c"],
                             c["sg_c"], yc, c["mu_t"], c["sg_t"], c["sg_t"], yt, alpha, part, stc))
    est.update(LX.ls_methods(LX.LSTable(D.LocationScaleDensity(part, c["z_LS2"])), "LS2", c["mu_c"], c["sm_c"],
                             c["sp_c"], yc, c["mu_t"], c["sm_t"], c["sp_t"], yt, alpha, part, stc))
    for m, S in est.items():
        r, _ = evaluate(S, yt, part, alpha, es)
        rows.append({"seed": seed, "scores": "estimated", "method": m, **r})
    # oracle scores
    mu_c, mu_t, s_c, s_t = mu_f(Xc), mu_f(Xt), sig_f(Xc), sig_f(Xt)
    st = part.stratum(yc)
    zl, zh = hdr_z(alpha)

    class _TrueG:  # exact table of the true standardised noise density
        grid = np.linspace(-np.sqrt(K_SHAPE) + 1e-9, 14.0, 8192)
        g = np.maximum(g_pdf(grid), 1e-12)
        gfloor = 1e-12
    T = LX.LSTable(_TrueG(), n_set_grid=4096)
    ex = LX.ls_methods(T, "O", mu_c, s_c, s_c, yc, mu_t, s_t, s_t, yt, alpha, part, st, full=False)
    oracle = {
        "O-HDR-X (exact X-conditional)": ("int", np.maximum(mu_t + zl * s_t, part.lo)[:, None],
                                          np.minimum(mu_t + zh * s_t, part.hi)[:, None]),
        "O-DLS-M": ex["DLS-M-O"],
        "O-S-Res": C.interval_method(np.abs(yc - mu_c), mu_t, alpha, part, kind="res", strata_cal=st),
        "O-S-NCP": C.interval_method(np.abs(yc - mu_c) / s_c, mu_t, alpha, part, kind="nres",
                                     scale_test=s_t, strata_cal=st),
        "O-S-HPD": ex["S-HPD-O"],
        "O-SDLC": ex["SDLC-O"],
    }
    for m, S in oracle.items():
        r, _ = evaluate(S, yt, part, alpha, es)
        rows.append({"seed": seed, "scores": "oracle", "method": m, **r})
    return rows


if __name__ == "__main__":
    seeds = range(int(sys.argv[1]) if len(sys.argv) > 1 else 10)
    with open(OUT, "w") as fh:
        for s in seeds:
            for r in run(s):
                fh.write(json.dumps(r) + "\n")
            print("seed", s, "done", flush=True)

"""Proposition 1: target-conditional coverage of the ORACLE X-conditional interval in the
Gaussian model X ~ N(0, tau^2), Y | X ~ N(X, sigma^2). Closed form vs Monte Carlo."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
from scipy import integrate
from scipy.stats import norm

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT.parent / "results" / "prop1_gaussian.json"


def pointwise_cov(y, r2, alpha=0.1):
    """P(|Y - X| <= z*sigma | Y = y) with tau^2 = r2, sigma^2 = 1 - r2 (Var Y = 1)."""
    tau2, s2 = r2, 1 - r2
    z = norm.ppf(1 - alpha / 2)
    m = (1 - r2) * y            # E[Y - X | Y = y] = sigma^2/(tau^2+sigma^2) * y
    sd = np.sqrt(tau2 * s2)     # sd(Y - X | Y = y) (Var Y = 1)
    sig = np.sqrt(s2)
    return norm.cdf((z * sig - m) / sd) - norm.cdf((-z * sig - m) / sd)


def stratum_cov(lo_q, hi_q, r2, alpha=0.1):
    a, b = norm.ppf(lo_q), norm.ppf(hi_q)
    num = integrate.quad(lambda y: pointwise_cov(y, r2, alpha) * norm.pdf(y), a, b)[0]
    return num / (hi_q - lo_q)


def monte_carlo(r2, alpha=0.1, n=2_000_000, seed=0):
    rng = np.random.default_rng(seed)
    x = rng.normal(0, np.sqrt(r2), n)
    y = x + rng.normal(0, np.sqrt(1 - r2), n)
    cov = np.abs(y - x) <= norm.ppf(1 - alpha / 2) * np.sqrt(1 - r2)
    q = np.quantile(y, [0.1, 0.9])
    return {"marginal": float(cov.mean()), "upper10": float(cov[y > q[1]].mean()),
            "lower10": float(cov[y < q[0]].mean()), "central80": float(cov[(y >= q[0]) & (y <= q[1])].mean())}


def main():
    res = {"model": "X~N(0,R2), Y|X~N(X,1-R2), oracle interval X +- z sigma, alpha=0.1", "rows": []}
    for r2 in (0.3, 0.5, 0.7, 0.9, 0.95):
        row = {"R2": r2,
               "analytic_upper10": stratum_cov(0.9, 1 - 1e-12, r2),
               "analytic_upper1": stratum_cov(0.99, 1 - 1e-12, r2),
               "analytic_central80": stratum_cov(0.1, 0.9, r2),
               "mc": monte_carlo(r2)}
        res["rows"].append(row)
        print(json.dumps(row))
    ys = np.linspace(-3.5, 3.5, 141)
    res["curve"] = {"y": ys.tolist(), **{str(r2): pointwise_cov(ys, r2).tolist() for r2 in (0.3, 0.5, 0.7, 0.9)}}
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()

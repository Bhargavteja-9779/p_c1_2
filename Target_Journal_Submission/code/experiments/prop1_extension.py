"""Extension of Proposition 1 beyond the Gaussian model (review cycle 1, C1-14).
Monte Carlo (2e6 draws) coverage of the ORACLE covariate-conditional set within target strata.
  (i)  heavy-tailed signal: X = sqrt(R2) * t_nu / sd(t_nu), Y | X ~ N(X, 1 - R2), oracle set X +- z sigma
  (ii) skewed noise: X ~ N(0, R2), Y = X + sigma * eps, eps = standardised Gamma(2); oracle set = X + shortest
       (highest-density) 90% interval of sigma * eps.
Reported: coverage among the bottom 10%, central 80%, top 10% and top 1% of Y."""
import json
from pathlib import Path

import numpy as np
from scipy import stats

OUT = Path(__file__).resolve().parents[2] / "results" / "prop1_extension.json"
A = 0.1


def strata_cov(y, cov):
    q = np.quantile(y, [0.1, 0.9, 0.99])
    return {"bottom10": float(cov[y < q[0]].mean()), "central80": float(cov[(y >= q[0]) & (y <= q[1])].mean()),
            "top10": float(cov[y > q[1]].mean()), "top1": float(cov[y > q[2]].mean()), "marginal": float(cov.mean())}


def gamma_hdr():
    z = np.linspace(-np.sqrt(2) + 1e-9, 15, 400001)
    g = stats.gamma.pdf(z * np.sqrt(2) + 2, 2) * np.sqrt(2)
    o = np.argsort(-g)
    m = np.cumsum(g[o]) * (z[1] - z[0])
    sel = o[: np.searchsorted(m, 1 - A) + 1]
    return z[sel].min(), z[sel].max()


def main(n=2_000_000):
    rng = np.random.default_rng(0)
    rows = []
    z = stats.norm.ppf(1 - A / 2)
    for r2 in (0.5, 0.9):
        sig = np.sqrt(1 - r2)
        for nu in (3, 5, 30):
            x = np.sqrt(r2) * rng.standard_t(nu, n) / np.sqrt(nu / (nu - 2))
            y = x + rng.normal(0, sig, n)
            rows.append({"model": f"t{nu} signal, Gaussian noise", "R2": r2,
                         **strata_cov(y, np.abs(y - x) <= z * sig)})
        x = rng.normal(0, np.sqrt(r2), n)
        eps = (rng.gamma(2, 1, n) - 2) / np.sqrt(2)
        y = x + sig * eps
        lo, hi = gamma_hdr()
        rows.append({"model": "Gaussian signal, Gamma(2) noise", "R2": r2,
                     **strata_cov(y, (y - x >= sig * lo) & (y - x <= sig * hi))})
    OUT.write_text(json.dumps(rows, indent=1))
    for r in rows:
        print({k: (round(v, 3) if isinstance(v, float) else v) for k, v in r.items()})


if __name__ == "__main__":
    main()

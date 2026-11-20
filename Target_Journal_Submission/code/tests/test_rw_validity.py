"""Monte Carlo check of the weighted split-conformal rule used by RW-DLC (experiments/run_rw.py):
relevance-weighted coverage E[phi(Y)1{covered}]/E[phi(Y)] must be >= 1 - alpha (up to MC error), with phi = 1/p_Y."""
import numpy as np
from scipy.stats import norm

from experiments.run_rw import WeightedThreshold


def test_weighted_coverage_heavy_tail():
    rng = np.random.default_rng(1)
    alpha, reps, ncal, ntest = 0.1, 300, 300, 300
    num = den = 0.0
    for _ in range(reps):
        x = rng.normal(size=ncal + ntest)
        y = x + rng.standard_t(3, size=ncal + ntest)
        mu, f = x, lambda y_, m_: np.exp(-0.5 * (y_ - m_) ** 2)       # deliberately wrong density model
        p = norm.pdf(y, 0, np.sqrt(4))                                # relevance: inverse (approx.) target density
        phi = 1 / np.maximum(p, 0.01 * p.max())
        sc = -phi[:ncal] * f(y[:ncal], mu[:ncal])
        W = WeightedThreshold(sc, phi[:ncal], alpha)
        st = -phi[ncal:] * f(y[ncal:], mu[ncal:])
        cov = st <= W(phi[ncal:])
        num += (phi[ncal:] * cov).sum()
        den += phi[ncal:].sum()
    assert num / den >= 1 - alpha - 0.01, num / den


def test_unweighted_reduces_to_split():
    s = np.arange(1.0, 20.0)
    W = WeightedThreshold(s, np.ones_like(s), 0.1)
    # ceil((19+1)*0.9) = 18th smallest
    assert W(np.array([1.0]))[0] == 18.0

"""Tests for the v3 location-scale implementation: geometry vs brute force, interval membership vs
exact score rule, and Monte-Carlo stratum-wise validity."""
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.evaluation.metrics import covered, sizes  # noqa: E402
from src.methods import ls_exact3 as L3  # noqa: E402
from src.methods.conformal import conformal_quantile  # noqa: E402
from src.methods.strata import make_partition  # noqa: E402
from src.models.density import RobustLSDensity  # noqa: E402


def _setup(seed=0, n=3000, heavy=False):
    rng = np.random.default_rng(seed)
    z = rng.standard_t(3, n) if heavy else (rng.gamma(2, 1, n) - 2) / np.sqrt(2)
    ytr = rng.normal(0, 2, 4000) + rng.standard_exponential(4000)
    part = make_partition(ytr)
    T = L3.LSTable3(RobustLSDensity(z))
    return rng, part, T


def test_size_matches_brute_force():
    for heavy in (False, True):
        rng, part, T = _setup(1, heavy=heavy)
        n = 40
        mu, sm, sp = rng.normal(0, 1, n), rng.uniform(0.3, 2, n), rng.uniform(0.3, 2, n)
        thr = -np.array([0.02, 0.05, 0.08, 0.05, 0.01])[: part.K]
        y_dummy = np.zeros(n)
        S = L3.build_sets("density", T, mu, sm, sp, thr, part, y_dummy, np.zeros(n))
        yy = np.linspace(part.lo, part.hi, 400001)
        dy = yy[1] - yy[0]
        for i in range(n):
            sc = L3.scores("density", T, yy, np.full_like(yy, mu[i]), np.full_like(yy, sm[i]), np.full_like(yy, sp[i]), part)
            member = sc <= thr[part.stratum(yy)]
            bf = member.sum() * dy
            assert abs(S[1][i] - bf) <= 0.01 * max(bf, 1e-3) + 5 * dy, (heavy, i, S[1][i], bf)


def test_membership_matches_exact_rule():
    rng, part, T = _setup(2)
    n = 60
    mu, sm, sp = rng.normal(0, 1, n), rng.uniform(0.3, 2, n), rng.uniform(0.3, 2, n)
    thr = -np.array([0.03, 0.06, 0.1, 0.06, 0.02])[: part.K]
    (S, iv) = L3.build_sets("density", T, mu, sm, sp, thr, part, np.zeros(n), np.zeros(n), return_intervals=True)
    disagree, total = 0, 0
    for i in range(n):
        yy = rng.uniform(part.lo, part.hi, 2000)
        sc = L3.scores("density", T, yy, np.full_like(yy, mu[i]), np.full_like(yy, sm[i]), np.full_like(yy, sp[i]), part)
        exact = sc <= thr[part.stratum(yy)]
        geo = np.zeros_like(exact)
        for a, b in iv[i]:
            geo |= (yy >= a) & (yy <= b)
        disagree += (exact != geo).sum()
        total += len(yy)
    assert disagree / total < 2e-3, disagree / total


def test_stratum_validity_monte_carlo():
    rng = np.random.default_rng(3)
    ytr = rng.normal(size=4000) + rng.standard_exponential(4000)
    part = make_partition(ytr)
    K = part.K
    T = L3.LSTable3(RobustLSDensity(rng.normal(size=2000)))
    cov, cnt = np.zeros(K), np.zeros(K)
    for r in range(300):
        yc = rng.normal(size=300) + rng.standard_exponential(300)
        yt = rng.normal(size=300) + rng.standard_exponential(300)
        mu_c, mu_t = np.full(300, 0.4), np.full(300, 0.4)
        s_c, s_t = np.full(300, 1.1), np.full(300, 1.1)
        st = part.stratum(yc)
        sc = L3.scores("density", T, yc, mu_c, s_c, s_c, part)
        q = np.array([conformal_quantile(sc[st == k], 0.1) for k in range(K)])
        S = L3.build_sets("density", T, mu_t, s_t, s_t, q, part, yt,
                          L3.scores("density", T, yt, mu_t, s_t, s_t, part))
        c = covered(S, yt, part)
        stt = part.stratum(yt)
        for k in range(K):
            cov[k] += c[stt == k].sum()
        cnt += np.bincount(stt, minlength=K)
    cv = cov / cnt
    assert np.all(cv >= 0.9 - 3 * np.sqrt(0.09 / cnt) - 0.005), cv

"""Correctness tests: finite-sample validity of every conformal procedure (Monte Carlo),
nesting of partitions, hull/floor supersets, and agreement of interval and mask paths."""
import sys
from pathlib import Path

import numpy as np
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from src.evaluation.metrics import covered, sizes  # noqa: E402
from src.methods import conformal as C  # noqa: E402
from src.methods.strata import make_partition  # noqa: E402
from src.models import density as D  # noqa: E402


def _data(rng, n):
    x = rng.uniform(-1, 1, n)
    y = np.sin(3 * x) + (0.2 + 0.5 * np.abs(x)) * rng.standard_exponential(n)
    return x, y


def test_conformal_quantile_rank():
    s = np.arange(1, 10, dtype=float)  # n = 9
    assert C.conformal_quantile(s, 0.1) == 9.0          # ceil(10*0.9)=9
    assert np.isinf(C.conformal_quantile(s[:8], 0.1))   # ceil(9*0.9)=9 > 8
    assert C.conformal_quantile(s, 0.5) == 5.0


def test_partition_nesting():
    rng = np.random.default_rng(0)
    for y in (rng.lognormal(size=3000), rng.integers(0, 25, 3000).astype(float)):
        p = make_partition(y)
        assert np.all(np.isin(p.strata_inner, p.fine_edges))
        st = p.fine_stratum
        assert np.all(np.diff(st) >= 0)
        assert np.bincount(p.fine_bin(y), minlength=p.M).min() > 0
        e, cell_to = D.coarse_bins(p)
        assert np.all(np.isin(e, p.fine_edges))


@pytest.mark.parametrize("alpha", [0.1, 0.2])
def test_stratum_conditional_validity_monte_carlo(alpha):
    """Average over 300 replications of the per-stratum coverage must be >= 1-alpha
    (minus Monte-Carlo error) for stratified methods, for any (even bad) score."""
    rng = np.random.default_rng(1)
    _, ytr = _data(rng, 4000)
    part = make_partition(ytr)
    K = part.K
    cov = {m: np.zeros(K) for m in ("S-Res", "SDLC", "SDLC-floor")}
    cnt = np.zeros(K)
    R = 300
    for r in range(R):
        xc, yc = _data(rng, 300)
        xt, yt = _data(rng, 300)
        mu_c, mu_t = np.sin(3 * xc) * 0.5, np.sin(3 * xt) * 0.5     # deliberately biased model
        sg_c, sg_t = np.full(300, 0.7), np.full(300, 0.7)
        lsd = D.LocationScaleDensity(part, rng.normal(size=500))
        Fc, Ft = lsd.cells(mu_c, sg_c), lsd.cells(mu_t, sg_t)
        st = part.stratum(yc)
        f_c = D.at(Fc, yc, part)
        sets = {"S-Res": C.interval_method(np.abs(yc - mu_c), mu_t, alpha, part, kind="res", strata_cal=st),
                "SDLC": C.mask_method(-f_c, Ft, alpha, part, strata_cal=st),
                "SDLC-floor": C.mask_method(-f_c, Ft, alpha, part, strata_cal=st, floor_beta=alpha)}
        stt = part.stratum(yt)
        for m, S in sets.items():
            c = covered(S, yt, part)
            for k in range(K):
                cov[m][k] += c[stt == k].sum()
        cnt += np.bincount(stt, minlength=K)
    for m in cov:
        cv = cov[m] / cnt
        se = np.sqrt(alpha * (1 - alpha) / cnt) * 3  # generous; dependence within replication
        assert np.all(cv >= 1 - alpha - se - 0.01), (m, cv)


def test_marginal_validity_and_supersets():
    rng = np.random.default_rng(2)
    _, ytr = _data(rng, 4000)
    part = make_partition(ytr)
    tot = {"SCP": 0, "DLS": 0, "HPD": 0, "DCP": 0}
    n = 0
    for r in range(200):
        xc, yc = _data(rng, 400)
        xt, yt = _data(rng, 400)
        mu_c, mu_t = np.sin(3 * xc), np.sin(3 * xt)
        lsd = D.LocationScaleDensity(part, rng.standard_exponential(800) - 1)
        Fc, Ft = lsd.cells(mu_c, np.full(400, 0.5)), lsd.cells(mu_t, np.full(400, 0.5))
        f_c = D.at(Fc, yc, part)
        Hc = D.at(D.hpd_value(Fc, part), yc, part)
        S = {"SCP": C.interval_method(np.abs(yc - mu_c), mu_t, 0.1, part, kind="res"),
             "DLS": C.mask_method(-f_c, Ft, 0.1, part),
             "HPD": C.mask_method(-Hc, D.hpd_value(Ft, part), 0.1, part),
             "DCP": C.dcp_method(Fc, yc, Ft, 0.1, part)}
        for m in S:
            tot[m] += covered(S[m], yt, part).sum()
        n += 400
        st = part.stratum(yc)
        base = C.mask_method(-f_c, Ft, 0.1, part, strata_cal=st)
        fl = C.mask_method(-f_c, Ft, 0.1, part, strata_cal=st, floor_beta=0.2)
        hull = C.to_hull(base, part)
        assert np.all(sizes(hull, part) >= sizes(base, part) - 1e-9)
        cb, ch = covered(base, yt, part), covered(hull, yt, part)
        assert np.all(ch[cb])                           # hull is a superset
        cm = covered(S["DLS"], yt, part)
        assert np.all(covered(fl, yt, part)[cm])        # floor ⊇ marginal set
    for m in tot:
        assert tot[m] / n >= 0.9 - 0.006, (m, tot[m] / n)


def test_density_normalised():
    rng = np.random.default_rng(3)
    _, ytr = _data(rng, 2000)
    part = make_partition(ytr)
    lsd = D.LocationScaleDensity(part, rng.normal(size=1000))
    F = lsd.cells(np.zeros(5), np.ones(5))
    assert np.allclose(F @ part.widths, 1.0)

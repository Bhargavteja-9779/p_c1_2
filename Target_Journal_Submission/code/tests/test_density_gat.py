"""g_at (tail density only outside the tabulated range) equals the original implementation exactly."""
import numpy as np

from src.models.density import RobustLSDensity


def _g_at_ref(d, z):
    z = np.asarray(z, float)
    inside = (z >= d.grid[0]) & (z <= d.grid[-1])
    out = d.tail_pdf(z)
    out[inside] = np.interp(z[inside], d.grid, d.g)
    return out


def test_g_at_equals_reference():
    rng = np.random.default_rng(1)
    d = RobustLSDensity(rng.standard_t(4, 3000))
    for z in (np.linspace(-80, 80, 20001), rng.normal(0, 30, (50, 400)), np.array([d.grid[0], d.grid[-1]])):
        assert np.array_equal(d.g_at(z), _g_at_ref(d, z))

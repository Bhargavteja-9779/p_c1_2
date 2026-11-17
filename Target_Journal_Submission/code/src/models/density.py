"""Conditional density estimators, represented as piecewise-constant densities on the
evaluation grid of a Partition (one value per grid cell, normalised over the domain D).

* HistogramDensity  : multiclass LightGBM over coarse equal-mass target bins
                      (a "regression-as-classification" histogram, cf. CHR / R2CCP).
* LocationScaleDensity : f(y|x) = g((y - mu(x)) / sigma(x)) / sigma(x), where mu, sigma are
                      the LightGBM mean and scale models and g is a Gaussian KDE of the
                      out-of-fold standardised training residuals (semiparametric
                      location-scale model with nonparametric noise).
The score of a calibration point is the cell value at the cell containing its target, which
is exactly how test sets are formed, so split-conformal exchangeability arguments apply.
"""
from __future__ import annotations

import numpy as np

from src.methods.strata import Partition, coarse_bins


def _normalise(F, part):
    mass = F @ part.widths
    return F / np.maximum(mass, 1e-300)[:, None]


class HistogramDensity:
    def __init__(self, part: Partition, n_coarse=40):
        self.part = part
        self.edges, self.cell_to = coarse_bins(part, n_coarse)
        self.n_classes = len(self.edges) - 1

    def labels(self, y):
        return np.clip(np.searchsorted(self.edges[1:-1], y, side="right"), 0, self.n_classes - 1)

    def cells(self, P):
        dens = P / np.diff(self.edges)[None, :]
        return _normalise(dens[:, self.cell_to], self.part)


class LocationScaleDensity:
    def __init__(self, part: Partition, z_train, n_grid=4096, floor=1e-6):
        z = np.asarray(z_train, float)
        z = z[np.isfinite(z)]
        sd = z.std()
        iqr = np.subtract(*np.quantile(z, [0.75, 0.25]))
        h = 0.9 * min(sd, iqr / 1.34 if iqr > 0 else sd) * len(z) ** (-0.2)  # Silverman
        h = max(h, 1e-3)
        self.grid = np.linspace(z.min() - 4 * h, z.max() + 4 * h, n_grid)
        g = np.zeros(n_grid)
        for chunk in np.array_split(z, max(1, len(z) // 2000)):
            g += np.exp(-0.5 * ((self.grid[:, None] - chunk[None, :]) / h) ** 2).sum(1)
        g /= len(z) * h * np.sqrt(2 * np.pi)
        self.g = np.maximum(g, floor * g.max())
        self.gfloor = floor * g.max()
        self.part, self.h = part, h

    def cells(self, mu, sigma):
        mid = 0.5 * (self.part.fine_edges[:-1] + self.part.fine_edges[1:])
        Z = (mid[None, :] - mu[:, None]) / sigma[:, None]
        G = np.interp(Z, self.grid, self.g, left=self.gfloor, right=self.gfloor)
        return _normalise(G / sigma[:, None], self.part)


class TwoPieceLocationScaleDensity(LocationScaleDensity):
    """Exploratory: f(y|x) proportional to g(z)/sigma_side(x), z = (y-mu)/sigma_minus(x) below mu and
    (y-mu)/sigma_plus(x) above mu; g = KDE of the correspondingly standardised OOF residuals.
    Normalised numerically on the grid for every x (so it is a proper density on D)."""

    def cells(self, mu, s_minus, s_plus):
        mid = 0.5 * (self.part.fine_edges[:-1] + self.part.fine_edges[1:])
        D_ = mid[None, :] - mu[:, None]
        S_ = np.where(D_ < 0, s_minus[:, None], s_plus[:, None])
        G = np.interp(D_ / S_, self.grid, self.g, left=self.gfloor, right=self.gfloor)
        return _normalise(G / S_, self.part)


def at(F, y, part):
    """Value of the cell-wise density at the cell of each y (0 outside D)."""
    out = F[np.arange(len(y)), part.fine_bin(y)]
    out[~part.in_domain(y)] = 0.0
    return out


def hpd_value(F, part):
    """H_j(x) = sum_l m_l(x) 1{f_l(x) <= f_j(x)}, m_l = cell mass (Izbicki et al., 2022)."""
    Mass = F * part.widths[None, :]
    order = np.argsort(F, axis=1, kind="stable")
    cs = np.cumsum(np.take_along_axis(Mass, order, axis=1), axis=1)
    H = np.empty_like(F)
    np.put_along_axis(H, order, cs, axis=1)
    return H


def cdf_at(F, y, part):
    Mass = F * part.widths[None, :]
    cs = np.concatenate([np.zeros((len(F), 1)), np.cumsum(Mass, axis=1)], axis=1)
    j = part.fine_bin(y)
    r = np.arange(len(y))
    frac = np.clip((y - part.fine_edges[j]) / part.widths[j], 0, 1)
    out = cs[r, j] + Mass[r, j] * frac
    out[y < part.lo], out[y > part.hi] = 0.0, 1.0
    return out


def cdf_inv(F, u, part):
    Mass = F * part.widths[None, :]
    cs = np.concatenate([np.zeros((len(F), 1)), np.cumsum(Mass, axis=1)], axis=1)
    u = np.clip(u, 0, 1)
    j = np.clip((cs[:, 1:] < u[:, None]).sum(1), 0, part.M - 1)
    r = np.arange(len(F))
    frac = np.clip((u - cs[r, j]) / np.maximum(Mass[r, j], 1e-300), 0, 1)
    return part.fine_edges[j] + frac * part.widths[j]


# ============================================================================ v3 estimator
def silverman(z):
    z = np.asarray(z, float)
    sd = z.std()
    iqr = np.subtract(*np.quantile(z, [0.75, 0.25]))
    s = min(sd, iqr / 1.349) if iqr > 0 else sd
    return max(0.9 * s * len(z) ** (-0.2), 1e-3)


class RobustLSDensity:
    """Noise density g for the (two-piece) location-scale model, v3.

    g = (1 - eps) * KDE(z_train; Gaussian kernel, Silverman bandwidth x bw_mult)
        + eps * t_nu(z / s_t) / s_t,          s_t = robust scale (IQR/1.349) of z_train.
    The defensive Student-t component makes g a proper density with polynomial tails and no
    arbitrary floor (z beyond the data receive a smooth, strictly decreasing density). The KDE is
    computed by linear binning + FFT convolution on a uniform grid of spacing <= h/4 that covers the
    data +/- 5h; the model g is the piecewise-linear interpolant of the mixture on that grid, and the
    exact t component outside it. z_train should be CROSS-FITTED standardised residuals.
    """

    def __init__(self, z_train, eps=0.01, nu=2.0, bw_mult=1.0, max_grid=2 ** 18):
        from scipy.signal import fftconvolve
        from scipy.stats import t as student_t
        z = np.asarray(z_train, float)
        z = z[np.isfinite(z)]
        self.n, self.eps, self.nu = len(z), eps, nu
        self.h = h = silverman(z) * bw_mult
        iqr = np.subtract(*np.quantile(z, [0.75, 0.25]))
        self.s_t = iqr / 1.349 if iqr > 0 else max(z.std(), 1e-3)
        lo, hi = z.min() - 5 * h, z.max() + 5 * h
        d = h / 4
        if (hi - lo) / d > max_grid:
            d = (hi - lo) / max_grid
        m = int(np.ceil((hi - lo) / d)) + 1
        grid = lo + d * np.arange(m)
        pos = (z - lo) / d
        i0 = np.clip(np.floor(pos).astype(int), 0, m - 2)
        w1 = pos - i0
        counts = np.bincount(i0, weights=1 - w1, minlength=m) + np.bincount(i0 + 1, weights=w1, minlength=m)
        kk = np.arange(-int(np.ceil(5 * h / d)), int(np.ceil(5 * h / d)) + 1) * d
        kern = np.exp(-0.5 * (kk / h) ** 2) / (h * np.sqrt(2 * np.pi))
        kde = np.maximum(fftconvolve(counts, kern, mode="same") / self.n, 0.0)
        self._t = student_t(nu)
        self._zq = np.quantile(z, [0.001, 0.999])
        self.grid = grid
        self.g = (1 - eps) * kde + eps * self._t.pdf(grid / self.s_t) / self.s_t
        self.gfloor = 0.0  # no floor in v3

    def tail_pdf(self, z):
        return self.eps * self._t.pdf(np.asarray(z, float) / self.s_t) / self.s_t

    def tail_cdf(self, z):
        return self.eps * self._t.cdf(np.asarray(z, float) / self.s_t)

    def g_at(self, z):
        z = np.asarray(z, float)
        inside = (z >= self.grid[0]) & (z <= self.grid[-1])
        out = self.tail_pdf(z)
        out[inside] = np.interp(z[inside], self.grid, self.g)
        return out


class GaussianNoiseDensity(RobustLSDensity):
    """Ablation: g = (1 - eps) N(0,1) + eps t_nu(z/s_t)/s_t (no data-driven shape; s_t = 1).
    With this g the SDLC score -g(z)/sigma(x) differs from the normalised residual |z| only through
    the factor 1/sigma(x) and the (negligible) defensive component."""

    def __init__(self, eps=0.01, nu=2.0):
        from scipy.stats import norm, t as student_t
        self.n, self.eps, self.nu, self.h, self.s_t = 0, eps, nu, 0.01, 1.0
        self._t = student_t(nu)
        self.grid = np.linspace(-40, 40, 32001)
        self.g = (1 - eps) * norm.pdf(self.grid) + eps * self._t.pdf(self.grid)
        self._zq = np.array([-3.09, 3.09])
        self.gfloor = 0.0

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

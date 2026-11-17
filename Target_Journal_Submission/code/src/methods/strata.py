"""Target strata and fine histogram bins, constructed from TRAINING targets only.

Fine bins are equal-mass bins at training quantiles j/M (``method='lower'`` so that every
edge is an observed training value and no interior bin is empty). Stratum edges are
training quantiles at user-given probabilities; they are always inserted into the set of
fine edges, so every fine bin lies inside exactly one stratum. Because the fine edges do
not depend on the stratification, several stratifications can share one density model.
"""
from __future__ import annotations

from dataclasses import dataclass, replace

import numpy as np

PRIMARY_STRATA = (0.1, 0.25, 0.75, 0.9)
ALL_STRATA_SCHEMES = {
    "S3": (0.1, 0.9),
    "S5": PRIMARY_STRATA,
    "S10": tuple(np.round(np.arange(1, 10) / 10, 2)),
}


@dataclass
class Partition:
    lo: float
    hi: float
    strata_inner: np.ndarray
    fine_edges: np.ndarray
    y_train: np.ndarray

    @property
    def K(self):
        return len(self.strata_inner) + 1

    @property
    def M(self):
        return len(self.fine_edges) - 1

    @property
    def widths(self):
        return np.diff(self.fine_edges)

    @property
    def fine_stratum(self):
        return np.searchsorted(self.strata_inner, self.fine_edges[:-1], side="right")

    @property
    def strata_edges(self):
        return np.concatenate([[self.lo], self.strata_inner, [self.hi]])

    def stratum(self, y):
        return np.searchsorted(self.strata_inner, y, side="right")

    def fine_bin(self, y):
        return np.clip(np.searchsorted(self.fine_edges[1:-1], y, side="right"), 0, self.M - 1)

    def in_domain(self, y):
        return (y >= self.lo) & (y <= self.hi)

    def with_strata(self, probs):
        inner = np.unique(np.quantile(self.y_train, probs, method="lower"))
        inner = inner[np.isin(inner, self.fine_edges[1:-1])]
        return replace(self, strata_inner=inner)


def make_partition(y_train, strata_probs=PRIMARY_STRATA, n_fine=200, margin=0.05,
                   anchor_schemes=tuple(ALL_STRATA_SCHEMES.values()), n_coarse=40, nonneg=False):
    """Evaluation grid of ~n_fine equal-mass cells. The coarse histogram-classifier bins
    (n_coarse equal-mass bins) and all stratum edges are subsets of the grid edges."""
    y = np.asarray(y_train, float)
    r = y.max() - y.min()
    lo, hi = y.min() - margin * r, y.max() + margin * r
    if nonneg and y.min() >= 0:      # v3: known support of non-negative targets (decided from training data)
        lo = max(lo, 0.0)
    probs = list(np.arange(1, n_fine) / n_fine) + list(np.arange(1, n_coarse) / n_coarse)
    for s in anchor_schemes:
        probs += list(s)
    inner = np.unique(np.quantile(y, sorted(set(np.round(probs, 6))), method="lower"))
    inner = inner[(inner > lo) & (inner < hi)]
    # with 'lower' quantiles only the first bin [lo, e_1) can be empty (if e_1 == min y)
    while len(inner) and not (y < inner[0]).any():
        inner = inner[1:]
    fine = np.concatenate([[lo], inner, [hi]])
    part = Partition(lo, hi, np.array([]), fine, y)
    return part.with_strata(strata_probs)


def coarse_bins(part: Partition, n_coarse=40):
    """Coarse equal-mass bins (subset of grid edges) used as classes of the histogram
    density classifier. Returns (coarse_edges, cell_to_coarse index array)."""
    y = part.y_train
    inner = np.unique(np.quantile(y, np.arange(1, n_coarse) / n_coarse, method="lower"))
    inner = inner[np.isin(inner, part.fine_edges[1:-1])]
    while len(inner) and not (y < inner[0]).any():
        inner = inner[1:]
    edges = np.concatenate([[part.lo], inner, [part.hi]])
    cell_to = np.searchsorted(inner, part.fine_edges[:-1], side="right")
    return edges, cell_to

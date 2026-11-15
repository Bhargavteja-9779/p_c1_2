"""Evaluation of prediction sets: coverage, size, stratum coverage, components, WSC."""
from __future__ import annotations

import numpy as np

from src.methods.strata import Partition


def covered(S, y, part: Partition):
    ind = part.in_domain(y)
    if S[0] == "int":
        lo, hi = S[1], S[2]
        c = ((lo <= y[:, None]) & (y[:, None] <= hi)).any(1)
    else:
        c = S[1][np.arange(len(y)), part.fine_bin(y)]
    return c & ind


def sizes(S, part):
    if S[0] == "int":
        return np.clip(S[2] - S[1], 0, None).sum(1)
    return S[1] @ part.widths


def n_components(S, part):
    if S[0] == "int":
        lo, hi = S[1], S[2]
        ok = hi > lo
        comp = ok.sum(1).astype(float)
        if lo.shape[1] > 1:
            touch = ok[:, :-1] & ok[:, 1:] & np.isclose(hi[:, :-1], lo[:, 1:])
            comp -= touch.sum(1)
        return comp
    m = S[1].astype(np.int8)
    return ((m[:, 0] == 1).astype(int) + (np.diff(m, axis=1) == 1).sum(1)).astype(float)


def wsc(Xt, cov, seed, delta=0.1, n_dir=100, grid=40):
    """Worst-slab coverage (Cauchois, Gupta & Duchi, 2021), unbiased variant: the slab is
    selected on a random half of the test set and evaluated on the other half.
    Slab end-points are restricted to a grid of 1/grid quantiles of the projection."""
    rng = np.random.default_rng(seed)
    n = len(cov)
    if n < 200:
        return np.nan
    idx = rng.permutation(n)
    A, B = idx[: n // 2], idx[n // 2:]
    mu, sd = Xt[A].mean(0), Xt[A].std(0) + 1e-12
    ZA, ZB = (Xt[A] - mu) / sd, (Xt[B] - mu) / sd
    V = rng.normal(size=(n_dir, Xt.shape[1]))
    V /= np.linalg.norm(V, axis=1, keepdims=True)
    pos = (np.linspace(0, 1, grid + 1) * len(A)).astype(int)
    L = pos[None, :] - pos[:, None]
    valid = L >= delta * len(A)
    best, arg = np.inf, None
    for v in V:
        z = ZA @ v
        o = np.argsort(z)
        cs = np.concatenate([[0], np.cumsum(cov[A][o].astype(float))])
        C = (cs[pos][None, :] - cs[pos][:, None]) / np.where(valid, L, 1)
        C[~valid] = np.inf
        i, j = np.unravel_index(np.argmin(C), C.shape)
        if C[i, j] < best:
            zs = z[o]
            best, arg = C[i, j], (v, zs[pos[i]], zs[min(pos[j], len(zs) - 1)])
    v, a, b = arg
    zb = ZB @ v
    sel = (zb >= a) & (zb <= b)
    return float(cov[B][sel].mean()) if sel.any() else np.nan


def evaluate(S, y, part, alpha, eval_strata, weights=None):
    """eval_strata: dict name -> integer group labels of the test points.
    weights: dict name -> importance weights (for shifted-test-distribution coverage)."""
    c = covered(S, y, part)
    sz = sizes(S, part)
    out = {"coverage": float(c.mean()), "size": float(sz.mean()),
           "size_median": float(np.median(sz)),
           "components": float(n_components(S, part).mean()),
           "empty_rate": float((sz <= 0).mean())}
    for name, lab in eval_strata.items():
        covs = []
        for k in np.unique(lab):
            mk = lab == k
            ck = float(c[mk].mean())
            out[f"{name}_cov_{k}"] = ck
            out[f"{name}_n_{k}"] = int(mk.sum())
            out[f"{name}_size_{k}"] = float(sz[mk].mean())
            covs.append(ck)
        out[f"{name}_worst"] = float(np.min(covs))
        out[f"{name}_deficit"] = float(np.mean(np.maximum(0, (1 - alpha) - np.array(covs))))
    for name, w in (weights or {}).items():
        w = w / w.sum()
        out[f"shift_{name}_cov"] = float((w * c).sum())
        out[f"shift_{name}_size"] = float((w * sz).sum())
    return out, c

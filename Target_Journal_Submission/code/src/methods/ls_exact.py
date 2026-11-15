"""Grid-free conformal sets for (two-piece) location-scale conditional densities.

f(y|x) = g(z) / s(x, y),  z = (y - mu(x)) / s(x, y),  s = sigma_minus(x) if y < mu(x) else sigma_plus(x)
(symmetric LS: sigma_minus = sigma_plus = sigma).  g is tabulated on a fine z-grid (KDE).

Scores are evaluated EXACTLY at the observed y (no target discretisation), so split-conformal
validity (Theorem 1) holds for the implemented procedure. Prediction sets are built on a
per-x, scale-free grid y = mu + s * z (resolution relative to the conditional scale), which
removes the inflation that a fixed grid over the marginal target range causes when the
conditional density is much narrower than a grid cell. Regions beyond the tabulated z-range
(density = floor) are handled analytically.

Set representation returned: ("int", LO, HI, covered_exact) with padded interval pieces.
"""
from __future__ import annotations

import numpy as np

from src.methods.conformal import conformal_quantile
from src.methods.strata import Partition


class LSTable:
    def __init__(self, dens, n_set_grid=2048):
        """dens: LocationScaleDensity (has .grid, .g, .gfloor)."""
        self.zg, self.g, self.gfloor = dens.grid, dens.g, dens.gfloor
        dz = np.gradient(self.zg)
        # HPD value of z: mass of g below level g(z)
        o = np.argsort(self.g, kind="stable")
        cs = np.cumsum((self.g * dz)[o])
        H = np.empty_like(self.g)
        H[o] = cs
        self.H = H / cs[-1]
        self.F = np.concatenate([[0], np.cumsum(0.5 * (self.g[1:] + self.g[:-1]) * np.diff(self.zg))])
        self.F /= self.F[-1]
        self.zs = np.linspace(self.zg[0], self.zg[-1], n_set_grid)       # set-construction grid
        self.gs = np.interp(self.zs, self.zg, self.g)
        self.Hs = np.interp(self.zs, self.zg, self.H)
        self.dzs = self.zs[1] - self.zs[0]

    def g_at(self, z):
        return np.interp(z, self.zg, self.g, left=self.gfloor, right=self.gfloor)

    def H_at(self, z):
        return np.interp(z, self.zg, self.H, left=0.0, right=0.0)

    def F_at(self, z):
        return np.interp(z, self.zg, self.F, left=0.0, right=1.0)

    def F_inv(self, u):
        return np.interp(u, self.F, self.zg)


def _z(y, mu, sm, sp):
    d = y - mu
    s = np.where(d < 0, sm, sp)
    return d / s, s


def scores(kind, T: LSTable, y, mu, sm, sp, part: Partition):
    """Nonconformity scores (larger = less conforming), exact at y. Outside D -> +inf-like."""
    z, s = _z(y, mu, sm, sp)
    if kind == "density":          # SDLC / DLS: -f(y|x)
        sc = -T.g_at(z) / s
    elif kind == "hpd":            # HPD-split: -H(z)
        sc = -T.H_at(z)
    elif kind == "dcp":            # DCP: |F(z) - 1/2|
        sc = np.abs(T.F_at(z) - 0.5)
    else:
        raise ValueError(kind)
    out_dom = ~part.in_domain(y)
    sc = np.where(out_dom, np.inf, sc)
    return sc


def _runs_to_intervals(inc, ylo, yhi, max_pieces):
    """inc: (n, G) bool on cells [ylo[:, j], yhi[:, j]] (ordered); returns padded LO, HI."""
    n, G = inc.shape
    m = inc.astype(np.int8)
    dm = np.diff(np.concatenate([np.zeros((n, 1), np.int8), m, np.zeros((n, 1), np.int8)], axis=1), axis=1)
    LO = np.full((n, max_pieces), np.inf)
    HI = np.full((n, max_pieces), -np.inf)
    rs, cs = np.nonzero(dm == 1)
    re, ce = np.nonzero(dm == -1)
    # starts and ends come in row-major order and pair up within rows
    cnt = np.zeros(n, int)
    for r, a, b in zip(rs, cs, ce - 1):
        k = cnt[r]
        if k < max_pieces:
            LO[r, k], HI[r, k] = ylo[r, a], yhi[r, b]
        else:  # merge overflow into last piece (superset; never loses coverage)
            HI[r, max_pieces - 1] = yhi[r, b]
        cnt[r] += 1
    return LO, HI


def build_sets(kind, T: LSTable, mu, sm, sp, thr_of_y, part: Partition, y_test, sc_test, max_pieces=12,
               chunk=1500):
    """Prediction sets {y in D : score(x, y) <= thr(stratum(y))}.

    thr_of_y: array (K,) of thresholds per stratum (use the same value for marginal methods).
    Coverage is decided exactly by comparing the exact test score with its stratum threshold.
    The set geometry uses the per-x grid y = mu + s z over the tabulated z-range, plus the two
    outer regions (beyond the table) where g = floor.
    """
    n = len(mu)
    E = part.strata_edges
    K = part.K
    LO_all, HI_all = [], []
    zs = T.zs
    # cell edges in z (midpoints between set-grid nodes)
    ze = np.concatenate([[zs[0] - T.dzs / 2], 0.5 * (zs[1:] + zs[:-1]), [zs[-1] + T.dzs / 2]])
    for a in range(0, n, chunk):
        b = min(n, a + chunk)
        m_, sm_, sp_ = mu[a:b, None], sm[a:b, None], sp[a:b, None]
        sz = np.where(zs[None, :] < 0, sm_, sp_)
        yc = m_ + sz * zs[None, :]                                   # cell centres
        ylo_c = m_ + np.where(ze[None, :-1] < 0, sm_, sp_) * ze[None, :-1]
        yhi_c = m_ + np.where(ze[None, 1:] < 0, sm_, sp_) * ze[None, 1:]
        if kind == "density":
            sc = -T.gs[None, :] / sz
        elif kind == "hpd":
            sc = np.broadcast_to(-T.Hs[None, :], yc.shape)
        else:
            raise ValueError(kind)
        k_c = part.stratum(yc)
        inc = (sc <= thr_of_y[k_c]) & (yc >= part.lo) & (yc <= part.hi)
        ylo_c = np.clip(ylo_c, part.lo, part.hi)
        yhi_c = np.clip(yhi_c, part.lo, part.hi)
        # split cells that straddle a stratum edge: approximate by cell-centre stratum (cell width
        # ~ s*dz is tiny relative to the conditional scale); then clip pieces to their stratum
        LO, HI = _runs_to_intervals(inc, ylo_c, yhi_c, max_pieces)
        # outer regions beyond the z-table: density = floor there
        lo_tab, hi_tab = yc[:, 0] - sz[:, 0] * T.dzs / 2, yc[:, -1] + sz[:, -1] * T.dzs / 2
        extra_lo, extra_hi = [], []
        for k in range(K):
            if kind == "density":
                ok_left = (-T.gfloor / sm[a:b]) <= thr_of_y[k]
                ok_right = (-T.gfloor / sp[a:b]) <= thr_of_y[k]
            else:
                ok_left = ok_right = np.full(b - a, 0.0 <= thr_of_y[k])
            # left outer region (part.lo, lo_tab) ∩ B_k
            L1, H1 = np.maximum(part.lo, E[k]), np.minimum(lo_tab, E[k + 1])
            extra_lo.append(np.where(ok_left & (H1 > L1), L1, np.inf))
            extra_hi.append(np.where(ok_left & (H1 > L1), H1, -np.inf))
            L2, H2 = np.maximum(hi_tab, E[k]), np.minimum(part.hi, E[k + 1])
            extra_lo.append(np.where(ok_right & (H2 > L2), L2, np.inf))
            extra_hi.append(np.where(ok_right & (H2 > L2), H2, -np.inf))
        LO_all.append(np.concatenate([LO, np.stack(extra_lo, 1)], 1))
        HI_all.append(np.concatenate([HI, np.stack(extra_hi, 1)], 1))
    LO, HI = np.concatenate(LO_all), np.concatenate(HI_all)
    k_t = part.stratum(y_test)
    cov = (sc_test <= thr_of_y[np.clip(k_t, 0, K - 1)]) & part.in_domain(y_test)
    # order pieces by lower end so that component counting works
    o = np.argsort(LO, axis=1)
    LO, HI = np.take_along_axis(LO, o, 1), np.take_along_axis(HI, o, 1)
    return ("int", LO, HI, cov)


def dcp_sets(T: LSTable, mu, sm, sp, sc_cal, alpha, part, y_test):
    t = conformal_quantile(sc_cal, alpha)
    n = len(mu)
    if not np.isfinite(t) or t >= 0.5:
        return ("int", np.full((n, 1), part.lo), np.full((n, 1), part.hi), part.in_domain(y_test))
    zl, zh = T.F_inv(0.5 - t), T.F_inv(0.5 + t)
    lo = np.maximum(mu + (sm if zl < 0 else sp) * zl, part.lo)
    hi = np.minimum(mu + (sm if zh < 0 else sp) * zh, part.hi)
    sc_t = scores("dcp", T, y_test, mu, sm, sp, part)
    return ("int", lo[:, None], hi[:, None], (sc_t <= t) & part.in_domain(y_test))


def ls_methods(T: LSTable, tag, mu_c, sm_c, sp_c, yc, mu_t, sm_t, sp_t, yt, alpha, part, st_c, full=True):
    """All LS-family methods, grid-free. Returns {name: set}."""
    out = {}
    K = part.K
    sd_c = scores("density", T, yc, mu_c, sm_c, sp_c, part)
    sd_t = scores("density", T, yt, mu_t, sm_t, sp_t, part)
    q_m = conformal_quantile(sd_c, alpha)
    q_s = np.array([conformal_quantile(sd_c[st_c == k], alpha) for k in range(K)])
    out[f"DLS-M-{tag}"] = build_sets("density", T, mu_t, sm_t, sp_t, np.full(K, q_m), part, yt, sd_t)
    out[f"SDLC-{tag}"] = build_sets("density", T, mu_t, sm_t, sp_t, q_s, part, yt, sd_t)
    sh_c = scores("hpd", T, yc, mu_c, sm_c, sp_c, part)
    sh_t = scores("hpd", T, yt, mu_t, sm_t, sp_t, part)
    qh_s = np.array([conformal_quantile(sh_c[st_c == k], alpha) for k in range(K)])
    out[f"S-HPD-{tag}"] = build_sets("hpd", T, mu_t, sm_t, sp_t, qh_s, part, yt, sh_t)
    if full:
        qh_m = conformal_quantile(sh_c, alpha)
        out[f"HPD-split-{tag}"] = build_sets("hpd", T, mu_t, sm_t, sp_t, np.full(K, qh_m), part, yt, sh_t)
        out[f"DCP-{tag}"] = dcp_sets(T, mu_t, sm_t, sp_t, scores("dcp", T, yc, mu_c, sm_c, sp_c, part),
                                     alpha, part, yt)
        beta = min(2 * alpha, 0.5)
        q_f = np.maximum(np.array([conformal_quantile(sd_c[st_c == k], beta) for k in range(K)]), q_m)
        out[f"SDLC-{tag}-floor"] = build_sets("density", T, mu_t, sm_t, sp_t, q_f, part, yt, sd_t)
        S = out[f"SDLC-{tag}"]
        ok = S[2] >= S[1]
        L = np.where(ok, S[1], np.inf).min(1)
        H = np.where(ok, S[2], -np.inf).max(1)
        cov_h = S[3] | ((yt >= L) & (yt <= H) & part.in_domain(yt))
        out[f"SDLC-{tag}-hull"] = ("int", L[:, None], H[:, None], cov_h)
    return out

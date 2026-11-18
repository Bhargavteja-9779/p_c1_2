"""v3 implementation of location-scale-family conformal sets (SDLC, DLS, S-HPD, HPD-split, DCP).

Model:  f(y|x) = g(z) / s(x,y),  z = (y - mu(x)) / s(x,y),  s = sigma_minus(x) if y < mu(x) else sigma_plus(x),
with g a RobustLSDensity (KDE + defensive Student-t component) fitted to CROSS-FITTED standardised residuals.

* Scores are exact at the observed target (no discretisation), so Theorem 1 applies to the coverage
  that is reported.
* Set geometry (size, pieces, hull, stratum alerts) is computed on a non-uniform standardised grid
  (dense over the bulk of the residuals, log-spaced beyond, z = 0 included) with LINEAR interpolation
  of g inside each cell and every cell split EXACTLY at stratum edges and at the domain bounds, so the
  geometry is that of the piecewise-linear interpolant of g; beyond the grid the analytic t tail is used.
  Its accuracy is checked by a grid-convergence study (experiments/grid_convergence.py).
Sets are returned as ("geo", size, pieces, hull_lo, hull_hi, alerts[n, K], covered_exact).
"""
from __future__ import annotations

import numpy as np

from src.methods.conformal import conformal_quantile
from src.methods.strata import Partition


class LSTable3:
    def __init__(self, dens, n_core=1536, n_tail=256):
        self.d = dens
        grid, g = dens.grid, dens.g
        h = dens.h
        # cell masses on the model grid (for HPD values and the CDF)
        mid_g = 0.5 * (g[1:] + g[:-1])
        cell_m = mid_g * np.diff(grid)
        left_tail, right_tail = dens.tail_cdf(grid[0]), dens.eps - dens.tail_cdf(grid[-1])
        order = np.argsort(mid_g, kind="stable")
        self._hpd_levels = mid_g[order]
        self._hpd_cum = np.cumsum(cell_m[order]) + left_tail + right_tail  # tails lie below every level
        tot = self._hpd_cum[-1]
        self._hpd_cum /= tot
        self._hpd_base = (left_tail + right_tail) / tot
        self._cdf_grid = grid
        self._cdf = (left_tail + np.concatenate([[0], np.cumsum(cell_m)])) / tot
        # set-construction grid: dense core over the residual bulk, log-spaced outer parts, 0 included
        core_lo = max(grid[0], dens._zq[0] - 4 * h)
        core_hi = min(grid[-1], dens._zq[1] + 4 * h)
        core = np.linspace(core_lo, core_hi, n_core)
        outer = []
        if grid[0] < core_lo:
            outer.append(core_lo - (np.geomspace(1e-3, 1, n_tail) * (core_lo - grid[0])))
        if grid[-1] > core_hi:
            outer.append(core_hi + (np.geomspace(1e-3, 1, n_tail) * (grid[-1] - core_hi)))
        zs = np.unique(np.concatenate([core, *outer, [0.0], [grid[0], grid[-1]]]))
        self.zs = zs
        self.gs = dens.g_at(zs)
        self._runs = None

    # ---------------------------------------------------------------- model functions
    def g_at(self, z):
        return self.d.g_at(z)

    def H_of_level(self, level):
        """Probability mass of {z: g(z) <= level} (monotone in level)."""
        return np.interp(level, self._hpd_levels, self._hpd_cum, left=self._hpd_base, right=1.0)

    def level_of_H(self, hval):
        return np.interp(hval, self._hpd_cum, self._hpd_levels, left=0.0, right=np.inf)

    def F_at(self, z):
        z = np.asarray(z, float)
        out = np.interp(z, self._cdf_grid, self._cdf)
        lo, hi = z < self._cdf_grid[0], z > self._cdf_grid[-1]
        out[lo] = self.d.tail_cdf(z[lo])
        out[hi] = 1 - (self.d.eps - self.d.tail_cdf(z[hi]))
        return out

    def F_inv(self, u):
        return np.interp(u, self._cdf, self._cdf_grid)

    def tail_radius(self, level):
        """|z| at which the t tail density equals `level` (inf if level <= 0)."""
        from scipy.stats import t as student_t
        nu, s, eps = self.d.nu, self.d.s_t, self.d.eps
        c0 = eps * student_t(nu).pdf(0.0) / s
        lv = np.asarray(level, float)
        with np.errstate(divide="ignore", invalid="ignore"):
            r = s * np.sqrt(np.maximum(nu * ((c0 / lv) ** (2.0 / (nu + 1.0)) - 1.0), 0.0))
        r = np.where(lv <= 0, np.inf, np.where(lv >= c0, 0.0, r))
        return r


def zside(y, mu, sm, sp):
    d = y - mu
    s = np.where(d < 0, sm, sp)
    return d / s, s


def scores(kind, T: LSTable3, y, mu, sm, sp, part: Partition):
    z, s = zside(y, mu, sm, sp)
    if kind == "density":
        sc = -T.g_at(z) / s
    elif kind == "hpd":
        sc = -T.H_of_level(T.g_at(z))
    elif kind == "dcp":
        sc = np.abs(T.F_at(z) - 0.5)
    else:
        raise ValueError(kind)
    return np.where(part.in_domain(y), sc, np.inf)


def _build_sets_ref(kind, T: LSTable3, mu, sm, sp, thr, part: Partition, y_test, sc_test, chunk=512,
                    return_intervals=False):
    """Prediction sets {y in D : score(x,y) <= thr[stratum(y)]} (see module docstring).
    Sub-intervals are generated in increasing y order (cells in z order, strata increasing within a
    cell, analytic tails first/last), so pieces are counted without sorting."""
    n, K = len(mu), part.K
    E = part.strata_edges.copy()
    E[0], E[-1] = part.lo, part.hi
    zs, gs = T.zs, T.gs
    zl, zr = zs[:-1], zs[1:]
    gl, gr = gs[:-1], gs[1:]
    dz_all = np.where(zr > zl, zr - zl, 1.0)
    neg = zr <= 0
    Cn = len(zl)
    size = np.zeros(n)
    pieces = np.zeros(n)
    hlo = np.full(n, np.inf)
    hhi = np.full(n, -np.inf)
    alerts = np.zeros((n, K), bool)
    ivals = [] if return_intervals else None
    if kind == "density":
        cvals = np.where(np.isfinite(thr), -thr, -np.inf)          # g(z)/s >= c
    else:
        cvals = np.array([-np.inf if not np.isfinite(t) else T.level_of_H(-t) for t in thr])
    for a in range(0, n, chunk):
        b = min(n, a + chunk)
        nc = b - a
        m_, sm_, sp_ = mu[a:b], sm[a:b], sp[a:b]
        s_cell = np.where(neg[None, :], sm_[:, None], sp_[:, None])
        yl = m_[:, None] + s_cell * zl[None, :]
        yr = m_[:, None] + s_cell * zr[None, :]
        Lm = np.full((nc, Cn, K), np.nan)
        Rm = np.full((nc, Cn, K), np.nan)
        for k in range(K):
            ya = np.maximum(yl, E[k])
            yb = np.minimum(yr, E[k + 1])
            ii = np.flatnonzero(yb > ya)
            if ii.size == 0:
                continue
            r, j = np.divmod(ii, Cn)
            s = s_cell.ravel()[ii]
            mm = m_[r]
            ya_, yb_ = ya.ravel()[ii], yb.ravel()[ii]
            za, zb = (ya_ - mm) / s, (yb_ - mm) / s
            ga = gl[j] + (gr[j] - gl[j]) * (za - zl[j]) / dz_all[j]
            gb = gl[j] + (gr[j] - gl[j]) * (zb - zl[j]) / dz_all[j]
            L = cvals[k] * s if kind == "density" else np.full(ii.size, cvals[k])
            if not np.isfinite(cvals[k]):
                L = np.full(ii.size, -np.inf)
            inA, inB = ga >= L, gb >= L
            with np.errstate(divide="ignore", invalid="ignore"):
                zc = za + (L - ga) * (zb - za) / (gb - ga)
            left = np.where(inA, za, zc)
            right = np.where(inB, zb, zc)
            keep = (inA | inB) & (right > left)
            Lm[r[keep], j[keep], k] = mm[keep] + s[keep] * left[keep]
            Rm[r[keep], j[keep], k] = mm[keep] + s[keep] * right[keep]
            alerts[a + r[keep], k] = True
        Lm, Rm = Lm.reshape(nc, Cn * K), Rm.reshape(nc, Cn * K)
        # analytic t tails beyond the grid: left tail pieces first, right tail pieces last
        lt_L, lt_R, rt_L, rt_R = [], [], [], []
        for k in range(K):
            for side in ("left", "right"):
                sc_ = sm_ if side == "left" else sp_
                z_end = zs[0] if side == "left" else zs[-1]
                y_end = m_ + sc_ * z_end
                if kind == "density":
                    Lv = cvals[k] * sc_ if np.isfinite(cvals[k]) else np.full(nc, -np.inf)
                else:
                    Lv = np.full(nc, cvals[k])
                rr = T.tail_radius(Lv)
                if side == "left":
                    lo_y = np.maximum(m_ - sc_ * rr, max(E[k], part.lo))
                    hi_y = np.minimum(y_end, E[k + 1])
                else:
                    lo_y = np.maximum(y_end, E[k])
                    hi_y = np.minimum(m_ + sc_ * rr, min(E[k + 1], part.hi))
                good = hi_y > lo_y
                alerts[a:b, k] |= good
                (lt_L if side == "left" else rt_L).append(np.where(good, lo_y, np.nan))
                (lt_R if side == "left" else rt_R).append(np.where(good, hi_y, np.nan))
        Lm = np.concatenate([np.stack(lt_L, 1), Lm, np.stack(rt_L, 1)], 1)
        Rm = np.concatenate([np.stack(lt_R, 1), Rm, np.stack(rt_R, 1)], 1)
        valid = ~np.isnan(Lm)
        size[a:b] = np.where(valid, Rm - Lm, 0.0).sum(1)
        prevR = np.maximum.accumulate(np.where(valid, Rm, -np.inf), axis=1)
        prevR = np.concatenate([np.full((nc, 1), -np.inf), prevR[:, :-1]], 1)
        tol = 1e-9 * (np.abs(np.where(valid, Lm, 0.0)) + 1.0)
        starts = valid & (Lm > prevR + tol)
        pieces[a:b] = starts.sum(1)
        hlo[a:b] = np.where(valid, Lm, np.inf).min(1)
        hhi[a:b] = np.where(valid, Rm, -np.inf).max(1)
        if return_intervals:
            for i in range(nc):
                v = valid[i]
                ivals.append(list(zip(Lm[i, v], Rm[i, v])))
    k_t = part.stratum(y_test)
    cov = (sc_test <= thr[np.clip(k_t, 0, K - 1)]) & part.in_domain(y_test)
    S = ("geo", size, pieces, hlo, hhi, alerts, cov)
    return (S, ivals) if return_intervals else S


def _monotone_runs(T: LSTable3):
    """Maximal runs of consecutive grid cells on which the interpolant of g is monotone (non-decreasing
    or decreasing) and z has a constant sign; returned as (i0, i1, up, neg) with boundary indices i0 < i1."""
    if getattr(T, "_runs", None) is None:
        zs, gs = T.zs, T.gs
        up = gs[1:] >= gs[:-1]
        neg = zs[1:] <= 0
        brk = np.flatnonzero((up[1:] != up[:-1]) | (neg[1:] != neg[:-1])) + 1
        starts = np.concatenate([[0], brk])
        ends = np.concatenate([brk, [len(up)]])
        runs = []
        for j0, j1 in zip(starts, ends):
            i0, i1 = int(j0), int(j1)
            zz, gg = zs[i0:i1 + 1], gs[i0:i1 + 1]
            if up[j0]:
                runs.append((i0, i1, True, bool(neg[j0]), gg, zz))
            else:
                runs.append((i0, i1, False, bool(neg[j0]), gg[::-1].copy(), zz[::-1].copy()))
        T._runs = runs
    return T._runs


def build_sets(kind, T: LSTable3, mu, sm, sp, thr, part: Partition, y_test, sc_test, chunk=4096,
               return_intervals=False):
    """Prediction sets {y in D : score(x,y) <= thr[stratum(y)]} (see module docstring).

    Exact geometry of the piecewise-linear interpolant of g, computed from its monotone runs: on a run
    the super-level set {z: g(z) >= L} is an interval whose free end is found by linear interpolation in
    the crossing cell. Each run interval is mapped to y = mu + s z and clipped to every stratum (and to
    the domain), so the cost is O(K R log G) per test point for R runs instead of O(K G). Pieces are
    generated in increasing y order (left analytic tails, strata in increasing order with runs in
    increasing z inside each stratum, right analytic tails), so they are counted without sorting.
    Numerically identical (up to rounding) to _build_sets_ref, see tests/test_ls_exact3.py."""
    n, K = len(mu), part.K
    E = part.strata_edges.astype(float).copy()
    E[0], E[-1] = part.lo, part.hi
    zs = T.zs
    runs = _monotone_runs(T)
    size = np.zeros(n)
    pieces = np.zeros(n)
    hlo = np.full(n, np.inf)
    hhi = np.full(n, -np.inf)
    alerts = np.zeros((n, K), bool)
    ivals = [] if return_intervals else None
    if kind == "density":
        cvals = np.where(np.isfinite(thr), -thr, -np.inf)          # g(z)/s >= c
    else:
        cvals = np.array([-np.inf if not np.isfinite(t) else T.level_of_H(-t) for t in thr])
    for a in range(0, n, chunk):
        b = min(n, a + chunk)
        nc = b - a
        m_, sm_, sp_ = mu[a:b], sm[a:b], sp[a:b]
        grid_L, grid_R = [], []
        for k in range(K):
            ck = cvals[k]
            for (i0, i1, up, neg, gg, zz) in runs:
                s = sm_ if neg else sp_
                if not np.isfinite(ck):
                    l, u = np.full(nc, zz[0] if up else zz[-1]), np.full(nc, zz[-1] if up else zz[0])
                    good = np.ones(nc, bool)
                else:
                    L = ck * s if kind == "density" else np.full(nc, ck)
                    if up:      # g non-decreasing on [zz[0], zz[-1]]: set = [z*, end]
                        good = L <= gg[-1]
                        l = np.where(L <= gg[0], zz[0], np.interp(L, gg, zz))
                        u = np.full(nc, zz[-1])
                    else:       # g decreasing in z; gg, zz stored reversed (gg increasing): set = [start, z*]
                        good = L <= gg[-1]
                        l = np.full(nc, zz[-1])
                        u = np.where(L <= gg[0], zz[0], np.interp(L, gg, zz))
                ylo = np.maximum(m_ + s * l, E[k])
                yhi = np.minimum(m_ + s * u, E[k + 1])
                good = good & (yhi > ylo)
                grid_L.append(np.where(good, ylo, np.nan))
                grid_R.append(np.where(good, yhi, np.nan))
                alerts[a:b, k] |= good
        # analytic t tails beyond the grid: left tail pieces first, right tail pieces last
        lt_L, lt_R, rt_L, rt_R = [], [], [], []
        for k_ in range(K):
            for side in ("left", "right"):
                sc_ = sm_ if side == "left" else sp_
                z_end = zs[0] if side == "left" else zs[-1]
                y_end = m_ + sc_ * z_end
                if kind == "density":
                    Lv = cvals[k_] * sc_ if np.isfinite(cvals[k_]) else np.full(nc, -np.inf)
                else:
                    Lv = np.full(nc, cvals[k_])
                rr = T.tail_radius(Lv)
                if side == "left":
                    lo_y = np.maximum(m_ - sc_ * rr, max(E[k_], part.lo))
                    hi_y = np.minimum(y_end, E[k_ + 1])
                else:
                    lo_y = np.maximum(y_end, E[k_])
                    hi_y = np.minimum(m_ + sc_ * rr, min(E[k_ + 1], part.hi))
                good = hi_y > lo_y
                alerts[a:b, k_] |= good
                (lt_L if side == "left" else rt_L).append(np.where(good, lo_y, np.nan))
                (lt_R if side == "left" else rt_R).append(np.where(good, hi_y, np.nan))
        Lm = np.stack(lt_L + grid_L + rt_L, 1)
        Rm = np.stack(lt_R + grid_R + rt_R, 1)
        valid = ~np.isnan(Lm)
        size[a:b] = np.where(valid, Rm - Lm, 0.0).sum(1)
        prevR = np.maximum.accumulate(np.where(valid, Rm, -np.inf), axis=1)
        prevR = np.concatenate([np.full((nc, 1), -np.inf), prevR[:, :-1]], 1)
        tol = 1e-9 * (np.abs(np.where(valid, Lm, 0.0)) + 1.0)
        starts = valid & (Lm > prevR + tol)
        pieces[a:b] = starts.sum(1)
        hlo[a:b] = np.where(valid, Lm, np.inf).min(1)
        hhi[a:b] = np.where(valid, Rm, -np.inf).max(1)
        if return_intervals:
            for i_ in range(nc):
                v = valid[i_]
                ivals.append(list(zip(Lm[i_, v], Rm[i_, v])))
    k_t = part.stratum(y_test)
    cov = (sc_test <= thr[np.clip(k_t, 0, K - 1)]) & part.in_domain(y_test)
    S = ("geo", size, pieces, hlo, hhi, alerts, cov)
    return (S, ivals) if return_intervals else S


def hull_of(S, y_test, part):
    _, size, pieces, hlo, hhi, alerts, cov = S
    cov_h = cov | ((y_test >= hlo) & (y_test <= hhi) & part.in_domain(y_test))
    return ("int", hlo[:, None], hhi[:, None], cov_h)


def dcp_sets(T, mu, sm, sp, sc_cal, alpha, part, y_test):
    t = conformal_quantile(sc_cal, alpha)
    n = len(mu)
    if not np.isfinite(t) or t >= 0.5:
        return ("int", np.full((n, 1), part.lo), np.full((n, 1), part.hi), part.in_domain(y_test))
    zl_, zh_ = T.F_inv(0.5 - t), T.F_inv(0.5 + t)
    lo = np.maximum(mu + (sm if zl_ < 0 else sp) * zl_, part.lo)
    hi = np.minimum(mu + (sm if zh_ < 0 else sp) * zh_, part.hi)
    sc_t = scores("dcp", T, y_test, mu, sm, sp, part)
    return ("int", lo[:, None], hi[:, None], (sc_t <= t) & part.in_domain(y_test))


def ls_methods(T, tag, mu_c, sm_c, sp_c, yc, mu_t, sm_t, sp_t, yt, alpha, part, st_c, full=True, hpd=True):
    out = {}
    K = part.K
    sd_c = scores("density", T, yc, mu_c, sm_c, sp_c, part)
    sd_t = scores("density", T, yt, mu_t, sm_t, sp_t, part)
    q_m = conformal_quantile(sd_c, alpha)
    q_s = np.array([conformal_quantile(sd_c[st_c == k], alpha) for k in range(K)])
    out[f"DLS-M-{tag}"] = build_sets("density", T, mu_t, sm_t, sp_t, np.full(K, q_m), part, yt, sd_t)
    out[f"SDLC-{tag}"] = build_sets("density", T, mu_t, sm_t, sp_t, q_s, part, yt, sd_t)
    if hpd:
        sh_c = scores("hpd", T, yc, mu_c, sm_c, sp_c, part)
        sh_t = scores("hpd", T, yt, mu_t, sm_t, sp_t, part)
        qh_s = np.array([conformal_quantile(sh_c[st_c == k], alpha) for k in range(K)])
        out[f"S-HPD-{tag}"] = build_sets("hpd", T, mu_t, sm_t, sp_t, qh_s, part, yt, sh_t)
        if full:
            out[f"HPD-split-{tag}"] = build_sets("hpd", T, mu_t, sm_t, sp_t, np.full(K, conformal_quantile(sh_c, alpha)),
                                                 part, yt, sh_t)
    if full:
        out[f"DCP-{tag}"] = dcp_sets(T, mu_t, sm_t, sp_t, scores("dcp", T, yc, mu_c, sm_c, sp_c, part), alpha, part, yt)
        beta = min(2 * alpha, 0.5)
        q_f = np.maximum(np.array([conformal_quantile(sd_c[st_c == k], beta) for k in range(K)]), q_m)
        out[f"SDLC-{tag}-floor"] = build_sets("density", T, mu_t, sm_t, sp_t, q_f, part, yt, sd_t)
        out[f"SDLC-{tag}-hull"] = hull_of(out[f"SDLC-{tag}"], yt, part)
    return out

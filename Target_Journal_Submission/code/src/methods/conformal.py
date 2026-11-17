"""Conformal prediction methods evaluated in the study.

Every method returns a *prediction set* represented either as
  ('int', lo, hi)   union of G disjoint intervals per test point, arrays (n, G)
  ('mask', mask)    boolean (n, M) mask over the fine histogram bins of the partition
All sets are restricted to the bounded target domain D = [part.lo, part.hi].

Notation: alpha = target miscoverage. ``conformal_quantile`` returns the
ceil((n+1)(1-alpha))-th smallest score, +inf if that rank exceeds n.
"""
from __future__ import annotations

import numpy as np

from .strata import Partition


def conformal_quantile(scores, alpha):
    s = np.sort(np.asarray(scores, float))
    n = len(s)
    r = int(np.ceil((n + 1) * (1 - alpha)))
    return np.inf if r > n or n == 0 else s[r - 1]


def stratified_quantiles(scores, strata, K, alpha):
    return np.array([conformal_quantile(scores[strata == k], alpha) for k in range(K)])


# ----------------------------------------------------------------------------- interval scores
def _clip_int(lo, hi, part):
    return np.maximum(lo, part.lo), np.minimum(hi, part.hi)


def interval_method(score_cal, base_test, alpha, part, *, kind, strata_cal=None, scale_test=None,
                    alpha_k=None, floor_beta=None, half_open=True):
    """Generic residual-type conformal intervals.

    kind='res' : base_test = mu (n,), score |y-mu|, set mu +- t
    kind='nres': base_test = mu, scale_test=sigma, score |y-mu|/sigma
    kind='cqr' : base_test = (qlo, qhi), score max(qlo-y, y-qhi)
    If strata_cal is None -> marginal threshold, single interval.
    Else -> one threshold per target stratum k, set = U_k ( interval(t_k) ∩ B_k ).
    """
    def interval(t):
        if kind == "res":
            return base_test - t, base_test + t
        if kind == "nres":
            return base_test - t * scale_test, base_test + t * scale_test
        if kind == "cqr":
            return base_test[0] - t, base_test[1] + t
        raise ValueError(kind)

    if strata_cal is None:
        t = conformal_quantile(score_cal, alpha)
        lo, hi = interval(t)
        lo, hi = _clip_int(lo, hi, part)
        return ("int", lo[:, None], hi[:, None])
    K = part.K
    ak = np.full(K, alpha) if alpha_k is None else np.asarray(alpha_k)
    if floor_beta is not None:
        ak = np.full(K, floor_beta)
    tk = np.array([conformal_quantile(score_cal[strata_cal == k], ak[k]) for k in range(K)])
    if floor_beta is not None:   # floor rule: max(marginal threshold at alpha, stratum threshold at beta)
        tk = np.maximum(tk, conformal_quantile(score_cal, alpha))
    E = part.strata_edges
    n = len(base_test[0]) if kind == "cqr" else len(base_test)
    LO, HI = np.empty((n, K)), np.empty((n, K))
    for k in range(K):
        if np.isinf(tk[k]):
            l, h = np.full(n, E[k]), np.full(n, E[k + 1])
        else:
            l, h = interval(tk[k])
        # strata are half-open [e_k, e_{k+1}): the piece of stratum k must exclude its upper edge
        upper = np.nextafter(E[k + 1], -np.inf) if (half_open and k < K - 1) else E[k + 1]
        LO[:, k], HI[:, k] = np.maximum(l, E[k]), np.minimum(h, upper)
    return ("int", LO, HI)


# ----------------------------------------------------------------------------- level-set methods
def mask_method(score_cal_neg, Ftest, alpha, part, *, strata_cal=None, alpha_k=None,
                floor_beta=None):
    """Level-set methods on the fine-bin grid.

    score = -g(x, y) where g is a conformity level (density f or HPD value H);
    bin j enters the set iff -g_j(x) <= threshold of its stratum.
    floor_beta: SDLC-floor variant, threshold_k = max(q_marginal(alpha), q_k(beta)).
    """
    if strata_cal is None:
        t = conformal_quantile(score_cal_neg, alpha)
        thr = np.full(part.M, t)
    else:
        K = part.K
        ak = np.full(K, alpha if floor_beta is None else floor_beta) if alpha_k is None else np.asarray(alpha_k)
        tk = np.array([conformal_quantile(score_cal_neg[strata_cal == k], ak[k]) for k in range(K)])
        if floor_beta is not None:
            tk = np.maximum(tk, conformal_quantile(score_cal_neg, alpha))
        thr = tk[part.fine_stratum]
    return ("mask", (-Ftest) <= thr[None, :])


def dcp_method(Fc, yc, Ft, alpha, part):
    """Distributional conformal prediction (Chernozhukov, Wuthrich & Zhu, 2021):
    score |F(y|x) - 1/2| with the estimated conditional CDF."""
    from src.models.density import cdf_at, cdf_inv
    t = conformal_quantile(np.abs(cdf_at(Fc, yc, part) - 0.5), alpha)
    n = len(Ft)
    if not np.isfinite(t) or t >= 0.5:
        return ("int", np.full((n, 1), part.lo), np.full((n, 1), part.hi))
    lo = cdf_inv(Ft, np.full(n, 0.5 - t), part)
    hi = cdf_inv(Ft, np.full(n, 0.5 + t), part)
    return ("int", lo[:, None], hi[:, None])


def to_hull(S, part):
    """Convex hull of a prediction set (an interval, hence a superset: validity preserved)."""
    if S[0] == "int":
        lo, hi = S[1], S[2]
        ok = hi >= lo
        L = np.where(ok, lo, np.inf).min(1)
        H = np.where(ok, hi, -np.inf).max(1)
    else:
        m = S[1]
        any_ = m.any(1)
        first = np.argmax(m, axis=1)
        last = part.M - 1 - np.argmax(m[:, ::-1], axis=1)
        L = np.where(any_, part.fine_edges[first], np.inf)
        H = np.where(any_, part.fine_edges[last + 1], -np.inf)
    return ("int", L[:, None], H[:, None])

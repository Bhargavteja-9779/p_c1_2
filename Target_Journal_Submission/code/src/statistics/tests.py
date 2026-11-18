"""Statistical procedures used in the study (unit of analysis = dataset, after averaging
over the 10 predefined seeds, following Demšar, 2006)."""
from __future__ import annotations

import numpy as np
from scipy import stats


def holm(pvals):
    """Holm step-down adjustment; NaN p-values (untestable comparisons) stay NaN and are not counted."""
    p = np.asarray(pvals, float)
    adj = np.full(len(p), np.nan)
    fin = np.flatnonzero(np.isfinite(p))
    o = fin[np.argsort(p[fin])]
    m = len(fin)
    run = 0.0
    for r, i in enumerate(o):
        run = max(run, (m - r) * p[i])
        adj[i] = min(1.0, run)
    return adj


def rank_biserial(d):
    """Matched-pairs rank-biserial correlation for differences d (Kerby, 2014)."""
    d = np.asarray(d, float)
    d = d[d != 0]
    if len(d) == 0:
        return 0.0
    r = stats.rankdata(np.abs(d))
    return float((r[d > 0].sum() - r[d < 0].sum()) / r.sum())


def bootstrap_ci(x, fn=np.median, B=10000, seed=0, level=0.95):
    rng = np.random.default_rng(seed)
    x = np.asarray(x, float)
    bs = np.array([fn(x[rng.integers(0, len(x), len(x))]) for _ in range(B)])
    a = (1 - level) / 2
    return float(np.quantile(bs, a)), float(np.quantile(bs, 1 - a))


def paired_wilcoxon(a, b, alternative="two-sided"):
    """Wilcoxon signed-rank on paired per-dataset values a, b (difference a - b)."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    d = a[ok] - b[ok]
    if np.allclose(d, 0):
        return dict(n=int(ok.sum()), stat=np.nan, p=1.0, median_diff=0.0, ci=(0.0, 0.0), rbc=0.0,
                    wins=0, losses=0)
    res = stats.wilcoxon(d, alternative=alternative, zero_method="wilcox")
    return dict(n=int(ok.sum()), stat=float(res.statistic), p=float(res.pvalue),
                median_diff=float(np.median(d)), ci=bootstrap_ci(d), rbc=rank_biserial(d),
                wins=int((d > 0).sum()), losses=int((d < 0).sum()))


def friedman(matrix):
    """matrix: datasets x methods. Returns statistic, p, mean ranks (1 = smallest value)."""
    m = np.asarray(matrix, float)
    ranks = np.apply_along_axis(stats.rankdata, 1, m)
    st = stats.friedmanchisquare(*m.T)
    return float(st.statistic), float(st.pvalue), ranks.mean(0)


def nemenyi_cd(k, n, alpha=0.05):
    """Critical difference of the Nemenyi test (Demšar, 2006) using the studentized range."""
    q = stats.studentized_range.ppf(1 - alpha, k, np.inf) / np.sqrt(2)
    return float(q * np.sqrt(k * (k + 1) / (6 * n)))


# ---------------------------------------------------------------- additions (review cycle 1)
def sign_test(d):
    d = np.asarray(d, float)
    d = d[np.isfinite(d) & (d != 0)]
    if len(d) == 0:
        return 1.0
    return float(stats.binomtest(int((d > 0).sum()), len(d), 0.5).pvalue)


def hodges_lehmann(d, level=0.95):
    """Hodges-Lehmann pseudo-median of paired differences with the distribution-free CI obtained by
    inverting the Wilcoxon signed-rank test (Walsh averages; normal approximation for the critical rank)."""
    d = np.asarray(d, float)
    d = d[np.isfinite(d)]
    n = len(d)
    i, j = np.triu_indices(n)
    w = np.sort((d[i] + d[j]) / 2)
    hl = float(np.median(w))
    z = stats.norm.ppf(1 - (1 - level) / 2)
    c = int(np.floor(n * (n + 1) / 4 - z * np.sqrt(n * (n + 1) * (2 * n + 1) / 24)))
    c = max(c, 0)
    return hl, (float(w[c]), float(w[len(w) - 1 - c]))


def tost_wilcoxon(d, margin):
    """Equivalence test |median shift| < margin: two one-sided Wilcoxon tests; returns the larger p."""
    d = np.asarray(d, float)
    d = d[np.isfinite(d)]
    p_low = stats.wilcoxon(d + margin, alternative="greater").pvalue
    p_up = stats.wilcoxon(d - margin, alternative="less").pvalue
    return float(max(p_low, p_up))


def paired_summary(a, b, better="smaller", log=False, alternative="two-sided"):
    """Full paired comparison of per-dataset values a (method) vs b (comparator).
    better: 'smaller' (size) or 'larger' (coverage) -> defines wins/losses of `a`."""
    a, b = np.asarray(a, float), np.asarray(b, float)
    ok = np.isfinite(a) & np.isfinite(b)
    if log:
        ok &= (a > 0) & (b > 0)
    a, b = a[ok], b[ok]
    d = (np.log(a) - np.log(b)) if log else (a - b)
    if len(d) < 3:          # too few paired datasets for any test (e.g. quick mode or an empty subgroup)
        nan = float("nan")
        out = dict(n=int(len(d)), p=nan, p_sign=nan, hl=nan, hl_lo=nan, hl_hi=nan, rbc=nan, wins=int((d < 0).sum()),
                   losses=int((d > 0).sum()), ties=int((d == 0).sum()))
        if log:
            out.update(geo_ratio=float(np.exp(d.mean())) if len(d) else nan, geo_lo=nan, geo_hi=nan, hl_ratio=nan,
                       hl_ratio_lo=nan, hl_ratio_hi=nan)
        return out
    res = paired_wilcoxon(a if not log else np.log(a), b if not log else np.log(b), alternative=alternative)
    hl, (lo, hi) = hodges_lehmann(d)
    wins = int((d < 0).sum()) if better == "smaller" else int((d > 0).sum())
    losses = int((d > 0).sum()) if better == "smaller" else int((d < 0).sum())
    out = dict(n=int(len(d)), p=res["p"], p_sign=sign_test(d), hl=hl, hl_lo=lo, hl_hi=hi, rbc=res["rbc"],
               wins=wins, losses=losses, ties=int((d == 0).sum()))
    if log:
        lo_, hi_ = bootstrap_ci(d, fn=np.mean)
        out.update(geo_ratio=float(np.exp(d.mean())), geo_lo=float(np.exp(lo_)), geo_hi=float(np.exp(hi_)),
                   hl_ratio=float(np.exp(hl)), hl_ratio_lo=float(np.exp(lo)), hl_ratio_hi=float(np.exp(hi)))
    return out

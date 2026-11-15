"""Statistical procedures used in the study (unit of analysis = dataset, after averaging
over the 10 predefined seeds, following Demšar, 2006)."""
from __future__ import annotations

import numpy as np
from scipy import stats


def holm(pvals):
    p = np.asarray(pvals, float)
    o = np.argsort(p)
    m = len(p)
    adj = np.empty(m)
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

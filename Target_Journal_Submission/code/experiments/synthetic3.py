"""Synthetic study v3 (review cycle 1, issues C1-18/C1-19): known conditional densities, misspecified
designs, small samples and a genuine label shift.

DGPs (X ~ U[-1,1]^5, mu(x) = 2 sin(pi x1) + 2 x2^2 + x3, sigma(x) = 0.2 + 0.8|x4|):
  A  Y = mu + sigma * eps, eps = standardised Gamma(2)                    (location-scale, skewed)
  B  eps = standardised skew-normal with shape 5 x5                       (covariate-dependent skewness)
  C  eps = mixture: N(-1, .35^2) w.p. logistic(3 x5), else N(1, .35^2)    (covariate-dependent bimodality)
  D  eps = t_3 / sqrt(3)                                                   (heavy tails, location-scale)
  E  Y = 0 w.p. 0.2 + 0.4 logistic(2 x1), else exp(mu/2 + 0.5 sigma Z)      (zero inflation; no oracle)
Regimes: n_train = n_cal = 5000 (all DGPs); 500 (A, B). 20,000 test points, 10 seeds, alpha = 0.1.
Label shift (A, B, n = 5000): test points drawn from a pool by rejection with acceptance proportional to
exp(gamma * Phi^{-1}(F_Y(y))), gamma in {0.5, 1, 2}; X | Y is unchanged (genuine label shift).
Estimated methods use the v3 pipeline (cross-fitted standardisation, robust KDE, exact geometry);
oracle methods use the true density on a fine per-x grid.
"""
from __future__ import annotations

import json
import os
import sys
from multiprocessing import Pool
from pathlib import Path

import numpy as np
from scipy import stats
from sklearn.model_selection import KFold

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from src.evaluation.metrics import evaluate  # noqa: E402
from src.methods import conformal as C  # noqa: E402
from src.methods import ls_exact3 as L3  # noqa: E402
from src.methods.strata import make_partition  # noqa: E402
from src.models import density as D  # noqa: E402
from src.models import learners as Lr  # noqa: E402

OUT = ROOT.parent / "results" / "synthetic_v3.jsonl"
ALPHA = 0.1
SN_A = lambda x5: 5 * x5


def mu_f(X):
    return 2 * np.sin(np.pi * X[:, 0]) + 2 * X[:, 1] ** 2 + X[:, 2]


def sig_f(X):
    return 0.2 + 0.8 * np.abs(X[:, 3])


def _sn_moments(a):
    d = a / np.sqrt(1 + a ** 2)
    m = d * np.sqrt(2 / np.pi)
    return m, np.sqrt(1 - m ** 2)


def sample(dgp, n, rng):
    X = rng.uniform(-1, 1, (n, 5))
    mu, s = mu_f(X), sig_f(X)
    if dgp == "A":
        eps = (rng.gamma(2.0, 1.0, n) - 2) / np.sqrt(2)
    elif dgp == "B":
        a = SN_A(X[:, 4])
        m, sd = _sn_moments(a)
        eps = (stats.skewnorm.rvs(a, random_state=rng) - m) / sd
    elif dgp == "C":
        p = 1 / (1 + np.exp(-3 * X[:, 4]))
        comp = rng.uniform(size=n) < p
        eps = np.where(comp, rng.normal(-1, 0.35, n), rng.normal(1, 0.35, n))
    elif dgp == "D":
        eps = rng.standard_t(3, n) / np.sqrt(3)
    elif dgp == "E":
        p0 = 0.2 + 0.4 / (1 + np.exp(-2 * X[:, 0]))
        y = np.where(rng.uniform(size=n) < p0, 0.0, np.exp(mu / 2 + 0.5 * s * rng.normal(size=n)))
        return X, y
    return X, mu + s * eps


def true_pdf(dgp, X, y):
    """Conditional density f(y|x) for each row of X (y broadcast as (n, G))."""
    mu, s = mu_f(X)[:, None], sig_f(X)[:, None]
    z = (y - mu) / s
    if dgp == "A":
        return stats.gamma.pdf(z * np.sqrt(2) + 2, 2.0) * np.sqrt(2) / s
    if dgp == "B":
        a = SN_A(X[:, 4])[:, None]
        m, sd = _sn_moments(a)
        return stats.skewnorm.pdf(z * sd + m, a) * sd / s
    if dgp == "C":
        p = (1 / (1 + np.exp(-3 * X[:, 4])))[:, None]
        return (p * stats.norm.pdf(z, -1, 0.35) + (1 - p) * stats.norm.pdf(z, 1, 0.35)) / s
    if dgp == "D":
        return stats.t.pdf(z * np.sqrt(3), 3) * np.sqrt(3) / s
    raise ValueError(dgp)


def oracle_sets(dgp, Xc, yc, Xt, yt, part, G=3000):
    """Oracle stratified density level sets, oracle X-conditional HDR, and oracle residual scores,
    computed on a fine per-x grid (mu +- 12 sigma, D: +- 40 sigma), restricted to the domain D."""
    K = part.K
    span = 40.0 if dgp == "D" else 12.0
    fc = true_pdf(dgp, Xc, yc[:, None])[:, 0]
    st_c = part.stratum(yc)
    q_s = np.array([C.conformal_quantile(-fc[st_c == k], ALPHA) for k in range(K)])
    mu_t, s_t = mu_f(Xt), sig_f(Xt)
    out = {"O-SDLC": dict(size=np.zeros(len(yt))), "O-HDR-X": dict(size=np.zeros(len(yt)))}
    cov_hdr = np.zeros(len(yt), bool)
    u = np.linspace(-span, span, G)
    for a in range(0, len(yt), 1000):
        b = min(len(yt), a + 1000)
        yy = mu_t[a:b, None] + s_t[a:b, None] * u[None, :]
        dy = (yy[:, 1] - yy[:, 0])[:, None]
        f = true_pdf(dgp, Xt[a:b], yy)
        inD = (yy >= part.lo) & (yy <= part.hi)
        k = part.stratum(yy)
        inc = (f >= -q_s[k]) & inD
        out["O-SDLC"]["size"][a:b] = (inc * dy).sum(1)
        # exact X-conditional HDR at level 1-alpha (per x)
        o = np.argsort(-f, axis=1)
        fs = np.take_along_axis(f, o, 1)
        cm = np.cumsum(fs * dy, 1)
        idx = np.argmax(cm >= 1 - ALPHA, axis=1)
        thr = fs[np.arange(b - a), idx]
        out["O-HDR-X"]["size"][a:b] = ((f >= thr[:, None]) & inD).sum(1) * dy[:, 0]
        cov_hdr[a:b] = true_pdf(dgp, Xt[a:b], yt[a:b, None])[:, 0] >= thr
    ft = true_pdf(dgp, Xt, yt[:, None])[:, 0]
    k_t = part.stratum(yt)
    out["O-SDLC"]["cov"] = (-ft <= q_s[k_t]) & part.in_domain(yt)
    out["O-HDR-X"]["cov"] = cov_hdr & part.in_domain(yt)
    sets = {m: ("geo", v["size"], np.ones(len(yt)), np.full(len(yt), np.nan), np.full(len(yt), np.nan),
                np.zeros((len(yt), K), bool), v["cov"]) for m, v in out.items()}
    mu_c, s_c = mu_f(Xc), sig_f(Xc)
    sets["O-S-Res"] = C.interval_method(np.abs(yc - mu_c), mu_t, ALPHA, part, kind="res", strata_cal=st_c)
    sets["O-S-NCP"] = C.interval_method(np.abs(yc - mu_c) / s_c, mu_t, ALPHA, part, kind="nres", scale_test=s_t,
                                        strata_cal=st_c)
    return sets


def fit_estimated(Xtr, ytr, seed):
    mu = Lr.fit_point(Xtr, ytr, seed, 1)
    sg, oof = Lr.fit_scale(Xtr, ytr, seed, 1, return_oof=True)
    r = ytr - oof
    floor = max(1e-3 * ytr.std(), 0.05 * float(np.median(np.abs(r)))) + 1e-12
    sig_cf = np.zeros_like(ytr)
    for k, (a, b) in enumerate(KFold(3, shuffle=True, random_state=seed).split(Xtr)):
        m = Lr._fit(Lr.lgb.LGBMRegressor(n_estimators=Lr.MAX_ROUNDS, **Lr.LGB_PARAMS), Xtr[a], np.abs(r[a]),
                    seed + 200 + k, 1)
        sig_cf[b] = m.predict(Xtr[b])
    ql = Lr.fit_quantile(Xtr, ytr, ALPHA / 2, seed, 1)
    qh = Lr.fit_quantile(Xtr, ytr, 1 - ALPHA / 2, seed, 1)
    T = L3.LSTable3(D.RobustLSDensity(r / np.maximum(sig_cf, floor)))
    TN = L3.LSTable3(D.GaussianNoiseDensity())
    return dict(mu=mu, sg=sg, floor=floor, ql=ql, qh=qh, T=T, TN=TN)


def estimated_sets(M, Xc, yc, Xt, yt, part):
    fl = lambda v: np.maximum(v, M["floor"])
    mu_c, mu_t = M["mu"].predict(Xc), M["mu"].predict(Xt)
    s_c, s_t = fl(M["sg"].predict(Xc)), fl(M["sg"].predict(Xt))
    qlc, qhc, qlt, qht = M["ql"].predict(Xc), M["qh"].predict(Xc), M["ql"].predict(Xt), M["qh"].predict(Xt)
    st = part.stratum(yc)
    res, nres, cqr = np.abs(yc - mu_c), np.abs(yc - mu_c) / s_c, np.maximum(qlc - yc, yc - qhc)
    sets = {"SCP": C.interval_method(res, mu_t, ALPHA, part, kind="res"),
            "NCP": C.interval_method(nres, mu_t, ALPHA, part, kind="nres", scale_test=s_t),
            "CQR": C.interval_method(cqr, (qlt, qht), ALPHA, part, kind="cqr"),
            "S-Res": C.interval_method(res, mu_t, ALPHA, part, kind="res", strata_cal=st),
            "S-NCP": C.interval_method(nres, mu_t, ALPHA, part, kind="nres", scale_test=s_t, strata_cal=st),
            "S-CQR": C.interval_method(cqr, (qlt, qht), ALPHA, part, kind="cqr", strata_cal=st)}
    sets.update(L3.ls_methods(M["T"], "LS", mu_c, s_c, s_c, yc, mu_t, s_t, s_t, yt, ALPHA, part, st, full=True))
    sets.update(L3.ls_methods(M["TN"], "N", mu_c, s_c, s_c, yc, mu_t, s_t, s_t, yt, ALPHA, part, st, full=False,
                              hpd=False))
    return sets


def tilted_test(dgp, n_test, gamma, rng, ref_sorted):
    """Genuine label shift: rejection sampling with acceptance prop. to exp(gamma * Phi^{-1}(F_Y(y)))."""
    Xs, ys = [], []
    while sum(len(v) for v in ys) < n_test:
        X, y = sample(dgp, 200_000, rng)
        u = (np.searchsorted(ref_sorted, y) + 0.5) / (len(ref_sorted) + 1)
        z = stats.norm.ppf(np.clip(u, 1e-5, 1 - 1e-5))
        w = np.exp(gamma * (z - z.max()))
        keep = rng.uniform(size=len(y)) < w / w.max()
        Xs.append(X[keep])
        ys.append(y[keep])
    X, y = np.concatenate(Xs)[:n_test], np.concatenate(ys)[:n_test]
    return X, y


def run(task):
    dgp, n, seed = task
    rng = np.random.default_rng(1000 * seed + ord(dgp) + n)
    Xtr, ytr = sample(dgp, n, rng)
    Xc, yc = sample(dgp, n, rng)
    part = make_partition(ytr, nonneg=(dgp == "E"))
    M = fit_estimated(Xtr, ytr, seed)
    rows = []
    shifts = [0.0] + ([0.5, 1.0, 2.0] if (dgp in "AB" and n == 5000) else [])
    ref = np.sort(sample(dgp, 200_000, np.random.default_rng(seed + 77))[1])
    for gamma in shifts:
        if gamma == 0.0:
            Xt, yt = sample(dgp, 20_000, rng)
        else:
            Xt, yt = tilted_test(dgp, 20_000, gamma, np.random.default_rng(seed * 31 + int(10 * gamma)), ref)
        es = {"cal": part.stratum(yt),
              "ext": np.searchsorted(np.quantile(ytr, [0.05, 0.95]), yt, side="right")}
        sets = estimated_sets(M, Xc, yc, Xt, yt, part)
        if dgp != "E":
            sets.update(oracle_sets(dgp, Xc, yc, Xt, yt, part))
        for m, S in sets.items():
            r, _ = evaluate(S, yt, part, ALPHA, es)
            rows.append(dict(dgp=dgp, n=n, seed=seed, gamma=gamma, K=part.K, method=m,
                             scores="oracle" if m.startswith("O-") else "estimated", **r))
    return rows


if __name__ == "__main__":
    tasks = [(d, 5000, s) for d in "ABCDE" for s in range(10)] + [(d, 500, s) for d in "AB" for s in range(10)]
    workers = int(sys.argv[1]) if len(sys.argv) > 1 else 4
    with Pool(workers) as pool, open(OUT, "w") as fh:
        for rows in pool.imap_unordered(run, tasks):
            for r in rows:
                fh.write(json.dumps(r) + "\n")
            fh.flush()
            print(rows[0]["dgp"], rows[0]["n"], rows[0]["seed"], "done", flush=True)

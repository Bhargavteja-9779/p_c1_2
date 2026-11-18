"""Decision study (review cycle 1, issues C1-21/C1-22): dedicated tail-alert rules versus alerts read off
prediction sets.

A unit is 'extreme' if its outcome falls in the upper (lower) calibration stratum, i.e. above (below) the
training 90% (10%) quantile. A prediction set C(x) raises an alert when it intersects that stratum; for any
method whose coverage of the stratum is >= 1 - alpha the alert recall is >= 1 - alpha by construction.
This script computes, from the cached model outputs (same models, same splits), dedicated rules:

  TC-LS   class-conditional conformal tail classifier: score p(x) = P_hat(Y in tail | x) from the
          cross-fitted location-scale model (same KDE noise density as SDLC); threshold = conformal
          quantile at level alpha of the scores of calibration units that ARE in the tail, which
          guarantees recall >= 1 - alpha (exchangeability within the tail class);
  TC-H    the same with p(x) from the histogram (multi-class) classifier;
  CS-BH-q conformal selection (Jin & Candes, 2023): conformal p-values against calibration units NOT in
          the tail, Benjamini-Hochberg at FDR level q in {0.1, 0.2}; controls the false discovery rate,
          not recall;
  Point   naive rule 'alert if mu_hat(x) is in the tail' (no guarantee).
Output: results/tail_alerts.jsonl (one row per dataset x seed x side x rule with counts).
"""
from __future__ import annotations

import json
import os
import sys
import traceback
from multiprocessing import Pool
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from experiments.evaluate_from_cache3 import CACHE, CACHE3, build_context  # noqa: E402
from experiments.run_benchmark import CFG  # noqa: E402
from src.data.openml_ctr23 import load  # noqa: E402
from src.methods import ls_exact3 as L3  # noqa: E402
from src.methods.conformal import conformal_quantile  # noqa: E402
from src.methods.strata import coarse_bins, make_partition  # noqa: E402

OUT = ROOT.parent / "results" / "tail_alerts.jsonl"
ALPHA = 0.1


def bh(p, q):
    m = len(p)
    o = np.sort(p)
    ok = np.nonzero(o <= q * np.arange(1, m + 1) / m)[0]
    if len(ok) == 0:
        return np.zeros(m, bool)
    return p <= o[ok[-1]]


def conformal_pvalues(s_null_cal, s_test, rng):
    """p_j = (#{null cal: s_i >= s_j} + U (1 + ties))/(n_cal + 1) for 'larger score = more extreme';
    calibration units in the tail are clipped to -inf (Jin & Candes' clipped score), so only the
    n_null units count, while the denominator uses the whole calibration set."""
    srt = np.sort(s_null_cal)
    ge = len(srt) - np.searchsorted(srt, s_test, side="left")
    eq = np.searchsorted(srt, s_test, side="right") - np.searchsorted(srt, s_test, side="left")
    return (ge - eq + rng.uniform(size=len(s_test)) * (1 + eq)) / (len(s_null_cal) + 1)


def one(did, seed):
    c = dict(np.load(CACHE / f"{did}_{seed}.npz"))
    c3 = dict(np.load(CACHE3 / f"{did}_{seed}.npz"))
    part = make_partition(c["y_train"], n_fine=CFG["n_fine"], n_coarse=CFG["n_coarse"], nonneg=True)
    ctx, tables, scales = build_context(c, c3, part, [ALPHA])
    T = tables["LS"]
    yc, yt = ctx["yc"], ctx["yt"]
    E = part.strata_edges
    st_c, st_t = part.stratum(yc), part.stratum(yt)
    edges, cell_to = coarse_bins(part, CFG["n_coarse"])
    Pc, Pt = c["P_c_H"].astype(float), c["P_t_H"].astype(float)
    name = load(did)[2]["name"]
    rng = np.random.default_rng(20_000 + seed)
    rows = []
    for side, k, cut in (("hi", part.K - 1, E[part.K - 1]), ("lo", 0, E[1])):
        def p_ls(mu, sg):
            F = T.F_at((cut - mu) / sg)
            return 1 - F if side == "hi" else F
        sc_c, sc_t = p_ls(ctx["mu_c"], ctx["sg_c"]), p_ls(ctx["mu_t"], ctx["sg_t"])
        lower_edge = edges[:-1]
        tail_bins = (lower_edge >= cut) if side == "hi" else (edges[1:] <= cut)
        hc, ht = Pc[:, tail_bins].sum(1), Pt[:, tail_bins].sum(1)
        pos_c, pos_t = st_c == k, st_t == k
        rules = {}
        for nm, (a_c, a_t) in (("TC-LS", (sc_c, sc_t)), ("TC-H", (hc, ht))):
            thr = conformal_quantile(-a_c[pos_c], ALPHA)          # recall >= 1 - alpha
            rules[nm] = -a_t <= thr
        for q in (0.1, 0.2):
            p = conformal_pvalues(sc_c[~pos_c], sc_t, rng)
            rules[f"CS-BH-{q}"] = bh(p, q)
        rules["Point"] = (part.stratum(ctx["mu_t"]) == k)
        for nm, al in rules.items():
            tp = int((al & pos_t).sum())
            rows.append(dict(did=did, dataset=name, seed=seed, side=side, rule=nm, n=len(yt),
                             positives=int(pos_t.sum()), alerts=int(al.sum()), tp=tp, n_cal_pos=int(pos_c.sum())))
    return rows


def _star(a):
    try:
        return one(*a)
    except Exception:
        print("FAILED", a, traceback.format_exc()[-1500:], flush=True)
        return []


if __name__ == "__main__":
    workers = int(sys.argv[1]) if len(sys.argv) > 1 else 1
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    tasks = [(d, s) for d in CFG["datasets"] for s in CFG["seeds"]]
    out = []
    with Pool(workers) as pool:
        for r in pool.imap_unordered(_star, tasks):
            out += r
    with open(OUT.with_suffix(".tmp"), "w") as fh:
        for r in out:
            fh.write(json.dumps(r) + "\n")
    os.replace(OUT.with_suffix(".tmp"), OUT)
    print("rows", len(out))

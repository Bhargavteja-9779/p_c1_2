"""Post-hoc and pre-registered-secondary analyses requested in review round 3 (REVIEW/review_03.md).
Does NOT modify the pre-registered confirmatory script (scripts/analyze_confirmatory.py).

  (a) held-out data, pre-registered secondary: hull forms SDLC-hull vs BCCP-hull (S-Res-hull) and vs S-NCP-hull;
  (b) post hoc: TOST equivalence (+-5% on the log-size scale, two one-sided Wilcoxon tests) of SDLC vs S-NCP and
      vs S-HPD on CTR23 and on the held-out data;
  (c) post hoc: target skewness of the held-out datasets and the size comparisons by skewness subgroup (|skew| > 1);
  (d) post hoc: per-dataset reliability: number of datasets whose seed-level 95% t-interval of the log size ratio
      excludes 0 (in either direction), CTR23 and held-out.
Writes results/statistics_secondary.json and tables/T18_secondary.csv.
"""
from __future__ import annotations

import glob
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
TOP = ROOT.parent
sys.path.insert(0, str(ROOT))
from src.statistics.tests import holm, paired_summary, tost_wilcoxon  # noqa: E402

RES, TAB = TOP / "results", TOP / "tables"
NAME = {"S-Res": "BCCP", "S-Res-hull": "BCCP-hull", "SDLC-LS": "SDLC", "SDLC-LS-hull": "SDLC-hull",
        "S-HPD-LS": "S-HPD", "S-NCP": "S-NCP", "S-NCP-hull": "S-NCP-hull", "S-CQR": "S-CQR"}


def load(d):
    x = pd.concat([pd.read_json(f, lines=True) for f in sorted(glob.glob(str(d / "*.jsonl")))], ignore_index=True)
    x = x[(x.alpha == 0.1) & (x.scheme == "S5") & (x.cal_frac.isna() | (x.cal_frac == 1.0))]
    x = x[x.method.isin(NAME)].copy()
    x["m"] = x.method.map(NAME)
    x["nsize"] = x["size"] / x["y_train_sd"]
    return x


def per_ds(x):
    return x.groupby(["did", "m"]).nsize.apply(lambda v: float(np.exp(np.log(v).mean()))).unstack()


def reliability(x, a, b):
    """Datasets whose seed-level 95% t-interval of log(size_a/size_b) excludes 0."""
    w = x.pivot_table(index=["did", "seed"], columns="m", values="nsize")
    lr = np.log(w[a] / w[b]).dropna()
    fav = unf = 0
    for _, v in lr.groupby(level=0):
        if len(v) < 2:
            continue
        m, se = v.mean(), v.std(ddof=1) / np.sqrt(len(v))
        h = stats.t.ppf(0.975, len(v) - 1) * se
        fav += int(m + h < 0)
        unf += int(m - h > 0)
    return dict(n=int(lr.index.get_level_values(0).nunique()), reliably_smaller=fav, reliably_larger=unf)


def skewness_conf():
    rows = []
    for f in sorted((RES / "confirmatory" / "raw_contexts").glob("*_0.npz")):
        y = np.load(f)["y_train"].astype(float)
        q = np.quantile(y, [0.125, 0.5, 0.875])
        rows.append(dict(did=int(f.stem.split("_")[0]), skew=float(stats.skew(y)),
                         octile_skew=float((q[2] + q[0] - 2 * q[1]) / (q[2] - q[0])) if q[2] > q[0] else 0.0,
                         min_y=float(y.min()), n_distinct=int(len(np.unique(y)))))
    return pd.DataFrame(rows)


def main():
    out, rows = {}, []
    suites = {"ctr23": RES / "raw_eval_v3", "confirmatory": RES / "confirmatory" / "raw_eval_v3"}
    data = {s: load(d) for s, d in suites.items()}
    for s, x in data.items():
        P = per_ds(x)
        # (a) hull forms (pre-registered secondary on the held-out data; descriptive on CTR23)
        hull = {}
        tests = [("SDLC-hull", "BCCP-hull"), ("SDLC-hull", "S-NCP-hull")]
        res = [paired_summary(P[a], P[b], better="smaller", log=True) for a, b in tests]
        ph = holm([r["p"] for r in res])
        for (a, b), r, h in zip(tests, res, ph):
            hull[f"{a} vs {b}"] = dict(r, p_holm=float(h))
            rows.append(dict(suite=s, analysis="hull (secondary)", comparison=f"{a} vs {b}", n=r["n"],
                             geo_ratio=r["geo_ratio"], geo_lo=r["geo_lo"], geo_hi=r["geo_hi"], hl_ratio=r["hl_ratio"],
                             wins=r["wins"], losses=r["losses"], p=r["p"], p_holm=float(h)))
        out[f"{s}.hull"] = hull
        # (b) TOST +-5% on log size
        tost = {}
        for b in ("S-NCP", "S-HPD"):
            d = (np.log(P["SDLC"]) - np.log(P[b])).dropna().values
            p = tost_wilcoxon(d, np.log(1.05))
            r = paired_summary(P["SDLC"], P[b], better="smaller", log=True)
            tost[b] = dict(p_tost=p, equivalent=bool(p < 0.05), hl_ratio=r["hl_ratio"], geo_ratio=r["geo_ratio"])
            rows.append(dict(suite=s, analysis="TOST +-5% (post hoc)", comparison=f"SDLC vs {b}", n=len(d),
                             geo_ratio=r["geo_ratio"], geo_lo=r["geo_lo"], geo_hi=r["geo_hi"], hl_ratio=r["hl_ratio"],
                             wins=r["wins"], losses=r["losses"], p=p, p_holm=p))
        out[f"{s}.tost5"] = tost
        # (d) reliability
        out[f"{s}.reliability"] = {b: reliability(x, "SDLC", b) for b in ("BCCP", "S-NCP", "S-CQR", "S-HPD")}
    # (c) skewness of the held-out targets and subgroup comparisons
    sk = skewness_conf()
    sk.to_csv(TAB / "T18b_confirmatory_skewness.csv", index=False)
    P = per_ds(data["confirmatory"])
    grp = {}
    for name, ids in (("|skew|>1", sk.did[sk["skew"].abs() > 1]), ("|skew|<=1", sk.did[sk["skew"].abs() <= 1])):
        g = {}
        for b in ("BCCP", "S-NCP", "S-CQR", "S-HPD"):
            Q = P.loc[P.index.isin(ids)]
            r = paired_summary(Q["SDLC"], Q[b], better="smaller", log=True)
            g[b] = dict(n=r["n"], geo_ratio=r["geo_ratio"], wins=r["wins"], losses=r["losses"])
            rows.append(dict(suite="confirmatory", analysis=f"subgroup {name} (post hoc, descriptive)",
                             comparison=f"SDLC vs {b}", n=r["n"], geo_ratio=r["geo_ratio"], geo_lo=r.get("geo_lo"),
                             geo_hi=r.get("geo_hi"), hl_ratio=r.get("hl_ratio"), wins=r["wins"], losses=r["losses"],
                             p=r["p"], p_holm=np.nan))
        grp[name] = g
    out["confirmatory.skew_groups"] = grp
    out["confirmatory.n_skewed"] = int((sk["skew"].abs() > 1).sum())
    out["confirmatory.skew_median"] = float(sk["skew"].abs().median())
    (RES / "statistics_secondary.json").write_text(json.dumps(out, indent=1, default=float))
    T = pd.DataFrame(rows)
    T.to_csv(TAB / "T18_secondary.csv", index=False)
    print(T.round(3).to_string())
    print(json.dumps({k: v for k, v in out.items() if "reliab" in k or "n_skew" in k or "median" in k}, indent=0))


if __name__ == "__main__":
    main()

"""Pre-registered analysis of the confirmatory replication (see ../PREREGISTRATION_confirmatory.md).

This file was committed, together with the pre-registration document, BEFORE any confirmatory evaluation
result existed. It reads results/confirmatory/raw_eval_v3/*.jsonl (evaluate_from_cache3.py run with
TSCP_CONFIG=confirmatory.json) and writes results/confirmatory/{statistics,metrics}_confirmatory.json and
tables/C*_*.csv/.md. The analysis is fixed:

  unit of analysis   dataset (metrics averaged over the 5 predefined seeds), alpha = 0.1, strata S5
  C-H1 (coverage)    SDLC worst-stratum coverage > each of the 7 marginal / covariate-adaptive methods;
                     one-sided Wilcoxon signed-rank, Holm over 7, level 0.05; supported iff all 7 reject
  C-H2 (validity)    number of datasets on which SDLC's worst-stratum coverage lies below the 5% quantile of
                     its exact-validity null reference; consistent with validity iff <= 3 (the 95% quantile
                     of Binomial(17, 0.05)); also a one-sided binomial test for excess
  C-H3 (size)        SDLC vs BCCP, S-NCP, S-CQR, S-HPD: two-sided Wilcoxon signed-rank on log size ratios,
                     Holm over 4, level 0.05; effect = geometric-mean ratio (95% bootstrap CI) and
                     Hodges-Lehmann ratio (95% CI); a comparison 'favours SDLC' iff Holm p < 0.05 and ratio < 1
  C-H4 (equivalence) TOST (Wilcoxon) of worst-stratum coverage, SDLC vs S-NCP and vs BCCP, margin 0.02
  secondary          price SDLC/DLS; upper-tail, top-5% and top-1% coverage; empty-set rate; worst sigma-hat
                     decile coverage; the C-H3 comparisons under decile strata (S10); all descriptive
Usage: python scripts/analyze_confirmatory.py [raw_dir] [out_root]
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
TOP = ROOT.parent
sys.path.insert(0, str(ROOT))
from scripts.analyze import null_worst_stratum  # noqa: E402
from src.statistics.tests import holm, paired_summary, tost_wilcoxon  # noqa: E402

RAW = Path(sys.argv[1]) if len(sys.argv) > 1 else TOP / "results" / "confirmatory" / "raw_eval_v3"
OUT = Path(sys.argv[2]) if len(sys.argv) > 2 else TOP / "results" / "confirmatory"
TAB = OUT / "tables"
TAB.mkdir(parents=True, exist_ok=True)
P = "SDLC-LS"
MARGINAL = ["SCP", "NCP", "CQR", "MCP-yhat", "DCP-LS", "HPD-split-LS", "DLS-M-LS"]
H3 = ["S-Res", "S-NCP", "S-CQR", "S-HPD-LS"]
NAME = {"SCP": "SCP", "NCP": "NCP", "CQR": "CQR", "MCP-yhat": "Mondrian-yhat", "DCP-LS": "DCP",
        "HPD-split-LS": "HPD-split", "DLS-M-LS": "DLS", "S-Res": "BCCP", "S-NCP": "S-NCP", "S-CQR": "S-CQR",
        "S-HPD-LS": "S-HPD", "SDLC-LS": "SDLC", "SDLC-N": "SDLC-N", "SDLC-LS-floor": "SDLC-floor",
        "SDLC-LS-hull": "SDLC-hull", "S-Res-hull": "BCCP-hull", "S-NCP-hull": "S-NCP-hull"}


def load():
    files = sorted(RAW.glob("*.jsonl"))
    df = pd.concat([pd.read_json(f, lines=True) for f in files], ignore_index=True)
    df["nsize"] = df["size"] / df["y_train_sd"]
    cc = [c for c in df.columns if c.startswith("cal_cov_") and c[8:].isdigit()]
    df["tail_hi"] = [r[f"cal_cov_{int(k) - 1}"] for k, r in zip(df.K, df[cc].to_dict("records"))]
    return df


def per_dataset(d):
    mk = d.groupby("did").K.agg(lambda k: k.value_counts().idxmax())
    d = d[d.K == d.did.map(mk)]
    cc = [c for c in d.columns if c.startswith("cal_cov_") and c[8:].isdigit()]
    cols = [c for c in ("coverage", "nsize", "tail_hi", "ext_cov_2", "ext1_cov_2", "empty_rate", "sig_worst",
                        "components") if c in d.columns]
    g = d.groupby(["did", "dataset", "method"])
    out = g[cols].mean()
    out["worst_stratum"] = g[cc].mean().min(axis=1, skipna=True)
    return out.reset_index(), d


def main():
    df = load()
    a = df[(df.alpha == 0.1) & (df.scheme == "S5") & (df.cal_frac == 1.0)]
    pdm, a_mk = per_dataset(a)
    n_ds = int(pdm.did.nunique())
    piv = lambda col: pdm.pivot(index="did", columns="method", values=col)
    res = {"n_datasets": n_ds, "n_seeds_min": int(a.groupby("did").seed.nunique().min()),
           "datasets": sorted(pdm.dataset.unique().tolist())}
    # C-H1
    W = piv("worst_stratum")
    rows = [{"comparison": f"SDLC vs {NAME[m]}", **paired_summary(W[P], W[m], better="larger", alternative="greater")}
            for m in MARGINAL]
    for r, p in zip(rows, holm([r["p"] for r in rows])):
        r["p_holm"] = p
    res["C-H1"] = {"tests": rows, "supported": bool(all(r["p_holm"] < 0.05 for r in rows))}
    # C-H2
    nul = null_worst_stratum(a_mk[a_mk.method == P])
    sd = pdm[pdm.method == P].set_index("did")
    below = int(sum(sd.loc[d, "worst_stratum"] < nul[d][1] for d in sd.index))
    crit = int(stats.binom.ppf(0.95, n_ds, 0.05))
    res["C-H2"] = {"n_below_null_q05": below, "critical": crit,
                   "binom_p_excess": float(stats.binomtest(below, n_ds, 0.05, alternative="greater").pvalue),
                   "consistent_with_validity": below <= crit,
                   "marginal_methods_below": {NAME[m]: int(sum(W.loc[d, m] < nul[d][1] for d in W.index)) for m in MARGINAL}}
    # C-H3
    S = piv("nsize")
    rows = [{"comparison": f"SDLC vs {NAME[m]}", **paired_summary(S[P], S[m], better="smaller", log=True)} for m in H3]
    for r, p in zip(rows, holm([r["p"] for r in rows])):
        r["p_holm"] = p
        r["favours_SDLC"] = bool(p < 0.05 and r["geo_ratio"] < 1)
        r["favours_comparator"] = bool(p < 0.05 and r["geo_ratio"] > 1)
    res["C-H3"] = {"tests": rows}
    # C-H4
    res["C-H4"] = [{"comparison": f"SDLC vs {NAME[m]}", "margin": 0.02, "p_tost": tost_wilcoxon(W[P] - W[m], 0.02),
                    "median_diff": float(np.median(W[P] - W[m]))} for m in ("S-NCP", "S-Res")]
    # secondary (descriptive)
    summ = []
    for m in MARGINAL + H3 + [P] + [x for x in ("SDLC-N", "SDLC-LS-floor", "SDLC-LS-hull", "S-Res-hull", "S-NCP-hull")
                                    if x in set(pdm.method)]:
        x = pdm[pdm.method == m]
        summ.append({"method": NAME.get(m, m), "code": m, "coverage": x.coverage.mean(), "upper_tail": x.tail_hi.mean(),
                     "worst_stratum": x.worst_stratum.mean(), "top5": x.ext_cov_2.mean(), "top1": x.ext1_cov_2.mean(),
                     "size_geo": float(np.exp(np.log(x.nsize).mean())), "empty_rate": x.empty_rate.mean(),
                     "sigma_decile_worst": x.sig_worst.mean(), "pieces": x.components.mean()})
    T = pd.DataFrame(summ)
    T.to_csv(TAB / "C2_main.csv", index=False)
    (TAB / "C2_main.md").write_text(T.drop(columns="code").to_markdown(index=False, floatfmt=".3f"))
    res["summary"] = {r["code"]: r for r in summ}
    lr = np.log(S[P] / S["DLS-M-LS"])
    res["price_vs_DLS_geo"] = float(np.exp(lr.mean()))
    s10 = df[(df.alpha == 0.1) & (df.scheme == "S10") & (df.cal_frac == 1.0)]
    if len(s10):
        p10, _ = per_dataset(s10)
        S10 = p10.pivot(index="did", columns="method", values="nsize")
        res["C-H3_S10_descriptive"] = [{"comparison": f"SDLC vs {NAME[m]}",
                                        **paired_summary(S10[P], S10[m], better="smaller", log=True)}
                                       for m in ("S-Res", "S-NCP", "S-CQR") if m in S10]
    per = pdm.pivot(index="dataset", columns="method", values="nsize")[[P] + H3]
    per.to_csv(TAB / "C3_per_dataset_size.csv")
    json.dump(res, open(OUT / "statistics_confirmatory.json", "w"), indent=1, default=float)
    print(json.dumps({k: res[k] for k in ("n_datasets", "C-H2")}, indent=1, default=float))
    for h in ("C-H1", "C-H3"):
        t = pd.DataFrame(res[h]["tests"])
        print(h, t[[c for c in ("comparison", "geo_ratio", "hl", "wins", "losses", "p", "p_holm") if c in t]].round(4).to_string(index=False))
    print(pd.DataFrame(res["C-H4"]).round(4).to_string(index=False))


if __name__ == "__main__":
    main()

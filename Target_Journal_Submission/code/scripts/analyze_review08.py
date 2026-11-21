"""Post hoc analyses for review round 8 (REVIEW/review_08.md). No model refitted.

 (a) Issue 3: RW-DLC versus stratified methods with dedicated 1% tail strata (scheme S7, experiments/eval_tail1.py)
     on the held-out data: top-1% coverage (y >= q_0.99 of the training targets; seeds with >= 10 such test points),
     marginal coverage, mean decile coverage is not available for S7 runs, normalised size. Two-sided Wilcoxon
     signed-rank tests over datasets; Holm over the comparisons within (a).
 (b) Issue 9: size of RW-DLC relative to SDLC: geometric-mean and Hodges-Lehmann ratios.
 (c) Issue 1: top-1% and top-5% coverage of SDLC versus S-NCP on CTR23 and held-out (S5 strata), two-sided Wilcoxon.
Writes results/statistics_review08.json and tables/T25_tail1_vs_rw.csv.
"""
from __future__ import annotations

import glob
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TOP = ROOT.parent
sys.path.insert(0, str(ROOT))
from src.statistics.tests import holm, paired_summary, paired_wilcoxon  # noqa: E402

RES, TAB = TOP / "results", TOP / "tables"
MIN_N = 10
NAME = {"S-Res": "BCCP", "S-NCP": "S-NCP", "S-HPD-LS": "S-HPD", "SDLC-LS": "SDLC"}


def jl(d):
    return pd.concat([pd.read_json(f, lines=True) for f in sorted(glob.glob(str(d / "*.jsonl")))], ignore_index=True)


def top1(x, col="ext1_cov_2", ncol="ext1_n_2"):
    x = x[x[ncol].fillna(0) >= MIN_N]
    return x.groupby(["did", "m"])[col].mean().unstack()


def main():
    out, rows = {}, []
    # (a) S7 versus RW-DLC
    t7 = jl(RES / "raw_tail1")
    t7["m"] = t7.method.map(NAME) + "-S7"
    t7["nsize"] = t7["size"] / t7["y_train_sd"]
    rw = pd.DataFrame([r for f in sorted((RES / "rw" / "confirmatory").glob("*.json")) for r in json.loads(f.read_text())])
    rw = rw[rw.method.isin(["RW-DLC-U", "SDLC", "S-NCP"])].copy()
    rw["m"] = rw.method + "-RWgrid"
    T1 = pd.concat([top1(t7), top1(rw.rename(columns={}), "top1h_cov", "n_top1h")], axis=1)
    cov = pd.concat([t7.groupby(["did", "m"]).coverage.mean().unstack(),
                     rw.groupby(["did", "m"]).coverage.mean().unstack()], axis=1)
    sz = pd.concat([t7.groupby(["did", "m"]).nsize.apply(lambda v: float(np.exp(np.log(v).mean()))).unstack(),
                    rw.groupby(["did", "m"])["size"].apply(lambda v: float(np.exp(np.log(v).mean()))).unstack()], axis=1)
    inf7 = t7.groupby(["did", "m"]).n_strata_inf.max().unstack()
    P = "RW-DLC-U-RWgrid"
    comps = ["SDLC-S7", "S-NCP-S7", "BCCP-S7"]
    res = []
    for m in comps:
        r1 = paired_wilcoxon(T1[P], T1[m])
        r2 = paired_summary(sz[P], sz[m], better="smaller", log=True)
        res.append((m, r1, r2))
    ph = holm([r[1]["p"] for r in res] + [r[2]["p"] for r in res])
    for i, (m, r1, r2) in enumerate(res):
        d1 = (T1[P] - T1[m]).dropna()
        out[f"vs {m}"] = dict(top1_rw=float(T1[P][d1.index].mean()), top1_comp=float(T1[m][d1.index].mean()),
                              top1_diff=float(d1.mean()), top1_wins=int((d1 > 0).sum()), top1_losses=int((d1 < 0).sum()),
                              top1_n=int(len(d1)), top1_p_holm=float(ph[i]),
                              cov_rw=float(cov[P].mean()), cov_comp=float(cov[m].mean()),
                              size_geo=r2["geo_ratio"], size_hl=r2["hl_ratio"], size_wins=r2["wins"],
                              size_losses=r2["losses"], size_p_holm=float(ph[len(res) + i]))
        rows.append(dict(comparison=f"RW-DLC vs {m.replace('-S7', ' (1% tail strata)')}", **out[f"vs {m}"]))
    out["S7.top1_mean"] = {m: float(T1[m].mean()) for m in comps}
    out["S7.top1_min"] = {m: float(T1[m].min()) for m in comps}
    out["S7.cov_mean"] = {m: float(cov[m].mean()) for m in comps}
    out["S7.datasets_with_inf_threshold"] = int((inf7["SDLC-S7"] > 0).sum())
    out["n_datasets"] = int(T1[P].notna().sum())
    pd.DataFrame(rows).to_csv(TAB / "T25_tail1_vs_rw.csv", index=False)
    # (b) RW-DLC vs SDLC size (same grid pipeline)
    r = paired_summary(sz[P], sz["SDLC-RWgrid"], better="smaller", log=True)
    out["rw_vs_sdlc_size"] = dict(geo=r["geo_ratio"], hl=r["hl_ratio"], median=float(np.median(sz[P] / sz["SDLC-RWgrid"])),
                                  wins=r["wins"], losses=r["losses"])
    # (c) SDLC vs S-NCP in the extreme tails (S5)
    for suite, d in (("ctr23", RES / "raw_eval_v3"), ("held-out", RES / "confirmatory" / "raw_eval_v3")):
        x = jl(d)
        x = x[(x.alpha == 0.1) & (x.scheme == "S5") & (x.cal_frac.isna() | (x.cal_frac == 1.0))]
        x = x[x.method.isin(["SDLC-LS", "S-NCP"])].copy()
        x["m"] = x.method.map(NAME)
        for lab, col, ncol in (("top1", "ext1_cov_2", "ext1_n_2"), ("top5", "ext_cov_2", "ext_n_2")):
            t = top1(x, col, ncol)
            d_ = (t["SDLC"] - t["S-NCP"]).dropna()
            w = paired_wilcoxon(t["SDLC"], t["S-NCP"])
            out[f"{suite}.{lab}_sdlc_vs_sncp"] = dict(n=int(len(d_)), sdlc=float(t["SDLC"][d_.index].mean()),
                                                     sncp=float(t["S-NCP"][d_.index].mean()), lower=int((d_ < 0).sum()),
                                                     higher=int((d_ > 0).sum()), p=float(w["p"]))
    (RES / "statistics_review08.json").write_text(json.dumps(out, indent=1, default=float))
    print(pd.DataFrame(rows).round(3).to_string())
    print(json.dumps({k: v for k, v in out.items() if not k.startswith("vs ")}, indent=1, default=float))


if __name__ == "__main__":
    main()

"""Tables/statistics for the supplementary experiments:
  * learner generality (results/raw_mlp)  -> tables/T12_mlp_generality.*, statistics_extra.json
  * synthetic oracle study (results/synthetic.jsonl) -> tables/T11_synthetic_oracle.*
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
from scripts.analyze import NAME, table  # noqa: E402
from src.statistics.tests import holm, paired_wilcoxon  # noqa: E402

OUT = {}


def worst(d):
    cc = [c for c in d.columns if c.startswith("cal_cov_")]
    g = d.groupby(["did", "method"])[cc].mean()
    return g.min(axis=1).rename("worst_stratum").reset_index()


def mlp():
    files = glob.glob(str(TOP / "results" / "raw_mlp" / "*.jsonl"))
    if not files:
        return
    d = pd.concat([pd.read_json(f, lines=True) for f in files], ignore_index=True)
    d["nsize"] = d["size"] / d["y_train_sd"]
    d["tail_hi"] = [r[f"cal_cov_{int(r['K']) - 1}"] for _, r in d.iterrows()]
    w = worst(d)
    g = d.groupby(["did", "method"])[["coverage", "nsize", "tail_hi", "cal_cov_0"]].mean().reset_index().merge(w)
    rows = []
    for m in ["SCP", "NCP", "MCP-yhat", "DCP-LS", "HPD-split-LS", "DLS-M-LS", "S-Res", "S-NCP", "S-HPD-LS",
              "SDLC-LS", "SDLC-LS-floor", "SDLC-LS-hull"]:
        x = g[g.method == m]
        rows.append({"method": NAME[m], "coverage": x.coverage.mean(), "lower_tail": x.cal_cov_0.mean(),
                     "upper_tail": x.tail_hi.mean(), "worst_stratum": x.worst_stratum.mean(),
                     "nsize_geo": float(np.exp(np.log(x.nsize).mean()))})
    T = pd.DataFrame(rows)
    table(T, "T12_mlp_generality")
    W = g.pivot(index="did", columns="method", values="worst_stratum")
    comp = ["SCP", "NCP", "MCP-yhat", "DCP-LS", "HPD-split-LS", "DLS-M-LS"]
    res = [paired_wilcoxon(W["SDLC-LS"], W[m], alternative="greater") for m in comp]
    adj = holm([r["p"] for r in res])
    OUT["mlp_tests_worst_stratum"] = {NAME[m]: {"median_diff": r["median_diff"], "p_holm": a, "rbc": r["rbc"],
                                               "n": r["n"]} for m, r, a in zip(comp, res, adj)}
    OUT["mlp_n_datasets"] = int(g.did.nunique())
    OUT["mlp_n_seeds"] = int(d.seed.nunique())
    S = g.pivot(index="did", columns="method", values="nsize")
    comp = ["S-Res", "S-NCP", "S-HPD-LS"]
    res = [paired_wilcoxon(np.log(S["SDLC-LS"]), np.log(S[m])) for m in comp]
    adj = holm([r["p"] for r in res])
    OUT["mlp_size_tests"] = {NAME[m]: {"geo": float(np.exp(np.log(S["SDLC-LS"] / S[m]).mean())),
                                       "n_smaller": int((S["SDLC-LS"] < S[m]).sum()), "n": int(S[m].notna().sum()),
                                       "p_holm": float(a)} for m, r, a in zip(comp, res, adj)}
    OUT["mlp_price_SDLC_vs_DLS_geo"] = float(np.exp(np.log(S["SDLC-LS"] / S["DLS-M-LS"]).mean()))
    OUT["mlp_price_SNCP_vs_NCP_geo"] = float(np.exp(np.log(S["S-NCP"] / S["NCP"]).mean()))
    print(T.round(3).to_string(index=False))


def synthetic():
    p = TOP / "results" / "synthetic.jsonl"
    if not p.exists():
        return
    d = pd.read_json(p, lines=True)
    cc = [c for c in d.columns if c.startswith("cal_cov_")]
    g = d.groupby(["scores", "method"])
    t = g[["coverage", "size", "components"]].mean()
    prof = g[cc].mean()
    t["worst_stratum"] = prof.min(axis=1)
    t["lower_tail"] = prof["cal_cov_0"]
    t["upper_tail"] = prof[cc[-1]]
    t["size_sd_over_seeds"] = g["size"].std()
    t = t.reset_index().sort_values(["scores", "size"])
    t["method"] = t.method.map(lambda m: NAME.get(m, m))
    table(t, "T11_synthetic_oracle", 4)
    o = d[d.scores == "oracle"].pivot_table(index="seed", columns="method", values="size")
    strat = ["O-S-Res", "O-S-NCP", "O-SDLC"]
    OUT["synthetic_oracle_sdlc_smallest_in_all_seeds"] = bool((o["O-SDLC"] <= o[strat + ["O-S-HPD"]].min(axis=1) + 1e-12).all())
    OUT["synthetic_osdlc_smallest_seeds"] = int((o["O-SDLC"] <= o[strat + ["O-S-HPD"]].min(axis=1) + 1e-12).sum())
    e = d[d.scores == "estimated"].pivot_table(index="seed", columns="method", values="size")
    OUT["synthetic_est_sdlc_lt_bccp_seeds"] = int((e["SDLC-LS"] < e["S-Res"]).sum())
    OUT["synthetic_est_sdlc_lt_sncp_seeds"] = int((e["SDLC-LS"] < e["S-NCP"]).sum())
    OUT["synthetic_est_sdlc_lt_scqr_seeds"] = int((e["SDLC-LS"] < e["S-CQR"]).sum())
    OUT["synthetic_oracle_sizes"] = o.mean().to_dict()
    OUT["synthetic_n_seeds"] = int(d.seed.nunique())
    print(t.round(3).to_string(index=False))


if __name__ == "__main__":
    mlp()
    synthetic()
    json.dump(OUT, open(TOP / "results" / "statistics_extra.json", "w"), indent=1, default=float)

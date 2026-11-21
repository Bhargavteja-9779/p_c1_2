"""Analysis of the relevance-weighted (RW-DLC) study exactly as fixed in PREREGISTRATION_relevance_weighted.md.

Unit of analysis: dataset (metrics averaged over seeds). For each suite (ctr23 = exploratory, confirmatory = held-out):
  RW-1  TOST (two one-sided Wilcoxon tests, margin 0.02) of dataset-mean Cov_phiU of RW-DLC-U against 0.90;
  RW-2  Cov_phiU of RW-DLC-U > SCP, NCP, CQR, DLS-M (one-sided Wilcoxon, Holm over the four);
  RW-3  top-1% coverage of RW-DLC-U > SDLC (one-sided Wilcoxon; mean difference with bootstrap CI);
  RW-4  size of RW-DLC-U vs RW-DLS-U and RW-NCP-U (two-sided Wilcoxon on log size, Holm over the two; a claim needs
        Holm p < 0.05 AND a 95% bootstrap CI of the geometric-mean ratio excluding 1);
  descriptive: RW-DLC-U vs SDLC and S-NCP (size, macro-/worst-decile coverage), RW-DLC-H, ESS, infinite thresholds.
Writes results/rw_statistics.json, tables/T17_rw_summary_<suite>.csv, tables/T17b_rw_tests.csv, figure F14.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TOP = ROOT.parent
sys.path.insert(0, str(ROOT))
from src.statistics.tests import bootstrap_ci, holm, paired_summary, paired_wilcoxon, tost_wilcoxon  # noqa: E402

RES, TAB, FIG = TOP / "results", TOP / "tables", TOP / "figures"
METHODS = ["SCP", "NCP", "CQR", "DLS-M", "S-NCP", "SDLC", "RW-NCP-U", "RW-DLS-U", "RW-DLC-U", "RW-DLC-H"]
COLS = ["coverage", "cov_phiU", "cov_phiH", "macro_decile", "worst_decile", "top1_cov", "bot1_cov", "size", "empty",
        "inf_thr", "ess_U"]


def load(suite):
    files = sorted((RES / "rw" / suite).glob("*.json"))
    if not files:
        return None
    d = pd.DataFrame([r for f in files for r in json.loads(f.read_text())])
    return d


def per_dataset(d):
    return d.groupby(["did", "method"])[COLS].mean().reset_index()


def wide(pd_, col):
    return pd_.pivot(index="did", columns="method", values=col)


def analyse(suite):
    d = load(suite)
    if d is None:
        return None
    pdm = per_dataset(d)
    out = dict(n_datasets=int(pdm.did.nunique()), n_runs=int(len(d) // len(METHODS)),
               seeds_per_dataset_min=int(d.groupby("did").seed.nunique().min()))
    # summary table (means over datasets)
    summ = pdm.groupby("method")[COLS].mean().reindex(METHODS).reset_index()
    summ.to_csv(TAB / f"T17_rw_summary_{suite}.csv", index=False)
    disp = summ[["method", "coverage", "cov_phiU", "macro_decile", "worst_decile", "top1_cov", "size"]].copy()
    geo = pdm.groupby("method")["size"].apply(lambda v: float(np.exp(np.log(v).mean()))).reindex(METHODS)
    disp["size_geo"] = geo.values
    disp.columns = ["Method", "Marginal cov.", "Relevance-weighted cov. (φ_U)", "Mean decile cov.", "Worst decile cov.",
                    "Top-1% cov.", "Normalised size (arith. mean)", "Normalised size (geo. mean)"]
    for c_ in disp.columns[1:]:
        disp[c_] = disp[c_].map(lambda v: f"{v:.3f}")
    disp.to_csv(TAB / f"D17_rw_{suite}.csv", index=False)
    out["summary"] = summ.set_index("method").to_dict(orient="index")
    tests = []
    P = "RW-DLC-U"
    # RW-1
    cU = wide(pdm, "cov_phiU")
    d1 = cU[P].values - 0.90
    p1 = tost_wilcoxon(d1, 0.02)
    out["RW-1"] = dict(mean=float(cU[P].mean()), ci=bootstrap_ci(cU[P].values, fn=np.mean), p_tost=p1,
                       supported=bool(p1 < 0.05))
    tests.append(dict(suite=suite, hypothesis="RW-1", comparison="Cov_phiU(RW-DLC) equivalent to 0.90 (margin 0.02)",
                      estimate=float(cU[P].mean()), p=p1, p_holm=p1, supported=p1 < 0.05))
    # RW-2
    comps = ["SCP", "NCP", "CQR", "DLS-M"]
    r2 = [paired_wilcoxon(cU[P], cU[m], alternative="greater") for m in comps]
    ph = holm([r["p"] for r in r2])
    out["RW-2"] = {m: dict(diff_mean=float((cU[P] - cU[m]).mean()), wins=r["wins"], n=r["n"], p=r["p"], p_holm=float(h))
                   for m, r, h in zip(comps, r2, ph)}
    out["RW-2"]["supported"] = bool(np.all(ph < 0.05))
    for m, r, h in zip(comps, r2, ph):
        tests.append(dict(suite=suite, hypothesis="RW-2", comparison=f"Cov_phiU: RW-DLC > {m}",
                          estimate=float((cU[P] - cU[m]).mean()), p=r["p"], p_holm=float(h), supported=h < 0.05))
    # RW-3
    t1 = wide(pdm, "top1_cov")
    ok = t1[P].notna() & t1["SDLC"].notna()
    r3 = paired_wilcoxon(t1[P][ok], t1["SDLC"][ok], alternative="greater")
    dd = (t1[P] - t1["SDLC"])[ok].values
    out["RW-3"] = dict(diff_mean=float(dd.mean()), ci=bootstrap_ci(dd, fn=np.mean), wins=r3["wins"], n=r3["n"],
                       p=r3["p"], rw=float(t1[P][ok].mean()), sdlc=float(t1["SDLC"][ok].mean()),
                       supported=bool(r3["p"] < 0.05))
    tests.append(dict(suite=suite, hypothesis="RW-3", comparison="top-1% coverage: RW-DLC > SDLC",
                      estimate=float(dd.mean()), p=r3["p"], p_holm=r3["p"], supported=r3["p"] < 0.05))
    # RW-4
    sz = wide(pdm, "size")
    r4 = {m: paired_summary(sz[P], sz[m], better="smaller", log=True) for m in ("RW-DLS-U", "RW-NCP-U")}
    ph4 = holm([r4[m]["p"] for m in r4])
    out["RW-4"] = {}
    for (m, r), h in zip(r4.items(), ph4):
        sup = bool(h < 0.05 and (r["geo_hi"] < 1 or r["geo_lo"] > 1))
        out["RW-4"][m] = dict(r, p_holm=float(h), claim=sup)
        tests.append(dict(suite=suite, hypothesis="RW-4", comparison=f"size: RW-DLC vs {m}", estimate=r["geo_ratio"],
                          p=r["p"], p_holm=float(h), supported=sup and r["geo_ratio"] < 1))
    out["RW-4"]["supported"] = bool(all(out["RW-4"][m]["claim"] and out["RW-4"][m]["geo_ratio"] < 1 for m in r4))
    # descriptive
    desc = {}
    for m in ("SDLC", "S-NCP", "RW-DLC-H"):
        s = paired_summary(sz[P], sz[m], better="smaller", log=True)
        desc[m] = dict(size_geo_ratio=s["geo_ratio"], size_geo_lo=s["geo_lo"], size_geo_hi=s["geo_hi"],
                       size_wins=s["wins"], n=s["n"], p_raw=s["p"],
                       macro_diff=float((wide(pdm, "macro_decile")[P] - wide(pdm, "macro_decile")[m]).mean()),
                       worst_diff=float((wide(pdm, "worst_decile")[P] - wide(pdm, "worst_decile")[m]).mean()),
                       top1_diff=float((t1[P] - t1[m]).mean()))
    out["descriptive"] = desc
    out["ess_U_median"] = float(pdm[pdm.method == P].ess_U.median())
    out["ess_U_min"] = float(pdm[pdm.method == P].ess_U.min())
    out["inf_thr_max"] = float(pdm[pdm.method == P].inf_thr.max())
    out["marg_cov_rw_min"] = float(wide(pdm, "coverage")[P].min())
    out["marg_cov_rw_mean"] = float(wide(pdm, "coverage")[P].mean())
    return out, pd.DataFrame(tests), pdm


def figure(pdms):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from adjustText import adjust_text
    from scripts.analyze3 import mcolor, mmarker
    show = ["SCP", "NCP", "CQR", "DLS-M", "S-NCP", "SDLC", "RW-NCP-U", "RW-DLS-U", "RW-DLC-H", "RW-DLC-U"]
    label = {"DLS-M": "DLS"}
    fig, axes = plt.subplots(1, len(pdms), figsize=(3.7 * len(pdms), 3.3), squeeze=False)
    for ax, (suite, pdm) in zip(axes[0], pdms.items()):
        dec = pdm[pdm.method.isin(show)]
        texts, xs, ys = [], [], []
        for m in show:
            x = dec[dec.method == m]
            nm = label.get(m, m)
            xv, yv = np.exp(np.log(x["size"]).mean()), x["top1_cov"].mean()
            ax.scatter(xv, yv, s=30, color=mcolor(nm), marker=mmarker(nm), zorder=3, edgecolor="white", lw=0.5)
            xs.append(xv)
            ys.append(yv)
            texts.append(ax.text(xv, yv, nm, fontsize=6.3, color="#3a3936"))
        ax.axhline(0.9, color="k", lw=0.8, ls="--")
        ax.set_xlim(min(xs) * 0.93, max(xs) * 1.12)
        ax.set_ylim(min(ys) - 0.05, 0.97)
        ax.set_xlabel("Normalised set size (geometric mean)", fontsize=7.5)
        ax.set_ylabel("Coverage of the top 1% of outcomes", fontsize=7.5)
        ax.tick_params(labelsize=7)
        ax.set_title({"ctr23": "OpenML-CTR23 (exploratory)", "confirmatory": "Held-out datasets"}[suite], fontsize=8)
        ax.grid(alpha=0.3)
        adjust_text(texts, x=xs, y=ys, ax=ax, arrowprops=dict(arrowstyle="-", color="#a3a29c", lw=0.5),
                    expand=(1.3, 1.6), ensure_inside_axes=True)
    fig.tight_layout()
    fig.savefig(FIG / "F14_rw_top1_vs_size.png", dpi=300, bbox_inches="tight")
    fig.savefig(FIG / "F14_rw_top1_vs_size.pdf", bbox_inches="tight")


def main():
    stats_, tests, pdms = {}, [], {}
    for suite in ("ctr23", "confirmatory"):
        r = analyse(suite)
        if r is None:
            continue
        stats_[suite], t, pdms[suite] = r
        tests.append(t)
    (RES / "rw_statistics.json").write_text(json.dumps(stats_, indent=1, default=float))
    T = pd.concat(tests, ignore_index=True)
    T.to_csv(TAB / "T17b_rw_tests.csv", index=False)
    print(T.to_string())
    figure(pdms)


if __name__ == "__main__":
    main()

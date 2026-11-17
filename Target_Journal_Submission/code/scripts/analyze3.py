"""v3 analysis (after review cycle 1). Generates every statistic, table and figure of the revised
manuscript from results/raw_eval_v3/*.jsonl (and auxiliary result files).

Conventions (declared in the manuscript, Section 5.6):
* unit of analysis = dataset (metrics averaged over seeds within dataset);
* primary size summary = geometric-mean ratio of mean set sizes across datasets with 95% bootstrap CI,
  accompanied by the Hodges-Lehmann ratio with its Wilcoxon-inversion CI, wins/losses (a 'win' = smaller
  set or higher coverage, as appropriate) and the sign test;
* families of comparisons are Holm-adjusted; directional (one-sided) tests only for H1;
* every size comparison on CTR23 is EXPLORATORY (the pre-registered implementation did not support it);
  confirmatory tests are in scripts/analyze_confirmatory.py on held-out data.
"""
from __future__ import annotations

import glob
import json
import os
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from scipy import stats  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
TOP = ROOT.parent
sys.path.insert(0, str(ROOT))
from scripts.analyze import (AQUA, BLUE, DARK, GRAY, ORANGE, null_worst_stratum)  # noqa: E402
from src.statistics.tests import (bootstrap_ci, holm, paired_summary, paired_wilcoxon,  # noqa: E402
                                  tost_wilcoxon)

CFG = json.loads((ROOT / "config" / "benchmark.json").read_text())
RAW = Path(sys.argv[1]) if len(sys.argv) > 1 else TOP / "results" / "raw_eval_v3"
_OUT = Path(os.environ["TSCP_OUT_ROOT"]) if os.environ.get("TSCP_OUT_ROOT") else TOP
RES, TAB, FIG = _OUT / "results", _OUT / "tables", _OUT / "figures"
for d_ in (RES, TAB, FIG):
    d_.mkdir(parents=True, exist_ok=True)

NAME = {"SCP": "SCP", "NCP": "NCP", "CQR": "CQR", "MCP-yhat": "Mondrian-ŷ", "DCP-LS": "DCP", "HPD-split-LS": "HPD-split",
        "DLS-M-LS": "DLS", "S-Res": "BCCP", "S-Res-hull": "BCCP-hull", "S-Res-floor": "BCCP-floor",
        "S-NCP": "S-NCP", "S-NCP-hull": "S-NCP-hull", "S-NCP-floor": "S-NCP-floor", "S-CQR": "S-CQR",
        "S-HPD-LS": "S-HPD", "SDLC-LS": "SDLC", "SDLC-LS-hull": "SDLC-hull", "SDLC-LS-floor": "SDLC-floor",
        "SDLC-N": "SDLC-N", "DLS-M-N": "DLS-N", "SDLC-LS2": "SDLC-2p", "SDLC-LS2-hull": "SDLC-2p-hull",
        "SDLC-LS2-floor": "SDLC-2p-floor", "DLS-M-LS2": "DLS-2p", "DCP-LS2": "DCP-2p",
        "SDLC-H": "SDLC-hist", "SDLC-H-hull": "SDLC-hist-hull", "SDLC-H-floor": "SDLC-hist-floor",
        "DLS-M-H": "DLS-hist", "HPD-split-H": "HPD-split-hist", "DCP-H": "DCP-hist", "S-HPD-H": "S-HPD-hist"}
MARGINAL = ["SCP", "NCP", "CQR", "MCP-yhat", "DCP-LS", "HPD-split-LS", "DLS-M-LS"]
STRAT = ["S-Res", "S-NCP", "S-CQR", "S-HPD-LS", "SDLC-N", "SDLC-LS"]
VARIANTS = ["S-Res-hull", "S-NCP-hull", "SDLC-LS-hull", "S-Res-floor", "S-NCP-floor", "SDLC-LS-floor",
            "SDLC-LS2", "SDLC-LS2-hull", "DLS-M-LS2", "SDLC-H", "DLS-M-H", "HPD-split-H", "S-HPD-H", "DLS-M-N"]
MAIN = MARGINAL + STRAT
P = "SDLC-LS"
H3_PRIMARY = ["S-Res", "S-NCP", "S-CQR", "S-HPD-LS"]
DEV = set(CFG["dev_datasets"])
DIAG = DEV | {44978, 44969, 44994, 44960, 44962, 45012, 44983}   # + 7 datasets of the v1 diagnostic
plt.rcParams.update({"font.size": 8, "axes.spines.top": False, "axes.spines.right": False, "axes.grid": True,
                     "grid.color": "#e6e5e0", "grid.linewidth": 0.5, "savefig.dpi": 300, "lines.linewidth": 1.5,
                     "axes.edgecolor": "#8a8984", "xtick.color": "#52514e", "ytick.color": "#52514e"})
STATS, METRICS = {}, {}


def save(fig, name):
    fig.tight_layout()
    fig.savefig(FIG / f"{name}.png", bbox_inches="tight")
    fig.savefig(FIG / f"{name}.pdf", bbox_inches="tight")
    plt.close(fig)


def table(df, name, nd=3):
    df.to_csv(TAB / f"{name}.csv", index=False)
    (TAB / f"{name}.md").write_text(df.to_markdown(index=False, floatfmt=f".{nd}f"))


def load():
    files = sorted(glob.glob(str(RAW / "*.jsonl")))
    df = pd.concat([pd.read_json(f, lines=True) for f in files], ignore_index=True)
    df["nsize"] = df["size"] / df["y_train_sd"]
    cc = [c for c in df.columns if c.startswith("cal_cov_") and c[8:].isdigit()]
    df["tail_lo"] = df["cal_cov_0"]
    df["tail_hi"] = [r[f"cal_cov_{int(k) - 1}"] for k, r in zip(df.K, df[cc].to_dict("records"))]
    for nm in ("up1", "up2", "down1", "tails1", "pc"):
        col = [c for c in df.columns if c.startswith(f"shift_{nm}_cal_cov_")]
        if col:
            df[f"shift_{nm}_upper"] = [r[f"shift_{nm}_cal_cov_{int(k) - 1}"] for k, r in zip(df.K, df[col].to_dict("records"))]
    return df


def modal_k(d):
    mk = d.groupby("did").K.agg(lambda k: k.value_counts().idxmax())
    return d[d.K == d.did.map(mk)]


def stratum_profile(d, prefix="cal_cov_"):
    d = modal_k(d)
    cc = [c for c in d.columns if c.startswith(prefix) and c[len(prefix):].isdigit()]
    g = d.groupby(["did", "dataset", "method"])[cc].mean()
    return pd.DataFrame({"worst_stratum": g.min(axis=1, skipna=True)}).reset_index()


def per_dataset(d, cols):
    cols = [c for c in cols if c in d.columns]
    return d.groupby(["did", "dataset", "method"])[cols].mean().reset_index().merge(
        stratum_profile(d), on=["did", "dataset", "method"])


def compare(pd_, a, b, col, better, log=False, alternative="two-sided", keep=None):
    x = pd_.pivot(index="did", columns="method", values=col)
    if keep is not None:
        x = x.loc[[i for i in x.index if i in keep]]
    return paired_summary(x[a], x[b], better=better, log=log, alternative=alternative)


def family(pd_, pairs, col, better, log, alternative, label, keep=None):
    rows = []
    for a, b in pairs:
        r = compare(pd_, a, b, col, better, log, alternative, keep)
        rows.append({"family": label, "metric": col, "comparison": f"{NAME[a]} vs {NAME[b]}", **r})
    ps = holm([r["p"] for r in rows])
    for r, p in zip(rows, ps):
        r["p_holm"] = p
    return rows


def main():
    df = load()
    df.to_csv(RES / "raw_results_v3.csv", index=False)
    a10 = df[(df.alpha == 0.1) & (df.scheme == "S5") & (df.cal_frac == 1.0)]
    METRICS.update(n_datasets=int(a10.did.nunique()), n_seeds_min=int(a10.groupby("did").seed.nunique().min()),
                   n_runs=int(a10[["did", "seed"]].drop_duplicates().shape[0]))
    first = a10.drop_duplicates(["did", "seed"])
    # ---------------------------------------------------------------- dataset table (incl. realised strata)
    from src.data.openml_ctr23 import load as dload
    rows = []
    for did, g in first.groupby("did"):
        y = dload(int(did))[1]
        q = np.quantile(y, [0.125, 0.25, 0.5, 0.75, 0.875])
        mass = np.array([m for m in g.train_stratum_mass])
        rows.append(dict(did=did, dataset=g.dataset.iloc[0], n=int(g.n.iloc[0]), p=int(g.p.iloc[0]),
                         skew_y=float(stats.skew(y)),
                         octile_skew=float(((q[4] - q[2]) - (q[2] - q[0])) / (q[4] - q[0])) if q[4] > q[0] else 0.0,
                         n_unique_y=int(np.unique(y).size), zero_frac=float((y == 0).mean()),
                         n_cal=float(g.n_cal.mean()), K=float(g.K.median()),
                         lower_mass=float(np.median([m[0] for m in mass])),
                         upper_mass=float(np.median([m[-1] for m in mass])),
                         rmse_over_sd=float(np.median(g.test_rmse / g.y_train_sd)),
                         out_dom=float(g.frac_test_out_domain.mean()), dev=did in DEV))
    T1 = pd.DataFrame(rows).sort_values("n")
    table(T1, "T1_datasets")
    nominal = set(T1[(T1.lower_mass.between(0.05, 0.15)) & (T1.upper_mass.between(0.05, 0.15)) & (T1.K >= 5)].did)
    skewed = set(T1[T1.skew_y.abs() > 1].did)
    large = set(T1[T1.n >= 1600].did)
    METRICS.update(n_nominal_tails=len(nominal), n_skewed=len(skewed), n_large=len(large),
                   frac_test_out_domain_max=float(T1.out_dom.max()), frac_test_out_domain_mean=float(T1.out_dom.mean()),
                   max_n_test=int(first.n_test.max()))
    # ---------------------------------------------------------------- main per-dataset table
    cols = ["coverage", "nsize", "tail_lo", "tail_hi", "components", "wsc", "empty_rate", "dec_worst", "ext_cov_0",
            "ext_cov_2", "ext1_cov_0", "ext1_cov_2", "sig_worst", "alert_hi_recall", "alert_hi_rate",
            "alert_hi_precision", "alert_lo_recall", "alert_lo_rate", "alert_lo_precision", "size_median",
            "shift_up1_cov", "shift_up2_cov", "shift_down1_cov", "shift_tails1_cov", "shift_pc_cov",
            "shift_up1_upper", "shift_up2_upper", "shift_pc_upper", "shift_up1_cal_worst", "shift_up2_cal_worst",
            "shift_pc_cal_worst", "shift_down1_cal_worst", "shift_tails1_cal_worst", "n_strata_inf"]
    pdm = per_dataset(a10, cols)
    nul = null_worst_stratum(modal_k(a10[a10.method == P]))
    pdm["null_worst_mean"] = pdm.did.map(lambda d: nul[d][0])
    pdm["null_worst_q05"] = pdm.did.map(lambda d: nul[d][1])
    pdm["below_null"] = pdm.worst_stratum < pdm.null_worst_q05
    pdm.to_csv(RES / "per_dataset_main_v3.csv", index=False)
    piv = lambda col: pdm.pivot(index="did", columns="method", values=col)
    S = piv("nsize")

    def summary_row(m):
        x = pdm[pdm.method == m]
        return {"method": NAME[m], "code": m, "coverage": x.coverage.mean(), "lower_tail_cov": x.tail_lo.mean(),
                "upper_tail_cov": x.tail_hi.mean(), "worst_stratum": x.worst_stratum.mean(),
                "n_ds_below_null": int(x.below_null.sum()), "top5_cov": x.ext_cov_2.mean(),
                "top1_cov": x.ext1_cov_2.mean(), "size_geo": float(np.exp(np.log(x.nsize).mean())),
                "size_median_ds": float(x.nsize.median()), "pieces": x.components.mean(),
                "empty_rate": x.empty_rate.mean(), "empty_ds": int((x.empty_rate > 0.001).sum()),
                "sigma_decile_worst": x.sig_worst.mean(), "wsc": x.wsc.mean(), "wsc_n": int(x.wsc.notna().sum())}
    T2 = pd.DataFrame([summary_row(m) for m in MAIN])
    T2v = pd.DataFrame([summary_row(m) for m in VARIANTS if m in set(pdm.method)])
    table(T2, "T2_main_results")
    table(T2v, "T2b_variants")
    METRICS["main"] = {r["code"]: r for r in T2.to_dict("records")}
    METRICS["variants"] = {r["code"]: r for r in T2v.to_dict("records")}
    METRICS["null_worst_mean_avg"] = float(pdm[pdm.method == P].null_worst_mean.mean())
    # ---------------------------------------------------------------- hypotheses
    tests = []
    tests += family(pdm, [(P, m) for m in MARGINAL], "worst_stratum", "larger", False, "greater", "H1 worst stratum")
    tests += family(pdm, [(P, m) for m in MARGINAL], "tail_hi", "larger", False, "greater", "H1 upper tail")
    tests += family(pdm, [(P, m) for m in MARGINAL], "worst_stratum", "larger", False, "greater",
                    "H1 worst stratum (excl. development)", keep=set(pdm.did) - DEV)
    tests += family(pdm, [(P, m) for m in H3_PRIMARY], "nsize", "smaller", True, "two-sided", "H3 size (primary)")
    tests += family(pdm, [(P, m) for m in ("SDLC-N", "SDLC-LS2", "SDLC-H")], "nsize", "smaller", True, "two-sided",
                    "H3 size (secondary)")
    tests += family(pdm, [("S-NCP", "S-Res"), ("SDLC-N", "S-NCP"), (P, "SDLC-N")], "nsize", "smaller", True,
                    "two-sided", "Decomposition BCCP -> S-NCP -> SDLC-N -> SDLC")
    tests += family(pdm, [(f"{P}-hull", "S-Res-hull"), (f"{P}-hull", "S-NCP-hull")], "nsize", "smaller", True,
                    "two-sided", "H3 size (hull forms)")
    cov_pairs = [(P, m) for m in H3_PRIMARY]
    fam = []
    for col in ("ext_cov_2", "ext1_cov_2", "shift_up1_upper", "shift_up2_upper"):
        fam += [{**r, "metric": col} for r in
                [{"comparison": f"{NAME[a]} vs {NAME[b]}", "family": "Extreme coverage vs stratified",
                  **compare(pdm, a, b, col, "larger")} for a, b in cov_pairs]]
    for r, p in zip(fam, holm([r["p"] for r in fam])):
        r["p_holm"] = p
    tests += fam
    tests += family(pdm, cov_pairs, "alert_hi_rate", "smaller", False, "two-sided", "Upper alert rate vs stratified")
    tests += family(pdm, cov_pairs, "alert_hi_precision", "larger", False, "two-sided",
                    "Upper alert precision vs stratified")
    T3 = pd.DataFrame(tests)
    table(T3, "T3_statistical_tests", 4)
    STATS["tests"] = T3.to_dict("records")
    tost = []
    for m in H3_PRIMARY:
        x = piv("worst_stratum")
        tost.append({"comparison": f"SDLC vs {NAME[m]}", "margin": 0.01, "p_tost": tost_wilcoxon(x[P] - x[m], 0.01),
                     "median_diff": float(np.median(x[P] - x[m]))})
    STATS["tost_worst_stratum"] = tost
    # ---------------------------------------------------------------- sensitivity of H3 (size) to choices
    sens = []

    def h3_rows(pd_, label, keep=None):
        for m in H3_PRIMARY:
            r = compare(pd_, P, m, "nsize", "smaller", True, keep=keep)
            sens.append({"analysis": label, "comparison": f"SDLC vs {NAME[m]}", **r})
    h3_rows(pdm, "primary (alpha=0.1, S5, all datasets)")
    h3_rows(pdm, "excluding development datasets", keep=set(pdm.did) - DEV)
    h3_rows(pdm, "excluding development + diagnostic datasets", keep=set(pdm.did) - DIAG)
    h3_rows(pdm, "datasets with nominal tail strata", keep=nominal)
    h3_rows(pdm, "|skewness| > 1", keep=skewed)
    h3_rows(pdm, "|skewness| <= 1", keep=set(pdm.did) - skewed)
    h3_rows(pdm, "n >= 1600", keep=large)
    h3_rows(pdm, "n < 1600", keep=set(pdm.did) - large)
    for a in (0.05, 0.2):
        da = df[(df.alpha == a) & (df.scheme == "S5") & (df.cal_frac == 1.0)]
        h3_rows(per_dataset(da, ["nsize"]), f"alpha = {a}")
    for sch in ("S3", "S10"):
        ds = df[(df.alpha == 0.1) & (df.scheme == sch) & (df.cal_frac == 1.0)]
        h3_rows(per_dataset(ds, ["nsize"]), f"strata {sch}")
    Ts = pd.DataFrame(sens)
    for lab, g in Ts.groupby("analysis"):
        Ts.loc[g.index, "p_holm"] = holm(g.p.values)
    table(Ts, "T3s_h3_sensitivity", 4)
    STATS["h3_sensitivity"] = Ts.to_dict("records")
    # ---------------------------------------------------------------- price and matched coverage
    pairs = [("SCP", "S-Res"), ("NCP", "S-NCP"), ("CQR", "S-CQR"), ("HPD-split-LS", "S-HPD-LS"), ("DLS-M-LS", P),
             ("DLS-M-N", "SDLC-N")]
    price = []
    for mm, sm in pairs:
        lr = np.log(S[sm] / S[mm]).dropna()
        lo, hi = bootstrap_ci(lr.values, fn=np.mean)
        dW = (piv("worst_stratum")[sm] - piv("worst_stratum")[mm]).dropna()
        price.append({"marginal": NAME[mm], "stratified": NAME[sm], "geo_ratio": float(np.exp(lr.mean())),
                      "ci_low": float(np.exp(lo)), "ci_high": float(np.exp(hi)), "median_ratio": float(np.exp(lr.median())),
                      "worst_gain": float(dW.mean()), "n_ratio_gt_1.5": int((np.exp(lr) > 1.5).sum())})
    T4 = pd.DataFrame(price)
    table(T4, "T4_price")
    STATS["price"] = T4.to_dict("records")
    d05 = per_dataset(df[(df.alpha == 0.05) & (df.scheme == "S5") & (df.cal_frac == 1.0)], ["nsize"])
    mc = []
    for m in MARGINAL:
        x05, x10 = d05[d05.method == m].set_index("did"), pdm[pdm.method == P].set_index("did")
        common = x05.index.intersection(x10.index)
        mc.append({"method_at_alpha_0.05": NAME[m], "worst_stratum": float(x05.loc[common].worst_stratum.mean()),
                   "size_geo": float(np.exp(np.log(x05.loc[common].nsize).mean())),
                   "SDLC_alpha_0.1_worst_stratum": float(x10.loc[common].worst_stratum.mean()),
                   "SDLC_alpha_0.1_size_geo": float(np.exp(np.log(x10.loc[common].nsize).mean())),
                   "n_ds_SDLC_smaller": int((x10.loc[common].nsize < x05.loc[common].nsize).sum())})
    table(pd.DataFrame(mc), "T4b_matched_coverage")
    STATS["matched_coverage"] = mc
    # ---------------------------------------------------------------- alpha, schemes, calibration size
    rows = []
    for a in sorted(df.alpha.unique()):
        da = per_dataset(df[(df.alpha == a) & (df.scheme == "S5") & (df.cal_frac == 1.0)], ["coverage", "nsize", "tail_hi"])
        for m in MARGINAL + STRAT + ["SDLC-LS-floor"]:
            x = da[da.method == m]
            if len(x):
                rows.append({"alpha": a, "method": NAME[m], "coverage": x.coverage.mean(), "worst_stratum": x.worst_stratum.mean(),
                             "upper_tail": x.tail_hi.mean(), "size_geo": float(np.exp(np.log(x.nsize).mean()))})
    table(pd.DataFrame(rows), "T5_alpha_sensitivity")
    rows = []
    for sch in ("S3", "S5", "S10"):
        ds = df[(df.alpha == 0.1) & (df.scheme == sch) & (df.cal_frac == 1.0)]
        dd = per_dataset(ds, ["coverage", "nsize", "n_strata_inf"])
        dec = ds.groupby(["did", "method"])[[f"dec_cov_{k}" for k in range(10)]].mean().min(axis=1).groupby("method").mean()
        for m in ["S-Res", "S-NCP", "S-CQR", "S-HPD-LS", "SDLC-N", P, "DLS-M-LS"]:
            x = dd[dd.method == m]
            if len(x):
                rows.append({"scheme": sch, "K_median": float(ds[ds.method == m].K.median()), "method": NAME[m],
                             "worst_stratum": x.worst_stratum.mean(), "worst_decile": float(dec.get(m, np.nan)),
                             "size_geo": float(np.exp(np.log(x.nsize).mean())), "runs_with_inf": int((ds[ds.method == m].n_strata_inf > 0).sum())})
    table(pd.DataFrame(rows), "T6_strata_schemes")
    rows = []
    for f in sorted(df.cal_frac.unique()):
        dc = df[(df.alpha == 0.1) & (df.scheme == "S5") & (df.cal_frac == f)]
        dd = per_dataset(dc, ["coverage", "nsize", "tail_hi"])
        for m in ["SCP", "NCP", "CQR", "S-Res", "S-NCP", "S-CQR", "SDLC-N", P]:
            x = dd[dd.method == m]
            if len(x):
                rows.append({"cal_frac": f, "mean_n_cal": float(dc.n_cal.mean() * f), "method": NAME[m],
                             "coverage": x.coverage.mean(), "worst_stratum": x.worst_stratum.mean(),
                             "size_geo": float(np.exp(np.log(x.nsize).mean())),
                             "runs_with_inf": int((dc[dc.method == m].n_strata_inf > 0).sum())})
    T7 = pd.DataFrame(rows)
    table(T7, "T7_calibration_size")
    # ---------------------------------------------------------------- shift (stratum-wise, ESS-aware)
    ess = first.groupby("did")[["ess_up1", "ess_up2", "ess_down1", "ess_tails1", "ess_pc"]].min()
    ok_ess = set(ess[ess.ess_up2 >= 50].index)
    METRICS["shift_n_ess_ge_50"] = len(ok_ess)
    METRICS["ess_up2_min"], METRICS["ess_up2_median"] = float(ess.ess_up2.min()), float(ess.ess_up2.median())
    rows = []
    for m in MARGINAL + STRAT:
        x = pdm[pdm.method == m]
        xe = x[x.did.isin(ok_ess)]
        rows.append({"method": NAME[m], "code": m, "pc_marginal": x.shift_pc_cov.mean(), "pc_worst": x.shift_pc_cal_worst.mean(),
                     "up1_marginal": x.shift_up1_cov.mean(), "up1_upper": x.shift_up1_upper.mean(),
                     "up2_marginal": x.shift_up2_cov.mean(), "up2_upper": x.shift_up2_upper.mean(),
                     "up2_upper_ess50": xe.shift_up2_upper.mean(), "down1_marginal": x.shift_down1_cov.mean()})
    T8 = pd.DataFrame(rows)
    table(T8.drop(columns="code"), "T8_shift")
    METRICS["shift"] = {r["code"]: r for r in T8.to_dict("records")}
    # ---------------------------------------------------------------- tail alerts
    rows = [{"method": NAME[m], **{c: pdm[pdm.method == m][c].mean() for c in
             ("alert_hi_recall", "alert_hi_rate", "alert_hi_precision", "alert_lo_recall", "alert_lo_rate", "alert_lo_precision")}}
            for m in MARGINAL + STRAT]
    table(pd.DataFrame(rows), "T13_tail_alerts")
    # ---------------------------------------------------------------- error analysis
    sd = pdm[pdm.method == P].merge(T1[["did", "skew_y", "octile_skew", "rmse_over_sd", "n_cal", "zero_frac"]], on="did")
    price_r = (S[P] / S["DLS-M-LS"]).rename("price")
    vs_ncp = (S[P] / S["S-NCP"]).rename("vs_sncp")
    vs_bccp = (S[P] / S["S-Res"]).rename("vs_bccp")
    sd = sd.merge(price_r, left_on="did", right_index=True).merge(vs_ncp, left_on="did", right_index=True).merge(
        vs_bccp, left_on="did", right_index=True)
    ea = {}
    for nm, col in (("rmse", "rmse_over_sd"), ("abs_skew", "skew_y"), ("log_ncal", "n_cal")):
        v = sd[col].abs() if nm == "abs_skew" else sd[col]
        r = stats.spearmanr(sd.price, v)
        ea[f"spearman_price_{nm}"] = [float(r.statistic), float(r.pvalue)]
        r2 = stats.spearmanr(np.log(sd.vs_sncp), v)
        ea[f"spearman_vs_sncp_{nm}"] = [float(r2.statistic), float(r2.pvalue)]
    Xr = np.column_stack([np.ones(len(sd)), stats.rankdata(sd.rmse_over_sd), stats.rankdata(sd.skew_y.abs()),
                          stats.rankdata(sd.n_cal)])
    yr = stats.rankdata(np.log(sd.price))
    beta, *_ = np.linalg.lstsq(Xr, yr, rcond=None)
    ea["rank_regression_price"] = dict(zip(["intercept", "rmse", "abs_skew", "n_cal"], beta.tolist()))
    STATS["error_analysis"] = ea
    table(sd[["dataset", "n_cal", "skew_y", "zero_frac", "rmse_over_sd", "worst_stratum", "nsize", "price", "vs_sncp",
              "vs_bccp", "empty_rate"]].sort_values("price"), "T10_error_analysis")
    # ---------------------------------------------------------------- figures
    figures(df, a10, pdm, S, T7, sd)
    json.dump(METRICS, open(RES / "metrics_v3.json", "w"), indent=1, default=float)
    json.dump(STATS, open(RES / "statistics_v3.json", "w"), indent=1, default=float)
    print(T2[["method", "coverage", "upper_tail_cov", "worst_stratum", "n_ds_below_null", "top5_cov", "top1_cov",
              "size_geo", "empty_rate", "sigma_decile_worst"]].round(3).to_string(index=False))
    print(T3[T3.family.str.startswith("H3") | T3.family.str.startswith("Decomp")][
        ["family", "comparison", "geo_ratio", "geo_lo", "geo_hi", "wins", "losses", "p", "p_holm"]].round(4).to_string(index=False))


def figures(df, a10, pdm, S, T7, sd):
    from adjustText import adjust_text
    # decile profile with 95% CI across datasets
    dc = [f"dec_cov_{k}" for k in range(10)]
    g = a10.groupby(["did", "method"])[dc].mean().reset_index()
    fig, ax = plt.subplots(figsize=(4.8, 3.1))
    for m, c, ls in (("SCP", GRAY, "--"), ("CQR", ORANGE, "-"), ("HPD-split-LS", DARK, ":"), ("S-NCP", AQUA, "-"), (P, BLUE, "-")):
        x = g[g.method == m][dc]
        mn, se = x.mean().values, x.std().values / np.sqrt(len(x))
        ax.plot(range(1, 11), mn, color=c, ls=ls, marker="o", ms=3, label=NAME[m])
        ax.fill_between(range(1, 11), mn - 1.96 * se, mn + 1.96 * se, color=c, alpha=0.12, lw=0)
    ax.axhline(0.9, color="#0b0b0b", lw=0.8)
    ax.set_xticks(range(1, 11))
    ax.set_xlabel("Target decile (training distribution)")
    ax.set_ylabel("Coverage (mean over datasets, 95% CI)")
    ax.legend(frameon=False, fontsize=7, ncol=2, loc="lower center")
    save(fig, "F3_decile_coverage_profile")
    # coverage-size trade-off
    fig, ax = plt.subplots(figsize=(4.8, 3.4))
    texts = []
    for m in MAIN + ["SDLC-LS-floor", "SDLC-LS-hull", "S-NCP-hull"]:
        x = pdm[pdm.method == m]
        c = BLUE if m == P else (AQUA if m in STRAT else (ORANGE if ("floor" in m or "hull" in m) else GRAY))
        xv, yv = x.worst_stratum.mean(), float(np.exp(np.log(x.nsize).mean()))
        ax.scatter(xv, yv, color=c, s=30, zorder=3, edgecolor="white", lw=0.8)
        texts.append(ax.text(xv, yv, NAME[m], fontsize=6.5, color="#0b0b0b" if m == P else "#52514e"))
    ax.axvline(0.9, color="#0b0b0b", lw=0.8)
    ax.set_xlabel("Worst-stratum coverage (mean over datasets)")
    ax.set_ylabel("Set size / sd(y) (geometric mean)")
    adjust_text(texts, ax=ax, arrowprops=dict(arrowstyle="-", color="#c3c2b7", lw=0.5), expand=(1.2, 1.4))
    save(fig, "F2_coverage_size_tradeoff")
    # per-dataset upper tail
    t = pdm[pdm.method.isin(["CQR", "HPD-split-LS", P])].pivot(index="dataset", columns="method", values="tail_hi").sort_values(P)
    fig, ax = plt.subplots(figsize=(4.8, 5.2))
    yy = np.arange(len(t))
    for m, c, mk in (("CQR", ORANGE, "s"), ("HPD-split-LS", GRAY, "^"), (P, BLUE, "o")):
        ax.scatter(t[m], yy, color=c, s=14, marker=mk, label=NAME[m], zorder=3)
    ax.axvline(0.9, color="#0b0b0b", lw=0.8)
    ax.set_yticks(yy)
    ax.set_yticklabels(t.index, fontsize=6)
    ax.set_xlabel("Coverage of the upper calibration stratum")
    ax.legend(frameon=False, fontsize=7, loc="lower left")
    save(fig, "F4_upper_tail_per_dataset")
    # shift: stratum-wise upper coverage under tilts + positive control
    fig, axs = plt.subplots(1, 2, figsize=(7.2, 2.9))
    order = [("pc", "Whole-strata\nre-weighting"), ("up1", "Upper tilt\nγ=1"), ("up2", "Upper tilt\nγ=2")]
    for m, c in (("SCP", GRAY), ("CQR", ORANGE), ("NCP", "#e87ba4"), ("S-Res", "#6250d6"), ("S-NCP", AQUA), (P, BLUE)):
        x = pdm[pdm.method == m]
        axs[0].plot(range(3), [x[f"shift_{k}_cov"].mean() for k, _ in order], marker="o", ms=3, color=c, label=NAME[m])
        axs[1].plot(range(3), [x[f"shift_{k}_upper"].mean() for k, _ in order], marker="o", ms=3, color=c, label=NAME[m])
    for ax, ttl in zip(axs, ("Coverage under shifted law", "Upper-stratum coverage under shifted law")):
        ax.axhline(0.9, color="#0b0b0b", lw=0.8)
        ax.set_xticks(range(3))
        ax.set_xticklabels([o[1] for o in order], fontsize=7)
        ax.set_title(ttl, fontsize=8)
    axs[1].legend(frameon=False, fontsize=6.5, ncol=2)
    save(fig, "F6_shift")
    # calibration size
    fig, axs = plt.subplots(1, 2, figsize=(7.0, 2.8))
    for m, c in (("SCP", GRAY), ("CQR", ORANGE), ("BCCP", "#6250d6"), ("S-NCP", AQUA), ("SDLC", BLUE)):
        x = T7[T7.method == m]
        axs[0].plot(x.cal_frac, x.worst_stratum, marker="o", ms=3, color=c, label=m)
        axs[1].plot(x.cal_frac, x.size_geo, marker="o", ms=3, color=c, label=m)
    axs[0].axhline(0.9, color="#0b0b0b", lw=0.8)
    axs[0].set_ylabel("Worst-stratum coverage")
    axs[1].set_ylabel("Set size / sd(y) (geo. mean)")
    for ax in axs:
        ax.set_xlabel("Fraction of the calibration split used")
        ax.set_xscale("log")
        ax.set_xticks([0.25, 0.5, 1.0])
        ax.set_xticklabels(["0.25", "0.5", "1"])
    axs[1].legend(frameon=False, fontsize=7)
    save(fig, "F7_calibration_size")
    # decomposition of size ratios (per-dataset), sorted
    fig, ax = plt.subplots(figsize=(4.8, 3.2))
    steps = [("S-NCP", "S-Res", "S-NCP / BCCP (adds σ̂)"), ("SDLC-N", "S-NCP", "SDLC-N / S-NCP (adds 1/σ̂ weighting)"),
             (P, "SDLC-N", "SDLC / SDLC-N (adds KDE shape)")]
    for i, (a, b, lab) in enumerate(steps):
        r = np.log(S[a] / S[b]).dropna()
        ax.scatter(np.full(len(r), i) + np.random.default_rng(i).uniform(-0.15, 0.15, len(r)), np.exp(r), s=10,
                   color=[AQUA, ORANGE, BLUE][i], alpha=0.8)
        ax.plot([i - 0.25, i + 0.25], [np.exp(r.mean())] * 2, color="#0b0b0b", lw=1.5)
    ax.axhline(1, color="#8a8984", lw=0.8)
    ax.set_yscale("log")
    ax.set_xticks(range(3))
    ax.set_xticklabels([s[2] for s in steps], fontsize=6.5)
    ax.set_ylabel("Per-dataset set-size ratio (log scale)")
    save(fig, "F11_decomposition")
    # error analysis
    fig, axs = plt.subplots(1, 2, figsize=(7.2, 3.0))
    axs[0].scatter(sd.rmse_over_sd, sd.price, color=BLUE, s=16)
    axs[0].set_yscale("log")
    from matplotlib.ticker import FixedLocator, NullFormatter, ScalarFormatter
    axs[0].yaxis.set_major_locator(FixedLocator([1, 1.5, 2, 4, 8]))
    axs[0].yaxis.set_major_formatter(ScalarFormatter())
    axs[0].yaxis.set_minor_formatter(NullFormatter())
    tx = [axs[0].text(r_.rmse_over_sd, r_.price, r_.dataset, fontsize=6, color="#52514e") for _, r_ in sd[sd.price > 1.4].iterrows()]
    adjust_text(tx, ax=axs[0], arrowprops=dict(arrowstyle="-", color="#c3c2b7", lw=0.5))
    axs[0].axhline(1, color="#0b0b0b", lw=0.8)
    axs[0].set_xlabel("Test RMSE / sd(y)")
    axs[0].set_ylabel("Price: size ratio SDLC / DLS (log)")
    dev_ = sd.worst_stratum - sd.null_worst_mean
    band = sd.null_worst_q05 - sd.null_worst_mean
    o = np.argsort(sd.n_cal.values)
    axs[1].fill_between(sd.n_cal.values[o], band.values[o], 0, color="#e6e5e0", lw=0, label="null 5% band")
    axs[1].scatter(sd.n_cal, dev_, color=BLUE, s=16, zorder=3, label="SDLC")
    axs[1].axhline(0, color="#0b0b0b", lw=0.8)
    axs[1].set_xscale("log")
    axs[1].set_xlabel("Calibration-set size")
    axs[1].set_ylabel("Worst-stratum coverage − null mean")
    axs[1].legend(frameon=False, fontsize=7, loc="lower right")
    save(fig, "F8_error_analysis")
    # sigma-hat decile coverage (covariate-conditional diagnostic)
    sc = [f"sig_cov_{k}" for k in range(10)]
    if all(c in a10.columns for c in sc):
        gs = a10.groupby(["did", "method"])[sc].mean().reset_index()
        fig, ax = plt.subplots(figsize=(4.8, 3.0))
        for m, c in (("NCP", "#e87ba4"), ("S-Res", "#6250d6"), ("S-NCP", AQUA), (P, BLUE), ("DLS-M-LS", GRAY)):
            ax.plot(range(1, 11), gs[gs.method == m][sc].mean().values, marker="o", ms=3, color=c, label=NAME[m])
        ax.axhline(0.9, color="#0b0b0b", lw=0.8)
        ax.set_xticks(range(1, 11))
        ax.set_xlabel("Decile of the estimated scale σ̂(x) (test points)")
        ax.set_ylabel("Coverage (mean over datasets)")
        ax.legend(frameon=False, fontsize=7, ncol=2)
        save(fig, "F12_scale_decile_coverage")


if __name__ == "__main__":
    main()

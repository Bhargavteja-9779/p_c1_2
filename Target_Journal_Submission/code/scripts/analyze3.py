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

import warnings
import matplotlib
matplotlib.use("Agg")
warnings.simplefilter("ignore", category=Warning)
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
    df = pd.concat([pd.read_json(f, lines=True) for f in files], ignore_index=True).copy()
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
    df.to_csv(RES / "raw_results_v3.csv.gz", index=False, compression="gzip")
    a10 = df[(df.alpha == 0.1) & (df.scheme == "S5") & (df.cal_frac == 1.0)]
    METRICS.update(n_methods_main=len(MAIN), n_datasets=int(a10.did.nunique()), n_seeds_min=int(a10.groupby("did").seed.nunique().min()),
                   n_runs=int(a10[["did", "seed"]].drop_duplicates().shape[0]))
    first = a10.drop_duplicates(["did", "seed"])
    # ---------------------------------------------------------------- dataset table (incl. realised strata)
    from src.data.openml_ctr23 import load as dload
    rows = []
    for did, g in first.groupby("did"):
        y = dload(int(did))[1]
        q = np.quantile(y, [0.125, 0.25, 0.5, 0.75, 0.875])
        mass = list(g.train_stratum_mass)
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
    for nm in ("pc", "up1", "up2", "down1", "tails1"):   # worst stratum under shift: min over strata of seed means
        sp_ = stratum_profile(a10, prefix=f"shift_{nm}_cal_cov_").rename(columns={"worst_stratum": f"shift_{nm}_worst"})
        pdm = pdm.merge(sp_, on=["did", "dataset", "method"], how="left")
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
        rows.append({"method": NAME[m], "code": m, "pc_marginal": x.shift_pc_cov.mean(), "pc_worst": x.shift_pc_worst.mean(),
                     "up2_worst": x.shift_up2_worst.mean(), "unshifted_worst": x.worst_stratum.mean(),
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
    # ---------------------------------------------------------------- decision study (tail alerts)
    alerts_study(a10)
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
    # ---------------------------------------------------------------- auxiliary studies
    aux_metrics(df, T1)
    prop1_table()
    synthetic_study()
    learner_studies(pdm)
    timing_study()
    # ---------------------------------------------------------------- figures
    figures(df, a10, pdm, S, T7, sd)
    display_tables()
    json.dump(METRICS, open(RES / "metrics_v3.json", "w"), indent=1, default=float)
    json.dump(STATS, open(RES / "statistics_v3.json", "w"), indent=1, default=float)
    print(T2[["method", "coverage", "upper_tail_cov", "worst_stratum", "n_ds_below_null", "top5_cov", "top1_cov",
              "size_geo", "empty_rate", "sigma_decile_worst"]].round(3).to_string(index=False))
    print(T3[T3.family.str.startswith("H3") | T3.family.str.startswith("Decomp")][
        ["family", "comparison", "geo_ratio", "geo_lo", "geo_hi", "wins", "losses", "p", "p_holm"]].round(4).to_string(index=False))


def aux_metrics(df, T1):
    if "forest_fires" in set(T1.dataset):
        METRICS["forest_zero_frac"] = float(T1.set_index("dataset").loc["forest_fires", "zero_frac"])
    z = df.drop_duplicates(["did", "seed"])
    METRICS["z_sd_ratio_median"] = float(np.median(z.z_sd_cf / z.z_sd_insample))
    METRICS["z_sd_cf_median"] = float(np.median(z.z_sd_cf))
    METRICS["n_runs_any_inf"] = int((df[(df.alpha == 0.1) & (df.scheme == "S5") & (df.cal_frac == 1.0) &
                                        (df.method == P)].n_strata_inf > 0).sum())
    la = TOP / "tables" / "S2_leakage_audit.csv"
    if la.exists():
        L = pd.read_csv(la).set_index("dataset")
        for ds in ("sarcos", "cps88wages", "health_insurance"):
            if ds in L.index:
                METRICS[f"dup_{ds.split('_')[0]}"] = float(L.loc[ds, "dup_rows_frac"])
    gc = TOP / "results" / "grid_convergence.json"
    if gc.exists():
        G = pd.DataFrame(json.loads(gc.read_text()))
        METRICS["grid_convergence"] = G.to_dict("records")
        d = G[G.core == 1536]
        METRICS["grid_max_rel_change"] = float(d.rel_size_diff_vs_finest.max())
        if "max_rel_size_diff_per_point" in d:
            METRICS["grid_max_rel_change_point"] = float(d.max_rel_size_diff_per_point.max())
            METRICS["grid_q99_rel_change_point"] = float(d.q99_rel_size_diff_per_point.max())


def prop1_table():
    P1 = json.loads((TOP / "results" / "prop1_gaussian.json").read_text())["rows"]
    rows = [{"model": "Gaussian signal, Gaussian noise (Prop. 1)", "R2": r["R2"], "bottom10": r["analytic_upper10"],
             "central80": r["analytic_central80"], "top10": r["analytic_upper10"], "top1": r["analytic_upper1"],
             "source": "analytic"} for r in P1 if r["R2"] in (0.5, 0.9)]
    ext = TOP / "results" / "prop1_extension.json"
    if ext.exists():
        for r in json.loads(ext.read_text()):
            rows.append({"model": r["model"], "R2": r["R2"], "bottom10": r["bottom10"], "central80": r["central80"],
                         "top10": r["top10"], "top1": r["top1"], "source": "Monte Carlo"})
    T = pd.DataFrame(rows).sort_values(["R2", "source"], kind="stable")
    table(T, "T0_prop1")


def synthetic_study():
    f = TOP / "results" / "synthetic_v3.jsonl"
    if not f.exists():
        return
    sy = pd.read_json(f, lines=True)
    sy["upper"] = [r[f"cal_cov_{int(k) - 1}"] for k, r in zip(sy.K, sy.to_dict("records"))]
    cc = [c for c in sy.columns if c.startswith("cal_cov_") and c[8:].isdigit()]
    sy["worst"] = sy[cc].min(axis=1, skipna=True)
    base = sy[sy.gamma == 0]
    keep = ["O-HDR-X", "O-SDLC", "O-S-NCP", "O-S-Res", "SCP", "CQR", "HPD-split-LS", "S-Res", "S-NCP", "S-CQR",
            "S-HPD-LS", "SDLC-N", "SDLC-LS"]
    g = base[base.method.isin(keep)].groupby(["dgp", "n", "method"])[["coverage", "upper", "worst", "size", "empty_rate"]].mean().reset_index()
    ref = g[g.method == "S-NCP"].set_index(["dgp", "n"])["size"]
    g["size_vs_SNCP"] = [r["size"] / ref.loc[(r["dgp"], r["n"])] for r in g.to_dict("records")]
    g["method"] = g.method.map(lambda m: NAME.get(m, m))
    table(g, "T11_synthetic")
    est = base[base.method.isin(["S-Res", "S-NCP", "S-CQR", "S-HPD-LS", "SDLC-N", P])]
    wins = {}
    for (dgp, n), gg in est.groupby(["dgp", "n"]):
        pv = gg.pivot(index="seed", columns="method", values="size")
        wins[f"{dgp}_{n}"] = {"sdlc_smallest": int((pv.idxmin(axis=1) == P).sum()), "n_seeds": int(len(pv)),
                              "sdlc_lt_sncp": int((pv[P] < pv["S-NCP"]).sum()), "sdlc_lt_bccp": int((pv[P] < pv["S-Res"]).sum()),
                              "ratio_sncp": float(np.exp(np.mean(np.log(pv[P] / pv["S-NCP"])))),
                              "ratio_bccp": float(np.exp(np.mean(np.log(pv[P] / pv["S-Res"]))))}
    METRICS["synthetic"] = wins
    gm = g.set_index(["dgp", "n", "method"])["size"]
    gains = [1 - gm.loc[(d_, 5000, "O-SDLC")] / gm.loc[(d_, 5000, "O-S-NCP")] for d_ in "ABCD"]
    METRICS["synthetic_oracle_gain_min"], METRICS["synthetic_oracle_gain_max"] = float(min(gains)), float(max(gains))
    METRICS["synthetic_est_lt_sncp"] = int(sum(wins[f"{d_}_5000"]["sdlc_lt_sncp"] for d_ in "ABCDE"))
    METRICS["synthetic_est_lt_bccp"] = int(sum(wins[f"{d_}_5000"]["sdlc_lt_bccp"] for d_ in "ABCDE"))
    METRICS["synthetic_small_lt_sncp"] = int(sum(wins[f"{d_}_500"]["sdlc_lt_sncp"] for d_ in "AB"))
    METRICS["synthetic_gap_C"] = float(gm.loc[("C", 5000, "SDLC")] / gm.loc[("C", 5000, "O-SDLC")] - 1)
    up = g.set_index(["dgp", "n", "method"])["upper"]
    METRICS["synthetic_hdrx_upper_A"] = float(up.loc[("A", 5000, "O-HDR-X")])
    METRICS["synthetic_hdrx_upper_C"] = float(up.loc[("C", 5000, "O-HDR-X")])
    sh = sy[(sy.gamma > 0) | ((sy.gamma == 0) & sy.dgp.isin(["A", "B"]) & (sy.n == 5000))]
    sh = sh[sh.method.isin(["SCP", "CQR", "HPD-split-LS", "S-Res", "S-NCP", "S-CQR", P, "O-SDLC", "O-HDR-X"])]
    t = sh.groupby(["dgp", "gamma", "method"])[["coverage", "upper", "worst"]].mean().reset_index()
    t["method"] = t.method.map(lambda m: NAME.get(m, m))
    table(t, "T12_synthetic_label_shift")
    METRICS["synthetic_shift"] = t.to_dict("records")


def learner_studies(pdm_lgb):
    out = {}
    for tag, d in (("mlp", TOP / "results" / "raw_mlp_v3"), ("dw", TOP / "results" / "raw_denseweight")):
        files = sorted(d.glob("*.jsonl")) if d.exists() else []
        if not files:
            continue
        x = pd.concat([pd.read_json(f_, lines=True) for f_ in files], ignore_index=True)
        x["nsize"] = x["size"] / x["y_train_sd"]
        cc = [c for c in x.columns if c.startswith("cal_cov_") and c[8:].isdigit()]
        x["tail_hi"] = [r[f"cal_cov_{int(k) - 1}"] for k, r in zip(x.K, x[cc].to_dict("records"))]
        pdx = per_dataset(x, ["coverage", "nsize", "tail_hi", "empty_rate"])
        pdx.to_csv(RES / f"per_dataset_{tag}.csv", index=False)
        piv = pdx.pivot(index="did", columns="method", values="nsize")
        rows = []
        for m in H3_PRIMARY:
            if m in piv:
                rows.append({"learner": tag, "comparison": f"SDLC vs {NAME[m]}",
                             **paired_summary(piv[P], piv[m], better="smaller", log=True)})
        for r, p_ in zip(rows, holm([r["p"] for r in rows])):
            r["p_holm"] = p_
        summ = []
        for m in MARGINAL + STRAT:
            xm = pdx[pdx.method == m]
            if len(xm):
                summ.append({"learner": tag, "method": NAME[m], "coverage": xm.coverage.mean(),
                             "upper_tail": xm.tail_hi.mean(), "worst_stratum": xm.worst_stratum.mean(),
                             "size_geo": float(np.exp(np.log(xm.nsize).mean()))})
        out[tag] = {"tests": rows, "summary": summ, "n_datasets": int(pdx.did.nunique()),
                    "n_seeds": int(x.seed.nunique())}
        table(pd.DataFrame(summ), f"T9_{tag}_summary")
        table(pd.DataFrame(rows), f"T9_{tag}_tests", 4)
        if tag == "dw":   # does imbalance-aware training remove the under-coverage of marginal methods?
            lg = pdm_lgb[pdm_lgb.method.isin(MARGINAL + STRAT)]
            cmp_ = []
            for m in ("SCP", "CQR", "NCP", "S-NCP", P):
                a_ = pdx[pdx.method == m].set_index("did")
                b_ = lg[lg.method == m].set_index("did")
                common = a_.index.intersection(b_.index)
                cmp_.append({"method": NAME[m], "worst_dw": float(a_.loc[common].worst_stratum.mean()),
                             "worst_lgb": float(b_.loc[common].worst_stratum.mean()),
                             "upper_dw": float(a_.loc[common].tail_hi.mean()),
                             "upper_lgb": float(b_.loc[common].tail_hi.mean()),
                             "size_ratio_dw_vs_lgb": float(np.exp(np.mean(np.log(a_.loc[common].nsize / b_.loc[common].nsize))))})
            out["dw_vs_lgb"] = cmp_
            table(pd.DataFrame(cmp_), "T9_dw_vs_lgb")
            rm = x.drop_duplicates(["did", "seed"])[["did", "test_rmse", "test_rmse_upper"]].groupby("did").mean()
            out["dw_rmse_upper_median"] = float(rm.test_rmse_upper.median())
    STATS["learners"] = out


def timing_study():
    f = TOP / "results" / "timing_methods_v3.csv"
    if f.exists():
        t = pd.read_csv(f)
        t["us_per_point"] = 1e6 * t.seconds / t.n_test
        med = t.groupby(["dataset", "method"]).us_per_point.median().reset_index()
        summ = med.groupby("method").us_per_point.agg(["median", "max"]).reset_index()
        summ["method"] = summ.method.map(lambda m: NAME.get(m, m))
        table(summ, "T15_timing_methods")
        METRICS["timing_us_per_point"] = {r["method"]: r["median"] for r in summ.to_dict("records")}
    f = TOP / "results" / "timing_fit.csv"
    if f.exists():
        tf = pd.read_csv(f)
        table(tf, "T15b_timing_fit")
        num = tf.select_dtypes("number")
        METRICS["timing_fit_median"] = num.median().to_dict()


def alerts_study(a10, ratios=(1, 5, 10, 20)):
    """Set-based tail alerts (from the evaluation) versus dedicated alert rules (experiments/tail_alerts.py).
    Counts per dataset x seed; dataset-level means; expected cost per unit (FP cost 1, FN cost r)."""
    f = TOP / "results" / "tail_alerts.jsonl"
    if not f.exists():
        return
    ta = pd.read_json(f, lines=True)
    rows = []
    set_methods = ["SCP", "CQR", "HPD-split-LS", "S-Res", "S-NCP", "S-CQR", P, "SDLC-LS-floor"]
    for side in ("hi", "lo"):
        x = a10[a10.method.isin(set_methods)].copy()
        kcol = [f"cal_n_{int(k) - 1}" if side == "hi" else "cal_n_0" for k in x.K]
        x["positives"] = [r[c] for r, c in zip(x.to_dict("records"), kcol)]
        x["alerts"] = x[f"alert_{side}_rate"] * x.n_test
        x["tp"] = x[f"alert_{side}_recall"] * x.positives
        x["rule"] = x.method.map(NAME)
        x["n"] = x.n_test
        x["side"] = side
        rows.append(x[["did", "dataset", "seed", "side", "rule", "n", "positives", "alerts", "tp"]])
    t2 = ta[["did", "dataset", "seed", "side", "rule", "n", "positives", "alerts", "tp"]]
    al = pd.concat(rows + [t2], ignore_index=True)
    al["fp"] = al.alerts - al.tp
    al["fn"] = al.positives - al.tp
    g = al.groupby(["did", "dataset", "side", "rule"])[["n", "positives", "alerts", "tp", "fp", "fn"]].sum().reset_index()
    g["recall"] = g.tp / g.positives
    g["rate"] = g.alerts / g.n
    g["precision"] = g.tp / g.alerts.where(g.alerts > 0)
    for r in ratios:
        g[f"cost_r{r}"] = (g.fp + r * g.fn) / g.n
    g.to_csv(RES / "tail_alerts_per_dataset.csv", index=False)
    summ = g.groupby(["side", "rule"])[["recall", "rate", "precision"] + [f"cost_r{r}" for r in ratios]].mean().reset_index()
    summ["n_ds_recall_ge_0.9"] = g.groupby(["side", "rule"]).recall.apply(lambda v: int((v >= 0.9 - 1e-12).sum())).values
    table(summ, "T13_tail_alerts")
    # paired comparisons of alert rate among rules that guarantee recall >= 0.9
    cmp_ = []
    for side in ("hi", "lo"):
        pv = g[g.side == side].pivot(index="did", columns="rule", values="rate")
        for other in ("TC-LS", "TC-H", "BCCP", "S-NCP", "S-CQR"):
            if other in pv:
                r_ = paired_summary(pv["SDLC"], pv[other], better="smaller", log=True)
                cmp_.append({"side": side, "comparison": f"SDLC vs {other}", **r_})
        for rr in (10, 20):
            pc = g[g.side == side].pivot(index="did", columns="rule", values=f"cost_r{rr}")
            for other in ("TC-LS", "CS-BH-0.2", "Point", "BCCP", "S-NCP", "HPD-split"):
                if other in pc:
                    r_ = paired_summary(pc["SDLC"], pc[other], better="smaller", log=False)
                    cmp_.append({"side": side, "comparison": f"cost r={rr}: SDLC vs {other}", **r_})
    T = pd.DataFrame(cmp_)
    table(T, "T13b_alert_tests", 4)
    STATS["alerts"] = T.to_dict("records")
    METRICS["alerts"] = {f"{r_['side']}|{r_['rule']}": {k: r_[k] for k in ("recall", "rate", "precision", "cost_r10")}
                         for r_ in summ.to_dict("records")}
    case = g[g.dataset.isin(["kings_county", "cps88wages", "miami_housing"]) & (g.side == "hi")]
    table(case[["dataset", "rule", "recall", "rate", "precision", "cost_r1", "cost_r5", "cost_r10", "cost_r20"]],
          "T14_case_study")
    # cost curves for the case-study datasets
    fig, axs = plt.subplots(1, 3, figsize=(7.4, 2.6), sharey=False)
    rr = np.array([1, 2, 5, 10, 20, 50])
    for ax, ds in zip(axs, ["kings_county", "cps88wages", "miami_housing"]):
        cs = g[(g.dataset == ds) & (g.side == "hi")].set_index("rule")
        for rule, c, ls in (("SCP", GRAY, "--"), ("CQR", ORANGE, "--"), ("Point", DARK, ":"), ("TC-LS", "#e87ba4", "-"),
                            ("CS-BH-0.2", "#6250d6", "-."), ("S-NCP", AQUA, "-"), ("SDLC", BLUE, "-")):
            if rule in cs.index:
                v = cs.loc[rule]
                ax.plot(rr, (v.fp + rr * v.fn) / v.n, color=c, ls=ls, marker="o", ms=2.5, label=rule)
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_title(ds.replace("_", " "), fontsize=8)
        ax.set_xlabel("Cost ratio c(FN)/c(FP)")
    axs[0].set_ylabel("Expected cost per unit")
    axs[2].legend(frameon=False, fontsize=6, loc="upper left")
    save(fig, "F13_alert_costs")


def _ci(g, lo, hi, d=3):
    return f"{g:.{d}f} [{lo:.{d}f}, {hi:.{d}f}]"


def _p(p):
    return "< 0.001" if p < 0.001 else f"{p:.3f}"


def display_tables():
    """Print-ready tables (strings) for the manuscript and the supplement: tables/D*.csv."""
    T2 = pd.read_csv(TAB / "T2_main_results.csv")
    d = pd.DataFrame({"Method": T2.method, "Marginal": T2.coverage.map("{:.3f}".format),
                      "Lower tail": T2.lower_tail_cov.map("{:.3f}".format),
                      "Upper tail": T2.upper_tail_cov.map("{:.3f}".format),
                      "Worst stratum": T2.worst_stratum.map("{:.3f}".format),
                      "Below null": T2.n_ds_below_null.astype(int).astype(str),
                      "Top 5%": T2.top5_cov.map("{:.3f}".format), "Top 1%": T2.top1_cov.map("{:.3f}".format),
                      "Size": T2.size_geo.map("{:.3f}".format), "Empty %": (100 * T2.empty_rate).map("{:.2f}".format),
                      "Pieces": T2.pieces.map("{:.2f}".format)})
    d.to_csv(TAB / "D2_main.csv", index=False)
    T3 = pd.read_csv(TAB / "T3_statistical_tests.csv")
    fams = {"H3 size (primary)": "Score (stratified)", "Decomposition BCCP -> S-NCP -> SDLC-N -> SDLC": "Decomposition",
            "H3 size (hull forms)": "Hull forms", "H3 size (secondary)": "Density estimator"}
    x = T3[T3.family.isin(fams)].copy()
    d = pd.DataFrame({"Family": x.family.map(fams), "Comparison": x.comparison,
                      "Ratio [95% CI]": [_ci(a, b, c_) for a, b, c_ in zip(x.geo_ratio, x.geo_lo, x.geo_hi)],
                      "HL ratio": x.hl_ratio.map("{:.3f}".format),
                      "Wins/losses": [f"{int(w)}/{int(l)}" for w, l in zip(x.wins, x.losses)],
                      "Holm p": x.p_holm.map(_p)})
    d.to_csv(TAB / "D3_size_tests.csv", index=False)
    Ts = pd.read_csv(TAB / "T3s_h3_sensitivity.csv")
    d = pd.DataFrame({"Analysis": Ts.analysis, "Comparison": Ts.comparison, "n": Ts.n.astype(int).astype(str),
                      "Ratio [95% CI]": [_ci(a, b, c_) for a, b, c_ in zip(Ts.geo_ratio, Ts.geo_lo, Ts.geo_hi)],
                      "Wins/losses": [f"{int(w)}/{int(l)}" for w, l in zip(Ts.wins, Ts.losses)],
                      "Holm p": Ts.p_holm.map(_p)})
    d.to_csv(TAB / "D3s_sensitivity.csv", index=False)
    T4 = pd.read_csv(TAB / "T4_price.csv")
    d = pd.DataFrame({"Score": [f"{a} → {b}" for a, b in zip(T4.marginal, T4.stratified)],
                      "Size ratio [95% CI]": [_ci(a, b, c_, 2) for a, b, c_ in zip(T4.geo_ratio, T4.ci_low, T4.ci_high)],
                      "Median ratio": T4.median_ratio.map("{:.2f}".format),
                      "Datasets > 1.5": T4["n_ratio_gt_1.5"].astype(int).astype(str),
                      "Worst-stratum gain": T4.worst_gain.map("{:+.3f}".format)})
    d.to_csv(TAB / "D4_price.csv", index=False)
    T4b = pd.read_csv(TAB / "T4b_matched_coverage.csv")
    d = pd.DataFrame({"Marginal method (α = 0.05)": T4b["method_at_alpha_0.05"],
                      "Worst stratum": T4b.worst_stratum.map("{:.3f}".format),
                      "Size": T4b.size_geo.map("{:.3f}".format),
                      "SDLC (α = 0.1) smaller on": T4b.n_ds_SDLC_smaller.astype(int).map(lambda v: f"{v}/31")})
    d.to_csv(TAB / "D4b_matched.csv", index=False)
    T8 = pd.read_csv(TAB / "T8_shift.csv")
    d = pd.DataFrame({"Method": T8.method, "Positive control: marginal": T8.pc_marginal.map("{:.3f}".format),
                      "Positive control: worst stratum": T8.pc_worst.map("{:.3f}".format),
                      "Tilt γ=1: upper stratum": T8.up1_upper.map("{:.3f}".format),
                      "Tilt γ=2: upper stratum": T8.up2_upper.map("{:.3f}".format),
                      "Tilt γ=2: upper (ESS ≥ 50)": T8.up2_upper_ess50.map("{:.3f}".format),
                      "Tilt γ=2: marginal": T8.up2_marginal.map("{:.3f}".format)})
    d.to_csv(TAB / "D8_shift.csv", index=False)
    T13 = pd.read_csv(TAB / "T13_tail_alerts.csv")
    x = T13[T13.side == "hi"]
    order = ["SCP", "CQR", "HPD-split", "BCCP", "S-NCP", "S-CQR", "SDLC", "SDLC-floor", "TC-LS", "TC-H", "CS-BH-0.1",
             "CS-BH-0.2", "Point"]
    x = x.set_index("rule").loc[[o for o in order if o in set(x.rule)]].reset_index()
    d = pd.DataFrame({"Rule": x.rule, "Recall": x.recall.map("{:.3f}".format), "Alert rate": x.rate.map("{:.3f}".format),
                      "Precision": x.precision.map("{:.3f}".format),
                      "Datasets recall ≥ 0.9": x["n_ds_recall_ge_0.9"].astype(int).astype(str),
                      "Cost r=1": x.cost_r1.map("{:.3f}".format), "Cost r=10": x.cost_r10.map("{:.3f}".format),
                      "Cost r=20": x.cost_r20.map("{:.3f}".format)})
    d.to_csv(TAB / "D13_alerts.csv", index=False)
    T1 = pd.read_csv(TAB / "T1_datasets.csv").sort_values("n")
    d = pd.DataFrame({"Dataset": T1.dataset.str.replace("_", " "), "n": T1.n.map("{:,}".format), "p": T1.p.astype(str),
                      "Skewness": T1.skew_y.map("{:.2f}".format), "Distinct y": T1.n_unique_y.map("{:,}".format),
                      "K": T1.K.astype(int).astype(str), "Lower mass": T1.lower_mass.map("{:.3f}".format),
                      "Upper mass": T1.upper_mass.map("{:.3f}".format), "RMSE/sd": T1.rmse_over_sd.map("{:.2f}".format)})
    d.to_csv(TAB / "D1_datasets.csv", index=False)
    if (TAB / "T11_synthetic.csv").exists():
        t = pd.read_csv(TAB / "T11_synthetic.csv")
        t = t[t.n == 5000]
        order = ["O-HDR-X", "O-SDLC", "O-S-NCP", "O-S-Res", "SCP", "CQR", "HPD-split", "BCCP", "S-NCP", "S-CQR", "S-HPD",
                 "SDLC-N", "SDLC"]
        rows = []
        for m in order:
            r = {"Method": m}
            for dgp in "ABCDE":
                x = t[(t.dgp == dgp) & (t.method == m)]
                r[dgp] = "" if x.empty else f"{x.upper.iloc[0]:.3f} / {x.size_vs_SNCP.iloc[0]:.3f}"
            rows.append(r)
        pd.DataFrame(rows).to_csv(TAB / "D11_synthetic.csv", index=False)
    if (TAB / "T12_synthetic_label_shift.csv").exists():
        t = pd.read_csv(TAB / "T12_synthetic_label_shift.csv")
        order = ["SCP", "CQR", "HPD-split", "O-HDR-X", "BCCP", "S-NCP", "S-CQR", "SDLC", "O-SDLC"]
        rows = []
        for m in order:
            r = {"Method": m}
            for dgp in "AB":
                for g in (0.0, 0.5, 1.0, 2.0):
                    x = t[(t.dgp == dgp) & (t.method == m) & (t.gamma == g)]
                    r[f"{dgp}, γ={g:g}"] = "" if x.empty else f"{x.upper.iloc[0]:.3f}"
            rows.append(r)
        pd.DataFrame(rows).to_csv(TAB / "D12_synthetic_shift.csv", index=False)
    cf = TOP / "results" / "confirmatory" / "statistics_confirmatory.json"
    if cf.exists():
        CF = json.loads(cf.read_text())
        rows = []
        for t in CF["C-H1"]["tests"]:
            rows.append({"Hypothesis": "C-H1 worst-stratum coverage (one-sided)", "Comparison": t["comparison"].replace("yhat", "ŷ"),
                         "Effect": f"HL difference {t['hl']:+.3f}", "Wins/losses": f"{t['wins']}/{t['losses']}",
                         "Holm p": _p(t["p_holm"]), "Decision": "supported" if CF["C-H1"]["supported"] else "not supported"})
        h2 = CF["C-H2"]
        rows.append({"Hypothesis": "C-H2 validity (datasets below null 5% quantile)", "Comparison": "SDLC",
                     "Effect": f"{h2['n_below_null_q05']} of {CF['n_datasets']} (critical value {h2['critical']})",
                     "Wins/losses": "", "Holm p": f"binomial {_p(h2['binom_p_excess'])}",
                     "Decision": "consistent" if h2["consistent_with_validity"] else "not consistent"})
        for t in CF["C-H3"]["tests"]:
            dec = "favours SDLC" if t["favours_SDLC"] else ("favours comparator" if t["favours_comparator"] else "no difference shown")
            rows.append({"Hypothesis": "C-H3 set size (two-sided)", "Comparison": t["comparison"],
                         "Effect": "ratio " + _ci(t["geo_ratio"], t["geo_lo"], t["geo_hi"]),
                         "Wins/losses": f"{t['wins']}/{t['losses']}", "Holm p": _p(t["p_holm"]), "Decision": dec})
        for t in CF["C-H4"]:
            rows.append({"Hypothesis": "C-H4 equivalence of worst-stratum coverage (margin 0.02)", "Comparison": t["comparison"],
                         "Effect": f"median difference {t['median_diff']:+.4f}", "Wins/losses": "",
                         "Holm p": f"TOST {_p(t['p_tost'])}", "Decision": "equivalent" if t["p_tost"] < 0.05 else "not shown"})
        pd.DataFrame(rows).to_csv(TAB / "C2_display.csv", index=False)
    for nm, src in (("D5_alpha", "T5_alpha_sensitivity"), ("D6_strata", "T6_strata_schemes"),
                    ("D7_calsize", "T7_calibration_size"), ("D2b_variants", "T2b_variants"),
                    ("D10_error", "T10_error_analysis")):
        if (TAB / f"{src}.csv").exists():
            t = pd.read_csv(TAB / f"{src}.csv")
            for c_ in t.columns:
                if pd.api.types.is_float_dtype(t[c_]):
                    t[c_] = t[c_].map(lambda v: "" if pd.isna(v) else f"{v:.3f}")
            t.to_csv(TAB / f"{nm}.csv", index=False)


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
    steps = [("S-NCP", "S-Res", "S-NCP / BCCP\n(adds σ̂)"), ("SDLC-N", "S-NCP", "SDLC-N / S-NCP\n(adds 1/σ̂ weighting)"),
             (P, "SDLC-N", "SDLC / SDLC-N\n(adds KDE shape)")]
    for i, (a, b, lab) in enumerate(steps):
        r = np.log(S[a] / S[b]).dropna()
        ax.scatter(np.full(len(r), i) + np.random.default_rng(i).uniform(-0.15, 0.15, len(r)), np.exp(r), s=10,
                   color=[AQUA, ORANGE, BLUE][i], alpha=0.8)
        ax.plot([i - 0.25, i + 0.25], [np.exp(r.mean())] * 2, color="#0b0b0b", lw=1.5)
    ax.axhline(1, color="#8a8984", lw=0.8)
    ax.set_yscale("log")
    from matplotlib.ticker import FixedLocator, NullFormatter, ScalarFormatter
    ax.yaxis.set_major_locator(FixedLocator([0.3, 0.5, 0.7, 0.85, 1.0, 1.2, 1.5]))
    ax.yaxis.set_major_formatter(ScalarFormatter())
    ax.yaxis.set_minor_formatter(NullFormatter())
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

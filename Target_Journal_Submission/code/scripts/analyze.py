"""Generate ALL statistics, tables and figures of the manuscript from results/raw/*.jsonl.

Unit of analysis for inference: dataset (metrics averaged over the 10 predefined seeds).
Outputs: results/raw_results.csv, results/metrics.json, results/statistics.json,
tables/*.csv|*.md, figures/*.png|*.pdf.
"""
from __future__ import annotations

import glob
import json
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
from src.statistics.tests import (bootstrap_ci, friedman, holm, nemenyi_cd,  # noqa: E402
                                  paired_wilcoxon)

CFG = json.loads((ROOT / "config" / "benchmark.json").read_text())
RAW = Path(sys.argv[1]) if len(sys.argv) > 1 else TOP / "results" / "raw_eval"
import os  # noqa: E402
_OUT = Path(os.environ["TSCP_OUT_ROOT"]) if os.environ.get("TSCP_OUT_ROOT") else TOP
RES, TAB, FIG = _OUT / "results", _OUT / "tables", _OUT / "figures"
for d in (RES, TAB, FIG):
    d.mkdir(parents=True, exist_ok=True)

NAME = {"SCP": "SCP", "NCP": "NCP", "CQR": "CQR", "MCP-yhat": "Mondrian-ŷ",
        "DCP-LS": "DCP", "HPD-split-LS": "HPD-split", "DLS-M-LS": "DLS",
        "DCP-H": "DCP (hist.)", "HPD-split-H": "HPD-split (hist.)", "DLS-M-H": "DLS (hist.)",
        "S-Res": "BCCP", "S-Res-hull": "BCCP-hull", "S-NCP": "S-NCP", "S-CQR": "S-CQR", "S-HPD-LS": "S-HPD",
        "S-HPD-H": "S-HPD (hist.)", "SDLC-LS": "SDLC (proposed)", "SDLC-H": "SDLC (hist.)",
        "SDLC-LS-floor": "SDLC-floor", "SDLC-H-floor": "SDLC-floor (hist.)",
        "SDLC-LS-hull": "SDLC-hull", "SDLC-H-hull": "SDLC-hull (hist.)",
        "SDLC-LS2": "SDLC-2p", "DLS-M-LS2": "DLS-2p", "S-HPD-LS2": "S-HPD-2p", "HPD-split-LS2": "HPD-split-2p",
        "DCP-LS2": "DCP-2p", "SDLC-LS2-floor": "SDLC-2p-floor", "SDLC-LS2-hull": "SDLC-2p-hull"}
MARGINAL = ["SCP", "NCP", "CQR", "MCP-yhat", "DCP-LS", "HPD-split-LS", "DLS-M-LS"]
STRAT = ["S-Res", "S-Res-hull", "S-NCP", "S-CQR", "S-HPD-LS", "SDLC-LS"]
VARIANTS = ["SDLC-LS2", "SDLC-LS2-floor", "SDLC-LS2-hull", "DLS-M-LS2", "HPD-split-LS2", "DCP-LS2", "S-HPD-LS2",
            "SDLC-H", "DLS-M-H", "HPD-split-H", "DCP-H", "S-HPD-H", "SDLC-H-floor", "SDLC-H-hull"]
MAIN = MARGINAL + STRAT + ["SDLC-LS-floor", "SDLC-LS-hull"]
PROPOSED = "SDLC-LS"
PAIRS = [("SCP", "S-Res"), ("NCP", "S-NCP"), ("CQR", "S-CQR"), ("HPD-split-LS", "S-HPD-LS"),
         ("DLS-M-LS", "SDLC-LS"), ("DLS-M-LS2", "SDLC-LS2"), ("DLS-M-H", "SDLC-H")]
BLUE, ORANGE, AQUA, GRAY, DARK = "#2a78d6", "#eb6834", "#1baf7a", "#a3a29c", "#52514e"
plt.rcParams.update({"font.size": 8, "axes.spines.top": False, "axes.spines.right": False,
                     "axes.edgecolor": "#8a8984", "axes.labelcolor": "#0b0b0b",
                     "xtick.color": "#52514e", "ytick.color": "#52514e", "axes.grid": True,
                     "grid.color": "#e6e5e0", "grid.linewidth": 0.5, "figure.dpi": 150,
                     "savefig.dpi": 300, "font.family": "DejaVu Sans", "lines.linewidth": 1.5})
STATS: dict = {}
METRICS: dict = {}


def save(fig, name):
    fig.tight_layout()
    fig.savefig(FIG / f"{name}.png", bbox_inches="tight")
    fig.savefig(FIG / f"{name}.pdf", bbox_inches="tight")
    plt.close(fig)


def table(df, name, floatfmt=3):
    df.to_csv(TAB / f"{name}.csv", index=False)
    with open(TAB / f"{name}.md", "w") as fh:
        fh.write(df.to_markdown(index=False, floatfmt=f".{floatfmt}f"))


def load():
    files = sorted(glob.glob(str(RAW / "*.jsonl")))
    df = pd.concat([pd.read_json(f, lines=True) for f in files], ignore_index=True)
    df["nsize"] = df["size"] / df["y_train_sd"]
    df["tail_lo"] = df["cal_cov_0"]
    df["tail_hi"] = [r[f"cal_cov_{int(r['K']) - 1}"] for _, r in df[["K"] + [c for c in df.columns
                     if c.startswith("cal_cov_")]].iterrows()]
    return df


def per_dataset(d, cols):
    return d.groupby(["did", "dataset", "method"])[cols].mean().reset_index()


def modal_k(d):
    """Keep, per dataset, only splits whose realised number of strata equals the modal one (tied
    targets can merge cut points differently across splits; only health_insurance is affected)."""
    mk = d.groupby("did").K.agg(lambda k: k.value_counts().idxmax())
    return d[d.K == d.did.map(mk)]


def stratum_profile(d):
    """Seed-averaged coverage of every stratum, then min over strata (avoids the downward
    bias of taking the minimum of noisy single-seed estimates)."""
    d = modal_k(d)
    cc = [c for c in d.columns if c.startswith("cal_cov_")]
    g = d.groupby(["did", "dataset", "method"])[cc].mean()
    out = pd.DataFrame({"worst_stratum": g.min(axis=1, skipna=True),
                        "mean_deficit": (0.9 - g).clip(lower=0).mean(axis=1, skipna=True)})
    return out.reset_index()


def null_worst_stratum(d, alpha=0.1, B=4000, seed=0):
    """Null reference for worst-stratum coverage under EXACT split-conformal validity.
    For each dataset: per seed and stratum, conditional coverage C ~ Beta(r, n+1-r) with
    r = ceil((n+1)(1-alpha)) (C = 1 if r > n), test coverage ~ Binomial(m, C)/m with the realised
    calibration size n and test size m of the stratum; average over seeds; minimum over strata.
    Returns {did: (mean, 5% quantile)}."""
    rng = np.random.default_rng(seed)
    out = {}
    one = d.drop_duplicates(["did", "seed"])
    for did, g in one.groupby("did"):
        sims = np.zeros((B, len(g)))
        covs = []
        for j, (_, r) in enumerate(g.iterrows()):
            nk = r["ncal_strata"]
            K = len(nk)
            cs = np.zeros((B, K))
            for k in range(K):
                n, m = int(nk[k]), int(r.get(f"cal_n_{k}", 0) or 0)
                if m == 0:
                    cs[:, k] = np.nan
                    continue
                rk = int(np.ceil((n + 1) * (1 - alpha)))
                C = np.ones(B) if rk > n else rng.beta(rk, n + 1 - rk, B)
                cs[:, k] = rng.binomial(m, C) / m
            covs.append(cs)
        avg = np.nanmean(np.stack(covs, 0), axis=0)      # B x K, averaged over seeds
        w = np.nanmin(avg, axis=1)
        out[did] = (float(w.mean()), float(np.quantile(w, 0.05)))
    return out


def main():
    df = load()
    df.to_csv(RES / "raw_results.csv", index=False)
    a10 = df[(df.alpha == 0.1) & (df.scheme == "S5") & (df.cal_frac == 1.0)]
    n_ds, n_seed = a10.did.nunique(), a10.seed.nunique()
    seeds_per_ds = a10.groupby("did").seed.nunique()
    METRICS["n_datasets"], METRICS["n_seeds_min"] = int(n_ds), int(seeds_per_ds.min())
    METRICS["n_runs"] = int(a10[["did", "seed"]].drop_duplicates().shape[0])
    dev = set(CFG["dev_datasets"])

    # ---------------------------------------------------------------- dataset table
    first = a10.drop_duplicates(["did", "seed"])
    dsum = first.groupby(["did", "dataset"]).agg(n=("n", "first"), p=("p", "first"),
                                                  n_cal=("n_cal", "mean"), n_test=("n_test", "mean"),
                                                  K=("K", "median"), rmse_over_sd=("test_rmse", "mean"),
                                                  sd=("y_train_sd", "mean"),
                                                  nll_LS=("test_nll_LS", "mean"), nll_H=("test_nll_H", "mean"),
                                                  out_dom=("frac_test_out_domain", "mean")).reset_index()
    dsum["rmse_over_sd"] = dsum["rmse_over_sd"] / dsum["sd"]
    dsum["nll_LS_minus_H"] = dsum["nll_LS"] - dsum["nll_H"]
    dsum["dev"] = dsum.did.isin(dev)
    skew = {}
    from src.data.openml_ctr23 import load as dload
    for did in dsum.did:
        y = dload(int(did))[1]
        skew[did] = float(stats.skew(y))
    dsum["skew_y"] = dsum.did.map(skew)
    table(dsum[["did", "dataset", "n", "p", "skew_y", "n_cal", "K", "rmse_over_sd", "nll_LS", "nll_H",
                "out_dom", "dev"]].sort_values("n"), "T1_datasets")
    METRICS["frac_test_out_domain_max"] = float(dsum.out_dom.max())
    METRICS["frac_test_out_domain_mean"] = float(dsum.out_dom.mean())
    METRICS["max_n_test"] = int(first.n_test.max())
    METRICS["forest_zero_frac"] = float((dload(44962)[1] == 0).mean()) if 44962 in set(dsum.did) else float("nan")
    inf = {}
    for a in CFG["alphas"]:
        col = f"n_strata_inf_a{a}"
        if col in first:
            inf[str(a)] = {"runs_with_inf": int((first[col] > 0).sum()), "runs": int(len(first)),
                           "datasets_with_inf": int(first[first[col] > 0].did.nunique()),
                           "strata_inf_total": int(first[col].sum())}
    METRICS["inf_threshold"] = inf
    METRICS["datasets_LS_better_nll"] = int((dsum.nll_LS_minus_H < 0).sum())

    # ---------------------------------------------------------------- main table
    cols = ["coverage", "nsize", "tail_lo", "tail_hi", "components", "wsc", "empty_rate",
            "dec_worst", "ext_cov_0", "ext_cov_2"] + (["t_calib_predict"] if "t_calib_predict" in a10 else [])
    pdm = per_dataset(a10, cols).merge(stratum_profile(a10), on=["did", "dataset", "method"])
    if "ncal_strata" in a10.columns:
        nul = null_worst_stratum(modal_k(a10[a10.method == PROPOSED]))
        pdm["null_worst_mean"] = pdm.did.map(lambda d: nul[d][0])
        pdm["null_worst_q05"] = pdm.did.map(lambda d: nul[d][1])
        pdm["below_null"] = pdm.worst_stratum < pdm.null_worst_q05
    pdm.to_csv(RES / "per_dataset_main.csv", index=False)
    rows = []
    for m in MAIN + VARIANTS:
        x = pdm[pdm.method == m]
        if x.empty:
            continue
        rows.append({"method": NAME[m], "code": m, "group": "marginal" if m in MARGINAL or m.startswith(("DLS-M", "HPD-split", "DCP")) else "stratified",
                     "coverage": x.coverage.mean(), "lower_tail_cov": x.tail_lo.mean(),
                     "upper_tail_cov": x.tail_hi.mean(), "worst_stratum": x.worst_stratum.mean(),
                     "n_ds_worst_lt_0.85": int((x.worst_stratum < 0.85).sum()),
                     "top5pct_cov": x.ext_cov_2.mean(), "bottom5pct_cov": x.ext_cov_0.mean(),
                     "nsize_mean": x.nsize.mean(), "nsize_median": x.nsize.median(),
                     "components": x.components.mean(), "wsc": x.wsc.mean(),
                     "null_worst_mean": x.null_worst_mean.mean() if "null_worst_mean" in x else np.nan,
                     "n_ds_below_null": int(x.below_null.sum()) if "below_null" in x else -1})
    T2 = pd.DataFrame(rows)
    table(T2, "T2_main_results")
    METRICS["main"] = T2.set_index("code").to_dict(orient="index")

    # ---------------------------------------------------------------- statistical tests (H1, H2, H3)
    piv = lambda col: pdm.pivot(index="did", columns="method", values=col)
    W, S = piv("worst_stratum"), piv("nsize")
    TU = piv("tail_hi")
    tests = []
    for name, col_piv, alt in (("worst_stratum", W, "greater"), ("upper_tail", TU, "greater")):
        comp = [m for m in MARGINAL]
        res = [paired_wilcoxon(col_piv[PROPOSED], col_piv[m], alternative=alt) for m in comp]
        adj = holm([r["p"] for r in res])
        for m, r, pa in zip(comp, res, adj):
            tests.append({"hypothesis": "H1", "metric": name, "comparison": f"SDLC vs {NAME[m]}",
                          "alternative": alt, **{k: v for k, v in r.items() if k != "ci"},
                          "ci_low": r["ci"][0], "ci_high": r["ci"][1], "p_holm": pa})
    # H3: size among stratified methods (two-sided)
    comp = ["S-Res", "S-NCP", "S-CQR", "S-HPD-LS", "SDLC-LS2", "SDLC-H"]
    res = [paired_wilcoxon(np.log(S[PROPOSED]), np.log(S[m])) for m in comp]
    adj = holm([r["p"] for r in res])
    for m, r, pa in zip(comp, res, adj):
        tests.append({"hypothesis": "H3", "metric": "log_size", "comparison": f"SDLC vs {NAME[m]}",
                      "alternative": "two-sided", **{k: v for k, v in r.items() if k != "ci"},
                      "ci_low": r["ci"][0], "ci_high": r["ci"][1], "p_holm": pa})
    # same, worst stratum among stratified (two-sided)
    res = [paired_wilcoxon(W[PROPOSED], W[m]) for m in comp]
    adj = holm([r["p"] for r in res])
    for m, r, pa in zip(comp, res, adj):
        tests.append({"hypothesis": "H3", "metric": "worst_stratum", "comparison": f"SDLC vs {NAME[m]}",
                      "alternative": "two-sided", **{k: v for k, v in r.items() if k != "ci"},
                      "ci_low": r["ci"][0], "ci_high": r["ci"][1], "p_holm": pa})
    T3 = pd.DataFrame(tests)
    # confirmatory subset (exclude development datasets)
    conf = []
    keep = [d for d in W.index if d not in dev]
    for m in MARGINAL:
        r = paired_wilcoxon(W.loc[keep, PROPOSED], W.loc[keep, m], alternative="greater")
        conf.append({"comparison": f"SDLC vs {NAME[m]}", "n": r["n"], "p": r["p"],
                     "median_diff": r["median_diff"], "rbc": r["rbc"]})
    cdf = pd.DataFrame(conf)
    cdf["p_holm"] = holm(cdf.p)
    table(cdf, "T3b_confirmatory_worst_stratum_excl_dev", 4)
    table(T3, "T3_statistical_tests", 4)
    STATS["tests"] = T3.to_dict(orient="records")
    STATS["confirmatory_excl_dev"] = cdf.to_dict(orient="records")

    # price of stratum validity (H2): size ratio stratified / marginal counterpart
    price = []
    for mm, sm in PAIRS:
        if mm not in S or sm not in S:
            continue
        lr = np.log(S[sm] / S[mm]).dropna()
        gm = float(np.exp(lr.mean()))
        lo, hi = bootstrap_ci(lr.values, fn=np.mean)
        dW = (W[sm] - W[mm]).dropna()
        price.append({"marginal": NAME[mm], "stratified": NAME[sm], "geo_mean_size_ratio": gm,
                      "ci_low": float(np.exp(lo)), "ci_high": float(np.exp(hi)),
                      "median_ratio": float(np.exp(lr.median())),
                      "worst_stratum_gain_mean": float(dW.mean()),
                      "n_ds_size_ratio_gt_1.5": int((np.exp(lr) > 1.5).sum())})
    T4 = pd.DataFrame(price)
    table(T4, "T4_price_of_stratum_validity")
    STATS["price"] = T4.to_dict(orient="records")

    # Friedman + Nemenyi on worst-stratum coverage and size across the 12 main methods
    fm = MARGINAL + STRAT
    Wm = W[fm].dropna()
    st, p, ranks = friedman(-Wm.values)   # rank 1 = highest worst-stratum coverage
    Sm = S[fm].dropna()
    st2, p2, ranks2 = friedman(Sm.values)  # rank 1 = smallest size
    STATS["friedman"] = {"worst_stratum": {"chi2": st, "p": p, "mean_ranks": dict(zip(fm, ranks.tolist()))},
                         "size": {"chi2": st2, "p": p2, "mean_ranks": dict(zip(fm, ranks2.tolist()))},
                         "nemenyi_cd_0.05": nemenyi_cd(len(fm), len(Wm)), "n": int(len(Wm))}
    fig, axs = plt.subplots(1, 2, figsize=(7.2, 3.0))
    for ax, rk, ttl in ((axs[0], ranks, "Worst-stratum coverage (rank 1 = best)"),
                        (axs[1], ranks2, "Set size (rank 1 = smallest)")):
        o = np.argsort(rk)
        cols_ = [BLUE if fm[i] == PROPOSED else (AQUA if fm[i] in STRAT else GRAY) for i in o]
        ax.barh([NAME[fm[i]] for i in o][::-1], rk[o][::-1], color=cols_[::-1], height=0.6)
        ax.set_xlabel("Mean Friedman rank across datasets")
        ax.set_title(ttl, fontsize=8)
        cd = STATS["friedman"]["nemenyi_cd_0.05"]
        ax.errorbar([rk[o][0]], [len(o) - 1], xerr=[[0], [cd]], color=DARK, capsize=3, lw=1)
        ax.grid(axis="y", visible=False)
    save(fig, "F5_friedman_ranks")

    # ---------------------------------------------------------------- decile profile figure
    dc = [f"dec_cov_{k}" for k in range(10)]
    prof = a10.groupby("method")[dc].mean()
    fig, ax = plt.subplots(figsize=(4.6, 3.0))
    show = [("SCP", GRAY, "--"), ("CQR", ORANGE, "-"), ("HPD-split-LS", DARK, ":"),
            ("NCP", "#e87ba4", "-."), ("S-NCP", AQUA, "-"), ("SDLC-LS", BLUE, "-")]
    xs = np.arange(1, 11)
    for m, c, ls in show:
        ax.plot(xs, prof.loc[m].values, color=c, ls=ls, marker="o", ms=3, label=NAME[m])
    ax.axhline(0.9, color="#0b0b0b", lw=0.8)
    ax.text(10.4, 0.9, "1-α", va="center", fontsize=7)
    ax.set_xticks(xs)
    ax.set_xlabel("Target decile (training distribution)")
    ax.set_ylabel("Coverage (mean over datasets)")
    ax.legend(frameon=False, fontsize=7, ncol=2, loc="lower center")
    save(fig, "F3_decile_coverage_profile")
    METRICS["decile_profile"] = prof.loc[[m for m, _, _ in show]].round(4).to_dict(orient="index")

    # ---------------------------------------------------------------- per-dataset tail plot
    t = pdm[pdm.method.isin(["CQR", "HPD-split-LS", "SDLC-LS"])].pivot(index="dataset", columns="method",
                                                                       values="tail_hi")
    t = t.sort_values("SDLC-LS")
    fig, ax = plt.subplots(figsize=(4.6, 5.2))
    yy = np.arange(len(t))
    for m, c, mk in (("CQR", ORANGE, "s"), ("HPD-split-LS", GRAY, "^"), ("SDLC-LS", BLUE, "o")):
        ax.scatter(t[m], yy, color=c, s=14, marker=mk, label=NAME[m], zorder=3)
    ax.axvline(0.9, color="#0b0b0b", lw=0.8)
    ax.set_yticks(yy)
    ax.set_yticklabels(t.index, fontsize=6)
    ax.set_xlabel("Coverage in the upper-tail stratum (top 10% of targets)")
    ax.legend(frameon=False, fontsize=7, loc="lower left")
    save(fig, "F4_upper_tail_per_dataset")

    # ---------------------------------------------------------------- trade-off figure
    from adjustText import adjust_text
    fig, ax = plt.subplots(figsize=(4.8, 3.4))
    texts = []
    for m in MAIN:
        x = pdm[pdm.method == m]
        c = BLUE if m == PROPOSED else (AQUA if m in STRAT else (ORANGE if "floor" in m or "hull" in m else GRAY))
        xv, yv = x.worst_stratum.mean(), np.exp(np.log(x.nsize).mean())
        ax.scatter(xv, yv, color=c, s=30, zorder=3, edgecolor="white", linewidth=0.8)
        texts.append(ax.text(xv, yv, NAME[m], fontsize=6.5, color="#0b0b0b" if m == PROPOSED else "#52514e"))
    ax.axvline(0.9, color="#0b0b0b", lw=0.8)
    ax.set_xlabel("Worst-stratum coverage (mean over datasets)")
    ax.set_ylabel("Set size / sd(y)  (geometric mean)")
    adjust_text(texts, ax=ax, arrowprops=dict(arrowstyle="-", color="#c3c2b7", lw=0.5), expand=(1.2, 1.4))
    save(fig, "F2_coverage_size_tradeoff")

    # ---------------------------------------------------------------- alpha sensitivity
    rows = []
    for a in sorted(df.alpha.unique()):
        d = df[(df.alpha == a) & (df.scheme == "S5") & (df.cal_frac == 1.0)]
        pd_ = per_dataset(d, ["coverage", "nsize", "tail_hi", "tail_lo"]).merge(stratum_profile(d).assign(
            worst_stratum=lambda z: z.worst_stratum), on=["did", "dataset", "method"])
        # worst-stratum coverage with the same seed-averaging and modal-K rule as the main table
        ws = stratum_profile(d)[["did", "method", "worst_stratum"]].rename(columns={"worst_stratum": "ws"})
        for m in MARGINAL + STRAT + ["SDLC-LS-floor"]:
            x = pd_[pd_.method == m]
            if x.empty:
                continue
            rows.append({"alpha": a, "method": NAME[m], "coverage": x.coverage.mean(),
                         "worst_stratum": ws[ws.method == m].ws.mean(),
                         "upper_tail": x.tail_hi.mean(), "nsize_geo": float(np.exp(np.log(x.nsize).mean()))})
    T5 = pd.DataFrame(rows)
    table(T5, "T5_alpha_sensitivity")

    # ---------------------------------------------------------------- strata-scheme sensitivity
    rows = []
    for sch in ("S3", "S5", "S10"):
        d = df[(df.alpha == 0.1) & (df.scheme == sch) & (df.cal_frac == 1.0)]
        sp = stratum_profile(d)
        for m in ["S-Res", "DLS-M-LS", "SDLC-LS", "DLS-M-H", "SDLC-H"]:
            x, y_ = d[d.method == m], sp[sp.method == m]
            if x.empty:
                continue
            rows.append({"scheme": sch, "K_median": float(x.K.median()), "method": NAME[m],
                         "coverage": x.coverage.mean(), "worst_stratum": y_.worst_stratum.mean(),
                         "decile_worst_seedavg": float(x.groupby("did")[[f"dec_cov_{k}" for k in range(10)]].mean()
                                                       .min(axis=1).mean()),
                         "nsize_geo": float(np.exp(np.log(x.groupby("did").nsize.mean()).mean()))})
    T6 = pd.DataFrame(rows)
    table(T6, "T6_strata_scheme_sensitivity")

    # ---------------------------------------------------------------- calibration-size sensitivity
    rows = []
    for f in sorted(df.cal_frac.unique()):
        d = df[(df.alpha == 0.1) & (df.scheme == "S5") & (df.cal_frac == f)]
        sp = stratum_profile(d)
        for m in CFG["cal_frac_methods"]:
            x, y_ = d[d.method == m], sp[sp.method == m]
            if x.empty:
                continue
            rows.append({"cal_frac": f, "mean_n_cal": float(x.n_cal.mean() * f), "method": NAME[m],
                         "coverage": x.coverage.mean(), "worst_stratum": y_.worst_stratum.mean(),
                         "upper_tail": x.tail_hi.mean(),
                         "nsize_geo": float(np.exp(np.log(x.groupby("did").nsize.mean()).mean()))})
    T7 = pd.DataFrame(rows)
    table(T7, "T7_calibration_size_sensitivity")
    fig, axs = plt.subplots(1, 2, figsize=(7.0, 2.8))
    for m, c in (("SCP", GRAY), ("CQR", ORANGE), ("NCP", "#e87ba4"), ("S-NCP", AQUA), ("SDLC-LS", BLUE)):
        x = T7[T7.method == NAME[m]]
        axs[0].plot(x.cal_frac, x.worst_stratum, marker="o", ms=3, color=c, label=NAME[m])
        axs[1].plot(x.cal_frac, x.nsize_geo, marker="o", ms=3, color=c, label=NAME[m])
    axs[0].axhline(0.9, color="#0b0b0b", lw=0.8)
    axs[0].set_ylabel("Worst-stratum coverage")
    axs[1].set_ylabel("Set size / sd(y) (geo. mean)")
    for ax in axs:
        ax.set_xlabel("Fraction of calibration set used")
        ax.set_xscale("log")
        ax.set_xticks([0.25, 0.5, 1.0])
        ax.set_xticklabels(["0.25", "0.5", "1"])
    axs[1].legend(frameon=False, fontsize=7)
    save(fig, "F7_calibration_size")

    # ---------------------------------------------------------------- label shift (H4)
    rows = []
    sh = [c for c in a10.columns if c.startswith("shift_") and c.endswith("_cov")]
    for m in MARGINAL + STRAT + ["SDLC-LS-floor"]:
        x = a10[a10.method == m].groupby("did")[sh].mean()
        r = {"method": NAME[m], "code": m}
        for c in sh:
            r[c.replace("shift_", "").replace("_cov", "")] = x[c].mean()
            r[c.replace("shift_", "").replace("_cov", "") + "_min_ds"] = x[c].min()
        rows.append(r)
    T8 = pd.DataFrame(rows)
    table(T8.drop(columns="code"), "T8_label_shift")
    STATS["label_shift"] = {}
    for c in sh:
        x = a10.groupby(["did", "method"])[c].mean().unstack()
        res = [paired_wilcoxon(x[PROPOSED], x[m], alternative="greater") for m in MARGINAL]
        adj = holm([r["p"] for r in res])
        STATS["label_shift"][c] = {NAME[m]: {"median_diff": r["median_diff"], "p_holm": pa, "rbc": r["rbc"]}
                                   for m, r, pa in zip(MARGINAL, res, adj)}
    fig, ax = plt.subplots(figsize=(4.6, 3.0))
    order = ["down1", "tails1", "up1", "up2"]
    labels = ["Lower-tail\ntilt γ=1", "Two-tail\ntilt γ=1", "Upper-tail\ntilt γ=1", "Upper-tail\ntilt γ=2"]
    for m, c in (("SCP", GRAY), ("CQR", ORANGE), ("HPD-split-LS", DARK), ("NCP", "#e87ba4"),
                 ("S-NCP", AQUA), ("SDLC-LS", BLUE)):
        r = T8[T8.code == m].iloc[0]
        ax.plot(range(4), [r[o] for o in order], marker="o", ms=3, color=c, label=NAME[m])
    ax.axhline(0.9, color="#0b0b0b", lw=0.8)
    ax.set_xticks(range(4))
    ax.set_xticklabels(labels, fontsize=7)
    ax.set_ylabel("Coverage under shifted target distribution")
    ax.legend(frameon=False, fontsize=7, ncol=2)
    save(fig, "F6_label_shift")

    # hull (interval) comparison: SDLC-hull vs BCCP-hull (both single intervals)
    r = paired_wilcoxon(np.log(S["SDLC-LS-hull"]), np.log(S["S-Res-hull"]))
    STATS["hull_vs_bccp_hull"] = {**{k: v for k, v in r.items() if k != "ci"}, "ci": r["ci"],
                                  "geo_ratio": float(np.exp(np.log(S["SDLC-LS-hull"] / S["S-Res-hull"]).mean()))}
    # geometric-mean size ratios of SDLC versus each stratified competitor (with bootstrap CI)
    STATS["sdlc_size_ratios"] = {}
    for m in ["S-Res", "S-NCP", "S-CQR", "S-HPD-LS", "SDLC-LS2", "SDLC-H"]:
        lr = np.log(S[PROPOSED] / S[m]).dropna()
        lo_, hi_ = bootstrap_ci(lr.values, fn=np.mean)
        STATS["sdlc_size_ratios"][m] = {"geo": float(np.exp(lr.mean())), "ci": [float(np.exp(lo_)), float(np.exp(hi_))],
                                        "n_smaller": int((lr < 0).sum()), "n": int(len(lr))}
    # ---------------------------------------------------------------- tail alerts (decision view)
    acols = ["alert_hi_recall", "alert_hi_rate", "alert_hi_precision", "alert_lo_recall", "alert_lo_rate",
             "alert_lo_precision"]
    if all(c in a10.columns for c in acols):
        al = a10.groupby(["did", "method"])[acols].mean().reset_index()
        rows = []
        for m in MAIN + ["SDLC-LS2", "SDLC-H"]:
            x = al[al.method == m]
            rows.append({"method": NAME[m], "code": m, **{c: x[c].mean() for c in acols}})
        T13 = pd.DataFrame(rows)
        table(T13.drop(columns="code"), "T13_tail_alerts")
        METRICS["alerts"] = T13.set_index("code").to_dict(orient="index")
        fig, ax = plt.subplots(figsize=(4.8, 3.4))
        texts = []
        keym = ["SCP", "NCP", "CQR", "HPD-split-LS", "S-Res", "S-Res-hull", "S-NCP", "S-CQR", "SDLC-LS",
                "SDLC-LS-floor", "SDLC-LS-hull"]
        sub = T13[T13.code.isin(keym)].copy()
        sub["key"] = list(zip(sub.alert_hi_recall.round(4), sub.alert_hi_precision.round(4)))
        for key, grp in sub.groupby("key", sort=False):   # coincident points share one label
            codes = list(grp.code)
            c = BLUE if PROPOSED in codes else (AQUA if any(cc in STRAT for cc in codes) else
                                                (ORANGE if any("floor" in cc or "hull" in cc for cc in codes) else GRAY))
            ax.scatter(key[0], key[1], color=c, s=30, edgecolor="white", lw=0.8, zorder=4 if PROPOSED in codes else 3)
            texts.append(ax.text(key[0], key[1], " = ".join(grp.method), fontsize=6.5,
                                 color="#0b0b0b" if PROPOSED in codes else "#52514e"))
        ax.axvline(0.9, color="#0b0b0b", lw=0.8)
        ax.set_xlabel("Upper-tail alert recall:  P(set reaches the upper stratum | Y in it)")
        ax.set_ylabel("Upper-tail alert precision")
        adjust_text(texts, ax=ax, arrowprops=dict(arrowstyle="-", color="#c3c2b7", lw=0.5), expand=(1.2, 1.5))
        save(fig, "F10_tail_alerts")

    # ---------------------------------------------------------------- efficiency
    # fit times: recorded by the fitting run (results/raw/*.jsonl, one base record per dataset x seed)
    fit_dir = Path(os.environ.get("TSCP_FIT_DIR", TOP / "results" / "raw"))
    fr = pd.concat([pd.read_json(f, lines=True) for f in sorted(glob.glob(str(fit_dir / "*.jsonl")))],
                   ignore_index=True)
    fit_cols = [c for c in fr.columns if c.startswith("t_fit_")]
    ft = fr.drop_duplicates(["did", "seed"]).groupby("did")[fit_cols + ["n"]].mean()
    eff = {"fit_seconds_median": ft[fit_cols].median().to_dict(), "fit_seconds_max": ft[fit_cols].max().to_dict()}
    tpath = RES / "timing_methods.csv"
    tc = pd.read_csv(tpath).groupby("method").seconds.median() if tpath.exists() else pd.Series(dtype=float)
    tmax = pd.read_csv(tpath).groupby("method").seconds.max() if tpath.exists() else pd.Series(dtype=float)
    eff["calib_predict_seconds_median"] = tc.to_dict()
    STATS["efficiency"] = eff
    rows = []
    model_cost = {"SCP": ["point"], "NCP": ["point", "scale"], "CQR": ["quantile"], "MCP-yhat": ["point"],
                  "DCP-LS": ["point", "scale", "density_LS"], "HPD-split-LS": ["point", "scale", "density_LS"],
                  "DLS-M-LS": ["point", "scale", "density_LS"], "S-Res": ["point"], "S-Res-hull": ["point"],
                  "S-NCP": ["point", "scale"], "S-CQR": ["quantile"], "S-HPD-LS": ["point", "scale", "density_LS"],
                  "SDLC-LS": ["point", "scale", "density_LS"],
                  "SDLC-LS2": ["point", "scale", "density_LS2"], "SDLC-H": ["density_H"]}
    for m, parts in model_cost.items():
        fitt = sum(ft[f"t_fit_{p}"] for p in parts)
        if "quantile" in parts:
            fitt = fitt / len(CFG["alphas"])   # quantile fit time was summed over the 3 alphas
        rows.append({"method": NAME[m], "fit_s_median": float(fitt.median()), "fit_s_max": float(fitt.max()),
                     "calib_predict_s_median": float(tc.get(m, np.nan)),
                     "calib_predict_s_max": float(tmax.get(m, np.nan))})
    T9 = pd.DataFrame(rows)
    table(T9, "T9_computational_cost", 3)

    # ---------------------------------------------------------------- error analysis
    sd = pdm[pdm.method == PROPOSED].merge(dsum, on=["did", "dataset"])
    ncp = pdm[pdm.method == "S-NCP"].set_index("did").nsize
    dlm = pdm[pdm.method == "DLS-M-LS"].set_index("did").nsize
    sd["size_ratio_vs_SNCP"] = sd.did.map(lambda d: sd.set_index("did").nsize[d] / ncp[d])
    sd["price_vs_DLS"] = sd.did.map(lambda d: sd.set_index("did").nsize[d] / dlm[d])
    # per-stratum calibration counts (expected): n_cal * stratum mass
    ea = sd[["dataset", "n", "n_cal", "skew_y", "rmse_over_sd", "worst_stratum", "tail_lo", "tail_hi",
             "nsize", "size_ratio_vs_SNCP", "price_vs_DLS", "components"]].sort_values("price_vs_DLS")
    table(ea, "T10_error_analysis_per_dataset")
    rho1 = stats.spearmanr(sd.price_vs_DLS, sd.rmse_over_sd)
    rho2 = stats.spearmanr(sd.worst_stratum, sd.n_cal)
    rho3 = stats.spearmanr(sd.price_vs_DLS, sd.skew_y.abs())
    STATS["error_analysis"] = {"spearman_price_vs_rmse_over_sd": [float(rho1.statistic), float(rho1.pvalue)],
                               "spearman_worst_stratum_vs_ncal": [float(rho2.statistic), float(rho2.pvalue)],
                               "spearman_price_vs_abs_skew": [float(rho3.statistic), float(rho3.pvalue)]}
    fig, axs = plt.subplots(1, 2, figsize=(7.2, 3.0))
    axs[0].scatter(sd.rmse_over_sd, sd.price_vs_DLS, color=BLUE, s=16, zorder=3)
    axs[0].set_yscale("log")
    from matplotlib.ticker import FixedLocator, NullFormatter, ScalarFormatter
    axs[0].yaxis.set_major_locator(FixedLocator([1, 1.5, 2, 4, 8]))
    axs[0].yaxis.set_major_formatter(ScalarFormatter())
    axs[0].yaxis.set_minor_formatter(NullFormatter())
    tx = [axs[0].text(r_.rmse_over_sd, r_.price_vs_DLS, r_.dataset, fontsize=6, color="#52514e")
          for _, r_ in sd[sd.price_vs_DLS > 1.4].iterrows()]
    adjust_text(tx, ax=axs[0], arrowprops=dict(arrowstyle="-", color="#c3c2b7", lw=0.5))
    axs[0].axhline(1.0, color="#0b0b0b", lw=0.8)
    axs[0].set_xlabel("Test RMSE / sd(y)")
    axs[0].set_ylabel("Size ratio SDLC / DLS (log scale)")
    if "null_worst_mean" in sd:
        dev_ = sd.worst_stratum - sd.null_worst_mean
        band = sd.null_worst_q05 - sd.null_worst_mean
        o = np.argsort(sd.n_cal.values)
        axs[1].fill_between(sd.n_cal.values[o], band.values[o], 0, color="#e6e5e0", lw=0, label="null 5% band")
        axs[1].scatter(sd.n_cal, dev_, color=BLUE, s=16, zorder=3, label="SDLC")
        axs[1].axhline(0, color="#0b0b0b", lw=0.8)
        axs[1].set_ylabel("Worst-stratum coverage minus null mean")
        axs[1].legend(frameon=False, fontsize=7, loc="lower right")
    axs[1].set_xscale("log")
    axs[1].set_xlabel("Calibration-set size")
    save(fig, "F8_error_analysis")

    # ---------------------------------------------------------------- per-dataset supplementary table
    sup = pdm[pdm.method.isin(MAIN)].copy()
    sup["method"] = sup.method.map(NAME)
    table(sup[["dataset", "method", "coverage", "worst_stratum", "tail_lo", "tail_hi", "nsize", "components",
               "wsc"]].sort_values(["dataset", "method"]), "S1_per_dataset_results")

    json.dump(METRICS, open(RES / "metrics.json", "w"), indent=1, default=float)
    json.dump(STATS, open(RES / "statistics.json", "w"), indent=1, default=float)
    print(f"datasets={n_ds} seeds={n_seed} runs={METRICS['n_runs']}")
    print(T2[["method", "coverage", "lower_tail_cov", "upper_tail_cov", "worst_stratum", "nsize_median",
              "components", "wsc"]].round(3).to_string(index=False))
    print(T4.round(3).to_string(index=False))


if __name__ == "__main__":
    main()

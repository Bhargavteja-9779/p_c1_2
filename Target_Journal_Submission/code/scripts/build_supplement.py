"""Build the Supplementary Material (manuscript/Supplementary_Material.docx and .pdf) from generated tables,
figures and result files. Numbering: Sections S1-S7, Tables S1-S20, Figures S1-S3 (cited in the main text).
No number is typed by hand."""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TOP = ROOT.parent
MS, BUILD = TOP / "manuscript", TOP / "manuscript" / "build"
TAB, RES, FIG = TOP / "tables", TOP / "results", TOP / "figures"
sys.path.insert(0, str(ROOT))


def md(df, nd=3):
    df = df.copy()
    for c in df.columns:
        if pd.api.types.is_float_dtype(df[c]):
            df[c] = df[c].map(lambda v: "" if pd.isna(v) else f"{v:.{nd}f}")
    return df.to_markdown(index=False, disable_numparse=True)


def csv(name, **kw):
    return pd.read_csv(TAB / f"{name}.csv", dtype=str, keep_default_na=False, **kw)


def main():
    from src.data.openml_ctr23 import load
    CFG = json.loads((ROOT / "config" / "benchmark.json").read_text())
    CC = json.loads((ROOT / "config" / "confirmatory.json").read_text())
    M = json.loads((RES / "metrics_v3.json").read_text())
    out = ["---", 'title: "Supplementary Material: Covering the rare outcomes: stratified conformal prediction with '
           'size-optimal density scores for imbalanced regression"', "---", ""]
    # S1 datasets ---------------------------------------------------------------------------------------
    out += ["# S1. Datasets", "",
            "**Table S1.** The OpenML-CTR23 datasets used in the main benchmark: size, number of features after "
            "one-hot encoding, skewness and number of distinct values of the target, realised number of calibration "
            "strata $K$, realised training mass of the lowest and highest stratum (nominal 0.10), relative test RMSE "
            "of the point model, and licence as recorded by OpenML.", ""]
    d1 = csv("D1_datasets")
    lic = {}
    for did in CFG["datasets"]:
        m = load(did)[2]
        lic[m["name"].replace("_", " ")] = m.get("licence", "") or "not stated"
    d1["Licence"] = d1.Dataset.map(lambda n: lic.get(n, ""))
    out += [d1.to_markdown(index=False, disable_numparse=True), ""]
    rows = []
    for did in CC["datasets"]:
        X, y, m = load(did)
        rows.append({"OpenML ID": str(did), "Dataset": m["name"], "n (used)": f"{len(y):,}", "p": str(X.shape[1]),
                     "Distinct y": f"{len(set(y.tolist())):,}", "Licence": m.get("licence", "") or "not stated"})
    out += ["**Table S2.** Held-out datasets of the confirmatory replication (regression datasets of OpenML suites "
            "335/336 without source overlap with CTR23; datasets above 50,000 rows subsampled once with seed 2026). "
            "Excluded by content overlap: " + "; ".join(CC["excluded_by_content_overlap_with_CTR23"]) +
            ". Excluded by the distinct-value rule: " + "; ".join(CC["excluded_by_rule_after_download"]) + ".", "",
            pd.DataFrame(rows).to_markdown(index=False, disable_numparse=True), ""]
    # S2 leakage ---------------------------------------------------------------------------------------
    la = pd.read_csv(TAB / "S2_leakage_audit.csv")
    la = la[["dataset", "n", "dup_rows_frac", "dup_X_frac", "test_X_in_train_frac_seed0", "missing_frac"]]
    la.columns = ["Dataset", "n", "Duplicate rows", "Duplicate feature vectors", "Test feature vectors seen in training (seed 0)",
                  "Missing values"]
    out += ["# S2. Leakage audit", "",
            "Exact duplicate rows (features and target), duplicate feature vectors, the share of test feature vectors "
            "that also occur in the training split (seed 0), and the share of missing values, recomputed on the final "
            "data files (scripts/leakage_audit.py). Random splitting keeps rows exchangeable, so the coverage guarantees "
            "hold for new rows from the same pool; repeated units (duplicates, repeated videos, repeat sales) mean "
            "that they do not transfer to new units.", "", "**Table S3.** Leakage audit (sorted by the share of test "
            "feature vectors seen in training).", "", md(la, 4), ""]
    # S3 implementation checks -----------------------------------------------------------------------------
    G = pd.DataFrame(json.loads((RES / "grid_convergence.json").read_text()))
    G = G[["did", "core", "tail", "mean_size", "rel_size_diff_vs_finest", "max_rel_size_diff_per_point",
           "q99_rel_size_diff_per_point", "frac_points_pieces_differ", "empty_mismatch"]]
    G.columns = ["OpenML ID", "Core points", "Tail points", "Mean size", "Rel. diff. of mean size", "Max rel. diff. per point",
                 "99% quantile rel. diff.", "Share with different piece count", "Empty-set mismatches"]
    out += ["# S3. Implementation checks", "",
            "*Exactness of scores.* Calibration and test scores are evaluated exactly at the observed target, so the "
            "coverage reported for every location–scale method is that of the exact rule (4) of the main text.", "",
            "*Set geometry.* Sizes, piece counts, hulls and alerts are those of the stratum-exact set for the "
            "piecewise-linear interpolant of $\\hat g$ on a standardised grid (1,536 core and 2×256 tail points by "
            "default). The production algorithm decomposes the interpolant into monotone runs, on each of which a "
            "super-level set is an interval. It reproduces a cell-by-cell reference implementation to a relative size "
            "difference below $10^{-14}$, with identical piece counts, hulls, alerts and coverage (unit test "
            "`tests/test_ls_exact3.py`). Table S4 compares three grid resolutions with the finest one.", "",
            "**Table S4.** Grid convergence of SDLC sets (seed 0, $\\alpha=0.1$).", "", md(G, 5), "",
            "*Finite-sample validity.* A Monte Carlo test with known exchangeable data (`tests/test_ls_exact3.py`) "
            "confirms that the empirical stratum-wise coverage matches the theoretical value "
            "$\\lceil (n_k+1)(1-\\alpha)\\rceil/(n_k+1)$.", ""]
    # S4 additional results ----------------------------------------------------------------------------------
    out += ["# S4. Additional results", "",
            "**Table S5.** Sensitivity of the set-size comparisons among stratified methods (geometric-mean ratio "
            "of SDLC to each comparator with 95% bootstrap CI, wins/losses of SDLC, Holm-adjusted two-sided Wilcoxon "
            "$p$ within each analysis). Development datasets: airfoil, concrete, QSAR fish; diagnostic datasets: "
            "cpu activity, naval propulsion, cars, energy efficiency, forest fires, fifa, Miami housing.", "",
            csv("D3s_sensitivity").to_markdown(index=False, disable_numparse=True), "",
            "**Table S6.** Miscoverage level: marginal coverage, worst-stratum coverage, upper-tail coverage and "
            "geometric-mean size (means over datasets).", "", csv("D5_alpha").to_markdown(index=False, disable_numparse=True), "",
            "**Table S7.** Strata: three (S3), five (S5) and ten (S10, deciles) strata from training quantiles; "
            "worst-stratum and worst-decile coverage, geometric-mean size and number of runs with an infinite "
            "stratum threshold.", "", csv("D6_strata").to_markdown(index=False, disable_numparse=True), "",
            "**Table S8.** Calibration-set size (fraction of the calibration split used; runs with an infinite "
            "threshold refer to the stratified methods).", "", csv("D7_calsize").to_markdown(index=False, disable_numparse=True), "",
            "**Table S9.** Density estimators and variants ($\\alpha=0.1$).", "",
            csv("D2b_variants").to_markdown(index=False, disable_numparse=True), "",
            "**Table S10.** Synthetic study: coverage of the upper stratum under a genuine label shift (test points "
            "drawn with acceptance probability proportional to $\\exp\\{\\gamma\\Phi^{-1}(F_Y(y))\\}$, so that $X\\mid Y$ "
            "is unchanged); designs A and B, 10 seeds.", "",
            csv("D12_synthetic_shift").to_markdown(index=False, disable_numparse=True), "",
            "**Table S11.** Per-dataset error analysis for SDLC ($\\alpha=0.1$): calibration size, target skewness, "
            "share of zero targets, relative RMSE, worst-stratum coverage, size, and size ratios to DLS (price), "
            "S-NCP and BCCP.", "", csv("D10_error").to_markdown(index=False, disable_numparse=True), ""]
    T13 = pd.read_csv(TAB / "T13_tail_alerts.csv")
    lo = T13[T13.side == "lo"].drop(columns=["side"])
    out += ["**Table S12.** Lower-tail alerts (means over datasets).", "", md(lo), ""]
    t15 = TAB / "T15_timing_methods.csv"
    if t15.exists():
        tm = pd.read_csv(t15)
        tm.columns = ["Method", "Median µs per test point", "Maximum over datasets"]
        out += ["**Table S13.** Calibration and prediction time per test point (median over datasets of the "
                "per-dataset median of three repetitions after a discarded warm-up; one thread).", "", md(tm, 1), ""]
    tfit = TAB / "T15b_timing_fit.csv"
    if tfit.exists():
        tf = pd.read_csv(tfit)
        out += ["**Table S15.** Fitting and prediction time of the model components in seconds (seed 0, one CPU "
                "thread; `experiments/timing_fit.py`). SDLC uses the mean model, the scale model with out-of-fold "
                "residuals, the cross-fitted scale models and the kernel density.", "", md(tf, 3), ""]
    t18 = TAB / "T18_secondary.csv"
    if t18.exists():
        s = pd.read_csv(t18)
        s17 = s[~s.analysis.str.startswith("subgroup")]
        out += ["**Table S17.** Pre-specified secondary analyses of the held-out replication (hull forms) and post hoc "
                "equivalence tests (±5% on the log-size scale, TOST with two one-sided Wilcoxon tests), on CTR23 and the "
                "held-out datasets (`scripts/analyze_secondary.py`).", "", md(s17, 3), ""]
        sk = pd.read_csv(TAB / "T18b_confirmatory_skewness.csv")
        out += ["**Table S18.** Held-out datasets: skewness and octile skewness of the training targets, and size "
                "comparisons of SDLC by skewness subgroup (post hoc, descriptive).", "", md(sk, 3), "",
                md(s[s.analysis.str.startswith("subgroup")], 3), ""]
    d17 = TAB / "D17_rw_ctr23.csv"
    if d17.exists():
        out += ["**Table S19.** Relevance-weighted study on the OpenML-CTR23 datasets ($\\alpha=0.1$, 10 seeds; means "
                "over datasets; columns as in the main-text table of the relevance-weighted study).", "",
                pd.read_csv(d17, dtype=str).to_markdown(index=False, disable_numparse=True), ""]
        t17 = TAB / "T17b_rw_tests.csv"
        out += ["**Table S20.** Pre-specified hypothesis tests of the relevance-weighted study (both collections).", "",
                md(pd.read_csv(t17), 4), ""]
    d16 = TAB / "D16_grouped.csv"
    if d16.exists():
        out += ["**Table S16.** Grouped versus random splits on datasets with repeated units ($\\alpha=0.1$, 5 seeds; "
                "size in units of the training-target standard deviation; random-split values from the same seeds of the "
                "main benchmark).", "", pd.read_csv(d16, dtype=str).to_markdown(index=False, disable_numparse=True), ""]
    for i, (f, cap) in enumerate((("F4_upper_tail_per_dataset.png", "Coverage of the upper calibration stratum per dataset ($\\alpha=0.1$)."),
                                  ("F8_error_analysis.png", "Error analysis. Left: price of stratum-wise validity (SDLC/DLS size ratio) "
                                   "against relative RMSE. Right: worst-stratum coverage of SDLC minus its null mean "
                                   "against calibration-set size, with the 5% null band."),
                                  ("F7_calibration_size.png", "Effect of the calibration-set size on worst-stratum coverage (left) "
                                   "and size (right).")), 1):
        out += [f"![**Fig. S{i}.** {cap}]({(FIG / f).as_posix()}){{width=100%}}", ""]
    # S5 earlier implementations ------------------------------------------------------------------------------
    v1 = json.loads((RES / "statistics_v1_preregistered.json").read_text())
    v2 = json.loads((TOP / "supplementary" / "v2_exact_insample_analysis" / "statistics.json").read_text())
    v3 = json.loads((RES / "statistics_v3.json").read_text())
    alias = {"S-SCP": "BCCP", "BCCP": "BCCP", "S-NCP": "S-NCP", "S-CQR": "S-CQR", "S-HPD": "S-HPD"}
    key2 = {"BCCP": "S-Res", "S-NCP": "S-NCP", "S-CQR": "S-CQR", "S-HPD": "S-HPD-LS"}
    rows = []
    for ver, S_ in (("v1 (marginal grid)", v1), ("v2 (exact, in-sample scale)", v2)):
        for t in S_["tests"]:
            if t.get("hypothesis") == "H3" and t.get("metric") == "log_size":
                comp = alias.get(t["comparison"].replace("SDLC vs ", ""))
                if comp is None:
                    continue
                geo = S_.get("sdlc_size_ratios", {}).get(key2[comp], {})
                rows.append({"Version": ver, "Comparison": f"SDLC vs {comp}",
                             "Median log size ratio": f"{t['median_diff']:+.3f}",
                             "Geometric-mean ratio": f"{geo['geo']:.3f}" if geo else "not computed",
                             "SDLC smaller on": f"{geo['n_smaller']}/{geo['n']}" if geo else "not computed",
                             "Holm p": "< 0.001" if t["p_holm"] < 0.001 else f"{t['p_holm']:.3f}"})
    for t in v3["tests"]:
        if t["family"] == "H3 size (primary)":
            rows.append({"Version": "final", "Comparison": t["comparison"], "Median log size ratio": f"{t['hl']:+.3f} (HL)",
                         "Geometric-mean ratio": f"{t['geo_ratio']:.3f}", "SDLC smaller on": f"{t['wins']}/{t['n']}",
                         "Holm p": "< 0.001" if t["p_holm"] < 0.001 else f"{t['p_holm']:.3f}"})
    out += ["# S5. Earlier implementations", "",
            "The first run (v1) evaluated all density-based sets on a fixed grid of 200 equal-mass cells of the "
            "marginal training-target distribution. The second (v2) used an exact implementation but standardised "
            "residuals with an in-sample scale model and used a density floor. Their complete analyses are archived "
            "in `supplementary/v1_preregistered_analysis/` and `supplementary/v2_exact_insample_analysis/`. The "
            "coverage results were the same in all versions. Table S14 shows how the size comparisons changed; this "
            "dependence on the implementation is why the comparisons on CTR23 are labelled exploratory and were "
            "replicated on held-out data (v1 reported medians of log ratios; v2 also geometric means; the final "
            "version reports the Hodges–Lehmann estimate).", "",
            "**Table S14.** Size comparisons of SDLC with the stratified comparators in the three implementations "
            "($\\alpha=0.1$, 31 datasets; negative log ratios favour SDLC).", "",
            pd.DataFrame(rows).to_markdown(index=False, disable_numparse=True), ""]
    # S6 pre-registration -------------------------------------------------------------------------------------
    pre = (TOP / "PREREGISTRATION_confirmatory.md").read_text().split("\n", 1)[1]
    pre = pre.replace("\n## ", "\n### ")
    out += ["# S6. Pre-registered analysis plan of the confirmatory replication", "",
            "Reproduced verbatim from `PREREGISTRATION_confirmatory.md`, committed to the public repository "
            "before any confirmatory evaluation.", "", pre]
    pre2 = (TOP / "PREREGISTRATION_relevance_weighted.md").read_text().split("\n", 1)[1].replace("\n## ", "\n### ")
    out += ["# S7. Pre-specified analysis plan of the relevance-weighted study", "",
            "Reproduced verbatim from `PREREGISTRATION_relevance_weighted.md`, committed to version control (commit "
            "`a9f31d2`) before RW-DLC was evaluated on any dataset.", "", pre2]
    text = "\n".join(out)
    BUILD.mkdir(parents=True, exist_ok=True)
    src = BUILD / "supplementary_filled.md"
    src.write_text(text)
    ref = BUILD / "reference.docx"
    subprocess.run(["pandoc", str(src), "-o", str(MS / "Supplementary_Material.docx"), f"--reference-doc={ref}",
                    "--resource-path", str(TOP)], check=True)
    from scripts.build_pdf import build
    build(src, MS / "Supplementary_Material.pdf", BUILD / "supplementary.html")
    print("written", MS / "Supplementary_Material.docx")


if __name__ == "__main__":
    main()

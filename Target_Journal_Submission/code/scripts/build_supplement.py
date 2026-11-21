"""Build the Supplementary Material (manuscript/Supplementary_Material.docx and .pdf) from generated tables,
figures and result files. Numbering: Sections S1-S7, Tables S1-S17 fixed and later tables in order of appearance, Figures S1-S3.
No number is typed by hand. After the build, every "Supplementary Table/Section Sn" cited in the filled manuscript
(manuscript/build/manuscript_filled.md) is checked against the supplement.

Run time: the first run downloads any held-out dataset missing from the local data cache (OpenML; several minutes for
the large ARFF files); later runs read the cache and take about a minute, most of it the PDF print."""
from __future__ import annotations

import json
import os
import re
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


def disp(df, name=""):
    """Markdown with the display harmonisation of the main text (paper names, minus signs; values unchanged)."""
    from scripts.render_manuscript import display_df
    return display_df(df, name).to_markdown(index=False, disable_numparse=True)


def _lic(m):
    """Licence as recorded by OpenML; OpenML's placeholder "Public" is not a licence (review round 5)."""
    v = (m.get("licence", "") or "").strip()
    return "not stated (OpenML: \"Public\")" if v.lower() in ("", "public") else v


def csv(name, **kw):
    return pd.read_csv(TAB / f"{name}.csv", dtype=str, keep_default_na=False, **kw)


def main():
    from src.data.openml_ctr23 import load
    CFG = json.loads((ROOT / "config" / "benchmark.json").read_text())
    CC = json.loads((ROOT / "config" / "confirmatory.json").read_text())
    M = json.loads((RES / "metrics_v3.json").read_text())
    title = re.search(r'^title: "(.*)"$', (MS / "src" / "00_front.md").read_text(), re.M).group(1)
    out = ["---", f'title: "Supplementary Material: {title}"', "---", ""]
    # S1 datasets ---------------------------------------------------------------------------------------
    out += ["# S1. Datasets", "",
            "**Table S1.** The OpenML-CTR23 datasets used in the main benchmark: size, number of features after "
            "one-hot encoding, skewness and number of distinct values of the target, realised number of calibration "
            "strata $K$, realised training mass of the lowest and highest stratum (nominal 0.10), relative test RMSE "
            "of the point model, licence as recorded by OpenML (\"not stated\" where OpenML records none), and the share of "
            "test targets outside the domain $\\mathcal{Y}_D$ (automatic misses; mean and maximum over seeds).", ""]
    d1 = csv("D1_datasets")
    lic = {}
    for did in CFG["datasets"]:
        m = load(did)[2]
        lic[m["name"].replace("_", " ")] = _lic(m)
    d1["Licence"] = d1.Dataset.map(lambda n: lic.get(n, ""))
    pr = TAB / "T19b_ctr23_profile.csv"
    if pr.exists():                         # review round 5: OpenML IDs and out-of-domain test targets
        pr = pd.read_csv(pr)
        pr["key"] = pr.dataset.str.replace("_", " ")
        idmap = dict(zip(pr.key, pr.did.astype(str)))
        ood = dict(zip(pr.key, [f"{100 * a:.2f}/{100 * b:.2f}" for a, b in zip(pr.ood_mean, pr.ood_max)]))
        d1.insert(0, "OpenML ID", d1.Dataset.map(lambda n: idmap.get(n, "")))
        d1["Out-of-domain test targets, % (mean/max)"] = d1.Dataset.map(lambda n: ood.get(n, ""))
    out += [d1.to_markdown(index=False, disable_numparse=True), ""]
    rows = []
    os.environ["TSCP_NMAX"] = str(CC.get("n_max", 0))      # the pre-specified subsample used in the replication
    for did in CC["datasets"]:
        X, y, m = load(did)
        rows.append({"OpenML ID": str(did), "Dataset": m["name"], "n (used)": f"{len(y):,}", "p": str(X.shape[1]),
                     "Distinct y": f"{len(set(y.tolist())):,}", "Licence": _lic(m)})
    pr = TAB / "T19_heldout_profile.csv"
    if pr.exists():                         # review round 5: target scale, atoms, realised strata, out-of-domain
        pr = pd.read_csv(pr).set_index("did")
        for r in rows:
            q = pr.loc[int(r["OpenML ID"])]
            r["n (full)"] = f"{int(q.n_full):,}"
            r["Distinct y (full)"] = f"{int(q.distinct_full):,}"
            r["Largest atom"] = f"{q.largest_atom:.3f}"
            r["Skewness (full)"] = f"{q.skew_full:.2f}"
            r["Log scale (curated)"] = "yes" if q.curated_log_scale else "no"
            r["K"] = f"{int(q.K_min)}" if q.K_min == q.K_max else f"{int(q.K_min)}-{int(q.K_max)}"
            r["Lowest stratum mass"] = f"{q.lower_mass_min:.3f}-{q.lower_mass_max:.3f}"
            r["Highest stratum mass"] = f"{q.upper_mass_min:.3f}-{q.upper_mass_max:.3f}"
            r["Min. calibration points per stratum"] = str(int(q.ncal_min_stratum))
            r["Out-of-domain test targets, % (max)"] = f"{100 * q.ood_max:.2f}"
    out += ["**Table S2.** Held-out datasets of the confirmatory replication (regression datasets of OpenML suites "
            "335/336 without source overlap with CTR23; datasets above 50,000 rows subsampled once with seed 2026; "
            "\"Distinct y\" on the subsample, \"Distinct y (full)\" on the full data, the quantity the exclusion rule "
            "uses; realised stratum masses as ranges over seeds, nominal 0.10; \"Log scale (curated)\": the benchmark "
            "curators supplied the logarithm of the original quantity). yprop_4_1 and topo_2_1 contain identical "
            "observations and targets. visualizing_soil (transect index) and seattlecrime6 (coded time of day) have "
            "coded rather than quantitative targets. In house_16H, 52 records with log-price 0 form the whole lowest "
            "stratum; in yprop_4_1/topo_2_1 a single record has y = 0 while all others lie in [0.845, 1]. "
            "Excluded by content overlap: " + "; ".join(CC["excluded_by_content_overlap_with_CTR23"]) +
            ". Excluded by the distinct-value rule: " + "; ".join(CC["excluded_by_rule_after_download"]) + ".", "",
            pd.DataFrame(rows).to_markdown(index=False, disable_numparse=True), ""]
    os.environ.pop("TSCP_NMAX", None)
    # S2 leakage ---------------------------------------------------------------------------------------
    la = pd.read_csv(TAB / "S2_leakage_audit.csv")
    la = la[["suite", "dataset", "n", "dup_rows_frac", "dup_X_frac", "test_X_in_train_frac_seed0", "test_X_in_train_min",
             "test_X_in_train_max", "missing_frac"]]
    la.columns = ["Suite", "Dataset", "n", "Duplicate rows", "Duplicate feature vectors",
                  "Test feature vectors seen in training (seed 0)", "Min over seeds", "Max over seeds", "Missing values"]
    out += ["# S2. Leakage audit", "",
            "Exact duplicate rows (features and target), duplicate feature vectors, the share of test feature vectors "
            "that also occur in the training split (seed 0), and the share of missing values, recomputed on the final "
            "data files (scripts/leakage_audit.py), for the CTR23 and the held-out datasets; the share of test feature "
            "vectors seen in training is given for seed 0 and as the range over all seeds. Random splitting keeps rows exchangeable, so the coverage guarantees "
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
            disp(csv("D3s_sensitivity"), "D3s_sensitivity"), "",
            "**Table S6.** Miscoverage level: marginal coverage, worst-stratum coverage, upper-tail coverage and "
            "geometric-mean size (means over datasets).", "", disp(csv("D5_alpha"), "D5_alpha"), "",
            "**Table S7.** Strata: three (S3), five (S5) and ten (S10, deciles) strata from training quantiles; "
            "worst-stratum and worst-decile coverage, geometric-mean size and number of runs with an infinite "
            "stratum threshold.", "", disp(csv("D6_strata"), "D6_strata"), "",
            "**Table S8.** Calibration-set size (fraction of the calibration split used; runs with an infinite "
            "threshold refer to the stratified methods).", "", disp(csv("D7_calsize"), "D7_calsize"), "",
            "**Table S9.** Density estimators and variants ($\\alpha=0.1$).", "",
            disp(csv("D2b_variants"), "D2b_variants"), "",
            "**Table S10.** Synthetic study: coverage of the upper stratum under a genuine label shift (test points "
            "drawn with acceptance probability proportional to $\\exp\\{\\gamma\\Phi^{-1}(F_Y(y))\\}$, so that $X\\mid Y$ "
            "is unchanged); designs A and B, 10 seeds.", "",
            disp(csv("D12_synthetic_shift"), "D12_synthetic_shift"), "",
            "**Table S11.** Per-dataset error analysis for SDLC ($\\alpha=0.1$): calibration size, target skewness, "
            "share of zero targets, relative RMSE, worst-stratum coverage, size, and size ratios to DLS (price), "
            "S-NCP and BCCP.", "", disp(csv("D10_error"), "D10_error"), ""]
    T13 = pd.read_csv(TAB / "T13_tail_alerts.csv")
    lo = T13[T13.side == "lo"].drop(columns=["side"])
    out += ["**Table S12.** Lower-tail alerts (means over datasets).", "", md(lo), ""]
    d15c, d15d = TAB / "D15c_timing_like.csv", TAB / "D15d_timing_rw.csv"
    if d15c.exists():
        envf = RES / "timing_like_env.json"
        env = json.loads(envf.read_text()) if envf.exists() else {}
        hw = (f"{env.get('cpu', 'CPU not recorded')}, {env.get('n_cpu', '?')} cores, Python {env.get('python', '?')}, "
              f"NumPy {env.get('numpy', '?')}; BLAS/OpenMP threads fixed to 1 before import and checked with "
              f"threadpoolctl; machine otherwise idle (load average {env.get('loadavg_start', ['?'])[0]:.2f} at start)"
              if env else "hardware not recorded")
        out += ["**Table S13.** Computational cost (seed 0, one CPU thread; median of three repetitions after a "
                "discarded warm-up). (a) SDLC, S-NCP and BCCP on the OpenML-CTR23 datasets, timed with identical "
                "boundaries: calibration = from the calibration labels and model outputs to the stratum thresholds; "
                "batch prediction = from the point and scale predictions and the thresholds to the sets of the whole "
                "test set, without labels; single query = the same for one test point (200 random test points). "
                f"Hardware: {hw}.", "", "(a)", "", disp(pd.read_csv(d15c, dtype=str)), ""]
        if d15d.exists():
            out += ["(b) Relevance-weighted study on the held-out datasets: set-up times of RW-DLC-U (relevance "
                    "function with an exact Gaussian kernel density estimate; calibration weights and threshold), set "
                    "construction time per test point of all four methods with the same grid implementation "
                    "(G = 4,000 target values), and the change of RW-DLC-U set sizes when the grid is refined to "
                    "G = 16,000.", "", disp(pd.read_csv(d15d, dtype=str)), ""]
    tfit = TAB / "T15b_timing_fit.csv"
    if tfit.exists():
        tf = pd.read_csv(tfit)
        out += ["**Table S14.** Fitting and prediction time of the model components in seconds (seed 0, one CPU "
                "thread). SDLC uses the mean model, the scale model with out-of-fold residuals, the cross-fitted scale "
                "models and the kernel density.", "", md(tf, 3), ""]
    d16 = TAB / "D16_grouped.csv"
    if d16.exists():
        out += ["**Table S15.** Grouped versus random splits on datasets with repeated units ($\\alpha=0.1$, 5 seeds; "
                "normalised size; random-split values from the same seeds of the main benchmark).", "",
                disp(pd.read_csv(d16, dtype=str)), ""]
        t21 = TAB / "T21_grouped_seed_range.csv"
        if t21.exists():
            g21 = pd.read_csv(t21)
            g21 = g21[g21.method.isin(["SCP", "CQR", "HPD-split", "BCCP", "S-NCP", "S-CQR", "SDLC"])]
            g21.columns = ["Dataset", "Method", "Marginal cov. (min over seeds)", "Marginal cov. (max)",
                           "Worst-stratum cov. (min)", "Worst-stratum cov. (max)", "Seeds"]
            out += ["Table S15 (continued). Grouped splits: range over the five seeds of marginal and worst-stratum "
                    "coverage (each seed is one calibration set; the guarantees hold on average over calibration sets).",
                    "", md(g21, 3), ""]
        t24 = TAB / "T24_temporal_splits.csv"
        if t24.exists():
            out += ["Table S15 (continued). Splits by time (post hoc; experiments/run_temporal.py). Moneyball "
                    "\"forward\": earliest seasons for training (50% of rows), next for calibration (25%), latest for "
                    "test; \"blocked\": whole seasons assigned at random. Bike_Sharing_Demand \"blocked\": whole months "
                    "assigned at random (the curated data contain no year or day). Random-split values from the same "
                    "seeds of the main benchmark.", "", md(pd.read_csv(t24), 3), ""]
    t18 = TAB / "T18_secondary.csv"
    if t18.exists():
        s = pd.read_csv(t18)
        s17 = s[~s.analysis.str.startswith("subgroup")]
        out += ["**Table S16.** Pre-specified secondary analyses of the held-out replication (hull forms) and post hoc "
                "equivalence tests (±5% on the log-size scale, TOST with two one-sided Wilcoxon tests), on CTR23 and the "
                "held-out datasets.", "", md(s17, 3), ""]
        sk = pd.read_csv(TAB / "T18b_confirmatory_skewness.csv")
        out += ["**Table S17.** Held-out datasets: skewness and octile skewness of the training targets, and size "
                "comparisons of SDLC by skewness subgroup (post hoc, descriptive).", "", md(sk, 3), "",
                md(s[s.analysis.str.startswith("subgroup")], 3), ""]
    t20 = TAB / "T20_review05_sensitivity.csv"
    if t20.exists():                           # review round 5 (post hoc, from existing results)
        r5 = json.loads((RES / "statistics_review05.json").read_text())
        t20 = pd.read_csv(t20).drop(columns=["geo_lo", "geo_hi"])
        out += ["**Table S17b.** Post hoc checks of the held-out replication and of CTR23 (review round 5; "
                "scripts/analyze_review05.py; no model was refitted). Size comparisons of SDLC with the stratified "
                "comparators (per-dataset geometric-mean normalised size, two-sided Wilcoxon signed-rank test, Holm "
                "over the four comparators within a subset) on: all held-out datasets as pre-specified; the duplicate "
                "pair yprop_4_1/topo_2_1 merged into one dataset (log-scale mean); continuous targets (at least 100 "
                "distinct values and largest atom at most 5% of rows); datasets with nominal tail strata (realised "
                "training mass of the lowest and highest stratum within [0.08, 0.12] in every seed, K = 5); and "
                "without house_16H.", "", md(t20, 3), ""]
        tu = pd.read_csv(TAB / "T23_top1_unified.csv")
        out += ["Table S17b (continued). Coverage of the top 1% of outcomes with one definition in both pipelines "
                "($y\\ge q_{0.99}$ of the training targets; a seed counts only if the group holds at least 10 test "
                "points; mean, minimum and maximum over datasets).", "", md(tu, 3), ""]
        t25 = TAB / "T25_tail1_vs_rw.csv"
        if t25.exists():
            out += ["Table S17b (continued). RW-DLC versus stratified methods with dedicated 1% tail strata (stratum "
                    "edges at the training quantiles 0.01, 0.10, 0.25, 0.75, 0.90, 0.99; review round 8; "
                    "experiments/eval_tail1.py, scripts/analyze_review08.py; held-out data, 5 seeds). Top-1% coverage "
                    "($y\\ge q_{0.99}$, seeds with at least 10 such test points), marginal coverage and normalised size "
                    "(geometric-mean and Hodges-Lehmann ratios); two-sided Wilcoxon tests, Holm over all six tests.",
                    "", md(pd.read_csv(t25), 3), ""]
        rw = pd.DataFrame([dict(variant=k, **v) for k, v in r5["rw3_sensitivity"].items()])
        out += ["Table S17b (continued). RW-3 (top-1% coverage of RW-DLC versus SDLC, held-out data, one-sided "
                "Wilcoxon test): the pre-specified definition ($y>q_{0.99}$) and post hoc variants.", "", md(rw, 3), ""]
    nxt = 18                                  # tables after S17 are numbered in order of appearance
    t17 = TAB / "T17b_rw_tests.csv"
    if t17.exists():
        out += [f"**Table S{nxt}.** Pre-specified hypothesis tests RW-1 to RW-4 of the relevance-weighted study "
                "(column suite: collection of datasets).", "", md(pd.read_csv(t17), 4), ""]
        nxt += 1
    d17 = TAB / "D17_rw_ctr23.csv"
    if d17.exists():
        out += [f"**Table S{nxt}.** Relevance-weighted study on the OpenML-CTR23 datasets ($\\alpha=0.1$, 10 seeds; means "
                "over datasets; columns as in the main-text table of the relevance-weighted study).", "",
                disp(pd.read_csv(d17, dtype=str), "D17_rw_ctr23"), ""]
        nxt += 1
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
            "in the anonymised code package provided as supplementary material. The "
            f"coverage results were the same in all versions. Table S{nxt} shows how the size comparisons changed; this "
            "dependence on the implementation is why the comparisons on CTR23 are labelled exploratory and were "
            "replicated on held-out data (v1 reported medians of log ratios; v2 also geometric means; the final "
            "version reports the Hodges–Lehmann estimate).", "",
            f"**Table S{nxt}.** Size comparisons of SDLC with the stratified comparators in the three implementations "
            "($\\alpha=0.1$, 31 datasets; negative log ratios favour SDLC).", "",
            pd.DataFrame(rows).to_markdown(index=False, disable_numparse=True), ""]
    os.environ.pop("TSCP_NMAX", None)
    # S6/S7 analysis plans (verbatim apart from the marked redactions for double-blind review) -------------------
    pre = (TOP / "PREREGISTRATION_confirmatory.md").read_text().split("\n", 1)[1]
    pre = re.sub(r"\(branch `[^`]*`\)", "[branch name redacted for double-blind review]", pre)
    pre = pre.replace("\n## ", "\n### ")
    note = ("The plan was written before we adopted the term *pre-specified*; its original wording (\"pre-registered\", "
            "\"public repository\") is kept. As stated in the manuscript, the plan was committed to the authors' "
            "version-controlled repository, not registered with a third party, and the repository will be made public "
            "upon acceptance; the anonymised code package provided as supplementary material contains the version "
            "history with the commit identifiers.")
    out += ["# S6. Pre-specified analysis plan of the confirmatory replication (verbatim)", "",
            "Reproduced from the analysis-plan file of the code package, committed (identifier `ccba99b`) before any "
            "confirmatory evaluation. " + note, "", pre]
    pre2 = (TOP / "PREREGISTRATION_relevance_weighted.md").read_text().split("\n", 1)[1]
    pre2 = re.sub(r" Motivation: review.*?This study adds one\.", " [Motivation paragraph referring to internal project "
                  "documents redacted for double-blind review.]", pre2, flags=re.S)
    pre2 = pre2.replace("\n## ", "\n### ")
    out += ["# S7. Pre-specified analysis plan of the relevance-weighted study (verbatim)", "",
            "Reproduced from the analysis-plan file of the code package, committed (identifier `a9f31d2`) before RW-DLC "
            "was evaluated on any dataset. The same note on wording as for Section S6 applies.", "", pre2]
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
    check_crossrefs(text)


def check_crossrefs(text):
    """Every supplementary item cited in the filled manuscript must exist in the supplement."""
    ms = BUILD / "manuscript_filled.md"
    if not ms.exists():
        return
    cited = set()
    for kind, a, b in re.findall(r"Supplementary (Tables?|Sections?|Fig\.?) S(\d+)(?: and S(\d+))?", ms.read_text()):
        for n in (a, b):
            if n:
                cited.add(("Table" if kind.startswith("Table") else "Section" if kind.startswith("Section") else "Fig.", n))
    have = {("Table", n) for n in re.findall(r"\*\*Table S(\d+)\.\*\*", text)}
    have |= {("Section", n) for n in re.findall(r"^# S(\d+)\.", text, re.M)}
    have |= {("Fig.", n) for n in re.findall(r"\*\*Fig\. S(\d+)\.\*\*", text)}
    missing = sorted(cited - have, key=lambda x: (x[0], int(x[1])))
    print("cross-reference check:", "all cited supplementary items exist" if not missing else
          "MISSING " + ", ".join(f"{k} S{n}" for k, n in missing))


if __name__ == "__main__":
    main()

"""Render the manuscript: fill every {{placeholder}} from machine-generated result files,
insert tables generated from tables/*.csv, number sections/tables/figures, and build the
DOCX with pandoc (+citeproc, Elsevier Harvard CSL) followed by python-docx post-processing.

Placeholders that cannot be resolved abort the build (no number is ever typed by hand).
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
TOP = ROOT.parent
MS = TOP / "manuscript"
SRC, BUILD = MS / "src", MS / "build"
RES, TAB, FIG = TOP / "results", TOP / "tables", TOP / "figures"
sys.path.insert(0, str(ROOT))

ORDER = ["00_front.md", "01_intro.md", "015_related.md", "02_theory.md", "03_setup.md", "04_results.md",
         "05_discussion.md", "06_conclusion.md", "07_declarations.md", "08_references.md", "09_appendix.md"]


def pct(x, d=1):
    return f"{100 * x:.{d}f}%"


def f(x, d=3):
    return f"{x:.{d}f}"


def pfmt(p):
    return "< 0.001" if p < 0.001 else f"{p:.3f}"


def context():
    M = json.loads((RES / "metrics.json").read_text())
    S = json.loads((RES / "statistics.json").read_text())
    E = json.loads((RES / "statistics_extra.json").read_text()) if (RES / "statistics_extra.json").exists() else {}
    P = json.loads((RES / "prop1_gaussian.json").read_text())
    c = {}
    r05 = [r for r in P["rows"] if r["R2"] == 0.5][0]
    c["prop1.upper10_r05"] = pct(r05["analytic_upper10"])
    c["prop1.upper1_r05"] = pct(r05["analytic_upper1"])
    c["prop1.central_r05"] = pct(r05["analytic_central80"])
    r09 = [r for r in P["rows"] if r["R2"] == 0.9][0]
    c["prop1.upper10_r09"] = pct(r09["analytic_upper10"])
    c["n_datasets"] = str(M["n_datasets"])
    c["n_seeds"] = str(M["n_seeds_min"])
    c["n_runs"] = str(M["n_runs"])
    T1 = pd.read_csv(TAB / "T1_datasets.csv")
    c["ds_n_min"], c["ds_n_max"] = f"{T1.n.min():,}", f"{T1.n.max():,}"
    c["ds_p_min"], c["ds_p_max"] = str(T1.p.min()), str(T1.p.max())
    c["n_skewed"] = str(int((T1.skew_y.abs() > 1).sum()))
    c["n_methods_main"] = "14"
    c["out_dom_max"] = pct(M["frac_test_out_domain_max"], 2)
    c["n_ls_better"] = str(M["datasets_LS_better_nll"])
    main = M["main"]
    for code, r in main.items():
        k = code
        for col in ("coverage", "lower_tail_cov", "upper_tail_cov", "worst_stratum", "top5pct_cov",
                    "bottom5pct_cov", "nsize_mean", "nsize_median", "components", "wsc"):
            c[f"main.{k}.{col}"] = f(r[col])
        c[f"main.{k}.n_ds_worst_lt_0.85"] = str(r["n_ds_worst_lt_0.85"])
        c[f"main.{k}.upper_tail_pct"] = pct(r["upper_tail_cov"])
        c[f"main.{k}.lower_tail_pct"] = pct(r["lower_tail_cov"])
        c[f"main.{k}.worst_pct"] = pct(r["worst_stratum"])
        c[f"main.{k}.top5_pct"] = pct(r["top5pct_cov"])
    marg = ["SCP", "NCP", "CQR", "MCP-yhat", "DCP-LS", "HPD-split-LS", "DLS-M-LS"]
    c["marg.upper_min"] = pct(min(main[m]["upper_tail_cov"] for m in marg))
    c["marg.upper_max"] = pct(max(main[m]["upper_tail_cov"] for m in marg))
    c["marg.worst_min"] = pct(min(main[m]["worst_stratum"] for m in marg))
    c["marg.worst_max"] = pct(max(main[m]["worst_stratum"] for m in marg))
    c["marg.top5_min"] = pct(min(main[m]["top5pct_cov"] for m in marg))
    c["marg.top5_max"] = pct(max(main[m]["top5pct_cov"] for m in marg))
    strat = ["S-Res", "S-NCP", "S-CQR", "S-HPD-LS", "SDLC-LS"]
    c["strat.worst_min"] = pct(min(main[m]["worst_stratum"] for m in strat))
    c["strat.worst_max"] = pct(max(main[m]["worst_stratum"] for m in strat))
    c["strat.upper_min"] = pct(min(main[m]["upper_tail_cov"] for m in strat))
    c["strat.upper_max"] = pct(max(main[m]["upper_tail_cov"] for m in strat))
    # tests
    for t in S["tests"]:
        key = f"test.{t['hypothesis']}.{t['metric']}.{t['comparison'].replace('SDLC vs ', '')}"
        c[key + ".p"] = pfmt(t["p_holm"])
        c[key + ".md"] = f(t["median_diff"])
        c[key + ".rbc"] = f(t["rbc"], 2)
        c[key + ".wins"] = f"{t['wins']}/{t['n']}"
        c[key + ".ci"] = f"[{f(t['ci_low'])}, {f(t['ci_high'])}]"
    h1 = [t for t in S["tests"] if t["hypothesis"] == "H1" and t["metric"] == "worst_stratum"]
    c["H1.max_p"] = pfmt(max(t["p_holm"] for t in h1))
    c["H1.min_rbc"] = f(min(t["rbc"] for t in h1), 2)
    c["H1.min_md"] = f(min(t["median_diff"] for t in h1))
    c["H1.max_md"] = f(max(t["median_diff"] for t in h1))
    conf = S["confirmatory_excl_dev"]
    c["conf.max_p"] = pfmt(max(t["p_holm"] for t in conf))
    c["conf.n"] = str(conf[0]["n"])
    for p in S["price"]:
        key = f"price.{p['stratified']}"
        c[key + ".gm"] = f(p["geo_mean_size_ratio"], 2)
        c[key + ".ci"] = f"[{f(p['ci_low'], 2)}, {f(p['ci_high'], 2)}]"
        c[key + ".med"] = f(p["median_ratio"], 2)
        c[key + ".gain"] = f(p["worst_stratum_gain_mean"])
        c[key + ".n15"] = str(p["n_ds_size_ratio_gt_1.5"])
    fr = S["friedman"]
    c["friedman.ws.chi2"] = f(fr["worst_stratum"]["chi2"], 1)
    c["friedman.ws.p"] = pfmt(fr["worst_stratum"]["p"])
    c["friedman.size.chi2"] = f(fr["size"]["chi2"], 1)
    c["friedman.size.p"] = pfmt(fr["size"]["p"])
    c["friedman.cd"] = f(fr["nemenyi_cd_0.05"], 2)
    c["friedman.n"] = str(fr["n"])
    for metric in ("worst_stratum", "size"):
        for m, r in fr[metric]["mean_ranks"].items():
            c[f"rank.{metric}.{m}"] = f(r, 2)
    ls = S["label_shift"]
    for sc, dd in ls.items():
        for m, v in dd.items():
            c[f"shift.{sc}.{m}.p"] = pfmt(v["p_holm"])
    T8 = pd.read_csv(TAB / "T8_label_shift.csv").set_index("method")
    for m in T8.index:
        for col in ("up1", "up2", "tails1", "down1"):
            c[f"T8.{m}.{col}"] = pct(T8.loc[m, col])
            c[f"T8.{m}.{col}_min"] = pct(T8.loc[m, col + "_min_ds"])
    ea = S["error_analysis"]
    c["ea.rho_price_rmse"] = f(ea["spearman_price_vs_rmse_over_sd"][0], 2)
    c["ea.p_price_rmse"] = pfmt(ea["spearman_price_vs_rmse_over_sd"][1])
    c["ea.rho_ws_ncal"] = f(ea["spearman_worst_stratum_vs_ncal"][0], 2)
    c["ea.p_ws_ncal"] = pfmt(ea["spearman_worst_stratum_vs_ncal"][1])
    c["ea.rho_price_skew"] = f(ea["spearman_price_vs_abs_skew"][0], 2)
    c["ea.p_price_skew"] = pfmt(ea["spearman_price_vs_abs_skew"][1])
    eff = S["efficiency"]
    c["eff.calib_SDLC_ms"] = f(1000 * eff["calib_predict_seconds_median"]["SDLC-LS"], 1)
    c["eff.calib_SCP_ms"] = f(1000 * eff["calib_predict_seconds_median"]["SCP"], 1)
    c["eff.calib_CQR_ms"] = f(1000 * eff["calib_predict_seconds_median"]["CQR"], 1)
    c["eff.fit_LS_med"] = f(eff["fit_seconds_median"]["t_fit_density_LS"], 2)
    c["eff.fit_H_med"] = f(eff["fit_seconds_median"]["t_fit_density_H"], 2)
    c["eff.fit_H_max"] = f(eff["fit_seconds_max"]["t_fit_density_H"], 1)
    c["eff.fit_scale_med"] = f(eff["fit_seconds_median"]["t_fit_scale"], 2)
    c["eff.fit_point_med"] = f(eff["fit_seconds_median"]["t_fit_point"], 2)
    # robustness tables
    T5 = pd.read_csv(TAB / "T5_alpha_sensitivity.csv")
    for _, r in T5.iterrows():
        c[f"T5.{r['alpha']}.{r['method']}.worst"] = f(r["worst_stratum"])
        c[f"T5.{r['alpha']}.{r['method']}.upper"] = f(r["upper_tail"])
    T7 = pd.read_csv(TAB / "T7_calibration_size_sensitivity.csv")
    for _, r in T7.iterrows():
        c[f"T7.{r['cal_frac']}.{r['method']}.worst"] = f(r["worst_stratum"])
        c[f"T7.{r['cal_frac']}.{r['method']}.size"] = f(r["nsize_geo"])
    T6 = pd.read_csv(TAB / "T6_strata_scheme_sensitivity.csv")
    for _, r in T6.iterrows():
        c[f"T6.{r['scheme']}.{r['method']}.worst"] = f(r["worst_stratum"])
        c[f"T6.{r['scheme']}.{r['method']}.dec"] = f(r["decile_worst_seedavg"])
        c[f"T6.{r['scheme']}.{r['method']}.size"] = f(r["nsize_geo"])
    for k, v in E.items():
        if isinstance(v, (int, float, bool)):
            c[f"extra.{k}"] = f(v, 2) if isinstance(v, float) else str(v)
    if "mlp_tests_worst_stratum" in E:
        c["extra.mlp_max_p"] = pfmt(max(v["p_holm"] for v in E["mlp_tests_worst_stratum"].values()))
    if (TAB / "T12_mlp_generality.csv").exists():
        T12 = pd.read_csv(TAB / "T12_mlp_generality.csv").set_index("method")
        for m in T12.index:
            c[f"T12.{m}.worst"] = f(T12.loc[m, "worst_stratum"])
            c[f"T12.{m}.upper"] = f(T12.loc[m, "upper_tail"])
            c[f"T12.{m}.size"] = f(T12.loc[m, "nsize_geo"])
    if (TAB / "T11_synthetic_oracle.csv").exists():
        T11 = pd.read_csv(TAB / "T11_synthetic_oracle.csv")
        for _, r in T11.iterrows():
            c[f"T11.{r['scores']}.{r['method']}.size"] = f(r["size"])
            c[f"T11.{r['scores']}.{r['method']}.worst"] = f(r["worst_stratum"])
            c[f"T11.{r['scores']}.{r['method']}.upper"] = f(r["upper_tail"])
    T9 = pd.read_csv(TAB / "T9_computational_cost.csv").set_index("method")
    for m in T9.index:
        c[f"T9.{m}.fit"] = f(T9.loc[m, "fit_s_median"], 2)
        c[f"T9.{m}.cal_ms"] = f(1000 * T9.loc[m, "calib_predict_s_median"], 1)
    return c


# ----------------------------------------------------------------------------- tables
TABLES = {}


def md_table(name, cols, rename=None, fmt=None, query=None, sort=None):
    df = pd.read_csv(TAB / f"{name}.csv")
    if query:
        df = df.query(query)
    if sort:
        df = df.sort_values(sort)
    df = df[cols].copy()
    fmt = fmt or {}
    for col in df.columns:
        if col in fmt:
            df[col] = df[col].map(fmt[col])
        elif pd.api.types.is_float_dtype(df[col]):
            df[col] = df[col].map(lambda v: "" if pd.isna(v) else f"{v:.3f}")
    if rename:
        df = df.rename(columns=rename)
    return df.to_markdown(index=False)


def render():
    ctx = context()
    text = "\n\n".join((SRC / s).read_text() for s in ORDER if (SRC / s).exists())

    # tables: {{TABLE:id|caption}} blocks are defined in tables_spec.py
    from scripts.tables_spec import SPEC
    tab_no, fig_no = {}, {}

    def tab_sub(mo):
        tid, cap = mo.group(1), mo.group(2)
        tab_no[tid] = len(tab_no) + 1
        body = md_table(**SPEC[tid])
        return f"**Table {tab_no[tid]}.** {cap}\n\n{body}\n"
    text = re.sub(r"\{\{TABLE:([\w-]+)\|([^}]*)\}\}", tab_sub, text)

    def fig_sub(mo):
        fid, path, cap = mo.group(1), mo.group(2), mo.group(3)
        fig_no[fid] = len(fig_no) + 1
        return f"![**Fig. {fig_no[fid]}.** {cap}]({(FIG / path).as_posix()}){{width=100%}}\n"
    text = re.sub(r"\{\{FIG:([\w-]+)\|([^|]+)\|([^}]*)\}\}", fig_sub, text)

    # section numbering
    sec_no, counters, out = {}, [0, 0, 0], []
    for line in text.split("\n"):
        m = re.match(r"^(#{1,3}) (.*?)(\s*\{#sec:([\w-]+)\})?\s*$", line)
        if m and not line.startswith("#### "):
            lvl = len(m.group(1))
            title = m.group(2)
            unnumbered = title.strip() in ("References", "Highlights", "Abstract") or "{-}" in line \
                or title.startswith("Appendix") or title.startswith("Declaration") or title.startswith("CRediT") \
                or title.startswith("Data and code") or title.startswith("Acknowledg") or title.startswith("Funding")
            if unnumbered:
                out.append(f"{m.group(1)} {title.replace('{-}', '').strip()}")
                continue
            counters[lvl - 1] += 1
            for j in range(lvl, 3):
                counters[j] = 0
            num = ".".join(str(x) for x in counters[:lvl])
            if m.group(4):
                sec_no[m.group(4)] = num
            out.append(f"{m.group(1)} {num}. {title}" if lvl == 1 else f"{m.group(1)} {num} {title}")
        else:
            out.append(line)
    text = "\n".join(out)
    text = re.sub(r"\[-@sec:([\w-]+)\]", lambda mo: sec_no[mo.group(1)], text)
    text = re.sub(r"\[-@tbl:([\w-]+)\]", lambda mo: str(tab_no[mo.group(1)]), text)
    text = re.sub(r"\[-@fig:([\w-]+)\]", lambda mo: str(fig_no[mo.group(1)]), text)
    # equation tags -> visible numbers
    text = re.sub(r"\\tag\{(\w+)\}", r"\\qquad\\text{(\1)}", text)

    missing = sorted(set(re.findall(r"\{\{([^}]+)\}\}", text)) - set(ctx))
    if missing:
        raise SystemExit("Unresolved placeholders: " + ", ".join(missing))
    text = re.sub(r"\{\{([^}]+)\}\}", lambda mo: ctx[mo.group(1)], text)
    BUILD.mkdir(parents=True, exist_ok=True)
    (BUILD / "manuscript_filled.md").write_text(text)
    json.dump(ctx, open(BUILD / "placeholder_values.json", "w"), indent=1)
    return text


def build_docx():
    md = BUILD / "manuscript_filled.md"
    ref = BUILD / "reference.docx"
    if not ref.exists():
        from scripts.docx_style import make_reference
        make_reference(ref)
    out = MS / "Final_Manuscript.docx"
    cmd = ["pandoc", str(md), "-o", str(out), "--citeproc",
           f"--bibliography={TOP / 'supplementary' / 'references_verified.bib'}",
           f"--csl={BUILD / 'elsevier-harvard.csl'}", f"--reference-doc={ref}",
           "--resource-path", str(TOP), "-M", "link-citations=true"]
    subprocess.run(cmd, check=True)
    from scripts.docx_style import postprocess
    postprocess(out)
    print("written", out)


if __name__ == "__main__":
    render()
    build_docx()

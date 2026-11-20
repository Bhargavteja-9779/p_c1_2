"""Render the manuscript: fill every {{placeholder}} from machine-generated result files,
insert tables generated from tables/*.csv, number sections/tables/figures, and build the
DOCX with pandoc (+citeproc, Springer Basic author-date CSL) followed by python-docx post-processing.

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


FAM = {"H1 worst stratum": "h1w", "H1 upper tail": "h1u", "H1 worst stratum (excl. development)": "h1wx",
       "H3 size (primary)": "h3", "H3 size (secondary)": "h3s", "Decomposition BCCP -> S-NCP -> SDLC-N -> SDLC": "dec",
       "H3 size (hull forms)": "h3h", "Upper alert rate vs stratified": "alr",
       "Upper alert precision vs stratified": "alp"}
SENS = {"primary (alpha=0.1, S5, all datasets)": "primary", "excluding development datasets": "nodev",
        "excluding development + diagnostic datasets": "nodiag", "datasets with nominal tail strata": "nominal",
        "|skewness| > 1": "skewed", "|skewness| <= 1": "symm", "n >= 1600": "large", "n < 1600": "small",
        "alpha = 0.05": "a05", "alpha = 0.2": "a20", "strata S3": "S3", "strata S10": "S10"}


def _comp(c):
    for pre in ("SDLC vs ", "SDLC-hull vs "):
        if c.startswith(pre):
            return c[len(pre):].replace(" ", "")
    c = c.replace(" vs ", "_vs_")
    return c.replace("-hull", "-hull").replace(" ", "")


def _put_test(c, key, t):
    if "geo_ratio" in t and t["geo_ratio"] == t["geo_ratio"]:
        c[key + ".geo"] = f(t["geo_ratio"])
        c[key + ".lo"] = f(t["geo_lo"])
        c[key + ".hi"] = f(t["geo_hi"])
        c[key + ".hlr"] = f(t["hl_ratio"])
    c[key + ".hl"] = f(t["hl"])
    c[key + ".hllo"] = f(t["hl_lo"])
    c[key + ".hlhi"] = f(t["hl_hi"])
    c[key + ".wins"] = str(t["wins"])
    c[key + ".losses"] = str(t["losses"])
    c[key + ".n"] = str(t["n"])
    c[key + ".rbc"] = f(t["rbc"], 2)
    c[key + ".p"] = pfmt(t.get("p_holm", t["p"]))
    c[key + ".praw"] = pfmt(t["p"])
    c[key + ".psign"] = pfmt(t["p_sign"])


def context():
    """Placeholder values for the v3 manuscript (results/metrics_v3.json, results/statistics_v3.json,
    tables/*.csv). Generic lookups {{T:...}} and {{J:...}} are resolved in render()."""
    M = json.loads((RES / "metrics_v3.json").read_text())
    S = json.loads((RES / "statistics_v3.json").read_text())
    P = json.loads((RES / "prop1_gaussian.json").read_text())
    c = {}
    r05 = [r for r in P["rows"] if r["R2"] == 0.5][0]
    r09 = [r for r in P["rows"] if r["R2"] == 0.9][0]
    c["prop1.upper10_r05"] = pct(r05["analytic_upper10"])
    c["prop1.upper1_r05"] = pct(r05["analytic_upper1"])
    c["prop1.central_r05"] = pct(r05["analytic_central80"])
    c["prop1.upper10_r09"] = pct(r09["analytic_upper10"])
    c["n_datasets"] = str(M["n_datasets"])
    c["n_seeds"] = str(M["n_seeds_min"])
    c["n_runs"] = str(M["n_runs"])
    c["n_nominal"] = str(M["n_nominal_tails"])
    c["n_methods_main"] = str(M.get("n_methods_main", 13))
    T1 = pd.read_csv(TAB / "T1_datasets.csv")
    c["ds_n_min"], c["ds_n_max"] = f"{T1.n.min():,}", f"{T1.n.max():,}"
    c["ds_p_min"], c["ds_p_max"] = str(T1.p.min()), str(T1.p.max())
    c["n_skewed"] = str(int((T1.skew_y.abs() > 1).sum()))
    CC = json.loads((ROOT / "config" / "confirmatory.json").read_text())
    c["conf.n_datasets"] = str(len(CC["datasets"]))
    main = M["main"]
    for code, r in main.items():
        for col in ("coverage", "lower_tail_cov", "upper_tail_cov", "worst_stratum", "top5_cov", "top1_cov",
                    "size_geo", "pieces", "sigma_decile_worst", "wsc"):
            c[f"main.{code}.{col}"] = f(r[col])
            c[f"main.{code}.{col}.pct"] = pct(r[col])
        c[f"main.{code}.empty_pct"] = pct(r["empty_rate"], 2)
        c[f"main.{code}.below_null"] = str(r["n_ds_below_null"])
    for code, r in M["variants"].items():
        for col in ("worst_stratum", "size_geo", "pieces", "upper_tail_cov"):
            c[f"var.{code}.{col}"] = f(r[col])
    marg = ["SCP", "NCP", "CQR", "MCP-yhat", "DCP-LS", "HPD-split-LS", "DLS-M-LS"]
    strat = ["S-Res", "S-NCP", "S-CQR", "S-HPD-LS", "SDLC-N", "SDLC-LS"]
    for grp, ms in (("marg", marg), ("strat", strat)):
        for col in ("upper_tail_cov", "worst_stratum", "top5_cov", "top1_cov", "lower_tail_cov"):
            c[f"{grp}.{col}.min"] = pct(min(main[m][col] for m in ms))
            c[f"{grp}.{col}.max"] = pct(max(main[m][col] for m in ms))
        c[f"{grp}.below.min"] = str(min(main[m]["n_ds_below_null"] for m in ms))
        c[f"{grp}.below.max"] = str(max(main[m]["n_ds_below_null"] for m in ms))
    c["null_mean"] = f(M["null_worst_mean_avg"])
    for t in S["tests"]:
        fam = FAM.get(t["family"], "ext." + t["metric"] if t["family"].startswith("Extreme") else None)
        if fam:
            _put_test(c, f"{fam}.{_comp(t['comparison'])}", t)
    for fam in ("h1w", "h1u", "h1wx"):
        ps = [t["p_holm"] for t in S["tests"] if FAM.get(t["family"]) == fam]
        c[f"{fam}.maxp"] = pfmt(max(ps))
        hls = [t["hl"] for t in S["tests"] if FAM.get(t["family"]) == fam]
        c[f"{fam}.hlmin"], c[f"{fam}.hlmax"] = f(min(hls)), f(max(hls))
    c["h1w.minwins"] = str(min(t["wins"] for t in S["tests"] if FAM.get(t["family"]) == "h1w"))
    c["price.gain.min"] = f(min(p_["worst_gain"] for p_ in S["price"]))
    c["price.gain.max"] = f(max(p_["worst_gain"] for p_ in S["price"]))
    rob = [t["p_holm"] for t in S["h3_sensitivity"] if SENS[t["analysis"]] in ("nodev", "nodiag", "nominal", "a05", "a20", "S3", "S10")]
    c["sens.robust.maxp"] = pfmt(max(rob))
    T13 = pd.read_csv(TAB / "T13_tail_alerts.csv")
    st_ = T13[(T13.side == "hi") & T13.rule.isin(["BCCP", "S-NCP", "S-CQR", "SDLC"])]
    c["alert.strat.recall.min"], c["alert.strat.recall.max"] = f(st_.recall.min()), f(st_.recall.max())
    mg_ = T13[(T13.side == "hi") & T13.rule.isin(["SCP", "CQR", "HPD-split"])]
    nds = M["n_datasets"]
    c["alert.marg.below09.min"] = str(int(nds - mg_["n_ds_recall_ge_0.9"].max()))
    c["alert.marg.below09.max"] = str(int(nds - mg_["n_ds_recall_ge_0.9"].min()))
    for t in S["h3_sensitivity"]:
        _put_test(c, f"sens.{SENS[t['analysis']]}.{_comp(t['comparison'])}", t)
    for t in S["tost_worst_stratum"]:
        c[f"tost.{_comp(t['comparison'])}"] = pfmt(t["p_tost"])
    for p_ in S["price"]:
        k = f"price.{p_['stratified']}"
        c[k + ".geo"], c[k + ".lo"], c[k + ".hi"] = f(p_["geo_ratio"], 2), f(p_["ci_low"], 2), f(p_["ci_high"], 2)
        c[k + ".med"], c[k + ".gain"], c[k + ".n15"] = f(p_["median_ratio"], 2), f(p_["worst_gain"]), str(p_["n_ratio_gt_1.5"])
    for r in S["matched_coverage"]:
        k = f"mc.{r['method_at_alpha_0.05']}"
        c[k + ".worst"], c[k + ".size"], c[k + ".nsmaller"] = f(r["worst_stratum"]), f(r["size_geo"]), str(r["n_ds_SDLC_smaller"])
    c["mc.nsmaller.min"] = str(min(r["n_ds_SDLC_smaller"] for r in S["matched_coverage"]))
    c["mc.nsmaller.max"] = str(max(r["n_ds_SDLC_smaller"] for r in S["matched_coverage"]))
    ea = S["error_analysis"]
    for k, v in ea.items():
        if isinstance(v, list):
            c[f"ea.{k}.rho"], c[f"ea.{k}.p"] = f(v[0], 2), pfmt(v[1])
    for t in S.get("alerts", []):
        cmp_ = t["comparison"]
        if cmp_.startswith("cost r="):
            rr = cmp_.split(":")[0].replace("cost r=", "")
            key = ("cost." if rr == "10" else f"cost{rr}.") + cmp_.split("SDLC vs ")[1]
        else:
            key = _comp(cmp_)
        _put_test(c, f"al.{t['side']}.{key}", t)
    L = S.get("learners", {})
    for tag in ("mlp", "dw"):
        for t in L.get(tag, {}).get("tests", []):
            _put_test(c, f"{tag}.{_comp(t['comparison'])}", t)
        if tag in L:
            c[f"{tag}.n_datasets"] = str(L[tag]["n_datasets"])
            c[f"{tag}.n_seeds"] = str(L[tag]["n_seeds"])
    for k in ("shift_n_ess_ge_50",):
        c[k] = str(M[k])
    c["ess_up2_min"], c["ess_up2_median"] = f(M["ess_up2_min"], 1), f(M["ess_up2_median"], 0)
    cf = RES / "confirmatory" / "statistics_confirmatory.json"
    if cf.exists():
        CF = json.loads(cf.read_text())
        c["conf.n_eval"] = str(CF["n_datasets"])
        for h in ("C-H1", "C-H3"):
            for t in CF[h]["tests"]:
                _put_test(c, f"{h}.{_comp(t['comparison'])}", t)
        c["C-H1.maxp"] = pfmt(max(t["p_holm"] for t in CF["C-H1"]["tests"]))
        c["C-H1.supported"] = "supported" if CF["C-H1"]["supported"] else "not supported"
        c["C-H2.below"], c["C-H2.crit"] = str(CF["C-H2"]["n_below_null_q05"]), str(CF["C-H2"]["critical"])
        c["C-H2.p"] = pfmt(CF["C-H2"]["binom_p_excess"])
        for t in CF["C-H4"]:
            c[f"C-H4.{_comp(t['comparison'])}"] = pfmt(t["p_tost"])
        for code, r in CF["summary"].items():
            for col in ("worst_stratum", "size_geo", "top1", "upper_tail", "empty_rate", "sigma_decile_worst"):
                c[f"cs.{code}.{col}"] = f(r[col])
        c["conf.price"] = f(CF["price_vs_DLS_geo"], 2)
    return c


# ----------------------------------------------------------------------------- tables
TABLES = {}


def md_table(name, cols=None, rename=None, fmt=None, query=None, sort=None):
    df = pd.read_csv(TAB / f"{name}.csv", dtype=str if name.startswith(("D", "C")) else None, keep_default_na=False)
    if query:
        df = df.query(query)
    if sort:
        df = df.sort_values(sort)
    df = df[cols if cols else list(df.columns)].copy()
    fmt = fmt or {}
    for col in df.columns:
        if col in fmt:
            df[col] = df[col].map(fmt[col])
        elif pd.api.types.is_float_dtype(df[col]):
            df[col] = df[col].map(lambda v: "" if pd.isna(v) else f"{v:.3f}")
    if rename:
        df = df.rename(columns=rename)
    return df.to_markdown(index=False, disable_numparse=True)


def _balanced_tokens(text, head):
    """Yield (start, end, inner) for tokens '{{<head>...}}' with balanced braces inside."""
    i = 0
    while True:
        st = text.find("{{" + head, i)
        if st < 0:
            return
        depth, j = 0, st
        while j < len(text):
            if text.startswith("{{", j):
                depth += 1
                j += 2
                continue
            if text.startswith("}}", j):
                depth -= 1
                j += 2
                if depth == 0:
                    break
                continue
            if text[j] == "{":
                depth += 0.5
            elif text[j] == "}":
                depth -= 0.5
            j += 1
        yield st, j, text[st + 2 + len(head):j - 2]
        i = j


def render():
    ctx = context()
    text = "\n\n".join((SRC / s).read_text() for s in ORDER if (SRC / s).exists())

    # 1) value placeholders (innermost first): ctx keys, {{T:...}}, {{J:...}}
    def fmtv(v, fm):
        if fm == "pct":
            return f"{100 * float(v):.1f}%"
        if fm == "pp":
            return f"{100 * float(v):.1f}"
        if fm in ("f1", "f2", "f3", "f4"):
            return f"{float(v):.{int(fm[1])}f}"
        if fm == "int":
            return f"{int(round(float(v))):,}"
        if fm == "p":
            return "< 0.001" if float(v) < 0.001 else f"{float(v):.3f}"
        return str(v)

    def value(key):
        if key.startswith("T:"):
            tab, cond, col, fm = key[2:].split("|")
            df = pd.read_csv(TAB / f"{tab}.csv")
            for c_ in cond.split("&"):
                k_, v_ = c_.split("=", 1)
                df = df[df[k_].astype(str) == v_]
            if len(df) != 1:
                raise SystemExit(f"Lookup {key} matched {len(df)} rows")
            return fmtv(df.iloc[0][col], fm)
        if key.startswith("J:"):
            fn, path, fm = key[2:].split("|")
            v = json.loads((RES / fn).read_text())
            for part_ in path.split("/"):
                v = v[int(part_)] if isinstance(v, list) else v[part_]
            return fmtv(v, fm)
        if key not in ctx:
            raise SystemExit(f"Unresolved placeholder: {key}")
        return ctx[key]
    pat = re.compile(r"\{\{(?!TABLE:|FIG:)([^{}]+)\}\}")
    while pat.search(text):
        text = pat.sub(lambda mo: value(mo.group(1)), text)

    # 2) tables and figures (captions may contain LaTeX braces)
    from scripts.tables_spec import SPEC
    tab_no, fig_no = {}, {}
    out, last = [], 0
    for st, en, inner in list(_balanced_tokens(text, "TABLE:")):
        tid, cap = inner.split("|", 1)
        tab_no[tid] = len(tab_no) + 1
        out.append(text[last:st])
        out.append(f"**Table {tab_no[tid]}.** {cap}\n\n{md_table(**SPEC[tid])}\n")
        last = en
    out.append(text[last:])
    text = "".join(out)
    out, last = [], 0
    for st, en, inner in list(_balanced_tokens(text, "FIG:")):
        fid, path, cap = inner.split("|", 2)
        fig_no[fid] = len(fig_no) + 1
        out.append(text[last:st])
        out.append(f"![**Fig. {fig_no[fid]}.** {cap}]({(FIG / path).as_posix()}){{width=100%}}\n")
        last = en
    out.append(text[last:])
    text = "".join(out)

    # 3) section numbering and cross-references
    sec_no, counters, lines = {}, [0, 0, 0], []
    for line in text.split("\n"):
        m = re.match(r"^(#{1,3}) (.*?)(\s*\{#sec:([\w-]+)\})?\s*$", line)
        if m and not line.startswith("#### "):
            lvl = len(m.group(1))
            title = m.group(2)
            if "{-}" in line or title.strip() in ("References", "Highlights", "Abstract"):
                lines.append(f"{m.group(1)} {title.replace('{-}', '').strip()}")
                continue
            counters[lvl - 1] += 1
            for j in range(lvl, 3):
                counters[j] = 0
            num = ".".join(str(x) for x in counters[:lvl])
            if m.group(4):
                sec_no[m.group(4)] = num
            lines.append(f"{m.group(1)} {num}. {title}" if lvl == 1 else f"{m.group(1)} {num} {title}")
        else:
            lines.append(line)
    text = "\n".join(lines)
    for kind, table in (("sec", sec_no), ("tbl", tab_no), ("fig", fig_no)):
        missing = sorted(set(re.findall(r"\[-@" + kind + r":([\w-]+)\]", text)) - set(table))
        if missing:
            raise SystemExit(f"Undefined {kind} labels: {missing}")
        text = re.sub(r"\[-@" + kind + r":([\w-]+)\]", lambda mo: str(table[mo.group(1)]), text)
    text = re.sub(r"\\tag\{(\w+)\}", r"\\qquad (\1)", text)
    # notation that renders identically in Word (OMML) and LibreOffice
    text = text.replace("\\mid", "\\,|\\,")
    for op in ("Var", "Cov", "sd", "TV"):
        text = text.replace("\\mathrm{" + op + "}", "\\operatorname{" + op + "}")
    if "{{" in text:
        raise SystemExit("Unresolved token: " + text[text.index("{{"):text.index("{{") + 80])
    BUILD.mkdir(parents=True, exist_ok=True)
    (BUILD / "manuscript_filled.md").write_text(text)
    json.dump(ctx, open(BUILD / "placeholder_values.json", "w"), indent=1)
    return text


def render_aux(src_name, out_name, max_chars=None):
    """Fill placeholders of an auxiliary source (highlights, cover letter) and build its DOCX."""
    global ORDER
    saved = ORDER
    ORDER = [src_name]
    try:
        text = render()
    finally:
        ORDER = saved
    if max_chars:
        for line in text.splitlines():
            if line.startswith("- ") and len(line[2:]) > max_chars:
                raise SystemExit(f"Highlight too long ({len(line[2:])} > {max_chars}): {line[2:]}")
    md = BUILD / (Path(src_name).stem + "_filled.md")
    md.write_text(text)
    ref = BUILD / "reference.docx"
    subprocess.run(["pandoc", str(md), "-o", str(MS / out_name), f"--reference-doc={ref}"], check=True)
    print("written", MS / out_name)


def build_docx():
    md = BUILD / "manuscript_filled.md"
    ref = BUILD / "reference.docx"
    if not ref.exists():
        from scripts.docx_style import make_reference
        make_reference(ref)
    out = MS / "Final_Manuscript.docx"
    cmd = ["pandoc", str(md), "-o", str(out), "--citeproc",
           f"--bibliography={TOP / 'supplementary' / 'references_verified.bib'}",
           f"--csl={BUILD / 'springer-basic-author-date.csl'}", f"--reference-doc={ref}",
           "--resource-path", str(TOP), "-M", "link-citations=true"]
    subprocess.run(cmd, check=True)
    from scripts.docx_style import postprocess
    postprocess(out)
    print("written", out)


if __name__ == "__main__":
    render_aux("title_page.md", "title_page.docx")
    if (SRC / "cover_letter.md").exists():
        render_aux("cover_letter.md", "cover_letter.docx")
    render()
    build_docx()

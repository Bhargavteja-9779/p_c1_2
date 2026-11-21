"""Post hoc analyses requested in review round 5 (REVIEW/review_05.md: dataset validity, leakage, generalisation).
Uses existing result files only (no model fits). Does NOT modify the pre-registered scripts
(analyze_confirmatory.py, analyze_rw.py); every analysis here is labelled post hoc in the manuscript.

Rules fixed in this docstring before the analyses were run:
  * duplicate tasks: two datasets are flagged when their full target vectors have identical sorted values;
  * merged analysis: the per-dataset (geometric-mean over seeds) sizes of a duplicate pair are averaged on the log scale
    and counted as one dataset;
  * "continuous" target: at least 100 distinct values and largest atom (most frequent value) <= 5% of rows, both on
    the full data (the quantities the eligibility rule uses);
  * "nominal tail strata": realised training mass of the lowest and of the highest stratum within [0.08, 0.12] in
    every seed (nominal 0.10) and K = 5;
  * curated log scale: max|y| < 50 and exp(|y|) lies on a 0.01 grid (relative tolerance 1e-6) for >= 99% of rows;
  * top/bottom 1% (one definition for both pipelines, as in evaluate_from_cache3): y >= q_0.99 and y < q_0.01 of
    the training targets; a seed contributes only if the group holds >= 10 test points; a dataset with no such seed
    is "undefined".
Size comparisons: per-dataset geometric-mean normalised size over seeds, two-sided Wilcoxon signed-rank on log ratios,
Holm over the four comparators within a subset (as in analyze_secondary.py).
Writes results/statistics_review05.json and tables/T19_heldout_profile.csv, T19b_ctr23_profile.csv,
T20_review05_sensitivity.csv, T21_grouped_seed_range.csv, T22_duplicate_targets.csv, T23_top1_unified.csv.
"""
from __future__ import annotations

import glob
import hashlib
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
TOP = ROOT.parent
sys.path.insert(0, str(ROOT))
from src.data.openml_ctr23 import load as load_data  # noqa: E402
from src.statistics.tests import holm, paired_summary, paired_wilcoxon  # noqa: E402

RES, TAB = TOP / "results", TOP / "tables"
NAME = {"S-Res": "BCCP", "SDLC-LS": "SDLC", "S-HPD-LS": "S-HPD", "S-NCP": "S-NCP", "S-CQR": "S-CQR",
        "SCP": "SCP", "CQR": "CQR", "HPD-split-LS": "HPD-split"}
COMPS = ["BCCP", "S-NCP", "S-CQR", "S-HPD"]
CTR = json.loads((ROOT / "config" / "benchmark.json").read_text())["datasets"]
HO = json.loads((ROOT / "config" / "confirmatory.json").read_text())["datasets"]
MIN_N = 10


def load_eval(d):
    x = pd.concat([pd.read_json(f, lines=True) for f in sorted(glob.glob(str(d / "*.jsonl")))], ignore_index=True)
    x = x[(x.alpha == 0.1) & (x.scheme == "S5") & (x.cal_frac.isna() | (x.cal_frac == 1.0))]
    x = x[x.method.isin(NAME)].copy()
    x["m"] = x.method.map(NAME)
    x["nsize"] = x["size"] / x["y_train_sd"]
    return x


def per_ds(x):
    return x.groupby(["did", "m"]).nsize.apply(lambda v: float(np.exp(np.log(v).mean()))).unstack()


def target_profile(did):
    _, y, meta = load_data(did)
    y = np.asarray(y, float)
    u, c = np.unique(y, return_counts=True)
    logscale = False
    if np.abs(y).max() < 50:
        e = np.exp(np.abs(y)) * 100
        logscale = bool(np.mean(np.abs(e - np.round(e)) <= 1e-6 * np.maximum(1, e)) >= 0.99)
    return dict(did=did, dataset=meta.get("name", str(did)), n_full=len(y), distinct_full=len(u),
                largest_atom=float(c.max() / len(y)), atom_value=float(u[c.argmax()]), skew_full=float(stats.skew(y)),
                curated_log_scale=logscale,
                y_hash=hashlib.sha1(np.round(np.sort(y), 9).tobytes()).hexdigest()[:16])


def strata_profile(x):
    r = x[x.m == "SDLC"].copy()
    rows = []
    for did, g in r.groupby("did"):
        lo = [m[0] for m in g.train_stratum_mass]
        hi = [m[-1] for m in g.train_stratum_mass]
        rows.append(dict(did=did, K_min=int(g.K.min()), K_max=int(g.K.max()), lower_mass_min=min(lo),
                         lower_mass_max=max(lo), upper_mass_min=min(hi), upper_mass_max=max(hi),
                         ncal_min_stratum=int(g.ncal_min_stratum.min()),
                         ood_mean=float(g.frac_test_out_domain.mean()), ood_max=float(g.frac_test_out_domain.max()),
                         nominal_tails=bool((g.K == 5).all() and all(0.08 <= v <= 0.12 for v in lo + hi))))
    return pd.DataFrame(rows)


def size_tests(P, label, suite, rows):
    res = [paired_summary(P["SDLC"], P[b], better="smaller", log=True) for b in COMPS]
    ph = holm([r["p"] for r in res])
    out = {}
    for b, r, h in zip(COMPS, res, ph):
        out[b] = dict(n=r["n"], geo_ratio=r["geo_ratio"], geo_lo=r["geo_lo"], geo_hi=r["geo_hi"], wins=r["wins"],
                      losses=r["losses"], p=r["p"], p_holm=float(h))
        rows.append(dict(suite=suite, subset=label, comparison=f"SDLC vs {b}", **out[b]))
    return out


def merge_pair(P, a, b):
    Q = P.drop(index=[a, b], errors="ignore").copy()
    Q.loc[a] = np.exp((np.log(P.loc[a]) + np.log(P.loc[b])) / 2)
    return Q


def top1_unified(x, suite):
    r = x[x.m.isin(["SDLC", "S-NCP", "BCCP", "S-CQR", "S-HPD", "SCP", "CQR", "HPD-split"])].copy()
    r = r[r.ext1_n_2.fillna(0) >= MIN_N]
    t = r.groupby(["did", "m"]).ext1_cov_2.mean().unstack()
    n_def = r[r.m == "SDLC"].groupby("did").size()
    rows = []
    for m in t.columns:
        v = t[m].dropna()
        rows.append(dict(suite=suite, method=m, n_datasets=len(v), mean=float(v.mean()), min=float(v.min()),
                         max=float(v.max())))
    return pd.DataFrame(rows), t, n_def


def rw_load():
    files = sorted((RES / "rw" / "confirmatory").glob("*.json"))
    return pd.DataFrame([r for f in files for r in json.loads(f.read_text())])


def rw3(d, col, ncol, drop=(), merge=None, min_n=0):
    d = d[~d.did.isin(drop)]
    if min_n:
        d = d[d[ncol] >= min_n]
    t = d.groupby(["did", "method"])[col].mean().unstack()
    if merge:
        a, b = merge
        if a in t.index and b in t.index:
            t.loc[a] = (t.loc[a] + t.loc[b]) / 2
            t = t.drop(index=b)
    ok = t["RW-DLC-U"].notna() & t["SDLC"].notna()
    r = paired_wilcoxon(t["RW-DLC-U"][ok], t["SDLC"][ok], alternative="greater")
    dd = (t["RW-DLC-U"] - t["SDLC"])[ok]
    return dict(n=int(ok.sum()), diff_mean=float(dd.mean()), wins=r["wins"], p=r["p"],
                rw=float(t["RW-DLC-U"][ok].mean()), rw_min=float(t["RW-DLC-U"][ok].min()),
                rw_max=float(t["RW-DLC-U"][ok].max()), sdlc=float(t["SDLC"][ok].mean()))


def grouped_range():
    g = pd.concat([pd.read_json(f, lines=True) for f in sorted((RES / "raw_grouped").glob("*.jsonl"))],
                  ignore_index=True)
    cc = [c for c in g.columns if c.startswith("cal_cov_") and c[8:].isdigit()]
    g["worst"] = g[cc].min(axis=1)
    g = g[g.method.isin(NAME)]
    g["m"] = g.method.map(NAME)
    rows = []
    for (ds, m), gg in g.groupby(["dataset", "m"]):
        rows.append(dict(dataset=ds, method=m, cov_min=gg.coverage.min(), cov_max=gg.coverage.max(),
                         worst_min=gg.worst.min(), worst_max=gg.worst.max(), n_seeds=gg.seed.nunique()))
    return pd.DataFrame(rows)


def main():
    out, sens = {}, []
    prof = pd.DataFrame([target_profile(d) for d in CTR + HO])
    prof["suite"] = np.where(prof.did.isin(HO), "held-out", "ctr23")
    # duplicate targets
    dup = prof[prof.duplicated("y_hash", keep=False)].sort_values("y_hash")
    dup[["suite", "did", "dataset", "n_full", "distinct_full", "y_hash"]].to_csv(TAB / "T22_duplicate_targets.csv",
                                                                                 index=False)
    out["duplicate_pairs"] = [list(map(int, g.did)) for _, g in dup.groupby("y_hash")]
    xc, xh = load_eval(RES / "raw_eval_v3"), load_eval(RES / "confirmatory" / "raw_eval_v3")
    sc, sh = strata_profile(xc), strata_profile(xh)
    T19 = prof[prof.suite == "held-out"].merge(sh, on="did").drop(columns=["y_hash", "suite"])
    T19b = prof[prof.suite == "ctr23"].merge(sc, on="did").drop(columns=["y_hash", "suite"])
    T19.to_csv(TAB / "T19_heldout_profile.csv", index=False)
    T19b.to_csv(TAB / "T19b_ctr23_profile.csv", index=False)
    for s, T in (("heldout", T19), ("ctr23", T19b)):
        out[f"{s}.n_range"] = [int(T.n_full.min()), int(T.n_full.max())]
        out[f"{s}.absskew_max"] = float(T.skew_full.abs().max())
        out[f"{s}.n_log_scale"] = int(T.curated_log_scale.sum())
        out[f"{s}.n_continuous"] = int(((T.distinct_full >= 100) & (T.largest_atom <= 0.05)).sum())
        out[f"{s}.n_nominal_tails"] = int(T.nominal_tails.sum())
        out[f"{s}.n_ood_nonzero"] = int((T.ood_max > 0).sum())
        out[f"{s}.ood_max"] = float(T.ood_max.max())
    out["heldout.log_scale_datasets"] = list(T19.dataset[T19.curated_log_scale])
    # size sensitivity analyses
    Ph, Pc = per_ds(xh), per_ds(xc)
    out["heldout.all"] = size_tests(Ph, "all 17 (pre-specified set)", "held-out", sens)
    pair = out["duplicate_pairs"][0] if out["duplicate_pairs"] else None
    hp = [p for p in out["duplicate_pairs"] if all(d in HO for d in p)]
    if hp:
        a, b = hp[0]
        out["heldout.merged"] = size_tests(merge_pair(Ph, a, b), "duplicate pair merged (n = 16)", "held-out", sens)
    for s, P, T in (("heldout", Ph, T19), ("ctr23", Pc, T19b)):
        cont = T.did[(T.distinct_full >= 100) & (T.largest_atom <= 0.05)]
        nom = T.did[T.nominal_tails]
        out[f"{s}.continuous"] = size_tests(P.loc[P.index.isin(cont)], "continuous targets", s, sens)
        out[f"{s}.nominal"] = size_tests(P.loc[P.index.isin(nom)], "nominal tail strata", s, sens)
    if hp:
        out["heldout.no_house16H_merged"] = size_tests(merge_pair(Ph, a, b).drop(index=[44139], errors="ignore"),
                                                       "merged pair, without house_16H", "held-out", sens)
    pd.DataFrame(sens).to_csv(TAB / "T20_review05_sensitivity.csv", index=False)
    # top 1 % with one definition
    tu = []
    for s, x in (("ctr23", xc), ("held-out", xh)):
        t, w, nd = top1_unified(x, s)
        tu.append(t)
        out[f"{s}.top1_defined_datasets"] = int(len(nd))
        out[f"{s}.top1_SDLC"] = dict(mean=float(w["SDLC"].mean()), min=float(w["SDLC"].min()),
                                     max=float(w["SDLC"].max()), n=int(w["SDLC"].notna().sum()))
    pd.concat(tu).to_csv(TAB / "T23_top1_unified.csv", index=False)
    # RW-3 sensitivity (held-out)
    d = rw_load()
    rw = {"pre-specified (strict y > q99)": rw3(d, "top1_cov", "n_top1")}
    if hp:
        rw["strict, pair merged"] = rw3(d, "top1_cov", "n_top1", merge=(a, b))
    rw["strict, without Ailerons"] = rw3(d, "top1_cov", "n_top1", drop=(44137,))
    if "top1h_cov" in d:
        rw["unified (y >= q99, >= 10 test points)"] = rw3(d, "top1h_cov", "n_top1h", min_n=MIN_N)
        if hp:
            rw["unified, pair merged"] = rw3(d, "top1h_cov", "n_top1h", min_n=MIN_N, merge=(a, b))
    out["rw3_sensitivity"] = rw
    # grouped splits: per-seed range
    gr = grouped_range()
    gr.to_csv(TAB / "T21_grouped_seed_range.csv", index=False)
    v = gr[gr.dataset == "video_transcoding"].set_index("method")
    out["grouped.video"] = {m: v.loc[m].drop("n_seeds").to_dict() for m in ("SDLC", "BCCP", "S-NCP", "S-CQR")
                            if m in v.index}
    (RES / "statistics_review05.json").write_text(json.dumps(out, indent=1, default=float))
    print(pd.DataFrame(sens).round(3).to_string())
    print(json.dumps({k: v for k, v in out.items() if not isinstance(v, dict) or k.startswith("rw3")}, indent=1,
                     default=float))


if __name__ == "__main__":
    main()

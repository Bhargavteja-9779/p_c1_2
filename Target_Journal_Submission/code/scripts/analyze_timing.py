"""Timing summaries for review round 6 (computational cost).

Inputs : results/timing_like.csv (experiments/timing_like.py; CTR23 seed 0, like-for-like boundaries),
         results/timing_rw.csv   (experiments/timing_rw.py; held-out datasets seed 0, grid implementation G=4000,
                                  grid accuracy G=4000 vs 16000),
         results/timing_fit.csv  (experiments/timing_fit.py; model fitting and inference).
Outputs: tables/T15c_timing_like.csv, tables/T15d_timing_rw.csv (per-dataset, display) and
         results/timing_summary.json (values cited in the manuscript).
"""
from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

TOP = Path(__file__).resolve().parents[2]
RES, TAB = TOP / "results", TOP / "tables"


def main():
    out = {}
    tf = pd.read_csv(RES / "timing_fit.csv")
    infer_us = 1e6 * (tf.predict_mean + tf.predict_scale) / tf.n_pred        # mu_hat and sigma_hat inference
    out["infer_us_median"] = float(infer_us.median())
    out["infer_us_max"] = float(infer_us.max())
    # SDLC needs mean, 3 OOF mean, scale, 3 cross-fitted scale models; S-NCP mean, 3 OOF mean, scale
    sdlc_fit = tf.fit_mean + tf.fit_scale_with_oof + tf.fit_scale_crossfit + tf.fit_kde + tf.build_table
    sncp_fit = tf.fit_mean + tf.fit_scale_with_oof
    out["fit_ratio_sdlc_sncp_median"] = float((sdlc_fit / sncp_fit).median())
    out["fit_sdlc_s_max"] = float(sdlc_fit.max())
    out["fit_sdlc_s_max_dataset"] = str(tf.dataset[sdlc_fit.idxmax()]).replace("_", " ")

    f = RES / "timing_like.csv"
    if f.exists():
        t = pd.read_csv(f)
        t.to_csv(TAB / "T15c_timing_like.csv", index=False)
        piv = t.pivot(index="dataset", columns="method", values="pred_us_per_point")
        lat = t.pivot(index="dataset", columns="method", values="single_p50_us")
        lat99 = t.pivot(index="dataset", columns="method", values="single_p99_us")
        cal = t.pivot(index="dataset", columns="method", values="cal_s")
        tfi = tf.assign(infer=infer_us.values).set_index(tf.dataset)["infer"]
        L = {}
        for m in ("SDLC", "S-NCP", "BCCP"):
            L[m] = {"pred_us_median": float(piv[m].median()), "pred_us_max": float(piv[m].max()),
                    "single_p50_us_median": float(lat[m].median()), "single_p99_us_max": float(lat99[m].max()),
                    "cal_ms_median": float(1e3 * cal[m].median()), "cal_ms_max": float(1e3 * cal[m].max())}
        r = piv["SDLC"] / piv["S-NCP"]
        L["ratio_pred_sdlc_sncp"] = {"median": float(r.median()), "min": float(r.min()), "max": float(r.max())}
        e2e = (piv["SDLC"] + tfi.reindex(piv.index)) / (piv["S-NCP"] + tfi.reindex(piv.index))
        L["ratio_e2e_sdlc_sncp"] = {"median": float(e2e.median()), "max": float(e2e.max())}
        out["like"] = L
        d = t[["dataset", "method", "n_cal", "n_test", "K", "cal_s", "pred_us_per_point", "single_p50_us",
               "single_p99_us"]].copy()
        d["cal_s"] = (1e3 * d.cal_s).map(lambda v: f"{v:.2f}")
        for c in ("pred_us_per_point", "single_p50_us", "single_p99_us"):
            d[c] = d[c].map(lambda v: f"{v:.2f}" if v < 10 else f"{v:.0f}")
        d.columns = ["Dataset", "Method", "n cal", "n test", "K", "Calibration (ms)", "Batch prediction (µs/point)",
                     "Single query p50 (µs)", "Single query p99 (µs)"]
        d["Dataset"] = d.Dataset.str.replace("_", " ")
        d.to_csv(TAB / "D15c_timing_like.csv", index=False)

    f = RES / "timing_rw.csv"
    if f.exists():
        w = pd.read_csv(f)
        w.to_csv(TAB / "T15d_timing_rw.csv", index=False)
        R = {}
        for m in ("RW-DLC", "RW-NCP", "SDLC", "S-NCP"):
            col = f"us_per_point_{m}_G4000"
            R[m] = {"us_median": float(w[col].median()), "us_max": float(w[col].max())}
        R["ratio_rwdlc_sdlc_grid_median"] = float((w["us_per_point_RW-DLC_G4000"] / w["us_per_point_SDLC_G4000"]).median())
        R["ratio_rwdlc_rwncp_median"] = float((w["us_per_point_RW-DLC_G4000"] / w["us_per_point_RW-NCP_G4000"]).median())
        R["relevance_fit_s_max"] = float(w.t_relevance_fit_s.max())
        R["relevance_fit_s_max_ntrain"] = int(w.n_train[w.t_relevance_fit_s.idxmax()])
        R["calibration_s_max"] = float(w.t_rw_calibration_s.max())
        R["mean_size_change_max"] = float(w.rw_mean_size_rel_change_G4000_vs_16000.max())
        R["point_change_median_max"] = float(w.rw_point_size_median_rel_change.max())
        R["point_change_max"] = float(w.rw_point_size_max_rel_change.max())
        R["point_change_max_did"] = int(w.did[w.rw_point_size_max_rel_change.idxmax()])
        R["n_datasets"] = int(len(w))
        if "like" in out:
            R["ratio_rwdlc_exact_sdlc_median"] = float(w["us_per_point_RW-DLC_G4000"].median() / out["like"]["SDLC"]["pred_us_median"])
        out["rw"] = R
        d = w[["did", "n_train", "n_test", "t_relevance_fit_s", "t_rw_calibration_s",
               "us_per_point_RW-DLC_G4000", "us_per_point_RW-NCP_G4000", "us_per_point_SDLC_G4000",
               "us_per_point_S-NCP_G4000", "rw_mean_size_rel_change_G4000_vs_16000",
               "rw_point_size_median_rel_change", "rw_point_size_max_rel_change"]].copy()
        for c in d.columns[3:5]:
            d[c] = d[c].map(lambda v: f"{v:.2f}")
        for c in d.columns[5:9]:
            d[c] = d[c].map(lambda v: f"{v:.0f}")
        for c in d.columns[9:]:
            d[c] = d[c].map(lambda v: f"{100 * v:.2f}")
        d.columns = ["OpenML ID", "n train", "n test", "Relevance fit (s)", "RW calibration (s)",
                     "RW-DLC (µs/point)", "RW-NCP (µs/point)", "SDLC, grid (µs/point)", "S-NCP, grid (µs/point)",
                     "Mean size change (%)", "Median per-point change (%)", "Max per-point change (%)"]
        d.to_csv(TAB / "D15d_timing_rw.csv", index=False)
    (RES / "timing_summary.json").write_text(json.dumps(out, indent=1))
    print(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()

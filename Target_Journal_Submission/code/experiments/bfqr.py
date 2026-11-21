"""Level-optimised stratified CQR in the spirit of binned fair quantile regression (BFQR; Wang et al., 2023):
the per-stratum coverage levels 1-a_k are chosen to minimise the expected set size estimated on the calibration
covariates, subject to the mass-weighted constraint sum_k p_k (1-a_k) = 1-alpha (p_k = training mass of stratum k),
which preserves marginal coverage but not stratum-wise coverage. Same CQR models, strata and cached outputs as the
main benchmark; seed 0 of all 31 datasets (the cached outputs of the other seeds are not retained); alpha = 0.1.
Writes results/bfqr_seed0.jsonl (BFQR, S-CQR, CQR and SDLC rows evaluated identically)."""
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from experiments.evaluate_from_cache3 import CACHE, CACHE3, all_sets, build_context, eval_strata3  # noqa: E402
from experiments.run_benchmark import CFG  # noqa: E402
from src.evaluation.metrics import evaluate  # noqa: E402
from src.methods import conformal as C  # noqa: E402
from src.methods.strata import make_partition  # noqa: E402

GRID = np.round(np.arange(0.0, 0.5001, 0.005), 3)


def piece_size(lo, hi, e0, e1):
    return np.clip(np.minimum(hi, e1) - np.maximum(lo, e0), 0, None)


def optimise_levels(score, st, qlo_c, qhi_c, part, alpha, pk):
    K, E = part.K, part.strata_edges
    S = np.full((K, len(GRID)), np.inf)
    for k in range(K):
        sk = score[st == k]
        for j, a in enumerate(GRID):
            t = C.conformal_quantile(sk, a) if a > 0 else np.inf
            if np.isinf(t):
                S[k, j] = E[k + 1] - E[k]
            else:
                S[k, j] = piece_size(qlo_c - t, qhi_c + t, E[k], E[k + 1]).mean()
    lo_l, hi_l = 0.0, 1e6 * (E[-1] - E[0])
    best = np.full(K, alpha)
    for _ in range(100):                                    # Lagrangian bisection on the coverage constraint
        lam = 0.5 * (lo_l + hi_l)
        idx = np.argmin(S + lam * pk[:, None] * GRID[None, :], axis=1)
        a = GRID[idx]
        if (pk * a).sum() <= alpha + 1e-12:   # feasible: try a smaller price on miscoverage
            best, hi_l = a, lam
        else:
            lo_l = lam
    return best


def main():
    out = ROOT.parent / "results" / "bfqr_seed0.jsonl"
    rows = []
    for did in CFG["datasets"]:
        c = dict(np.load(CACHE / f"{did}_0.npz"))
        c3 = dict(np.load(CACHE3 / f"{did}_0.npz"))
        part = make_partition(c["y_train"], n_fine=CFG["n_fine"], n_coarse=CFG["n_coarse"], nonneg=True)
        ctx, tables, scales = build_context(c, c3, part, [0.1])
        yc, yt = ctx["yc"], ctx["yt"]
        qlo_c, qhi_c = ctx["q_c"][0.1]
        qlo_t, qhi_t = ctx["q_t"][0.1]
        st = part.stratum(yc)
        score = np.maximum(qlo_c - yc, yc - qhi_c)
        pk = np.bincount(part.stratum(part.y_train), minlength=part.K) / len(part.y_train)
        ak = optimise_levels(score, st, qlo_c, qhi_c, part, 0.1, pk)
        sets = all_sets(ctx, tables, scales, 0.1, part, only=["CQR", "S-CQR", "SDLC-LS", "S-NCP"])
        sets["BFQR"] = C.interval_method(score, (qlo_t, qhi_t), 0.1, part, kind="cqr", strata_cal=st, alpha_k=ak)
        es = eval_strata3(part, yt, ctx["sg_t"])
        for m, S in sets.items():
            r, _ = evaluate(S, yt, part, 0.1, es)
            cc = [r[f"cal_cov_{k}"] for k in range(part.K)]
            rows.append(dict(did=did, seed=0, method=m, K=part.K, coverage=r["coverage"], worst_stratum=min(cc),
                             upper=cc[-1], lower=cc[0], nsize=r["size"] / float(part.y_train.std()),
                             levels=(1 - ak).round(3).tolist() if m == "BFQR" else None))
        print(did, "levels", (1 - ak).round(3).tolist(), flush=True)
    out.write_text("\n".join(json.dumps(r) for r in rows) + "\n")



def summarise():
    """Paired dataset-level comparison (one seed per dataset) -> results/bfqr_summary.json, tables/T17_bfqr.csv."""
    import pandas as pd
    from scipy.stats import wilcoxon
    d = pd.read_json(ROOT.parent / "results" / "bfqr_seed0.jsonl", lines=True)
    name = {"BFQR": "BFQR (level-optimised)", "CQR": "CQR", "S-CQR": "S-CQR", "S-NCP": "S-NCP", "SDLC-LS": "SDLC"}
    T = d.groupby("method").agg(coverage=("coverage", "mean"), worst_stratum=("worst_stratum", "mean"),
                                lower_tail=("lower", "mean"), upper_tail=("upper", "mean"),
                                size_geo=("nsize", lambda v: float(np.exp(np.log(v).mean())))).reset_index()
    T["method"] = T.method.map(name)
    T.to_csv(ROOT.parent / "tables" / "T17_bfqr.csv", index=False)
    w = d.pivot(index="did", columns="method", values="nsize")
    ws = d.pivot(index="did", columns="method", values="worst_stratum")
    lr = np.log(w["SDLC-LS"] / w["BFQR"])
    s = {"n": int(len(w)), "sdlc_vs_bfqr_geo": float(np.exp(lr.mean())), "sdlc_smaller": int((lr < 0).sum()),
         "p_size": float(wilcoxon(lr).pvalue),
         "bfqr_vs_scqr_geo": float(np.exp(np.log(w["BFQR"] / w["S-CQR"]).mean())),
         "bfqr_smaller_than_scqr": int((w["BFQR"] < w["S-CQR"]).sum()),
         "worst_sdlc_gt_bfqr": int((ws["SDLC-LS"] > ws["BFQR"]).sum()),
         "p_worst": float(wilcoxon(ws["SDLC-LS"] - ws["BFQR"]).pvalue),
         "bfqr_upper_below_08": int((d[d.method == "BFQR"].upper < 0.8).sum()),
         "bfqr_min_level_median": float(np.median([min(v) for v in d[d.method == "BFQR"].levels]))}
    for c in ("coverage", "worst_stratum", "upper", "lower"):
        s[f"bfqr_{c}"] = float(d[d.method == "BFQR"][c].mean())
    (ROOT.parent / "results" / "bfqr_summary.json").write_text(json.dumps(s, indent=1))
    print(s)


if __name__ == "__main__":
    if "--summary" not in sys.argv:
        main()
    summarise()

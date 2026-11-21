"""Valuation case study in money units (seed 0, alpha = 0.1, primary strata): for King County (44989) and Miami
(44983) house prices, coverage of the most expensive stratum and, for interval methods, how far the upper bound
falls below the true price of a missed expensive house. Uses the cached model outputs of the main benchmark
(no refitting). Writes results/case_study_dollars.json."""
import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from experiments.evaluate_from_cache3 import CACHE, CACHE3, all_sets, build_context  # noqa: E402
from experiments.run_benchmark import CFG  # noqa: E402
from src.evaluation.metrics import covered, sizes  # noqa: E402
from src.methods.strata import make_partition  # noqa: E402

METHODS = {"SCP": "SCP", "CQR": "CQR", "HPD-split-LS": "HPD-split", "S-Res": "BCCP", "S-NCP": "S-NCP", "SDLC-LS": "SDLC"}


def main():
    out = {}
    for did, name in ((44989, "kings_county"), (44983, "miami_housing")):
        c = dict(np.load(CACHE / f"{did}_0.npz"))
        c3 = dict(np.load(CACHE3 / f"{did}_0.npz"))
        part = make_partition(c["y_train"], n_fine=CFG["n_fine"], n_coarse=CFG["n_coarse"], nonneg=True)
        ctx, tables, scales = build_context(c, c3, part, [0.1])
        yt = ctx["yt"]
        top = part.stratum(yt) == part.K - 1
        sets = all_sets(ctx, tables, scales, 0.1, part)
        r = {"n_test": int(len(yt)), "n_top": int(top.sum()),
             "top_threshold": float(np.min(yt[top])), "expected_missed": 0.1 * float(top.sum()), "top_median_price": float(np.median(yt[top]))}
        for m, lab in METHODS.items():
            S = sets[m]
            cv = covered(S, yt, part)
            sz = sizes(S, part)
            d = {"top_coverage": float(cv[top].mean()), "top_missed": int((~cv[top]).sum()),
                 "median_rel_width_top": float(np.median(sz[top] / yt[top])),
                 "coverage": float(cv.mean()), "mean_size_top": float(sizes(S, part)[top].mean())}
            if S[0] == "int":                       # interval: shortfall of the upper bound for missed top houses
                hi = np.max(np.where(S[2] > S[1], S[2], -np.inf), axis=1)
                miss = top & ~cv & (yt > hi)
                d["median_shortfall"] = float(np.median(yt[miss] - hi[miss])) if miss.any() else 0.0
                d["total_shortfall"] = float(np.sum(yt[miss] - hi[miss]))
            r[lab] = d
        # top-stratum coverage over all 10 splits (from the evaluation files of the main benchmark)
        rows = [json.loads(l) for f in sorted((ROOT.parent / "results" / "raw_eval_v3").glob(f"{did}_*.jsonl"))
                for l in f.read_text().splitlines()]
        for m, lab in METHODS.items():
            v = [x[f"cal_cov_{x['K'] - 1}"] for x in rows
                 if x["method"] == m and x.get("alpha") == 0.1 and x.get("scheme", "S5") == "S5"
                 and x.get("cal_frac", 1.0) == 1.0]
            r[lab]["top_coverage_10seeds_mean"] = float(np.mean(v))
            r[lab]["top_coverage_10seeds_min"] = float(np.min(v))
            r[lab]["top_coverage_10seeds_max"] = float(np.max(v))
            r[lab]["n_seeds"] = len(v)
        out[name] = r
        print(name, json.dumps(r, indent=0)[:1500])
    (ROOT.parent / "results" / "case_study_dollars.json").write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()

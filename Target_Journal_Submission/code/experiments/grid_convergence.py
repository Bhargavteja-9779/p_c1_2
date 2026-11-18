"""Grid-convergence check for the v3 set geometry (review cycle 1, C1-27/C1-40/C1-06).
For seed 0 of heavy-tailed and large datasets, SDLC-LS sets are rebuilt with different set-grid
resolutions (core points x tail points); sizes and piece counts are compared with the finest grid."""
import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from experiments.evaluate_from_cache3 import CACHE, CACHE3, build_context  # noqa: E402
from experiments.run_benchmark import CFG  # noqa: E402
from src.methods import ls_exact3 as L3  # noqa: E402
from src.methods.conformal import conformal_quantile  # noqa: E402
from src.methods.strata import make_partition  # noqa: E402
from src.models import density as D  # noqa: E402

OUT = ROOT.parent / "results" / "grid_convergence.json"
DATASETS = [44963, 45012, 44987, 44958, 44990, 44975]
GRIDS = [(512, 64), (1536, 256), (6144, 1024)]


def main():
    rows = []
    for did in DATASETS:
        c, c3 = dict(np.load(CACHE / f"{did}_0.npz")), dict(np.load(CACHE3 / f"{did}_0.npz"))
        part = make_partition(c["y_train"], n_fine=CFG["n_fine"], n_coarse=CFG["n_coarse"], nonneg=True)
        ctx, _, _ = build_context(c, c3, part, [0.1])
        dens = D.RobustLSDensity(c3["z_LS_cf"].astype(float))
        yc, yt = ctx["yc"], ctx["yt"]
        st = part.stratum(yc)
        res = {}
        for core, tail in GRIDS:
            T = L3.LSTable3(dens, n_core=core, n_tail=tail)
            sc = L3.scores("density", T, yc, ctx["mu_c"], ctx["sg_c"], ctx["sg_c"], part)
            q = np.array([conformal_quantile(sc[st == k], 0.1) for k in range(part.K)])
            t0 = time.perf_counter()
            S = L3.build_sets("density", T, ctx["mu_t"], ctx["sg_t"], ctx["sg_t"], q, part, yt,
                              L3.scores("density", T, yt, ctx["mu_t"], ctx["sg_t"], ctx["sg_t"], part))
            res[(core, tail)] = (S[1].mean(), S[2].mean(), time.perf_counter() - t0, S[1].copy(), S[2].copy())
        ref = res[GRIDS[-1]]
        for g, (sz, pc, tm, szv, pcv) in res.items():
            ok = ref[3] > 0
            rel_pt = np.abs(szv[ok] - ref[3][ok]) / ref[3][ok]
            rows.append(dict(did=did, core=g[0], tail=g[1], mean_size=sz, mean_pieces=pc, seconds=tm,
                             rel_size_diff_vs_finest=abs(sz - ref[0]) / ref[0], pieces_diff_vs_finest=pc - ref[1],
                             max_rel_size_diff_per_point=float(rel_pt.max()) if ok.any() else 0.0,
                             q99_rel_size_diff_per_point=float(np.quantile(rel_pt, 0.99)) if ok.any() else 0.0,
                             frac_points_pieces_differ=float(np.mean(pcv != ref[4])),
                             empty_mismatch=int(np.sum((szv > 0) != (ref[3] > 0)))))
        print(did, {k: (round(v[0], 4), round(v[1], 3), round(v[2], 1)) for k, v in res.items()}, flush=True)
    OUT.write_text(json.dumps(rows, indent=1))


if __name__ == "__main__":
    main()

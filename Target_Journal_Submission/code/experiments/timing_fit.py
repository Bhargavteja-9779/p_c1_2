"""Isolated fit timing per model component (review cycle 1, C1-35): seed 0 of every dataset, one process,
single-threaded (OMP/MKL/OPENBLAS=1, LightGBM n_jobs=1), each component timed separately (fit only),
plus prediction time on calibration+test charged separately. Writes results/timing_fit.csv."""
import os
import sys
import time
from pathlib import Path

for v in ("OMP_NUM_THREADS", "MKL_NUM_THREADS", "OPENBLAS_NUM_THREADS"):
    os.environ[v] = "1"
import numpy as np  # noqa: E402
import pandas as pd  # noqa: E402
from sklearn.model_selection import KFold  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from experiments.run_benchmark import CFG, split  # noqa: E402
from src.data.openml_ctr23 import load  # noqa: E402
from src.methods import ls_exact3 as L3  # noqa: E402
from src.methods.strata import make_partition  # noqa: E402
from src.models import density as D  # noqa: E402
from src.models import learners as Lr  # noqa: E402

OUT = ROOT.parent / "results" / "timing_fit.csv"


def tm(fn):
    t0 = time.perf_counter()
    r = fn()
    return r, time.perf_counter() - t0


def main():
    rows = pd.read_csv(OUT).to_dict("records") if OUT.exists() else []   # resumable after a restart
    done = {int(r["did"]) for r in rows}
    for did in CFG["datasets"]:
        if did in done:
            continue
        X, y, meta = load(did)
        tr, ca, te = split(len(y), 0)
        Xtr, ytr, Xct = X[tr], y[tr], X[np.concatenate([ca, te])]
        part = make_partition(ytr, n_fine=CFG["n_fine"], n_coarse=CFG["n_coarse"], nonneg=True)
        mu, t_mu = tm(lambda: Lr.fit_point(Xtr, ytr, 0, 1))
        (sg, oof), t_sc = tm(lambda: Lr.fit_scale(Xtr, ytr, 0, 1, return_oof=True))
        r = ytr - oof

        def cf():
            out = np.zeros_like(ytr)
            for k, (a, b) in enumerate(KFold(3, shuffle=True, random_state=0).split(Xtr)):
                m = Lr._fit(Lr.lgb.LGBMRegressor(n_estimators=Lr.MAX_ROUNDS, **Lr.LGB_PARAMS), Xtr[a], np.abs(r[a]), 200 + k, 1)
                out[b] = m.predict(Xtr[b])
            return out
        sig_cf, t_cf = tm(cf)
        dens, t_kde = tm(lambda: D.RobustLSDensity(r / np.maximum(sig_cf, 1e-12)))
        _, t_tab = tm(lambda: L3.LSTable3(dens))
        _, t_q = tm(lambda: (Lr.fit_quantile(Xtr, ytr, 0.05, 0, 1), Lr.fit_quantile(Xtr, ytr, 0.95, 0, 1)))
        hd = D.HistogramDensity(part, CFG["n_coarse"])
        clf, t_clf = tm(lambda: Lr.fit_classifier(Xtr, hd.labels(ytr), hd.n_classes, 0, 1))
        _, p_mu = tm(lambda: mu.predict(Xct))
        _, p_sg = tm(lambda: sg.predict(Xct))
        _, p_clf = tm(lambda: Lr.predict_proba_full(clf, Xct, hd.n_classes))
        rows.append(dict(did=did, dataset=meta["name"], n_train=len(ytr), n_pred=len(Xct),
                         fit_mean=t_mu, fit_scale_with_oof=t_sc, fit_scale_crossfit=t_cf, fit_kde=t_kde,
                         build_table=t_tab, fit_quantile_pair=t_q, fit_histogram_classifier=t_clf,
                         predict_mean=p_mu, predict_scale=p_sg, predict_histogram=p_clf))
        print(meta["name"], "done", flush=True)
        pd.DataFrame(rows).to_csv(OUT, index=False)


if __name__ == "__main__":
    main()

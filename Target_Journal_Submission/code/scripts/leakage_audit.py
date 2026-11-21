"""Leakage audit: exact duplicate rows (features+target), duplicate feature vectors with
different targets, missing values, and the share of test feature vectors present in the training split, for seed 0
and as min/max over all seeds. Covers the CTR23 datasets (seeds 0-9) and, since review round 5, the held-out datasets
(seeds 0-4, the pre-specified 50,000-row subsample)."""
import json
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from experiments.run_benchmark import CFG, split  # noqa: E402
from src.data.openml_ctr23 import load  # noqa: E402

CC = json.loads((ROOT / "config" / "confirmatory.json").read_text())
rows = []
for suite, ids, seeds, nmax in (("ctr23", CFG["datasets"], CFG["seeds"], 0),
                                ("held-out", CC["datasets"], CC["seeds"], CC["n_max"])):
  os.environ["TSCP_NMAX"] = str(nmax)
  for did in ids:
    X, y, m = load(did)
    df = pd.DataFrame(X)
    keyX = pd.util.hash_pandas_object(df.fillna(-9.99e99), index=False).values
    keyXY = pd.util.hash_pandas_object(pd.DataFrame(np.c_[np.nan_to_num(X, nan=-9.99e99), y]), index=False).values
    cr = []
    for sd in seeds:
        tr, ca, te = split(len(y), sd)
        cr.append(float(np.isin(keyX[te], keyX[tr]).mean()))
    cross = cr[0]
    rows.append(dict(suite=suite, did=did, dataset=m["name"], n=len(y), test_X_in_train_min=min(cr),
                     test_X_in_train_max=max(cr), dup_rows_frac=1 - len(np.unique(keyXY)) / len(y),
                     dup_X_frac=1 - len(np.unique(keyX)) / len(y), test_X_in_train_frac_seed0=float(cross),
                     missing_frac=float(np.isnan(X).mean())))
out = pd.DataFrame(rows).sort_values("test_X_in_train_frac_seed0", ascending=False)
top = ROOT.parent
out.to_csv(top / "tables" / "S2_leakage_audit.csv", index=False)
(top / "tables" / "S2_leakage_audit.md").write_text(out.to_markdown(index=False, floatfmt=".4f"))
print(out.head(10).to_string(index=False))

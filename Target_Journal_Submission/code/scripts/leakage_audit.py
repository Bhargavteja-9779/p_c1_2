"""Leakage audit: exact duplicate rows (features+target), duplicate feature vectors with
different targets, missing values, and cross-split duplicate rate for seed 0."""
import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from experiments.run_benchmark import CFG, split  # noqa: E402
from src.data.openml_ctr23 import load  # noqa: E402

rows = []
for did in CFG["datasets"]:
    X, y, m = load(did)
    df = pd.DataFrame(X)
    keyX = pd.util.hash_pandas_object(df.fillna(-9.99e99), index=False).values
    keyXY = pd.util.hash_pandas_object(pd.DataFrame(np.c_[np.nan_to_num(X, nan=-9.99e99), y]), index=False).values
    tr, ca, te = split(len(y), 0)
    cross = np.isin(keyX[te], keyX[tr]).mean()
    rows.append(dict(did=did, dataset=m["name"], n=len(y), dup_rows_frac=1 - len(np.unique(keyXY)) / len(y),
                     dup_X_frac=1 - len(np.unique(keyX)) / len(y), test_X_in_train_frac_seed0=float(cross),
                     missing_frac=float(np.isnan(X).mean())))
out = pd.DataFrame(rows).sort_values("test_X_in_train_frac_seed0", ascending=False)
top = ROOT.parent
out.to_csv(top / "tables" / "S2_leakage_audit.csv", index=False)
(top / "tables" / "S2_leakage_audit.md").write_text(out.to_markdown(index=False, floatfmt=".4f"))
print(out.head(10).to_string(index=False))

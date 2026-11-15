"""Download and cache the OpenML-CTR23 regression suite (Fischer, Feurer & Bischl, 2023).

Each dataset is stored as a parquet file with numeric features (categoricals are
one-hot encoded) and the default target column renamed to ``__target__``.
"""
from __future__ import annotations

import json
import os
from pathlib import Path

import numpy as np
import pandas as pd

SUITE_ID = 353
CACHE = Path(os.environ.get("TSCP_DATA", Path(__file__).resolve().parents[3] / "data"))


def suite_ids() -> list[int]:
    import openml
    return [int(i) for i in openml.study.get_suite(SUITE_ID).data]


def _prepare(did: int) -> tuple[pd.DataFrame, dict]:
    import openml
    ds = openml.datasets.get_dataset(did, download_data=True, download_qualities=False,
                                     download_features_meta_data=False)
    tgt = ds.default_target_attribute
    X, y, cat_mask, names = ds.get_data(target=tgt, dataset_format="dataframe")
    X = X.copy()
    cats = [n for n, c in zip(names, cat_mask) if c]
    for c in X.columns:
        if c in cats or str(X[c].dtype) == "category":
            X[c] = X[c].astype("category")
        elif not pd.api.types.is_numeric_dtype(X[c]):
            # pandas >= 3 stores strings as StringDtype (not object): parse as numbers if
            # every non-missing value is numeric, otherwise one-hot encode.
            num = pd.to_numeric(X[c], errors="coerce")
            if num[X[c].notna()].notna().all():
                X[c] = num
            else:
                X[c] = X[c].astype("category")
    X = pd.get_dummies(X, columns=[c for c in X.columns if str(X[c].dtype) == "category"],
                       dummy_na=True, dtype=float)
    X = X.apply(pd.to_numeric, errors="coerce").astype(float)
    X.columns = [f"f{i}" for i in range(X.shape[1])]
    y = pd.to_numeric(y, errors="coerce").astype(float)
    keep = y.notna().values
    df = X.loc[keep].reset_index(drop=True)
    df["__target__"] = y.loc[keep].values
    meta = {"did": did, "name": ds.name, "target": tgt, "n": int(len(df)),
            "p": int(X.shape[1]), "n_unique_y": int(np.unique(df["__target__"]).size),
            "licence": ds.licence}
    return df, meta


def load(did: int) -> tuple[np.ndarray, np.ndarray, dict]:
    CACHE.mkdir(parents=True, exist_ok=True)
    pq, mj = CACHE / f"{did}.parquet", CACHE / f"{did}.json"
    if not pq.exists():
        df, meta = _prepare(did)
        df.to_parquet(pq.with_suffix(".parquet.tmp"))
        os.replace(pq.with_suffix(".parquet.tmp"), pq)
        mj.write_text(json.dumps(meta, indent=1))
    df = pd.read_parquet(pq)
    meta = json.loads(mj.read_text())
    y = df.pop("__target__").to_numpy(float)
    return df.to_numpy(float), y, meta


if __name__ == "__main__":
    for d in suite_ids():  # all 35; exclusion rule applied in config
        X, y, m = load(d)
        print(m)

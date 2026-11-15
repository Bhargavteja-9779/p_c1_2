"""Base learners shared by every conformal method (identical across methods for fairness).

All learners are LightGBM models with one fixed, pre-registered configuration.
Early stopping uses an internal validation split carved out of the *proper training
set only*; calibration and test data are never seen during fitting.
"""
from __future__ import annotations

import warnings

import numpy as np
import lightgbm as lgb

warnings.filterwarnings("ignore", category=Warning, module="lightgbm")
from sklearn.model_selection import KFold, train_test_split

LGB_PARAMS = dict(learning_rate=0.05, num_leaves=31, min_child_samples=20,
                  subsample=0.8, subsample_freq=1, colsample_bytree=0.8,
                  reg_lambda=1.0, verbose=-1)
MAX_ROUNDS = 2000
PATIENCE = 50


def _fit(est, X, y, seed, n_jobs):
    est.set_params(random_state=seed, n_jobs=n_jobs)
    Xtr, Xva, ytr, yva = train_test_split(X, y, test_size=0.1, random_state=seed)
    est.fit(Xtr, ytr, eval_set=[(Xva, yva)],
            callbacks=[lgb.early_stopping(PATIENCE, verbose=False)])
    return est


def fit_point(X, y, seed=0, n_jobs=4):
    return _fit(lgb.LGBMRegressor(n_estimators=MAX_ROUNDS, **LGB_PARAMS), X, y, seed, n_jobs)


def fit_quantile(X, y, q, seed=0, n_jobs=4):
    return _fit(lgb.LGBMRegressor(objective="quantile", alpha=q, n_estimators=MAX_ROUNDS,
                                  **LGB_PARAMS), X, y, seed, n_jobs)


def fit_scale(X, y, seed=0, n_jobs=4, folds=3, return_oof=False):
    """Difficulty model sigma(x) ~ E|Y - mu(X)| fitted on out-of-fold residuals
    (Lei et al., 2018 locally weighted conformal), so that sigma is not trained
    on in-sample (optimistic) residuals. Optionally returns the OOF predictions."""
    oof = np.zeros_like(y)
    for k, (a, b) in enumerate(KFold(folds, shuffle=True, random_state=seed).split(X)):
        m = fit_point(X[a], y[a], seed + 100 + k, n_jobs)
        oof[b] = m.predict(X[b])
    m = _fit(lgb.LGBMRegressor(n_estimators=MAX_ROUNDS, **LGB_PARAMS),
             X, np.abs(y - oof), seed + 7, n_jobs)
    return (m, oof) if return_oof else m


def fit_classifier(X, labels, n_classes, seed=0, n_jobs=4):
    est = lgb.LGBMClassifier(objective="multiclass", n_estimators=MAX_ROUNDS, **LGB_PARAMS)
    est.set_params(random_state=seed, n_jobs=n_jobs)
    Xtr, Xva, ytr, yva = train_test_split(X, labels, test_size=0.1, random_state=seed,
                                          stratify=labels if np.bincount(labels).min() >= 2 else None)
    est.fit(Xtr, ytr, eval_set=[(Xva, yva)],
            callbacks=[lgb.early_stopping(PATIENCE, verbose=False)])
    return est


def predict_proba_full(est, X, n_classes, eps=1e-4):
    """Class probabilities over all n_classes (classes unseen in the fit get 0),
    then a tiny floor so that every bin has strictly positive density."""
    P = np.zeros((X.shape[0], n_classes))
    P[:, est.classes_] = est.predict_proba(X)
    P = (P + eps) / (1.0 + n_classes * eps)
    return P

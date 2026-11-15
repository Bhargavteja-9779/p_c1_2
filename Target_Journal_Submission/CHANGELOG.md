# CHANGELOG
- v0.1 initial pipeline (histogram density only)
- v0.2 added location-scale density, fine evaluation grid (200 cells), coarse classifier bins nested in grid
- v0.2.1 fix: stratified validation split fallback for tiny datasets
- v0.3 (v2 run) BCCP-hull baseline; all stratified methods under S3/S10 schemes; exploratory two-piece LS density
  (LS2); tail-alert metrics; cached model outputs (results/raw_contexts) — v2 reproduces v1 exactly for shared methods
- v0.4 grid-free exact implementation of all location-scale-family methods (src/methods/ls_exact.py) and a
  cache-based evaluation stage (experiments/evaluate_from_cache.py); MLP and synthetic studies use it too
- v0.4.1 analysis: BCCP naming, H3 vs BCCP/S-CQR/S-NCP/S-HPD/2p/hist, hull-vs-hull test, tail-alert table

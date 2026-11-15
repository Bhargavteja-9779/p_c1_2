# EXPERIMENT_LOG

1. Quick smoke test (3 dev datasets, seed 0): pipeline ran. Histogram (40-class GBDT) density under-trained on small
   data (early stopping ~21 rounds) → large fragmented SDLC-H sets. Recorded as negative finding.
2. Dev iteration (3 dev datasets × 3 seeds): added location-scale density (hypothesis: more sample-efficient).
   Test NLL improved on all 3 dev datasets (1.57→1.28, 3.13→2.04, 3.82→3.02). SDLC-LS size ≈ S-NCP size (1.62 vs 1.57 sd(y)).
   Decision frozen before full run: primary = SDLC-LS; SDLC-H reported as secondary.
3. Timing probe: largest dataset (wave_energy, 72k rows) 211 s/task single-thread.
4. Full run launched (31 datasets × 10 seeds, α ∈ {0.1, 0.05, 0.2}).
   Failure: energy_efficiency seed 0 — ValueError in stratified validation split (39 val points < 40 classes).
   Fix: fall back to unstratified split when n_val < n_classes. Failed tasks rerun after main run.
5. Proposition 1 (Gaussian): analytic = Monte Carlo (2M samples) to 3 decimals. R²=0.5: oracle X-conditional interval
   covers 70.5% of top-10% targets, 37.5% of top-1%.
6. DATA BUG found by leakage audit (scripts/leakage_audit.py): with pandas 3, string columns not flagged as
   categorical by OpenML (StringDtype) were coerced to NaN — forest_fires (month, day) and fps_benchmark
   (GpuNumberOfExecutionUnits) lost features. Loader fixed (numeric parse if all values numeric, else one-hot).
   Action: ALL raw results of 44962 and 44992 are deleted and recomputed for all seeds after the main run.
   Leakage audit: exact duplicate rows exist (sarcos 9.1%, cps88wages 7.6%, health_insurance 4.4%); random
   splitting preserves exchangeability, so coverage guarantees hold; reported as limitation.

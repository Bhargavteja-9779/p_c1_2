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
7. PRIOR-ART FINDING (literature agent, verified): Y-bin (stratified) conformal calibration for regression is
   published: Randahl, Williams & Hegre (2026, Political Analysis, BCCP; arXiv 2024) and Wang et al. (2023,
   NeurIPS, Equal Opportunity of Coverage / BFQR). Novelty repositioned (no claim on stratified calibration per se).
8. DECISION (recorded BEFORE inspecting complete v1 results): v2 run of the full benchmark adding
   (a) BCCP-hull baseline (contiguized BCCP), (b) all stratified methods under decile strata (BFQR-style
   equal-mass bins), (c) EXPLORATORY two-piece location-scale density (LS2; motivated by Theorem 2: set size
   depends on density accuracy; x-dependent skewness typical of imbalanced targets), (d) tail-alert recall /
   alert-rate metrics, (e) cached model outputs for later re-analysis. Primary pre-registered method unchanged
   (SDLC-LS). v1 raw results preserved in results/raw_v1_preregistered/ for a determinism audit.
9. v1 (pre-registered) complete: 310/310 runs. H1 supported (all Holm p<0.001, rbc≥0.99). H3 NOT supported in v1:
   SDLC-LS vs BCCP(S-SCP) p=0.81 (15/16 wins), vs S-NCP p=0.13. Analysis: supplementary/v1_preregistered_analysis/.
10. DIAGNOSIS of H3 failure: SDLC lost mainly on high-R² datasets (naval, cpu_activity, energy) → hypothesis:
   fixed 200-cell grid over the MARGINAL target range is too coarse when the CONDITIONAL density is narrower
   than a cell, inflating every grid-based density set (also the HPD-split/DCP/DLS baselines; fifa: HPD-split
   8.83 sd(y) grid vs 0.82 exact). Implemented grid-free sets for location-scale densities (src/methods/ls_exact.py:
   exact scores at observed y; per-x scale-free z-grid for set geometry). Diagnostic on 7 datasets, seed 0
   (development check of implementation correctness, not tuning): SDLC-LS size cpu_activity 0.553→0.359,
   naval 0.209→0.168, fifa 1.490→0.885, energy 0.284→0.219 (still > BCCP 0.146), forest_fires 9.91→9.50.
   DECISION: all LS-family methods (baselines and proposed) use the exact implementation in the final analysis;
   evaluation is recomputed for all tasks from cached model outputs (experiments/evaluate_from_cache.py).
   The v1 grid-based results remain archived and are reported as the pre-registered implementation.

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
11. REVIEW CYCLE 1 (10 reviewer agents; REVIEW/review_01.md, 46 issues). Decisions taken BEFORE any v3 result
   was inspected: (a) cross-fitted standardisation of OOF residuals for g (refit_scales.py; z sd in-sample
   shrinkage confirmed), (b) g = 0.99 FFT-KDE + 0.01 Student-t2 (no ad hoc floor), harmonised sigma floor
   max(1e-3 sd(y), 0.05 median|r_oof|), (c) stratum-exact set geometry (ls_exact3.py), half-open stratum
   pieces for interval methods, D ∩ [0,inf) for non-negative targets, (d) new comparators/ablations S-NCP-hull,
   S-NCP-floor, BCCP-floor, SDLC-N (Gaussian g), (e) new metrics: top/bottom 1% and 5%, sigma-hat-decile
   coverage, empty-set rate, stratum-wise tilted coverage, ESS of shift weights, positive-control shift,
   (f) confirmatory replication on 17 held-out CTR23-excluded/OpenML datasets (config/confirmatory.json,
   committed 1762ec0 before any confirmatory fit) — pre-registration document to be committed before evaluation.
12. v3 evaluation started 2026-11-17; container restart killed it at 78/310 (outputs are atomic, resumable).
13. PERFORMANCE (2026-11-18): profiling showed ~90% of evaluation time in ls_exact3.build_sets (cell-wise
   O(G K) per test point). Replaced by an exact monotone-run algorithm (super-level set of the piecewise-linear
   g on each monotone run is an interval; O(K R log G), R = 3–282 runs, median 25). Equivalence with the
   cell-wise reference (_build_sets_ref, kept): 7 datasets x {LS, LS2, N} x {density, hpd} x 4 threshold
   patterns incl. +inf: max relative size difference 7e-15, piece counts/alerts/coverage/hulls identical;
   full task 44956_0 re-run: max |diff| 3.6e-15 over all 214 output fields. New unit test
   tests/test_ls_exact3.py::test_run_geometry_equals_cellwise_reference. Speed-up 10–60x per call; the
   evaluation was restarted with the new code at 84/310 (first 84 files computed with the reference code,
   numerically identical). Timing results (Experiment 6) are measured with the final implementation.
14. QUEUE COMPLETE (2026-11-21). Container rebuilt before the grouped-split step; dependencies reinstalled
   (liac-arff needs `pip install --no-build-isolation`), OpenML hosts allowed in the cloud environment.
   Grouped task 44976_0 failed with a corrupt ARFF (four workers downloading the same file at once); rerun with
   one worker after clearing the cache. Results: sarcos and superconductivity unchanged under grouped splits;
   video_transcoding sets ~7x larger, SDLC smaller than S-NCP (0.88) but larger than BCCP (1.20), BCCP/S-CQR
   overall coverage 0.875/0.873 over 5 splits (reported, not hidden). Timing: SDLC 13.1 us per test point.
   build_supplement.py now caches dataset licences/metadata (tables/S1_licences.csv, S2_confirmatory_datasets.csv,
   seeded from the previous build; Tables S1/S2 byte-identical) because the full ARFF downloads take > 1 h.

# Response to review 6 (computational complexity, latency, memory and deployment)

Computation added: `experiments/timing_like.py` (like-for-like SDLC/S-NCP/BCCP timing on all CTR23 datasets, seed 0,
one thread, same inputs, model predictions excluded and reported separately, batch and single-query latency),
`experiments/timing_rw.py` (RW-DLC grid cost, relevance fit, calibration, peak memory, grid refinement), both
summarised by `scripts/analyze_timing.py` → `results/timing_summary.json`, Supplementary Table S13 (a) and (b).

| # | Issue | Status | What was done |
|---|---|---|---|
| 1 | RW-DLC has no exact implementation; complexity not stated | fixed | §4.5 states that RW-DLC's threshold depends on the candidate, so its sets are computed on a grid of G = 4,000 values, with per-point cost O(G log G_g) and memory O(cG) per chunk; coverage is still decided exactly at the observed target. |
| 2 | RW-DLC cost not reported | fixed | §6.7: 143 µs per test point (median), equal to SDLC on the same grid (ratio 1.01); relevance fit ≤ 4.9 s; Table S13(b). |
| 3 | Quadratic cost of the relevance KDE | partially fixed | §4.5 states the O(N²), O(nN), O(GN) costs of the exact Gaussian KDE used and that a binned estimate (as for ĝ) reduces them to O(N + G log G). The reported results keep the pre-specified exact implementation; the binned version is named as a deployment option, not run. |
| 4 | No grid-convergence check for RW-DLC | fixed | `timing_rw.py` re-computes sets on a finer grid: mean set sizes change by less than 0.1% (max 0.026%); the largest per-point change (0.33, dataset 44069) is reported in Table S13(b). |
| 5 | Memory is the binding constraint | fixed | Peak memory recorded by `timing_rw.py` and now tabulated in Table S13(b) (at most 202 MB for G = 4,000 and 807 MB for G = 16,000); §6.7 cites it; §4.5 gives the O(cG) memory per chunk. |
| 6 | SDLC vs S-NCP timing not like-for-like; ratio hides the tail | fixed | Like-for-like measurement: SDLC 13.3 µs per point in batches vs 0.07 µs for S-NCP (median factor 207, range 75–1,636 across datasets), but end-to-end including model predictions only 1.32× slower (median; at most 77× on the dataset with the cheapest point model, now stated in §6.7). Single-query latency (about 6 ms vs 6 µs) is now reported and the text says an interval method is preferable when single-query latency matters. |
| 7 | Cited timing tables do not exist | fixed | Table S13 is built from `tables/D15c_timing_like.csv` and `D15d_timing_rw.csv`; the supplement's cross-reference check passes. Supplementary numbering is stable (S19 CTR23 RW study, S20 earlier implementations, S21–S23 moved tables). |
| 8 | Deployment footprint and refitting cost | fixed | §4.5 "Deployment": eight stored gradient-boosted models (five for S-NCP), tabulated ĝ, thresholds; recalibration without refitting for new α, strata or φ; refitting needed after a change of the feature distribution. |
| 9 | Total compute, energy, carbon | partially fixed | Statements: hardware (4-core Intel Xeon 2.1 GHz, no GPU), about 15 CPU-hours for the final pipeline (≈4 h on four cores), about 26 including superseded implementations, from the logged task times. Energy and CO₂e were not measured. |
| 10 | §4.5 overstates generality | fixed | §4.5 gives the per-point orders O(K M log G_g) for SDLC, O(G log G_g) for RW-DLC on a grid and O(K) for S-NCP; §6.7 gives the measured medians. |

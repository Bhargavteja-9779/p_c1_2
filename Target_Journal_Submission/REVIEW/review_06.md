# Review 6: computational complexity, latency, memory and deployment

**Journal:** Journal of King Saud University – Computer and Information Sciences
**Reviewer:** #6, assigned to computational cost and deployability only
**Material inspected:**
- `manuscript/build/manuscript_filled.md`: §1 contribution 2, §4.4, §4.5, §4.7, §5.7, §6.6, §6.9 and the Statements.
- `manuscript/build/supplementary_filled.md` and `manuscript/Supplementary_Material.pdf`.
- `code/experiments/run_rw.py`, `timing.py`, `timing_fit.py` and `run_benchmark.py` (`run_methods`).
- `code/src/methods/ls_exact3.py` and `code/src/models/density.py`.
- `results/timing_methods_v3.csv`, `results/timing_fit.csv`, `results/rw/confirmatory/*.json` and `tables/T15*`.
- Reviews 01–04 and their responses (review 05 does not exist). Points already raised there are not repeated. They include the SDLC prediction bound O(K·R·log G) (R4-6), the 8 vs 12 regressions, the warm-up and per-dataset medians (C1-40), and isolated fit timing (C1-35).

## Summary

The paper claims that SDLC and the new RW-DLC "both have exact implementations whose cost is linear in the number of test points" (§1, contribution 2). It gives a complexity analysis (§4.5) and a timing paragraph (§6.9) for SDLC only.

**RW-DLC has no exact implementation.** Its threshold q(y) depends on the candidate through φ(y), so the monotone-run inversion that makes SDLC fast does not apply. The released code (`run_rw.py`) constructs every RW-DLC set by brute force on a uniform grid of G = 4000 target values. Each test point costs O(G) density evaluations and each 400-point chunk materialises 400×G arrays.

The setup is also quadratic. The relevance function is an exact `scipy.stats.gaussian_kde` evaluated at all N_tr training targets (for τ) and at all n calibration targets.

None of this is stated, timed or compared with S-NCP or SDLC. Yet the paper's main new method is the expensive one, and its score advantage over the cheaper relevance-weighted ablation (RW-4) was not significant.

My own measurements, described under the timing section below, show the following:
- RW-DLC set construction takes about 0.35–0.44 ms per test point. That is about 30× SDLC and several thousand times S-NCP.
- The cost grows linearly in G, and so does memory: about 190 MB per 400-point chunk at G = 4000, and 3 GB at G = 64,000.
- On a dataset with narrow sets, G = 4000 changes individual set sizes by up to 33% relative to G = 16,000.

The SDLC timing comparison is also not like-for-like. The timing tables cited in §6.9 (S13, S15) are absent from the Supplementary Material.

None of this threatens the validity results. It does undermine the "exact, linear-cost" claim, the deployability narrative and the cost–benefit case for RW-DLC.

**Recommendation: major revision.**

## Measurements made for this review

**Setup:**
- Script: `/tmp/claude-0/-home-user-p-c1-2/5b94335e-9e3c-5183-ae4d-3d0694ecad77/scratchpad/time_rw.py`.
- It re-uses `run_rw.py` (`SUITES`, `WeightedThreshold`, `CHUNK = 400`, `RobustLSDensity`, `make_partition`) on the cached contexts in `results/confirmatory/raw_contexts{,_v3}`, seed 0, φ_U, α = 0.1.
- Conditions: single process, BLAS/OMP threads = 1 set before import, `nice 19`, one warm-up and the median of 2–3 repetitions.
- **Caveat:** the 4-core machine was fully loaded by a concurrent LightGBM refit (4 processes at about 88% CPU, load average > 4). The absolute times are therefore probably inflated by up to about 2×. The ratios between grid sizes are reliable.
- Only RW-DLC-U was timed, not the other nine methods that `run_rw.py` evaluates in the same loop.

| Dataset (N_tr / n_cal / n_test) | Step | G = 1000 | G = 4000 | G = 16,000 | G = 64,000 |
|---|---|---|---|---|---|
| 44061 (2104 / 1052 / 1053) | batch sets, µs per test point | 155 | 416 | 2094 | 9247 |
| | single-query latency, µs | 401 | 378 | 1215 | 3907 |
| | peak memory of one 400-point chunk (RW-DLC only) | 48 MB | 190 MB | 762 MB | 3046 MB |
| 44069 (25,000 / 12,500 / 12,500) | batch sets, µs per test point | 126 | 440 | 1833 | — |
| | single-query latency, µs | 196 | 351 | 1146 | — |
| | peak memory of one chunk | 48 MB | 190 MB | 762 MB | — |

The table covers only the per-test-point work. The one-off setup for 44069 (N_tr = 25,000) took:
- 5.2 s for τ, which evaluates the KDE at all N_tr training targets;
- 2.4 s for the calibration weights and the threshold;
- 0.76 s at G = 4000 to evaluate φ on the grid and compute q(y);
- 2.3 s (188 µs per point) to evaluate φ at the test labels, which the exact-rule coverage needs.

Grid accuracy on 44069:
- Median set width at G = 4000: **18 grid cells** (5th percentile 12).
- Mean size changes by only 0.03% between G = 4000 and 16,000, but the largest per-point change is **33%**.
- At G = 1000 the largest per-point change is 100%: sets become empty.
- On 44061 (median width 2511 cells), the largest per-point change is 0.2%.

The archived run records in `results/rw/confirmatory/*.json` show the same pattern. The mean RW-DLC set is only 22.5 cells wide on 44069 and 40 cells on 44056. These two datasets carry the highest rates of empty sets (0.66% and 0.92%).

Reference figures from the authors' own files:
- `timing_methods_v3.csv`: SDLC takes a median of 13.5 µs per test point (maximum 89 µs) and S-NCP 0.089 µs. The ratio SDLC/S-NCP has a median over datasets of 107× and ranges from 58× to 1046×.
- `timing_fit.csv`: LightGBM inference for μ̂ and σ̂ takes a median of 39 µs per point (maximum 261 µs). Fitting SDLC's models costs a median 1.34× S-NCP's.

---

## Numbered issues

### 1. MAJOR: RW-DLC has no exact implementation, and its complexity is never stated

**Location:**
- §1, contribution 2 ("both have exact implementations whose cost is linear in the number of test points").
- Table 1.
- §4.5, which treats SDLC only.
- §5.7 line 290 ("evaluated on a grid of 4,000 target values").
- `run_rw.py` lines 28 (`G = 4000`), 128–152 and 46–60.

**Evidence:**
- In (11) the threshold q(y) depends on y through φ(y), and the score −φ(y)f̂(y|x) is not a monotone function of a single standardised variable. The exact level inversion of `ls_exact3.build_sets` therefore cannot be used.
- `run_rw.py` builds every RW-DLC set by evaluating f̂ at all G = 4000 grid points for every test point and summing the indicator times dy.
- Only coverage uses the exact rule. Set size, emptiness and every size comparison in RW-4 and Table 9 come from the grid.

The true costs, none of which appears in the paper:

| Stage | Cost |
|---|---|
| Fitting the relevance function | O(N_tr²) for τ = 0.01·max_i p̂_Y(Y_i) with an exact Gaussian KDE |
| Calibration | O(n·N_tr) for φ at the calibration targets, plus O(n log n) for the sort and cumulative sum |
| Grid preparation | O(G·N_tr) for φ on the grid, plus O(G log n) for q on the grid |
| Prediction, per test point | O(G log G_g) to interpolate ĝ at G points, plus O(G) comparisons |

The cost per test point is "linear in the number of test points" only with a constant of G = 4000 density evaluations. That is roughly 30× SDLC's measured cost.

The required G is not a constant either. It must scale with (range of D)/(width of the narrowest set) to keep per-point sizes accurate (issue 4).

**Fix:**
1. Delete "exact" for RW-DLC in contribution 2 and Table 1, and say the sets are computed on a grid.
2. Add an RW-DLC paragraph to §4.5 with the costs in the table above and the memory cost (issue 3).
3. Better, provide an exact or adaptive algorithm. Because q(y) is a non-decreasing step function of φ(y) with at most n+1 levels, the y-axis can be partitioned once, at calibration, into intervals on which q is constant.

   Within each interval the set is a super-level set of φ(y)ĝ((y−μ̂)/σ̂)/σ̂. Its boundaries can be found by bracketing and root-finding on the tabulated pieces, or approximated with an adaptive grid concentrated around μ̂(x) ± cσ̂(x) plus the high-φ regions where q = +∞.
4. Report the resulting complexity.

### 2. MAJOR: RW-DLC's computational cost is not reported, so the cost–benefit claim is unsupported

**Location:** §6.6, §6.9 ("Computational cost"), §7.2, Tables S13 and S15 (T15). `timing.py` does not time any RW method.

**Evidence:**
- The paper times SDLC at 13.5 µs per test point and calls the cost "negligible next to model fitting". RW-DLC is never timed.
- I measured 0.35–0.44 ms per test point at the paper's G = 4000 (see the measurements above). That is about 30× SDLC and about 4000× S-NCP, and it grows linearly in G (1.8–2.1 ms at G = 16,000; 9.2 ms at 64,000).
- End to end, including the LightGBM inference that every method needs (median 39 µs from `timing_fit.csv`), the costs are:
  - S-NCP: about 39 µs;
  - SDLC: about 53 µs (1.35×);
  - RW-DLC: about 0.48 ms (about 12× S-NCP).
- The paper never states these deployment-relevant ratios. It also never compares with the cheaper relevance-weighted alternatives.
- RW-4 shows that RW-DLC's sets were not significantly smaller than those of RW-NCP (ratio 0.904) or RW-DLS (0.885) after Holm correction. RW-NCP needs no density evaluation.

**Fix:**
1. Add SDLC, S-NCP, RW-NCP-U, RW-DLS-U, RW-DLC-U and RW-DLC-H to one timing harness on seed 0 of all 31 + 17 datasets, using the same settings as `timing.py`.
2. Report setup time (φ, τ, calibration, q on the grid) and per-test-point time separately, as per-dataset medians.
3. Report batch-amortised time and single-query latency (p50 and p99).
4. Report end-to-end time including μ̂/σ̂ inference.
5. Add a Pareto plot of top-1% coverage (and Cov_φ) against end-to-end latency.
6. State in §7.2 what RW-DLC's top-1% gain costs in latency and memory relative to RW-NCP and S-NCP.

### 3. MAJOR: the relevance function is fitted and evaluated at quadratic cost, and the paper's scalability claims do not cover it

**Location:** §4.7 (φ_U, τ = 0.01·max_i p̂_Y(Y_i)); §4.5 (an FFT-binned KDE is claimed, but for ĝ only); `run_rw.py` lines 94–98 (`gaussian_kde`, `kde(ytr).max()`, `pY(yc)`, `pY(yg)`).

**Evidence:**
- `scipy.stats.gaussian_kde` evaluates exactly: O(N_tr) per evaluation point.
- τ requires N_tr² kernel evaluations. On 44069 (N_tr = 25,000) it took 5.2 s, and φ at the 12,500 calibration points took 2.4 s, single-threaded.
- Extrapolated quadratically, τ alone takes about 2.3 h for N_tr = 10⁶. Every refit or change of relevance function repeats this.
- In deployment, deciding exactly whether an off-grid candidate y is in the set requires φ(y) at O(N_tr) cost. The relevance "model" must also store all N_tr training targets.
- This contradicts the paper's implicit scalability story, which rests on the FFT-binned KDE for ĝ.

**Fix:**
1. Use a binned or FFT KDE for p̂_Y, as is already done for ĝ, tabulated on the grid and interpolated. Take τ from the tabulated maximum.
2. Report a scaling experiment: setup time and per-point time against N_tr ∈ {10³, 10⁴, 10⁵, 10⁶}, using subsamples of the largest held-out datasets or a synthetic generator, and against n_cal and G.
3. State the stored-artefact size.

### 4. MODERATE: no grid-convergence check for RW-DLC, and per-point sizes and empty sets are grid-dependent on narrow-set datasets

**Location:** §5.7 line 290; Table 9 (size, empty sets); RW-4. Supplementary Table S4 covers SDLC's exact geometry only.

**Evidence:**
- The grid is uniform over D, with a spacing dy/sd of 0.0009–0.0084 depending on the dataset.
- On 44069 the median RW-DLC set is 18 cells wide. The largest per-point size difference is 33% between G = 4000 and 16,000, and 100% between G = 1000 and 16,000.
- Mean sizes are stable to 0.03%, so the size ratios in RW-4 are probably safe.
- Per-point quantities are not safe: emptiness, the number of pieces and any hull. The datasets with the narrowest sets (44069, 44056) are exactly those with the highest recorded empty-set rates (0.66% and 0.92%).
- I found no test point whose exact-rule coverage contradicted an empty grid set, but the authors do not check this.

**Fix:**
1. Add a Table S4 analogue for RW-DLC, RW-DLS and RW-NCP on all 17 held-out datasets with G ∈ {1000, 4000, 16,000, 64,000}, or an adaptive grid. Report:
   - the change in mean size;
   - the largest per-point size change;
   - the change in the empty-set rate;
   - the number of points that are covered by the exact rule but have an empty grid set.
2. Choose G per dataset so that the narrowest 5% of sets span at least, say, 100 cells.

### 5. MODERATE: the chunk × G materialisation makes memory, not time, the binding constraint on grid refinement

**Location:** `run_rw.py` lines 128–148 (`CHUNK = 400`; arrays `Fg`, `Rg`, `Zg` and ten boolean masks per chunk); `density.py:169–174` (`g_at`).

**Evidence:**
- Peak traced memory for one 400-point chunk, counting RW-DLC alone, is 190 MB at G = 4000, 762 MB at 16,000 and 3.0 GB at 64,000. That is about 119 bytes per (point, grid-cell) pair, roughly 15 float64 temporaries.
- One cause is that `g_at` evaluates `tail_pdf` on every point, then overwrites the inside points with `np.interp`, so the work is done twice.
- `run_rw.py` holds three float arrays and ten masks for all methods at once and runs 4 worker processes. The refinement needed for issue 4 is therefore memory-bound on ordinary hardware.
- The paper reports no memory figures. C1-40 estimated about 200 MB for the old SDLC grid, and that grid has now been reintroduced for RW-DLC.

**Fix:**
1. Make the chunk size adaptive to a fixed memory budget, for example CHUNK = budget/(G·bytes per cell).
2. Compute `tail_pdf` only outside the tabulated range.
3. Evaluate f̂ only on a window where the set can be non-empty: since f̂ ≤ max ĝ/σ̂, the window can be bounded from q.
4. Report peak RSS per worker for the RW study.

### 6. MAJOR: the SDLC vs S-NCP timing is not like-for-like, and the reported ratio hides the tail

**Location:** §6.9 ("13.5 µs … against 0.09 µs … roughly two orders of magnitude"); `timing.py` lines 36–58 and 72–74; `run_benchmark.py` lines 124–153.

**Evidence:**
- **What is timed differs.** SDLC's timer (`ls_timed.sdlc`) includes:
  - computing the calibration scores (`LX.scores` on `yc`);
  - computing the test-label scores (`LX.scores` on `yt`), which serves evaluation, not prediction;
  - the coverage and alert bookkeeping inside `build_sets(…, yt, st)`.

  S-NCP's timer (`put("S-NCP", …)`) excludes the calibration scores, which are computed as `nres_c` before the timer starts, and computes no coverage. The per-point ratio is therefore biased against SDLC in an unknown direction and size, and it is not a "prediction time" for either method.
- **Threads.** `timing.py` sets `OMP/MKL/OPENBLAS_NUM_THREADS = 1` inside `main()`, after `numpy` (and through it OpenBLAS) has been imported at module level, so the setting is not guaranteed to take effect. `timing_fit.py` does it correctly, before the import.
- **Reporting.** No hardware, CPU model, library versions or machine load are reported in the manuscript, although C1-40 asked for them and response_01 lists the issue as fixed.

  Times are batch-amortised over the whole test set. Single-query latency, which is what an interactive deployment pays (Python overhead dominates there: 196–401 µs in my RW-DLC measurements), is not reported.
- **Ratio.** "Two orders of magnitude" is the ratio of medians (13.5/0.09 ≈ 150). The per-dataset ratio has a median of 107× and reaches **1046×** (`timing_methods_v3.csv`). The worst case, which determines tail latency, is not mentioned.

**Fix:**
1. Re-time every method with the same boundaries:
   - (a) calibration, from scores to thresholds;
   - (b) prediction, from μ̂(x), σ̂(x) and the thresholds to a set, with no labels involved.
2. Set the thread variables before any import, and verify them with `threadpoolctl`.
3. Report the hardware and software versions, and whether the machine was otherwise idle.
4. Report per-dataset medians and the maximum ratio.
5. Report single-query p50/p99 latency and end-to-end latency including GBDT inference (median 39 µs, maximum 261 µs). End to end, SDLC is only about 1.35× S-NCP, which is a more useful and more favourable statement than "150×".

### 7. MODERATE: the cited timing tables, and other cited supplementary tables, do not exist

**Location:** §6.9 cites "Supplementary Tables S13 and S15". The manuscript also cites S16–S19.

**Evidence:**
- `supplementary_filled.md` and `Supplementary_Material.pdf` jump from Table S12 to S14 and contain no S13 or S15–S19.
- `tables/T15_timing_methods.md` exists only in the repository, uses internal method names, and does not state units. Its values match µs per test point.
- §6.6 says RW-DLC results on CTR23 are in Table S19, but `results/rw/` contains only `confirmatory/`. `PROJECT_STATE.md` lists the CTR23 RW run (310 tasks) as still to be run.

**Fix:**
1. Include the timing tables with units, hardware and per-dataset values.
2. Include the RW timing from issue 2.
3. Run and include the CTR23 RW study, or remove the citation of Table S19.

### 8. MODERATE: the deployment footprint and refitting cost are not described

**Location:** §4.5, §7.2.

**Evidence:**
- SDLC and RW-DLC need 8 LightGBM models with up to 2000 rounds each: mean, 3 out-of-fold mean models, scale, and 3 cross-fitted scale models.
- S-NCP with an out-of-fold scale needs 5. Measured fit cost is a median 1.34× S-NCP's (`timing_fit.csv`).
- RW-DLC additionally stores ĝ, the KDE of the training targets (all N_tr values with the exact KDE), the sorted calibration scores with their cumulative weights, and the q-on-grid table.
- The paper reports none of: model sizes in MB, the number of models, or what must be refitted versus only recalibrated.

  This matters because it is an advantage. Changing α, or changing φ (for example to track a known target shift, Theorem 2), needs only recalibration and grid preparation, O(n log n + G log n) with a binned KDE, and no GBDT refit.

**Fix:** Add a short deployment table covering:
- the number of fitted models and their total serialised size;
- what must be refitted when the data drift, and what only recalibrated when α or φ changes;
- the cost of each.

Mention that the per-test-point work is embarrassingly parallel.

### 9. MINOR: total compute, energy and carbon

**Location:** Statements and Declarations; §5.

**Evidence:**
- JKSU-CIS and Springer Nature do not require carbon reporting, so this is not a condition of acceptance.
- The study is nonetheless compute-heavy: 31 datasets × 10 seeds, 17 × 5, refits, an MLP, DenseWeight, grouped splits, the RW study and three superseded implementations.
- Neither total CPU-hours nor hardware is reported.

**Fix:** Report the total CPU-hours by experiment, the hardware, and optionally an energy and CO₂e estimate (for example with Green Algorithms or CodeCarbon) in the reproducibility statement. Give the expected runtime of `run_all.py --mode full` on stated hardware.

### 10. MINOR: §4.5 overstates generality

**Location:** §4.5 ("one fit serves every α"; "the prediction cost is linear in the number of test points").

**Evidence:**
- For RW-DLC, each α requires recomputing q on the grid. This is cheap, but it should be stated.
- "Linear in the number of test points" holds for every split-conformal method and says nothing about the constant. For RW-DLC the constant is G, and for SDLC it is K·R.

**Fix:** State the per-test-point constants explicitly: O(K·R·log G) for SDLC, O(G log G_g) for RW-DLC on a grid, and O(K) for S-NCP. Give the measured medians next to them.

---

## Overall assessment for the editor

The computational story is told for SDLC, the method the paper now concedes is only a few per cent better than S-NCP. It is not told for RW-DLC, the method that carries the paper's novelty. RW-DLC's implementation is a grid approximation with quadratic-cost relevance fitting and memory that grows with chunk × G. It is about an order of magnitude more expensive than S-NCP end to end and roughly 30× SDLC in set construction.

None of this is disqualifying. Sub-millisecond latency is acceptable for most tabular applications. But the "exact, linear-cost" claim must be corrected, and the costs must be measured and reported fairly (issues 1, 2, 3 and 6).

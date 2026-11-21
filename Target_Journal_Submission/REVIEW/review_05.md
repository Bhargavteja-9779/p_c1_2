# Review 5: dataset validity, leakage and generalisation

**Journal:** Journal of King Saud University – Computer and Information Sciences
**Reviewer:** #5, assigned to dataset validity, leakage and generalisation only

**Material inspected:**
- `manuscript/build/manuscript_filled.md`: abstract, §4.4, §4.7, §5.1–5.2, §5.7, §6.3.3, §6.4, §6.7, §6.8, §7.1–7.3, §8 and the Statements.
- `manuscript/build/supplementary_filled.md`: Tables S1–S3, S5, S15, S17, S18 and Sections S6–S7.
- Code:
  - `code/src/data/openml_ctr23.py`, `code/src/methods/strata.py` and `code/src/models/learners.py` (early-stopping splits);
  - `code/src/models/density.py` (`RobustLSDensity`);
  - `code/experiments/run_benchmark.py`, `refit_scales.py`, `evaluate_from_cache3.py`, `run_grouped.py` and `run_rw.py`;
  - `code/scripts/leakage_audit.py` and `analyze3.py`;
  - `code/config/benchmark.json` and `confirmatory.json`, including the committed version `1762ec0`.
- Results:
  - `tables/S2_leakage_audit.csv`, `tables/D16_grouped.csv` and `results/raw_grouped/*.jsonl`;
  - `results/raw_eval_v3/*.jsonl` and `results/confirmatory/raw_eval_v3/*.jsonl`;
  - `results/confirmatory/raw_contexts/*.npz`, `results/confirmatory/statistics_confirmatory.json` and `results/confirmatory/tables/C3_per_dataset_size.csv`;
  - `results/rw/confirmatory/*.json`.
- Processed data in `data/*.parquet|json` (43 datasets cached; 45034, 45041, 45043, 45046 and 45047 are not cached).
- From the public OpenML API (small JSON and ARFF files only): the membership of suites 335, 336 and 353, the dataset descriptions, and the four CTR23 datasets excluded by the distinct-value rule.
- History: reviews 01–04, 06 and 07, their responses, and `EXPERIMENT_LOG.md`. I do not repeat points that were fixed. Where an earlier request was not met (C1-12, C1-31(d) and C1-32(3)), I say so explicitly.

**How the numbers below were computed:** All are from the authors' own files, using light pandas/numpy/scipy scripts with no refitting.
- Target statistics come from the cached contexts, concatenating `y_train`, `yc` and `yt` for seed 0.
- Realised strata come from the `train_stratum_mass`, `K`, `ncal_strata` and `frac_test_out_domain` fields of the v3 evaluation files.
- Re-tests of the confirmatory size hypotheses apply the same two-sided Wilcoxon signed-rank test to `C3_per_dataset_size.csv`. On all 17 datasets this reproduces the paper's p-values exactly (0.0004 / 0.0038 / 0.0002 / 0.0046 unadjusted; Holm 0.001 / 0.008 / < 0.001 / 0.008).
- Held-out duplicate statistics use the paper's own `load()` with `TSCP_NMAX = 50000` and `split(n, 0)`. They were checked against the cached test targets.

## Summary

The leakage control in the narrow sense is sound. I traced every modelling choice and found no use of calibration or test labels:
- the strata and evaluation grid (`make_partition(y_train)`);
- the domain 𝒴_D and the non-negativity decision;
- the noise density (cross-fitted out-of-fold residuals of the training set);
- the scale floor;
- the early-stopping splits (carved from the training set);
- the ŷ-bins of Mondrian-ŷ;
- the relevance function and its floor τ (`gaussian_kde(ytr)`);
- the evaluation deciles and 1% groups (training quantiles).

The CTR23 eligibility rule was applied as stated. The membership of suites 335 and 336 is fully accounted for, and the 50,000-row cap and the held-out list were committed before evaluation (commit `1762ec0`).

The problems lie in what the held-out collection is and in what the paper says it shows:
1. **Two of the 17 "independent" held-out datasets are the same task.** yprop_4_1 and topo_2_1 have identical rows and identical target values and differ only in their descriptors.
2. **Most held-out targets are on a log scale,** apparently transformed by the benchmark curators. All held-out datasets have at least 4,209 rows. The replication therefore cannot speak to the regimes in which the CTR23 advantage disappeared (strong skew, n < 1,600). Yet the abstract and conclusion state the confirmation without that scope.
3. **The paper's own rationale for excluding ordinal targets is not applied to the held-out set,** and the limitations section states something false about it. visualizing_soil's target is a track index from 1 to 40. seattlecrime6's target is a coded time of day with 20 principal levels.
4. **Data-coding artefacts define whole tail strata.** On house_16H, the 52 records with log-price 0 form the lower stratum. They produce the single largest held-out loss of SDLC against S-NCP.
5. **"Top 1%" is defined two ways.** The two definitions give 0.747 and 0.688 for the same SDLC quantity, and the top 1% is empty on two datasets.
6. **The grouped-split evidence is thinner than presented.** One earlier request (temporal split for Moneyball) was dropped silently, and five held-out datasets are hourly or daily series that were split at random.

None of these overturns the coverage results. My re-analyses show that the confirmatory size conclusions survive:
- removing one of the duplicate pair;
- restricting to the 11 held-out datasets with nominal tail strata;
- restricting to the 10 continuous, non-atom-heavy datasets.

The statements of scope, the dataset documentation and two promised reports need to be corrected.

**Recommendation: major revision.**

---

## Numbered issues

### 1. MAJOR: The held-out set contains a duplicated task (yprop_4_1 ≡ topo_2_1), so the confirmatory replication has 16 independent targets, not 17

**Location:**
- §5.1 line 247 ("removed every dataset sharing source data with CTR23 and duplicate versions").
- Table 8, Table 9, Table S2, Table S17 (rows 45032 and 45041 are identical) and Table S18.
- `code/config/confirmatory.json` (`duplicate_versions_dropped`).

**Evidence:**

*The two datasets are the same rows with the same target.*
- 45032 (yprop_4_1, suite 336, target `oz252`, p = 42) and 45041 (topo_2_1, suite 335, target `oz267`, p = 261) both have n = 8,885 and 1,336 distinct target values.
- In the cached contexts, `y_train`, `yc` and `yt` are element-wise identical (`np.array_equal` is True for every array, seed 0).
- Because n is equal and the split seed is shared, both datasets receive the same partition. They are the same observations with the same response; only the descriptor set differs. The base-model predictions correlate at only 0.68, but the relative RMSE is identical (0.88).
- Table S17 shows the duplication directly: skewness −4.856, octile skewness 0.376 and 1,117 distinct training values for both.

*The duplicated pair is not a neutral member of the replication.*
- It supplies 2 of SDLC's 3 losses to BCCP and both of its losses to S-CQR in C-H3 (`C3_per_dataset_size.csv`: yprop 3.862 vs BCCP 3.831 and S-CQR 3.780; topo 3.906 vs 3.861 and 3.845).
- It supplies both datasets on which RW-DLC loses RW-3 (top-1% coverage of RW-DLC vs SDLC: yprop 0.521 vs 0.779, topo 0.508 vs 0.736; `results/rw/confirmatory`).
- It contributes 2 of the 7 "skewed" held-out datasets in Table S17.

*Re-analysis (two-sided Wilcoxon on log ratios, Holm over 4).* Dropping either member, or averaging the pair on the log scale, gives n = 16 and leaves every C-H3 decision unchanged:

| Comparison | Geometric-mean ratio | Wins | Holm p |
|---|---|---|---|
| SDLC vs BCCP | 0.853 | 14/16 | 0.0009 |
| SDLC vs S-NCP | 0.978 | 14/16 | 0.013 |
| SDLC vs S-CQR | 0.831 | 15/16 | 0.0004 |
| SDLC vs S-HPD | 0.985 | 14/16 | 0.013 |

RW-3 also survives: with n = 14 the mean difference is 0.213 and the one-sided p is 0.003. The conclusions stand, but the reported n, the win counts and the subgroup sizes are wrong.

*Further non-independence among the held-out units, less severe:*
- elevators and Ailerons come from the same F-16 control simulator.
- house_16H (1990 US census, median house price by area) shares source and target type with CTR23's california_housing (1990 census, median house value). The exclusion criterion "sharing source data" is not defined precisely enough to tell whether it should have been excluded.

**Fix:**
1. Report the duplication in §5.1 and Table S2. Because the list was pre-specified, keep the 17-dataset analysis as the pre-specified result and add a clearly labelled post hoc sensitivity analysis with the pair merged (n = 16) for C-H1 to C-H4 and RW-1 to RW-4. Report "15/2" as "14/2 on 16 independent targets" where relevant.
2. Define "content overlap" operationally (same original source or same response variable) and list, for every held-out dataset, its original source. Justify keeping house_16H, or report the analysis without it.
3. Add an automated check to the data pipeline that flags pairs of datasets with identical target multisets, and run it on all 48 datasets. No new model fits are needed.

### 2. MAJOR: The held-out collection is mostly log-transformed, contains no small datasets, and under-represents strong skew; the "confirmed" claims need that scope

**Location:**
- Abstract (line 6: "which a pre-specified analysis plan confirmed on 17 held-out datasets").
- §7.1 line 565.
- §8 line 596.
- §5.1 line 247.
- Tables S2 and S17.

**Evidence:**

*Log scale.* The held-out targets are not on their natural scale. The atoms are exact logarithms:

| Dataset | Atoms observed |
|---|---|
| house_16H | 13.7% at 9.61581 = ln 15,000 (a bottom code) |
| nyc-taxi | 0, ln 2, ln 3, ln 4 |
| Airlines_DepDelay | 0, −ln 2, −ln 3 (a signed log) |
| particulate-matter | ln 9 |
| delays_zurich | ln 20 |

For house_16H, Airlines and delays_zurich, exp(|y|) is an integer or on a 0.01 grid for 100% of rows. For Allstate, SGEMM and nyc-taxi it is on a 0.01 grid for 100% of rows. The OpenML description of SGEMM recommends the logarithm. At least six, and probably eight, of the 17 targets are therefore log-transformed versions of skewed quantities. This is consistent with the curators' preprocessing ("transformed in the same way" in every OpenML description), but the paper never mentions it.

CTR23, by contrast, is on the raw scale. Its training-target skewness reaches 12.8 (forest fires) and 58.95 (brazilian houses), against a held-out maximum of 7.36 (sulfur).

This matters for three reasons:
- **Skewness subgroup.** On CTR23 (Table S5), SDLC's advantage over S-NCP vanished for |skew| > 1 (ratio 0.988, p = 0.127). On held-out data it vanished in the same subgroup (Table S17: 1.017). The held-out set has only 7 such datasets, and 2 of them are the duplicate pair (issue 1).
- **Size is not invariant.** Lebesgue set size on a log scale measures relative width, so held-out size ratios are a different estimand from CTR23 size ratios.
- **Relevance is not invariant.** φ_U = 1/p̂_Y depends on the scale, so "uniform over the target range" means "uniform over log-range" for these datasets. Quantile strata and stratum-wise coverage are invariant, so C-H1, C-H2 and C-H4 are unaffected.

*Size.* The held-out datasets have n = 4,209 to 50,000 (smallest calibration set 1,052). CTR23 has 9 datasets with n < 1,600, on which SDLC was larger than S-NCP (ratio 1.050, 5/4, Table S5) and not significantly smaller than BCCP (0.948). The replication therefore contains no dataset from the regime where the exploratory result failed. Saying that the ordering "was confirmed" on held-out data, without that qualification (§7.1, §8, abstract), extends the confirmation to a regime it never tested.

*Domain balance.* Housing prices make up 4 of 31 CTR23 datasets plus house_16H in the held-out set. Transport delays make up 2 of 17 held-out datasets (Airlines, delays_zurich).

**Fix:**
1. In §5.1 and Table S2, state which held-out targets were log-transformed by the benchmark curators (add a "target scale" column), and give the held-out n range and skewness range next to those of CTR23.
2. Qualify the abstract, §7.1 and §8. For example: "confirmed on 17 held-out datasets with 4,209–50,000 rows, most with log-scale targets; small and strongly skewed targets were not represented".
3. Optional, but cheap and informative: re-run the held-out evaluation on the back-transformed targets (exp or sign·expm1 of y) for the six to eight log-scale datasets. This is a new experiment, and it requires refitting the base models on the back-transformed targets for those datasets × 5 seeds (comparable in cost to the original held-out fit). Report it as post hoc, alongside the pre-specified result. If it is not done, say explicitly that the held-out size results concern log-scale targets.

### 3. MAJOR: The eligibility rule is applied as written but not as justified; the limitation statement about excluded targets is false (C1-12 not adequately fixed)

**Location:**
- §5.1 line 245 (rationale: "Lebesgue set size does not measure informativeness for such ordinal targets").
- §7.3 line 587 ("ordinal, count and temporally dependent targets were excluded").
- Tables S1, S2 and S17.
- Response to C1-12 ("T" only; the requested sensitivity analysis was not run).

**Evidence:**

*The rule as stated holds.* From the OpenML ARFF files, the four excluded CTR23 targets have 8 (solar_flare), 17 (student_performance_por G3), 7 (white_wine) and 6 (red_wine) distinct values. The smallest retained CTR23 target has 28 (abalone). The rule itself is implemented nowhere in code: the excluded IDs are hard-coded in `benchmark.json`.

*The rationale is violated in the held-out set:*
- **visualizing_soil (44056):** the target `track` takes the integer values 1–40, with 93–604 rows each. It is a transect index that the coordinates predict almost deterministically (relative test RMSE 0.017). It is a label, not a quantity, so "rare extreme outcomes" and Lebesgue size have no meaning for it, and its top 1% is empty in every seed (issue 5).
- **seattlecrime6 (45043):** the target `Reported_Time` takes 29 values:
  - 0 (6.0%);
  - 61, 122, 183, 244, 305, 610, …, 1403 (multiples of 61, each 3–6% of rows), giving 20 principal levels;
  - 1–9 (199 of 50,000 rows).

  It passes "at least 20 distinct values" only at the boundary. It is a coded, cyclic time of day: 0 and 1403 are adjacent hours, so the "lower" and "upper" tail strata are neighbours.
- **Count and other discrete targets are retained,** contrary to §7.3:
  - CTR23 includes socmob (a count, 20.1% zeros), abalone rings (a count), Moneyball (team-season panel) and fifa (a wage on a coarse grid, 15.3% at one value).
  - The held-out set includes Bike_Sharing_Demand (an hourly count), Ailerons (35 values, 13.5% at one value) and elevators (61 values, 15.1% at one value).
  - Temporally dependent targets are also retained (issue 6).

*Re-analysis.* Under a rule consistent with the rationale (< 100 distinct values or largest atom > 5%), 7 held-out datasets are flagged: visualizing_soil, elevators, Ailerons, house_16H, nyc-taxi (15.1% zeros), seattlecrime6 and Airlines (18.6% zeros). On the remaining 10 continuous datasets, SDLC vs S-NCP gives a ratio of 0.953 with 10/0 wins (Wilcoxon p = 0.002); vs S-HPD 0.971, 10/0 (p = 0.002); vs BCCP 0.897, 7/3 (p = 0.037). On the 7 flagged datasets, SDLC vs S-NCP is 1.013 (5/2, p = 0.38). The held-out S-NCP/S-HPD advantage is therefore a continuous-target result, which is a useful finding the paper does not state. The same rule flags 8 CTR23 datasets, as in C1-12.

**Fix:**
1. Replace the §7.3 sentence with an accurate one, for example: "targets with fewer than 20 distinct values were excluded; count, heavily discretised and time-indexed targets were retained (list)".
2. Implement the rule in code: report `n_unique_y` for all 35 + 36 candidate IDs, including the excluded ones, in Tables S1 and S2.
3. Report, as a post hoc sensitivity analysis, C-H3 and RW-3 on the continuous subset (largest atom ≤ 5% and ≥ 100 distinct values), and for CTR23 the n = 23 analysis requested in C1-12. Both come from existing result files; no new fits are needed.
4. State in Table S2 what the visualizing_soil and seattlecrime6 targets are, and either flag them as non-quantitative targets or exclude them in a sensitivity analysis.

### 4. MODERATE: Data-coding artefacts define whole tail strata on held-out data, and realised strata are not reported for the held-out set

**Location:**
- §4.4 ("the sensitivity analyses repeat the main comparisons on datasets whose realised tail strata are close to nominal": done for CTR23 only).
- Table S2, which has no K or stratum-mass columns, unlike Table S1.
- §6.3.3.

**Evidence:**

*house_16H (44139).* The target is log(price). The data contain:
- 52 rows with value exactly 0;
- 13.7% of rows at the bottom code ln 15,000;
- nothing in between.

Because the stratum edges are training quantiles with `method='lower'`, the 0.10 quantile equals the bottom code. The lower calibration stratum therefore contains only the zero-price records: realised training mass 0.002–0.003, 10–13 calibration points and 13.6 test points per seed.
- Covering this atom forces sets to reach far below the bulk. SDLC's sets average 4.87 pieces (S-NCP 1.81), and its mean size for test points in the bulk stratum is 5.52 against 3.97 for S-NCP (seed means, `raw_eval_v3`).
- house_16H is SDLC's largest held-out loss to S-NCP: log ratio +0.295, a ratio of 1.34. No other dataset exceeds +0.001.
- The same 52 records make house_16H's skewness −3.43. Without the 27 training zeros of seed 0 it is 0.80, so the dataset moves between the "skewed" and "symmetric" subgroups of Table S17.

*yprop_4_1 and topo_2_1.* A single row has y = 0, while all other targets lie in [0.845, 1]. When that row is in the training set (3 of 5 seeds):
- it sets 𝒴_D = [0, 1.05], so 85% of the RW grid of 4,000 points covers an empty range;
- it turns the skewness from +1.27 into −4.86.

*Other non-nominal held-out strata* (realised training mass of the tail strata, nominal 0.10):

| Dataset | Lower stratum | Upper stratum | Other |
|---|---|---|---|
| nyc-taxi | 0.18–0.25 (zeros) | | K = 4 |
| Ailerons | | 0.21–0.22 | |
| visualizing_soil | 0.043–0.049 | | |
| elevators | 0.036–0.100 | | |
| seattlecrime6 | 0.064–0.100 | 0.117–0.124 | |

Six of the 17 held-out datasets therefore have non-nominal tail strata. None of this is visible in the paper.

*Re-analysis.* On the 11 held-out datasets with nominal tail strata, C-H3 still holds:

| Comparison | Ratio | Wins | p |
|---|---|---|---|
| SDLC vs S-NCP | 0.953 | 11/0 | 0.001 |
| SDLC vs S-HPD | 0.973 | 11/0 | 0.001 |
| SDLC vs BCCP | 0.902 | 8/3 | 0.024 |
| SDLC vs S-CQR | 0.946 | 9/2 | 0.010 |

**Fix:**
1. Add realised K, lower and upper stratum masses and the minimum calibration count per stratum to Table S2, as in Table S1.
2. Run the "nominal tail strata" sensitivity analysis on the held-out data and report the numbers above.
3. Name the house_16H zero-price records and the yprop/topo zero, and report the house_16H and yprop/topo results with these records removed by a pre-declared, training-only plausibility rule. C1-33 asked for such a rule for brazilian_houses; it applies here too. This needs a re-evaluation of two to three datasets × 5 seeds.

### 5. MODERATE: "Top 1%" is defined inconsistently, is empty or nearly empty on discrete targets, and the same SDLC quantity is reported as 0.747 and 0.688

**Location:**
- §6.3.3 line 431 ("SDLC covered 0.747 of the top 1%").
- §6.4 lines 455 and 459, and Table 9 ("0.688 for SDLC").
- §7.2 item 1 line 573 ("covered the top 1% at close to the nominal level").
- §8 line 596.
- Code:
  - `evaluate_from_cache3.eval_strata3` uses `searchsorted(..., side='right')`, so the top group is y ≥ q₀.₉₉.
  - `run_rw.py` uses `top = yt > q99`, a strict inequality.

**Evidence:**

*Two definitions of the same quantity.* The main pipeline includes ties at q₀.₉₉; the RW pipeline excludes them.
- On the held-out data, SDLC's top-1% coverage is 0.747 over 17 datasets in the main pipeline and 0.688 over 15 datasets in the RW pipeline.
- The top group is undefined for visualizing_soil and seattlecrime6 in all 5 seeds, because their maximum is an atom at q₀.₉₉.
- In the main pipeline the same group holds 1.1% (visualizing_soil) and 3.15% (seattlecrime6, the 1403 atom) of the test points.

*Ailerons.* The RW "top 1%" contains 1–4 test points per seed (0.06% of the test set), against 1.9% in the main pipeline. SDLC's coverage there is 0.200 (RW) against 0.760 (main).

*Effect on RW-3.* Ailerons alone moves the RW-3 mean difference from 0.143 to 0.184. Without Ailerons, RW-3 still holds: n = 14, 12/14 positive, one-sided p = 0.021.

*Per-dataset range.* RW-DLC's top-1% coverage ranges from 0.508 (topo_2_1) and 0.521 (yprop_4_1) through 0.781 (Airlines) to 0.988. "Close to the nominal level" (§7.2) describes the mean, not a typical dataset.

**Fix:**
1. Use one definition throughout. Preferably define the extreme groups by rank with random tie-breaking, as asked in C1-08(4), or report the realised share of test points in the group and mark it undefined below a minimum count, for example 10 test points per seed.
2. Recompute the secondary top-1% results and RW-3 with that definition (from cache; no refits).
3. Report the number of datasets and the per-dataset range wherever top-1% coverage is quoted, and change §7.2 to "on average 0.872 (range 0.51–0.99 over 15 datasets)".

### 6. MODERATE: The grouped-split evidence is thinner than presented; temporal structure is untested, and seed-level coverage dispersion under grouping is hidden

**Location:**
- §5.2 line 251, §6.7 line 547, §7.3 line 587 and Table S15.
- `run_grouped.py`.
- Response to C1-31 (item (d), a temporal split for Moneyball, was not done and is not mentioned).

**Evidence:**

*Dispersion under grouping is averaged away.* With video_transcoding split by video (1,099 videos; 0% of test videos seen in training), coverage varies widely across the 5 seeds (`raw_grouped/44974_*.jsonl`):

| Method | Marginal coverage per seed | Worst-stratum coverage per seed |
|---|---|---|
| SDLC | 0.788 to 0.935 | 0.750 to 0.893 |
| BCCP | 0.807 to 0.931 | 0.743 to 0.893 |
| S-CQR | 0.857 to 0.901 | 0.647 to 0.866 |

Table S15 reports only seed means (SDLC 0.900 marginal, 0.873 worst stratum). For a deployment on new videos, the per-calibration-set guarantee is much weaker than the averages suggest.

The grouped analysis also changes the ranking: SDLC/BCCP = 0.775/0.643 = 1.205, and S-CQR (0.516) is smaller than SDLC. The paper reports this correctly in §6.7, but the abstract and §8 do not.

*Coverage of repeated and serial structure.*
- Only three datasets were tested.
- Units known from C1-31 remain untested: Moneyball (team × season), kings_county (repeat sales) and the 82% test-feature overlap of cps88wages (Table S3). For cps88wages I accept that coarse demographics create identical feature vectors without repeated persons, so this is not a leak.
- Five held-out datasets are time-indexed and were split at random:
  - Bike_Sharing_Demand (hourly, 2011–2012);
  - particulate-matter-ukair-2017 (hourly);
  - nyc-taxi (December 2016);
  - delays_zurich_transport;
  - Airlines_DepDelay.

  Random splits there measure interpolation between neighbouring hours.
- §5.2 and §7.3 correctly say the guarantees refer to "a new row from the same pool". The efficiency conclusions, however, are stated without this qualification.

*Unreported held-out duplicates.* The leakage audit (Table S3) does not cover the held-out datasets. My run of the authors' audit logic on the 12 cached held-out datasets finds:
- Mercedes_Benz: 21.9% duplicate feature vectors, and 24.7% of test feature vectors present in training (seed 0);
- Bike_Sharing: 2.3%;
- yprop_4_1: 1.2%;
- all others below 0.2%.

**Fix:**
1. Add the per-seed minimum and maximum of marginal and worst-stratum coverage to Table S15.
2. Run the temporal split for Moneyball by season (C1-31(d); 1,232 rows, 5 seeds, minutes of CPU time).
3. Run a blocked-by-time split for Bike_Sharing_Demand (contiguous blocks of days, using its year/month/hour features) as a held-out temporal check. If the curated features no longer identify time, say so.
4. Add one sentence to the abstract or §8 limiting the efficiency claims to random splits of the same pool.
5. Extend `leakage_audit.py` to the 17 held-out datasets, report it in Table S3, and run it for all seeds, not seed 0 only. This needs no fits.

### 7. MODERATE: The fraction of test targets outside 𝒴_D is promised but not reported (C1-32 item 3 not met)

**Location:**
- §4.4 line 185 ("We report the fraction of test targets outside 𝒴_D and how often q̂_k = +∞ occurs").
- `code/scripts/analyze3.py` lines 175 and 182 compute `frac_test_out_domain_max/mean`, but neither the manuscript nor the supplement prints them.

**Evidence:**
- The forest fires domain is decided by whether the 1,090.84 ha fire falls in the training set. In 3 of 10 seeds, 1, 1 and 3 test targets lie above max(y_train) + 0.05Δ and are therefore automatic misses.
- In seed 8, 3 of the 20 upper-stratum test points are out of domain, which caps upper-stratum coverage at 0.85 (observed 0.850).
- Other non-zero out-of-domain maxima:

| Dataset | Out-of-domain maximum per run |
|---|---|
| cars | 0.50% |
| QSAR fish | 0.44% |
| space_ga | 0.39% |
| Moneyball | 0.32% |
| Mercedes (held-out) | 0.19% |

- Forest fires also has realised K = 3 with a 74.4% lower stratum (Table S1). Its middle stratum receives only 7–24 calibration points, so q̂ = +∞ in seed 5 (7 points).

The effect on dataset means is small. However, the stratum-wise coverage of forest fires rests on 3–20 test points per stratum and seed, and the paper promised this report.

**Fix:** Add per-dataset mean and maximum out-of-domain fractions, and the stratum in which they fall, to Table S1 and Table S2. Note in §6.1 that forest fires' upper-stratum misses include out-of-domain targets. No computation beyond the existing `analyze3.py` output is needed.

### 8. MINOR: Subsampling above 50,000 rows is described only in a table caption, and is inconsistent with CTR23

**Location:**
- §5.1 line 247 ("with up to 50,000 observations").
- Table S2 caption.
- `openml_ctr23.load` (`TSCP_NMAX`).

**Evidence:**
- Eight held-out datasets were reduced to one fixed subsample (rng 2026) shared by all seeds: particulate-matter 394,299 → 50,000; SGEMM 241,600; nyc-taxi 581,835; medical_charges 163,065; delays_zurich; seattlecrime6; Allstate; Airlines_DepDelay_1M (about 5% of 1M).
- The cap was pre-specified (it is present in commit `1762ec0`), which is good.
- The main text does not say that rows were subsampled.
- Seed-to-seed variation does not include subsample variation.
- CTR23 datasets above 50,000 rows (diamonds 53,940, video 68,784, wave 72,000) were not subsampled.
- Table S2's "Distinct y" is computed on the subsample (particulate matter 6,195 vs 21,599 in full), while the rule was applied to the full data. Table S17's `n_distinct` is a third quantity (training targets of one seed).

**Fix:**
1. State the subsampling in §5.1 and why CTR23 was not capped.
2. Report distinct values on the full data (the quantity the rule used) in Table S2.
3. Use one definition of "distinct values" across Tables S1, S2 and S17.

### 9. MINOR: Data availability, licences and ethics statements are inaccurate in details

**Location:**
- Statements (lines 669–673).
- Tables S1 and S2 ("Licence").
- `.gitignore` and the tracked result files.

**Evidence:**
- The Data availability statement says "the OpenML identifier and licence of each dataset are listed in Supplementary Tables S1 and S2". Table S1 has no OpenML IDs.
- "Public", the entry for 10 CTR23 and 11 held-out datasets, is not a licence.
- socmob is licensed "Non-commercial scholarly and teaching purposes" and health_insurance "GPL (>= 2)". The code package tracks 513 context files (`git ls-files results | grep contexts`) that contain the training, calibration and test target values of every dataset and seed. Depositing these "in a public repository upon acceptance" redistributes derived data, so the licence terms of these datasets should be checked and stated.
- The ethics statement says the study "involved no … personal data". cps88wages and health_insurance are individual-level survey microdata, and seattlecrime6 contains crime reports. They are de-identified, which the statement also says, but "no personal data" is too strong.

**Fix:**
1. Add an OpenML ID column to Table S1.
2. Replace "Public" by the licence on the original source page, or by "not stated on OpenML".
3. State the licence under which the derived per-run files are released, and exclude or aggregate the target values of datasets whose licences restrict redistribution.
4. Change the ethics sentence to "publicly available, de-identified data, including individual-level survey records".

### 10. MINOR: The pre-specified CTR23 arm of the relevance-weighted study is not reported

**Location:**
- §5.7 line 291, §6.4 and Table S18.
- Plan S7 §2 ("Exploratory: all 31 OpenML-CTR23 datasets … The same analysis is run on both").

**Evidence:**
- `results/rw/` contains only `confirmatory/`.
- Table S18's "suite" column has only the value "confirmatory".
- The manuscript reports RW-DLC on the held-out data only and does not mention the CTR23 arm. I understand from the project files that this run is in progress. Under the authors' own plan ("Negative or null outcomes will be reported whatever their direction"), it must appear in the paper.

**Fix:**
1. Report RW-1 to RW-4 on CTR23 in Table S18 and one sentence in §6.4.
2. If the run is not finished, list it as a deviation in §5.7.
3. Apply the single top-1% definition of issue 5 to both arms.

---

## Points checked and found adequate

- **Training-only modelling.** Strata, grid, domain, non-negativity, noise density (cross-fitted OOF residuals), scale floor, early stopping, Mondrian-ŷ bins, relevance KDE and τ all use the proper training set only. I found no use of calibration or test labels in any modelling choice (`run_benchmark.fit_context`, `refit_scales.py`, `evaluate_from_cache3.build_context`, `run_rw.run`). σ̂-deciles of the test set are an evaluation device, not a modelling choice. The design-level adaptivity (v3 choices made after seeing CTR23 results) is already acknowledged in §5.7.
- **CTR23 rule.** The excluded targets have 6–17 distinct values (verified from OpenML ARFF files); all retained targets have ≥ 28.
- **Suite accounting.** All 36 IDs of suites 335 and 336 are accounted for in `confirmatory.json`: 19 candidates, 12 IDs excluded for content overlap and 5 duplicate versions. The held-out list and `n_max` were fixed in commit `1762ec0` before any confirmatory fit, and the evaluation asserts that cached targets match the split.
- **Exact duplicates across splits in CTR23.** Sarcos (9.1%) and cps88wages (7.6% duplicate rows) do not invalidate the row-level guarantee under random splitting, and the sarcos de-duplicated rerun changes sizes only slightly (0.356 → 0.373). The text reports this correctly.

## Overall assessment for the editor

Leakage control is clean, and the CTR23 eligibility rule was applied as stated. The coverage conclusions are not threatened by anything in my remit.

The generalisation claims are a different matter:
- The "confirmatory replication on 17 held-out datasets" contains a duplicated task.
- Most of its targets are log-transformed.
- Its eligibility rationale is not applied consistently (two targets are a track label and a coded time of day).
- Some of its tail strata are made of zero-price records.
- It contains no dataset in the small-n or strong-skew regime where the exploratory CTR23 result failed.

My re-analyses from the authors' own result files show that the pre-specified size decisions survive each of these corrections. The paper's own subgroup results further suggest that the SDLC-over-S-NCP advantage is a property of continuous, moderately skewed targets.

The fixes are mostly re-analyses of existing files and corrections of wording. The only new computations I request are small: a temporal split for Moneyball and Bike sharing, an optional re-fit on back-transformed held-out targets, and a re-evaluation without the zero-coded records. One sentence in §7.3 is factually wrong and should be corrected in any case.

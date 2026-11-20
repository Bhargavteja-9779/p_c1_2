# Review 3: statistical validity, experimental fairness and leakage

**Manuscript:** "Covering the rare outcomes: stratified conformal prediction with size-optimal density scores for imbalanced regression" (JKSU-CIS submission)
**Reviewer:** #3 (statistics, fairness, leakage, pre-registration compliance)
**Material inspected:** `manuscript/build/manuscript_filled.md`, `supplementary_filled.md`, `code/src/statistics/tests.py`, `code/scripts/analyze3.py`, `code/scripts/analyze_confirmatory.py`, `code/scripts/analyze.py` (null reference), `code/experiments/{run_benchmark,refit_scales,evaluate_from_cache3,tail_alerts,run_denseweight,run_learner_generality3}.py`, `code/src/models/learners.py`, `code/src/data/openml_ctr23.py`, `code/src/methods/{strata,ls_exact3}.py`, `code/config/*.json`, `results/statistics_v3.json`, `results/metrics_v3.json`, `results/confirmatory/statistics_confirmatory.json`, raw per-run files, and the git history (`git log --follow PREREGISTRATION_confirmatory.md`, `git diff ccba99b HEAD`). Issues already raised in `REVIEW/review_01.md` are not repeated unless the revision introduced a new form of them.

---

## 1. Summary

The paper benchmarks stratified (Mondrian, label-conditional) conformal calibration and a density-score variant (SDLC) on 31 CTR23 datasets, plus a 17-dataset replication run under an analysis plan the authors call pre-registered. I checked the code, not only the text. The basic pipeline is sound:

- **Splits and leakage.** Splits come from predefined seeds (0–9; 0–4 for the replication). Strata, domain, noise density and every model are fitted on the proper training set. Test targets are used only to decide membership.
- **Tests.** The tests reported are the ones implemented, with the stated sides: one-sided only for the coverage hypotheses.
- **Pre-registration.** The confirmatory script was not edited after the plan was committed. The only later changes are a NaN-safe Holm function and a guard for n < 3, and neither changes any number.
- **Numbers.** All 23 numbers I sampled match the result files (Section 3).

The problems lie in what the statistics are taken to show:

1. **The size test and the size effect measure different things.** The Wilcoxon test is about the typical dataset, while the effect reported and used for direction is the geometric mean. For the information-matched comparators, the two disagree.
2. **Pre-registered secondary analyses are missing.** Some of them are unfavourable to SDLC, and they are not reported.
3. **"Made public before evaluation" cannot be verified,** and the paper's own code-availability statement contradicts it.
4. **The replication sample probably under-represents skewed targets,** which is where SDLC's advantage on CTR23 disappeared.
5. **Three of the four confirmatory hypotheses could not have failed,** because they follow from Theorem 1.
6. **The decision study leaves out its most relevant comparison.** On cost, S-NCP alerts beat SDLC alerts on almost every dataset.

## 2. Recommendation

**Major revision.** Nothing is fatal: coverage validity is intact and the numbers are reproducible. However, the size-efficiency claim in the abstract and conclusion ("smallest stratum-valid sets", "a pre-registered replication ... confirmed the ordering") rests on an incoherent estimand and on selective reporting of pre-registered results. It needs re-analysis and rewording before acceptance.

## 3. Verification log

### 3.1 Numbers checked against result files (all match)

| # | Manuscript (line) | Value | Source |
|---|---|---|---|
| 1 | Table 3, SDLC worst stratum / size (l. 303) | 0.891 / 0.874 | `metrics_v3.json` main.SDLC-LS: 0.8906 / 0.8742 |
| 2 | Table 3, SDLC empty % / pieces | 0.36 / 1.53 | empty_rate 0.0036, pieces 1.5265 |
| 3 | §6.3 top-1% SDLC vs S-NCP, S-HPD; Holm p (l. 375) | 0.736 vs 0.789, 0.790; 0.031, 0.017 | `statistics_v3.json` "Extreme coverage" ext1_cov_2: p_holm 0.0312, 0.0170 |
| 4 | §6.3 worst σ-decile (l. 375) | 0.769 vs 0.793 | sigma_decile_worst 0.7688 / 0.7934 |
| 5 | Table 6 SDLC vs BCCP (l. 354) | 0.902 [0.841, 0.956], HL 0.933, 24/7 | 0.9025 [0.8410, 0.9565], 0.9334, 24/7 |
| 6 | Table 6 SDLC vs S-NCP (l. 355) | 0.975 [0.941, 1.020], HL 0.962, 27/4, Holm < 0.001 | 0.9748 [0.9412, 1.0195], 0.9615, 27/4, 0.0003 |
| 7 | Table 6 S-NCP vs BCCP (l. 360) | 0.926, 18/13, p 0.111 | 0.9258, 18/13, 0.1110 |
| 8 | Table 6 hull SDLC vs S-NCP (l. 364) | 1.014, 23/8, Holm 0.034 | 1.0144, 23/8, 0.0338 |
| 9 | Table 4 DLS → SDLC (l. 327) | 1.24 [1.12, 1.45], median 1.11, 3, +0.231 | 1.243 [1.119, 1.447], 1.113, 3, 0.231 |
| 10 | Table 5 NCP row (l. 336) | 0.858, 1.005, 28/31 | matched_coverage: 0.858, 1.005, 28 |
| 11 | §6.1 HL differences (l. 308) | 0.081–0.250 | H1 worst-stratum hl 0.0812–0.2496 |
| 12 | §6.3 sensitivity, "Holm p ≤ 0.002" (l. 348) | ≤ 0.002 | max is alpha = 0.05 vs S-NCP: 0.0019 |
| 13 | §6.3 skewed subset, S-NCP (l. 348) | 12/3, Holm 0.127 | 12/3, 0.1274 |
| 14 | Table 8 C-H3 BCCP (l. 426) | 0.862 [0.785, 0.932], 14/3, 0.001 | 0.862 [0.7849, 0.9324], 14/3, 0.0011 |
| 15 | Table 8 C-H3 S-NCP (l. 427) | 0.977 [0.940, 1.028], 15/2, 0.008 | 0.9772 [0.9398, 1.0278], 15/2, 0.0077 |
| 16 | Table 8 C-H2 (l. 425) | 1 of 17, critical value 3, 0.582 | 1, 3, 0.5819 |
| 17 | Table 8 C-H4 TOST | < 0.001 / < 0.001 | 7.6e-6 / 5.3e-5 |
| 18 | §6.5 secondary (l. 412) | 0.747 vs 0.781; 0.817 vs 0.831; 1.22 | summary.SDLC-LS / S-NCP; price_vs_DLS_geo 1.2206 |
| 19 | §6.9 Spearman (l. 506) | 0.62, −0.41 (0.022), 0.38 (0.034), 0.47 (0.008) | error_analysis: 0.619, −0.409 (0.0225), 0.382 (0.034), 0.465 (0.0083) |
| 20 | §6.8 MLP (l. 496) | 0.946 (0.019), 0.938, 0.927 | learners.mlp |
| 21 | §6.7 alerts (l. 462–464) | 1.559, 0/31; r=10: 14/31, p 0.130; r=20: 22, p 0.083 | alerts rows 0, 5, 11 |
| 22 | §6.6 ESS (l. 436) | median 49, min 5.9, 15 datasets | ess_up2_median 49.3, min 5.90, 15 |
| 23 | §6.8 DenseWeight (l. 498) | 0.630 → 0.759; 0.720 → 0.775; 1.31 / 1.45; ratios 0.906, 0.948, 0.694, 0.964 | learners.dw, dw_vs_lgb |

### 3.2 Pre-registration compliance

- **Order of commits.** `git log --follow PREREGISTRATION_confirmatory.md` and the history of `code/scripts/analyze_confirmatory.py` both show a single commit, `ccba99b` (2026-11-18 09:49:14 UTC). The confirmatory results were first committed in `c3cad49` (10:10:20) and `adeec38` (10:17:20). The dataset list was fixed earlier, in `1762ec0` (2026-11-17).
- **Changes to the pipeline after the plan.** `git diff ccba99b HEAD` on the pipeline shows two changes:
  - `refit_scales.py`: the task list is now discovered from the cache.
  - `src/statistics/tests.py`: NaN-safe `holm`, and a guard for n < 3 in `paired_summary`.

  With 17 complete datasets neither change alters any value. **The analysis follows the script.**
- **Deviations from the written plan.** See R3-02 and R3-03:
  - pre-registered secondary analyses are not reported (S10 strata, hull variants);
  - pre-registered effect sizes are not shown in Table 8 (Hodges–Lehmann ratio with CI, sign test);
  - "public" is asserted but not demonstrated.

### 3.3 Seeds, splits, leakage

- **Seeds.** Split seeds are fixed in `config/benchmark.json` (0–9) and `config/confirmatory.json` (0–4), with `run_benchmark.py:34–40`. Other fixed seeds: LightGBM `random_state = seed`, early-stopping split `random_state = seed`, calibration subsample `10_000 + seed`, alert rule `20_000 + seed`, and confirmatory subsample 2026. The auxiliary studies use leading subsets of the predefined seeds (DenseWeight 0–2, MLP 0–4, grouped 0–4). **I found no evidence of post-hoc seed selection.**
- **Training-only fitting.** Strata (`strata.py`), the domain D, the floor ς and the noise density all use training targets or residuals only. Early stopping uses a 10% split of the proper training set (`learners.py:27`).
- **Use of test targets.** Test targets enter `ls_methods` only through the exact membership rule (`ls_exact3.py:346–368`).
- **Residual leakage.** The remaining minor leaks are listed in R3-11 and R3-12.

---

## 4. Issues

### MAJOR

#### R3-01 (MAJOR) The size test and the size effect measure different things, and the pre-registered decision rule mixes them

**Location:** §5.6 (l. 268), §6.3 (l. 346), Table 6, §6.5 C-H3 (l. 409), Table 8, abstract ("confirmed the ordering (size ratios between 0.841 and 0.984)"), PREREGISTRATION §3 C-H3, `analyze_confirmatory.py:98–102`.

**Evidence:**
- **Two quantities.** The test is a Wilcoxon signed-rank test on per-dataset log size ratios. It is a test about the pseudo-median, that is, the typical dataset. The effect that is reported, and that the decision rule uses for direction (`r["geo_ratio"] < 1`), is the geometric mean, i.e. the mean log ratio.
- **They disagree for S-NCP and S-HPD.** The distribution of log ratios is strongly skewed: many small wins and a few large losses. Examples are socmob at 1.64 on CTR23 and house_16H at 1.343 on the replication.
  - CTR23, SDLC vs S-NCP: Holm p = 0.0003, but GM 0.975 with 95% CI [0.941, 1.020].
  - Replication, SDLC vs S-NCP: GM 0.977 [0.940, 1.028], declared "favours SDLC".
  - Replication, SDLC vs S-HPD: GM 0.984 [0.963, 1.014], declared "favours SDLC".
  - The same pattern holds with the S-NCP CI including 1 for alpha = 0.05, S3, S10, and after excluding the development and diagnostic datasets (`statistics_v3.json` h3_sensitivity).
- **The decision rule gives perverse answers.** SDLC-hull vs S-NCP-hull on CTR23 has GM 1.014, Holm p = 0.034, and SDLC wins on 23 of 31 datasets. Under the pre-registered C-H3 rule, this comparison would be declared "favours comparator", even though SDLC wins on 23/31 and the HL ratio is 0.979. A rule whose direction can contradict its own test is not well defined.
- **No smallest effect of interest was set.** A two-sided test of "any difference" with n = 17 declared a 1.6% (S-HPD) and a 2.3% (S-NCP) GM reduction a confirmed ordering, although the CIs include 1.

**Fix:**
1. Declare one estimand for size. Either:
   - (a) the pseudo-median: report the HL ratio with its Wilcoxon-inversion CI as the effect, and decide direction by the HL ratio (replication HL CIs: S-NCP 0.973 [0.948, 0.988], S-HPD 0.980 [0.965, 0.991]); or
   - (b) the mean log ratio: test it with a paired t-test or a bootstrap test on log ratios.
2. Report the pre-registered result as it stands, then add the re-analysis as clearly labelled post hoc.
3. Rewrite the abstract and §8 to say that, for S-NCP and S-HPD, the typical dataset shows a 2–3% reduction while the mean ratio is not distinguishable from 1.
4. Add a TOST equivalence test on log size, SDLC vs S-NCP and vs S-HPD, with a stated margin (for example ±5%, as review_01 C1-02 suggested). Without it, "smallest" cannot be separated from "practically equivalent".

#### R3-02 (MAJOR) Pre-registered secondary analyses are omitted, and one of them is unfavourable

**Location:** PREREGISTRATION §3 ("Effect sizes are reported for every comparison: ... the Hodges–Lehmann ratio with its 95% CI, wins/losses and the sign test") and §4 ("the C-H3 comparisons under decile strata (S10); hull variants"); manuscript §6.5 and Table 8; Supplement (no confirmatory S10 or hull table; lines 186–189 are CTR23 only, n = 31).

**Evidence:** I recomputed these from `results/confirmatory/raw_eval_v3` with the committed `analyze_confirmatory.per_dataset`.
- **Hull variants.** SDLC-hull vs S-NCP-hull: GM ratio **1.040** [0.980, 1.144], 10/7, two-sided Wilcoxon p = 0.71. SDLC-hull is not smaller than S-NCP-hull on the held-out data. (SDLC-hull vs BCCP-hull: 0.893 [0.817, 0.964], 13/4, p = 0.007.) The geometric-mean sizes in `statistics_confirmatory.json` summary agree: SDLC-hull 1.363, S-NCP-hull 1.311.
- **S10 strata.** In `statistics_confirmatory.json` "C-H3_S10_descriptive", SDLC vs S-NCP has GM 0.988 [0.958, 1.034], 14/3, unadjusted p = 0.013. None of this is reported.
- **Table 8.** It omits the pre-registered HL ratios and sign tests, which the script computes.
- **Effect on the guidance.** Guidance §7.2(4) ("SDLC-hull is valid and remains smaller than BCCP-hull, but it loses part of the advantage") and §6.3 rely on CTR23 only. On held-out data the hull advantage over S-NCP-hull does not exist.

**Fix:**
1. Add a table, "Confirmatory replication: pre-registered secondary analyses", with S10 C-H3 and the hull comparisons (vs BCCP-hull and S-NCP-hull).
2. Add the HL ratio with CI and the sign-test p to Table 8.
3. State in §6.5, §7.2(4) and §8 that, when an interval is required, SDLC-hull did not beat S-NCP-hull on held-out data.

#### R3-03 (MAJOR) "Made public before evaluation" cannot be verified and contradicts the code-availability statement; base-model test metrics existed before the plan

**Location:** abstract and contribution 3 (l. 24: "an analysis plan that was made public before evaluation"), §5.7 (l. 276: "committed it to the public repository"), Supplement S6 (l. 409–417), Statements: Code availability (l. 587: code "will be deposited in a public repository [repository URL] upon acceptance").

**Evidence:**
- **Where the plan lives.** The plan sits on a feature branch (`claude/amazing-maxwell-i1mihd`) of an author-controlled GitHub repository. Git author and commit dates are set by the client and can be rewritten. No third-party registry, DOI or hash is cited.
- **A contradiction.** The paper says the code will become public only upon acceptance. It cannot also claim that the plan was "made public" beforehand.
- **What existed before the plan.** The plan itself says model fitting "may be in progress". The fit-only files `results/confirmatory/raw/*.jsonl` contain, for every confirmatory dataset and seed, the **test-set** negative log-likelihood of the very location–scale density used by SDLC (`test_nll_LS`), the test NLL of the histogram density and the test RMSE. This is outcome-relevant information about the held-out data. The plan says fitting "produces only base-model outputs ... and no conformal-method result", which is literally true but omits this.
- **Timing.** All 85 evaluations and the analysis were committed 21–28 minutes after the plan.

**Fix:**
1. Replace "made public" and "public repository" with "committed to version control (commit ccba99b)".
2. Give the GitHub server-side push time of that commit (for example from the repository events API), not the client-side author date.
3. Deposit the plan, the script and their SHA-256 hashes on OSF or Zenodo now, and say explicitly that this deposit post-dates the evaluation.
4. Disclose that base-model test-set metrics for the confirmatory data had been computed, and possibly viewed, before the plan was fixed.
5. Do not use the word "pre-registered" in the abstract unless a third-party time stamp exists. Review_01 C1-01 required the same for the main benchmark, and the same standard applies here.

#### R3-04 (MAJOR) The replication sample may under-represent skewed targets, which are exactly where SDLC's advantage vanished on CTR23

**Location:** §5.1 "Confirmatory datasets" (l. 232), §6.5, abstract.

**Evidence:**
- **On CTR23, SDLC's advantage over S-NCP depends on skewness.** On the 15 datasets with |skewness| > 1, the advantage was not significant: GM 0.988 [0.920, 1.082], 12/3, Holm p = 0.127; vs S-CQR, Holm p = 0.127. On the 16 less-skewed datasets it was clear: GM 0.963 [0.947, 0.977], 15/1 (h3_sensitivity rows 16–23).
- **The replication targets.** They come from the Grinsztajn et al. (2022) benchmark, whose curation preprocesses targets; my recollection is that heavy-tailed regression targets are log-transformed. The targets in `data/*.parquet` fit that:
  - targets that are strongly right-skewed in their original form have small skewness here: SGEMM run time 0.79, medical charges 0.88, NYC taxi tip −0.00, particulate matter −0.54;
  - only 7 of the 12 locally available confirmatory targets have |skew| > 1.
- **The paper's framing.** The paper is framed around "rare, extreme outcomes" in imbalanced regression. A replication on de-skewed targets tests the favourable regime, not the one in the title.

**Fix:**
1. Report the skewness, octile skewness and any source-side transformation of every confirmatory target in Table S2.
2. Report the confirmatory C-H3 comparisons by skewness subgroup, descriptively.
3. If targets were log-transformed by the source, say so in §5.1 and §7.3, and either re-run on the untransformed targets as a further, labelled-exploratory analysis or limit the claim accordingly.

### MODERATE

#### R3-05 (MODERATE) Three of the four confirmatory hypotheses follow from Theorem 1, so "all four hypotheses were supported" overstates the empirical confirmation

**Location:** §6.5 (l. 405), abstract, conclusion, cover letter.

**Evidence:**
- **C-H2 and C-H4 hold by construction.** C-H2 (worst-stratum coverage consistent with exact validity) holds for any score under stratified calibration, by Theorem 1. C-H4 (equivalence of SDLC's worst-stratum coverage with S-NCP's and BCCP's) holds because all three are stratified.
- **C-H1 was not in doubt.** Higher worst-stratum coverage than marginal methods is implied by Theorem 1 together with §3.1 and the CTR23 results. Nothing specific to SDLC is tested.
- **Only C-H3 tests SDLC, and its result for S-NCP and S-HPD is a 2% reduction** (see R3-01).

**Fix:** Present C-H1, C-H2 and C-H4 as manipulation and validity checks, and C-H3 as the only confirmatory test of the method. Replace "all four hypotheses were supported" with a sentence about C-H3.

#### R3-06 (MODERATE) Decision study: the most relevant comparison is left out, and the p-values are not adjusted

**Location:** §6.7 (l. 462–464), Table 10, guidance §7.2(5), `analyze3.py:573–646` (no Holm call).

**Evidence:**
- **S-NCP is cheaper than SDLC.** On expected cost, S-NCP alerts beat SDLC alerts on **27/31 datasets at r = 10 and 29/31 at r = 20** (p < 0.001; `statistics_v3.json` alerts rows "cost r=10/20: SDLC vs S-NCP": SDLC wins 3/31 and 1/31).
- **HPD-split is cheaper too.** HPD-split alerts are cheaper than SDLC's on 28/31 datasets at both ratios.
- **What the text says instead.** The text says that "set-based alerts with stratum-wise coverage are the cheapest at the highest ratios" and that SDLC "was cheaper than TC-LS on 22 datasets", but it never states that another stratified score dominates SDLC for alerts.
- **Unadjusted p-values.** About 14 comparisons per side are made without Holm adjustment; the p-values quoted (0.130, 0.083) are raw.
- **Unreported cost ratio.** r = 5 is computed (`ratios=(1, 5, 10, 20)`) but not reported.

**Fix:**
1. Report SDLC vs S-NCP in the text and add it to the cost discussion.
2. Apply Holm within a defined alert family, or label all alert p-values as unadjusted and descriptive.
3. Report r = 5, or drop it from the code.
4. Rewrite §7.2(5) to say that, among stratified scores, S-NCP gives the cheapest alerts.

#### R3-07 (MODERATE) Dataset-level wins are not separated from split-to-split noise

**Location:** wins/losses columns in Tables 6 and 8; §6.3 and §6.5 ("the reduction occurs on most datasets").

**Evidence:** Wins are counted on 5- or 10-seed means without checking whether a dataset's difference exceeds its own seed variability. For the replication, SDLC vs S-NCP, I computed per-dataset log ratios over the 5 seeds (mean, SD, t):
- **7 of the 15 "wins" have |t| < 2.78** (the 97.5% quantile of t with 4 df): 44056, 44061, 44069, 44143, 44145, 45032 and 45046.
- **One "loss" is clearly real:** house_16H, mean log ratio +0.33, t = 3.0.
- **Consequence.** "15/2" therefore overstates how consistent the advantage is. The sign-test p-values quoted as corroboration rest on the same noisy signs.

**Fix:**
1. Fit a linear mixed model to per-run log size, with method as a fixed effect, a random dataset intercept and slope, and seed nested in dataset. Alternatively, report per-dataset 95% CIs of the log ratio across seeds.
2. Report the number of datasets with a reliably positive or negative effect.
3. Keep the dataset-level Wilcoxon as the primary test, but stop using raw win counts as evidence of consistency.

#### R3-08 (MODERATE) Holm families are undefined and ad hoc, and some displayed Holm p-values belong to a different family than the table suggests

**Location:** §5.6 ("Holm's step-down correction within each family"; families never defined), Table 6, `analyze3.py:196–222`.

**Evidence:**
- **How the code defines families.** It forms about 10 families on CTR23 alone, plus 12 sensitivity families, each at α = 0.05 with no overall control. Family size changes the reported p, and families were set after the results were known (the CTR23 analysis is exploratory, see §5.7).
- **The same comparison in two families.** SDLC vs SDLC-N appears in both "H3 size (secondary)" and "Decomposition", with Holm p = 0.0676 in each.
- **A mislabelled display family.** Table 6's "Density estimator" family shows two rows, but their Holm p-values were computed in a three-member family that also contains SDLC vs SDLC-N.
- **A pooled family.** "Extreme coverage vs stratified" pools 16 tests across four different metrics, including shift metrics.
- **Unadjusted correlations.** The six Spearman tests of §6.9 are unadjusted.

**Fix:**
1. Define the families in §5.6 as a list, so readers can see the multiplicity.
2. Remove duplicate membership, and show Holm p-values only for the family displayed.
3. Since CTR23 is declared exploratory, consider reporting unadjusted p-values with an explicit "exploratory" label, together with the number of tests performed.

#### R3-09 (MODERATE) "No method receives method-specific tuning" is misleading: SDLC's density pipeline was engineered on CTR23 after its test results had been seen

**Location:** §5.3 (l. 240), §7.3 (l. 538), EXPERIMENT_LOG items 10–11.

**Evidence:**
- **What was chosen after v2.** The defensive mixture weight ε = 0.01, the t₂ component, the floor 0.05·median|r|, the stratum-exact grid and cross-fitted standardisation were all chosen in review cycle 1, after v2 results on the CTR23 test splits had been inspected.
- **The baselines got no such attention.** Their components received no comparable development. CQR quantile models reuse the mean-model LightGBM configuration with no check of quantile calibration. The DenseWeight smoothing parameter is fixed at A = 1 (`run_denseweight.py:34`), although Steininger et al. treat it as a hyperparameter.
- **What the paper concedes.** It correctly labels the CTR23 size comparisons exploratory. However, the sentence in §5.3 suggests a symmetry of effort that did not exist, and §7.3 calls the configuration "chosen without tuning to avoid favouring any method".

**Fix:**
1. Rephrase §5.3: the base learners share one untuned configuration, but the density-score pipeline (Eqs. 8–9, the floor and the grid) was revised after CTR23 results were inspected (§5.7).
2. List the SDLC-specific choices that were fixed after inspection.
3. For DenseWeight, either tune A on a training-only validation split or state that A was fixed.

### MINOR

#### R3-10 (MINOR) The modal-K filter silently drops runs, and only for some metrics

`analyze3.py:93–109` and `analyze_confirmatory.py:60–69` keep only runs with the modal realised number of strata before computing worst-stratum coverage and the null reference. Size, coverage and alert metrics are averaged over **all** runs, because `per_dataset` averages `cols` before merging `stratum_profile`.
- On CTR23 this drops 4 of the 10 seeds of health_insurance (K = 3 vs K = 2) for worst-stratum coverage only.
- Nothing is dropped on the replication.
- The filter is described neither in §5.6 nor in the plan's prose.

**Fix:** State the rule in §5.6 and apply the same run set to every metric, or compute worst-stratum coverage per K-configuration.

#### R3-11 (MINOR) Second-order leakage in the cross-fitted scales

`refit_scales.py:52–60` trains the scale model for fold j on |r_oof| of the other folds. Those residuals come from fold mean models (`learners.py:51–53`) that were trained **on fold j**, so y_j influences σ̂₋ⱼ indirectly. The claim at l. 181, that "neither μ̂ nor σ̂ has seen the residual it standardises", is true only to first order.

**Fix:** Use nested cross-fitting: residuals for training σ̂₋ⱼ should come from mean models fitted without fold j. Alternatively, qualify the sentence.

#### R3-12 (MINOR) Preprocessing and subgroup definitions use the full dataset

- One-hot encoding, including `dummy_na`, is applied to the whole dataset before splitting (`openml_ctr23.py:43`). Columns therefore exist for categories seen only in test rows.
- The skewness subgroup and the error-analysis covariate use the skewness of all targets, test included (`analyze3.py:140–144`).

Neither affects validity. Both contradict the literal statement at l. 236 that "every model, every stratum boundary and every density estimate uses the proper training set only" only for preprocessing, but subgroup membership is a data-dependent choice.

**Fix:** Compute skewness on training targets, or on a fixed seed-0 training split. Add one sentence on the encoding.

#### R3-13 (MINOR) Confidence-interval methods

- **Geometric-mean CIs.** These are percentile bootstraps (`tests.py:33–38`), which under-cover for n = 17 and skewed log ratios. Review_01 C1-30(b) asked for BCa, and the response (l. 51) does not say it was adopted.
- **HL CIs.** These use a normal approximation for the critical rank (`tests.py:86–90`). For n = 17 this gives c = 35 against the exact c = 34, so the CI is one Walsh average too narrow.

**Fix:** Use BCa or a studentised bootstrap for the GM ratio, and exact Wilcoxon critical values (`scipy.stats.wilcoxon` null distribution) for n ≤ 50.

#### R3-14 (MINOR) C-H2 is a non-rejection test with unknown power

"Consistent with exact validity" means that at most 3 of 17 datasets fall below their 5% null quantile. The expected count under validity is 0.85, and no power analysis is given. For example, it is not shown how often a method with true stratum coverage 0.88 would pass.

**Fix:** Report the power of the C-H2 rule against plausible under-coverage, or report the mean null-standardised deficit with a CI.

#### R3-15 (MINOR) Equivalence margins differ without justification

The CTR23 TOST uses a margin of 0.01 (`analyze3.py:226`); the plan uses 0.02. At 0.01 the replication still passes (p_TOST = 0.0002 vs S-NCP and 0.0033 vs BCCP; my recomputation).

**Fix:** Report both margins, or justify 0.02.

#### R3-16 (MINOR) Reporting glitches

- "$p\le$ < 0.001" appears at l. 308 (three times) and l. 346: placeholder rendering.
- "Holm $p$ < 0.001 or smaller" (l. 498).
- "median difference −0.0000" (l. 430).
- In Table 8, the C-H2 binomial p is placed in the "Holm p" column (l. 425).
- §6.8 says that SDLC "gave the smallest stratified sets" with the MLP, but S-CQR was not run with the MLP.

**Fix:** Correct each instance.

#### R3-17 (MINOR) Possible non-independence among the confirmatory datasets

topo_2_1 (45041) and yprop_4_1 (45032) both have 8,885 rows and appear to come from the same compound collection with different targets. If they share X, they are not independent units of analysis.

**Fix:** Check this. If they share X, keep one of them, or treat the pair as a cluster in a sensitivity analysis.

---

## 5. What does not need to change

- The unit of analysis (the dataset, after averaging over seeds), the use of one-sided tests only for the directional coverage hypotheses, and the exact-validity null reference are appropriate. They are implemented as described.
- The data flow from training to calibration to test is clean.
- All 23 numbers I sampled are reproduced by the released result files.

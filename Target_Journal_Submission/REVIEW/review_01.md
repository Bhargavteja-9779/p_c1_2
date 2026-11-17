# Consolidated review, cycle 1

Manuscript: stratified density-level conformal prediction (SDLC) for rare and extreme regression targets. Target journal: Expert Systems with Applications (ESWA).

Inputs:
- 10 independent reviews (Agents 1-10).
- REVIEW_HISTORY.md, which is empty because this is the first cycle, so no issue repeats an earlier fix.

Issues raised by several reviewers are merged below. Each merged issue lists the reviewers who raised it (A1 = Agent 1, and so on) and keeps their separate supporting arguments.

Paths are relative to `Target_Journal_Submission/`. Manuscript sections are in `manuscript/src/`:

| File | Content |
|---|---|
| 00_front.md | abstract and keywords |
| highlights.md | highlights |
| cover_letter.md | cover letter |
| 01_intro.md | Section 1, Introduction |
| 015_related.md | Section 2, Related work |
| 02_theory.md | Sections 3-4, problem formulation and method |
| 03_setup.md | Section 5, experimental design |
| 04_results.md | Section 6, Results |
| 05_discussion.md | Section 7, Discussion |
| 06_conclusion.md | Conclusion |
| 07_declarations.md | declarations |
| 09_appendix.md | Appendix A, proofs |

Action types:
- **text**: wording, framing or citations only.
- **re-analysis**: recompute from existing results or cached contexts (`results/raw_eval`, `results/raw_contexts`) with no refitting.
- **code fix**: change the pipeline code, then re-evaluate.
- **new experiment**: new fits, data or designs.

---

## 1. Summary of recommendations

| Reviewer | Focus | Recommendation |
|---|---|---|
| Agent 1 | Novelty and prior art | Major revision |
| Agent 2 | Methodology: theory and implementation consistency | Major revision |
| Agent 3 | Experimental design | Major revision |
| Agent 4 | Statistics | Major revision |
| Agent 5 | Datasets and leakage | Major revision |
| Agent 6 | Robustness and generalisation | Major revision |
| Agent 7 | Computational efficiency | Minor revision |
| Agent 8 | Literature and citations | Major revision |
| Agent 9 | Associate Editor (ESWA scope and readiness) | Major revision (desk-reject risk about 35-40% as is, about 15-20% after fixes) |
| Agent 10 | Hostile competitor (BCCP perspective) | Major revision |

**Consensus: major revision. No issue is fatal.**

Every reviewer who checked them confirmed the following:
- **Validity holds.** Stratified calibration is valid, and the theorems' algebra is correct (A2).
- **RQ1 is robust.** Marginal and covariate-adaptive methods under-cover the tails. This holds across alpha levels, strata schemes and both learners (A3, A4, A6).
- **No label leakage** (A5).
- **The basic inference setup is sound:** the dataset is the unit of analysis, and Holm correction is implemented correctly (A4).

The revision must fix three kinds of problem:
1. **Novelty and efficiency claims for SDLC.** The comparison was framed as pre-registered, the headline comparators were weak, there is no advantage over S-NCP, and SDLC loses extreme-tail coverage.
2. **The density estimator.** The pipeline has defects that confound the score comparison.
3. **Reporting.** Several reports are inaccurate (error-analysis prose, Table 5 signs, tail-stratum labels), and the editorial and readiness gaps flagged by A9 remain.

---

## 2. Fatal / Critical

No issue is fatal: validity is intact and every problem can be repaired. Three issues are critical, because each one by itself invalidates a headline claim as currently worded.

### C1-01 (critical) The "pre-registered" framing is overstated, and the H3 size advantage comes from a post-hoc implementation change

**Raised by:** A3, A4, A9, A10, and A8 (minor: post-hoc comparators placed inside the pre-registered sentence).

**Arguments:**
- **The frozen config does not contain what the paper says it contains.** It is commit 4d0a39c, `code/config/benchmark.json`, and it holds no hypotheses, primary method, test sides, Holm families or endpoints (A3, A4, A10). The analysis code with H1/H3 first appears in commit 2badc22, together with 91 raw result files (A4). The H3 family later grew from 5 to 6 comparisons when SDLC-LS2 was added (A3, A4).
- **The headline is post hoc.** Under the pre-registered implementation, H3 failed (EXPERIMENT_LOG items 9-10): SDLC vs BCCP p = 0.81, and S-NCP was nominally smaller (raw p = 0.044 in the opposite direction, A4). The exact implementation was adopted after a "diagnosis of H3 failure" on 7 benchmark datasets at seed 0, with test data seen.
- **The change was not neutral.** It shrank only the density-based methods. BCCP, S-NCP and S-CQR were always exact (A4, A9, A10).
- **The abstract still presents the 0.93 ratio as a pre-registered result.** The "pre-registration" is also a private commit, not an external, time-stamped registry (A9).
- **The comparators in that sentence were added after the run.** BCCP-hull and S-CQR/BFQR-style were added post hoc (Section 5.7, item 2), yet they appear inside the "pre-registered" sentence (A8).

**Corrective action:**
1. Replace "pre-registered" everywhere (00_front, highlights, cover_letter, 03_setup Section 5.7, 06_conclusion) with "protocol frozen in a version-controlled configuration (commit 4d0a39c, timestamp) before the full run". State exactly what was frozen: datasets, seeds, splits, alphas, strata, cal_fracs and the development datasets. Delete the claim that hypotheses and the primary method were in the config. Keep "pre-registered" only if a verifiable public snapshot (for example on Zenodo) is created and cited.
2. In 00_front, 03_setup Section 5.7, 04_results Section 6.3 and 06_conclusion, state:
   - that under the pre-registered grid implementation SDLC was not smaller than BCCP (p = 0.81) or S-NCP (p = 0.13);
   - that the exact implementation was adopted after this failure, following a diagnostic on 7 benchmark datasets;
   - that all exact-implementation H3 results, the hull test and the S-CQR/BCCP-hull comparisons are post hoc or exploratory.
3. Move the v1 H3 rows from `supplementary/v1_preregistered_analysis` into the main Table 5, or an adjacent column. Report the H3 family as originally specified (5 tests) next to the extended family (6 tests).
4. Justify the switch on grounds independent of the outcome: show that the grid inflated all density-based methods on all datasets (A4(d)).
5. Run the **grid-convergence check** (A10), from cache with no refitting:
   - pre-registered marginal-grid implementation with n_fine in {200, 500, 1000, 2000, 5000};
   - methods SDLC-LS, S-HPD, DLS and HPD-split; 31 datasets x 10 seeds; alpha = 0.1;
   - report the SDLC/BCCP geometric-mean ratio and its Wilcoxon p as functions of n_fine, plus the maximum per-dataset discrepancy from the exact sizes.

   If the grid does not converge to the exact implementation, the exact implementation is a different estimator, and the H3 claim must be withdrawn.
6. **Confirmatory replication** (recommended by A3 and A4):
   - First publish a time-stamped protocol: frozen analysis script and hash; primary endpoint = two-sided Wilcoxon on per-dataset mean log normalised size, SDLC vs BCCP; secondary family = S-NCP, S-CQR, S-HPD with Holm; decision rule.
   - Then run the frozen code on new split seeds 10-19 for all 31 datasets.
   - Ideally also run it on 15-25 regression datasets outside CTR23, for example from Grinsztajn et al. 2022 or PMLB, chosen with the same exclusion rule.
   - Report the result whichever way it goes.

**Action type:** text + re-analysis + new experiment (convergence check from cache; confirmatory replication).

### C1-02 (critical) SDLC has no size advantage over the information-matched S-NCP, and the headline comparisons use weakened competitors

**Raised by:** A1, A3, A6, A9, A10, and A7 (cost-benefit).

**Arguments:**
- **The headline omits the matched comparator.** SDLC/S-NCP is 1.004 [0.963, 1.059] under S5, 0.997 under S3 and 1.008 under S10 (A1, A3, A10). At alpha = 0.05 S-NCP is smaller (1.299 vs 1.364). By arithmetic mean S-NCP is smaller (1.369 vs 1.518). Yet the abstract, highlights, cover letter and conclusion name only BCCP (0.93) and S-CQR (0.83).
- **Sigma normalisation alone explains the gain over BCCP.** S-NCP/BCCP is 0.928, about the same as SDLC/BCCP at 0.932 (A10). BCCP uses only mu-hat, whereas SDLC uses mu-hat, sigma-hat and g-hat, so the SDLC-vs-BCCP comparison mixes the score with the extra scale model (A3).
- **BCCP is understated in the text.** Its paper is score-agnostic. Its reference package (pintervals 1.3.3, `pinterval_bccp`) offers `heterogeneous_error` = |y - yhat| / sigma(yhat), which is essentially S-NCP (A1).
- **S-NCP is at least as good on every secondary criterion** (A10):
  - smaller per-test-point median set on 25/31 datasets (p = 0.001);
  - fewer pieces (1.290 vs 1.480);
  - better worst-slab coverage (WSC) and tilt robustness;
  - equal alert precision.
- **The theory delivers little gain even where it should.** In the correctly specified synthetic study the oracle gain is only 4% and the estimated gain 2.3% (A10). The method's contribution therefore rests on Theorem 2, whose empirical value over the obvious baseline is not shown (A9).
- **Cost** (A7): SDLC costs about 750x more per test point and about 1.5x more to fit than S-NCP, for no size gain.

**Corrective action:**
1. **Headline comparator.**
   - Make SDLC vs S-NCP, with its CI, the primary efficiency comparison in 00_front, highlights, cover_letter, 06_conclusion and 05_discussion Section 7.1.
   - State plainly that with gradient boosting the density score is not smaller than a stratified normalised residual on mean, geometric-mean or median size, and that S-NCP is smaller at alpha = 0.05.
   - Rename the 0.93 comparison "BCCP with the absolute-residual score".
2. **Decompose the gain over BCCP** as BCCP -> S-NCP (adds sigma-hat) -> SDLC (adds the density shape), using existing results (Section 6.3).
3. **Describe BCCP accurately** in 015_related Section 2.2 and 03_setup Section 5.4: score-agnostic, with heteroscedastic scores in its reference implementation.
4. **Equivalence test:** add per-test-point median size to Tables 3 and 10, and a TOST equivalence test on the log size ratio SDLC vs S-NCP (margin +/-5%, stated in advance).
5. **Practical guidance (Section 7.2(iii)):** recommend S-NCP as the default, as it is simpler and at least as robust. Present SDLC as the option for users who specifically want minimal expected Lebesgue measure. Add the cost-benefit statement and a Pareto plot of size vs time (A7).
6. **Rewrite Highlight 4** to name the comparators exactly.
7. **New experiments:**
   - (a) **BCCP-het** (A1): BCCP with pintervals' `heterogeneous_error` score (sigma linear in yhat, fitted on the training split), via rpy2 or reimplemented in `conformal.py`; 31 datasets x 10 seeds; alpha in {0.05, 0.1, 0.2}; Holm-adjusted tests against SDLC and S-NCP.
   - (b) **Score ablation from cache** (A10): SDLC with a Gaussian g; SDLC with a Laplace g; S-NCP with score |y - mu| / sigma^gamma, gamma in {0, 0.5, 1, 1.5} chosen on out-of-fold training residuals only. If SDLC-Gauss or the tuned-gamma S-NCP matches SDLC, withdraw the claim that Theorem 2 drives the empirical gains.
   - (c) **Flexible conditional density** (A9, optional): one estimator that captures covariate-dependent shape, such as NGBoost or LightGBMLSS with a skew-t / Johnson SU likelihood, on all 31 datasets x 10 seeds at alpha = 0.1. This tests whether the theory can deliver gains in practice.

**Action type:** text + re-analysis + new experiment.

### C1-03 (critical) SDLC covers the most extreme outcomes worse than S-NCP and S-HPD, contradicting the title and highlight framing

**Raised by:** A6. Supporting numbers from A3 and A10 (tilt coverage), and A3 (top-1% not evaluated).

**Arguments:**
- **SDLC is systematically worse than S-NCP and S-HPD at the extremes** (alpha = 0.1, S5, two-sided Wilcoxon over 31 datasets, unadjusted):

  | Metric | SDLC minus S-NCP / S-HPD | Datasets where SDLC is lower | p |
  |---|---|---|---|
  | Top-5% coverage | -0.0066 vs both | 21/31; 22/31 | 0.039; 0.021 |
  | Upper tilt, gamma = 1 | -0.0052 / -0.0039 | 21/31 vs S-NCP | 0.003; 0.027 |
  | Upper tilt, gamma = 2 | -0.021 vs both | 20/31; 23/31 | 0.009; 0.010 |
  | Two-tail tilt, gamma = 1 | -0.0037 / -0.0028 | 25/31 | 0.0005; 0.003 |

  The largest gaps: video_transcoding 0.749 vs 0.908, fifa 0.778 vs 0.865.
- **The cause is structural.** Within a tail stratum, the size-optimal set spends coverage near the high-density inner edge, as Theorem 2 implies.
- **The paper tests these quantities only against marginal methods.** It calls the result "somewhat more exposed" (Section 6.5).
- **The guarantee is described as robust although it is not.** Highlight 2 promises coverage of "rare, extreme outcomes", and Section 7.1 says "robust to moderate target shift", although every stratified method is below 0.90 at gamma = 1.
- **Top-1% is never evaluated** (A3), although Proposition 1 emphasises it.

**Corrective action:**
1. Add a Holm-corrected family "SDLC vs stratified baselines (BCCP, S-NCP, S-CQR, S-HPD)" for top-5% coverage, bottom-5% coverage and all four tilted coverages. Put it in Table 5 or a new table.
2. State in 04_results Sections 6.1 and 6.5, 05_discussion Section 7.1 and 00_front that SDLC trades coverage at the outer end of tail strata for size, and that S-NCP and S-HPD protect the most extreme outcomes better.
3. Rewrite Highlight 2 to promise coverage within calibrated strata only.
4. Replace "robust to moderate target shift" with the quantified loss.
5. Add a top-1% evaluation stratum to `eval_strata_for` (`code/experiments/run_benchmark.py`), for datasets with at least 50 such test points per split.
6. **Extreme-strata stress test** (A6), from cache with a new scheme in `evaluate_from_cache.py`:
   - cut points at training quantiles {0.01, 0.05, 0.10, 0.25, 0.75, 0.90, 0.95, 0.99};
   - only datasets with n_cal >= 2000; alpha in {0.05, 0.1};
   - methods SDLC, S-NCP, S-HPD and BCCP;
   - report top-1% and top-5% coverage, the number of infinite thresholds, size, and tilted coverage at gamma in {1, 2}.

**Action type:** text + re-analysis + code fix (new strata scheme and evaluation stratum).

---

## 3. Major

### C1-04 (major) SDLC returns empty sets and has lower worst-slab and high-sigma coverage; its size gain partly comes from reallocating coverage away from hard inputs

**Raised by:** A3, A10, A1 (empty sets and the Sadinle null region, inside the Theorem 2 issue).

**Arguments:**
- **Empty sets.**
  - SDLC-LS returns empty sets on 13/31 datasets, up to 2.52% of test points on fps_benchmark (A3); across raw_eval the mean is 0.30% and the maximum 6.25% on energy_efficiency (A1).
  - SDLC-LS-floor reaches 7.3%, and DLS reaches 5.0%.
  - S-NCP and BCCP are essentially never empty (maximum 0.08%).
  - Empty sets occur exactly on the datasets where SDLC beats S-NCP (A3).
  - An empty set also gives no tail alert (A1).
- **Worst-slab coverage (WSC):** SDLC 0.857 vs S-NCP 0.886. SDLC is lower on 18/27 datasets (p = 0.005), and below S-HPD on 20/27 (p = 0.0025) (A3, A10).
- **Mechanism** (A10): for symmetric unimodal g-hat, SDLC is S-NCP with a radius that decreases in sigma-hat(x). That lowers mean size and raises typical (median) size.
- **Section 6.3's "the size differences are not bought with coverage"** checks stratum coverage only.

**Corrective action:**
1. Add the empty-set rate to Table 3 and to the per-dataset table S1.
2. Report coverage and size by quintiles of sigma-hat(x), with quintiles taken from training data, for SDLC, S-NCP and BCCP. Report both overall and within the upper stratum, with per-dataset Wilcoxon tests.
3. Test WSC differences among the stratified methods, with Holm correction.
4. Recompute H3 two ways:
   - (a) restricted to test points where both sets are non-empty;
   - (b) for an SDLC variant that always contains the mode of f-hat(.|x). It is a superset, so validity is preserved.
5. Qualify "not bought with coverage" to stratum-wise coverage only. Discuss the trade-off in Sections 6.3 and 7.2: the hardest cases receive less protection. Discuss Sadinle et al.'s null-region remedies.

**Action type:** text + re-analysis (from cache).

### C1-05 (major) The noise density g-hat is fitted to residuals standardised by an in-sample scale model

**Raised by:** A2, A3, A10.

**Arguments:**
- **The scale model is evaluated in sample.** `run_benchmark.py` lines 74-75 compute `sg_tr = sg.predict(Xtr)`, using the same points sigma-hat was trained on with target |r_oof|. Only the numerator of the standardised residual is out-of-fold. Section 4.3 describes the residuals as fully out-of-fold.
- **The tails are too light** (A2). The 99th percentile of |z| on calibration data divided by that on training data has median 1.17 and is as high as 1.74.
- **The median is too large and the shape distorted** (A3). Median |z| is 0.891 on training vs 0.594 on calibration for airfoil, and 0.917 vs 0.550 for energy. g-hat has a dip at 0: g(0)/max is 0.133 for forest_fires and 0.149 for geographical_origin_of_music. DLS has 2.9 pieces on forest_fires and socmob, which are exactly where SDLC loses most (1.71x and 1.55x S-NCP).
- **The defect confounds RQ3 and weakens every density-based baseline** (DLS, HPD-split, DCP, S-HPD). It may also explain the small-dataset failures that Section 6.8 attributes to n (A10).

**Corrective action:**
1. Cross-fit the standardisation. Using the existing 3 folds, fit sigma-hat_{-j} on the other folds and set z_i = r_oof,i / sigma-hat_{-j(i)}(X_i). Keep the full-data sigma-hat for calibration and test.
2. Describe the estimator accurately in 02_theory Section 4.3.
3. Report per-dataset diagnostics in the supplement: training vs calibration |z| tail quantiles, KS distance, and g(0)/max g.
4. Re-run the fit stage for the scale models only (31 datasets x 10 seeds), recompute z_LS and z_LS2, and re-evaluate all LS-family methods at alpha in {0.05, 0.1, 0.2}.
5. Report old and new side by side: SDLC/S-NCP, SDLC/BCCP and SDLC/S-HPD ratios with CIs, test NLL, and Tables 3, 4, 5, 7 and 12, plus the explanation in Section 6.8.

**Action type:** code fix + new experiment (partial refit).

### C1-06 (major) The KDE tail floor, bandwidth and table/grid resolution are ad hoc and decide tail thresholds; heavy-tailed sets explode

**Raised by:** A2, A6, A7 (G sensitivity and the 12-piece cap).

**Arguments:**
- **Floor regime** (A2). On forest_fires, 18.8% of upper-stratum calibration g-hat values sit at the 1e-6 x max floor. In 5 of its 7 runs with a finite threshold, the upper-tail threshold is itself a floor score, so the tail piece depends on an arbitrary constant. This happens in 8 of 310 runs overall.
- **Under-smoothing** (A2). Silverman's bandwidth gives a median of 7 local maxima, up to 91 (did 44963), and single-threshold DLS averages 1.138 pieces.
- **Scale degeneration** (A6). On brazilian_houses, seed 4, alpha = 0.05, SDLC's normalised size is 32.4 against 0.64 for BCCP: |z| reaches 739 and 1.2% of sigma-hat values sit at the floor. Across the caches, 57 runs on 15 datasets have degenerate scales, and in 21 runs on 11 datasets the set-grid spacing exceeds 0.1 standardised units (0.63 on physiochemical_protein, where h = 0.15). This contradicts the claimed "resolution relative to the conditional scale" and Section 5.7 deviation 3.
- **Grid sensitivity** (A7). Sizes are within 0.3% of the G = 32768 values, but piece counts depend on G. The 12-piece merge is undocumented.

**Corrective action:**
1. Replace the constant floor with a parametric tail extension (Student-t or GPD fitted to the outer residuals), or with a KDE mixed with a heavy-tailed component.
2. Use a bandwidth suited to heavy tails: Sheather-Jones, an adaptive bandwidth, or a log-concave MLE.
3. Tabulate g-hat on a bandwidth-adapted grid with spacing <= h/4 over the 0.1%-99.9% quantiles of z, extended analytically beyond. Make the set grid at least as fine, or remove it (see C1-27).
4. Use a robust sigma floor, for example 0.05 x median|r_oof|, applied identically in both pipelines (see C1-20), and document it.
5. Report per dataset: the share of tail thresholds at the floor, the number of modes of g-hat, DLS pieces, runs with degenerate scales or coarse grids, and a "catastrophic run" statistic (per-run maximum size relative to BCCP; number of runs with ratio > 2).
6. Run the sensitivity grid from cache: floor in {1e-8, 1e-6, 1e-4}; bandwidth x {0.5, 1, 2} plus Sheather-Jones; the tail-extended g-hat; and G in {512, 2048, 8192, 32768}, also recording how often the 12-piece cap binds. Report the SDLC/BCCP and SDLC/S-NCP ratios with Holm p for each setting.
7. Add brazilian_houses at alpha = 0.05 to Section 6.8 and the Limitations as a heavy-tail failure mode.

**Action type:** code fix + re-analysis (from cache).

### C1-07 (major) Interval baselines are scored with closed stratum pieces, which inflates their coverage on tied targets

**Raised by:** A2. Raised to major because it is an asymmetric evaluation bug that affects every coverage table.

**Arguments:**
- `conformal.py` lines 263-270 build closed pieces [max(l, E_k), min(h, E_{k+1})], and `metrics.covered` tests membership geometrically. Eq. (4) and `strata.py` define half-open strata.
- Cut points are observed training values. Up to 35% of test targets lie exactly on a cut point (abalone 34.5%, health_insurance 34.7%).
- BCCP's stratum coverage is inflated by up to 3.85 pp (geographical_origin_of_music) and its upper-tail coverage by 1.77 pp (cpu_activity).
- The LS-family methods, including SDLC, are scored with the exact rule, so the comparison favours the baselines.

**Corrective action:**
1. Score every method with the exact rule s(X, Y) <= q_{k(Y)}, or make the pieces half-open in `covered()`.
2. Add a unit test that geometric membership equals the exact rule on data with ties at cut points.
3. Re-evaluate BCCP, S-NCP, S-CQR and their hulls from cache for every seed, alpha and scheme. Recompute Tables 3, 5, 8 and 9 and the null reference.

**Action type:** code fix + re-analysis.

### C1-08 (major) Realised strata differ greatly from the nominal tails, are unstable across seeds, and decile labels break down with ties

**Raised by:** A2, A3, A4, A5, A6.

**Arguments:**
- **Realised stratum masses** (raw_eval `train_stratum_mass`):
  - health_insurance has K = 2 in 5-6 of 10 seeds, with an "upper tail" holding 44% of the mass. The 0.9 quantile flips between 40 and 41.
  - forest_fires: lowest stratum 74% of the mass.
  - fifa and socmob: lowest stratum 20-25%.
  - abalone: lowest stratum 4%.
- **These strata are averaged as "top 10%" tails** in Table 3, Table 8, Table 9, the abstract and the Fig. 2 caption. Table 9's worst gamma = 2 dataset is health_insurance (A6).
- **`modal_k` drops splits silently,** so rows of the same table use different splits (A4).
- **Section 4.4 promises per-dataset realised masses,** but Table 2 reports only median K.
- **Decile labels break down with ties** (A5). `np.quantile` + `searchsorted` leaves empty deciles: forest_fires deciles 0-3 are empty, and health_insurance has 1,700 points in "decile 2". These labels feed Fig. 1, the worst decile in Table 11, and the top/bottom-5% columns.
- **Under S3**, 4 datasets have K = 2 (A6).

**Corrective action:**
1. Add the realised mass of each stratum and the realised K per dataset (median and range over seeds) to Table 2 or S1. Report the splits dropped by `modal_k`.
2. Relabel the tail columns "lowest/highest calibrated stratum (nominally 10%)". Also report the tail rows of Tables 3, 5, 8 and 9 restricted to datasets whose realised tail mass is in [0.05, 0.15], or excluding the datasets with realised K < 5.
3. Make the strata deterministic across seeds for tied targets with a training-only tie-aware rule (for example cut points on sorted distinct values, or method = 'higher' for upper cuts).
4. Compute deciles and the top/bottom-5% groups by rank with seeded random tie-breaking, or mark them undefined. Recompute Fig. 1 and the worst decile in Table 11.
5. Correct "top 10%" wording in 00_front, 04_results Section 6.1 and the figure captions.

**Action type:** code fix (`strata.py`, `run_benchmark.py` decile labels) + re-analysis + text.

### C1-09 (major) SDLC's advantage over BCCP depends on alpha, dataset size, hull form and the choice of summary statistic

**Raised by:** A4, A6, A10.

**Arguments:**
- **The headline evidence is fragile** (A4):
  - the CI of the geometric-mean ratio, [0.862, 1.003], includes 1;
  - a sign test gives Holm p = 0.059;
  - the paired differences are skewed (skewness of the log ratios -0.65 vs BCCP and +2.83 vs S-NCP), so the signed-rank symmetry assumption is doubtful;
  - Friedman ranks lie within the critical difference.
- **The size summaries disagree** (A4, A10): by arithmetic mean SDLC is larger than BCCP (1.518 vs 1.509) and larger than S-NCP; by geometric mean S-NCP is smaller; Section 6.3 picks the median ("smallest in median").
- **The price of stratification is reported selectively.** The abstract gives the median ratio (1.05-1.14) and omits the geometric mean (1.16-1.24) and the arithmetic-mean ratios (1.40-1.48).
- **The advantage does not hold at other alpha levels** (A6, A10):
  - alpha = 0.05: SDLC/BCCP 0.943-0.946, p of about 0.053-0.058; hull vs hull p = 0.34;
  - alpha = 0.2: 0.969-0.972, p of about 0.058-0.066; the hull form is larger for SDLC (p = 0.048);
  - at alpha = 0.2 the median and arithmetic-mean rankings reverse the geometric-mean claim of 0.631 vs 0.652.
- **The advantage does not hold on small datasets** (A6). For n < 1600 (9 datasets), SDLC is larger than S-NCP (1.141) and than BCCP (1.063). Spearman correlation of the log ratio with n: -0.47 to -0.55.
- **Table 11 omits S-NCP.**
- **"Robust across miscoverage levels" and "robust default" are unsupported.**

**Corrective action:**
1. In 03_setup Section 5.6, declare one primary size summary: the geometric-mean ratio with a bootstrap CI (BCa).
2. For each H3 comparison in Table 5, report: the Hodges-Lehmann estimate with its exact CI, the sign-test p, and the geometric-mean ratio with its CI. Put the arithmetic mean, the median over datasets and the per-test median in one secondary table.
3. Run the H3 family (union and hull forms) at alpha = 0.05 and 0.2, and under S3 and S10, with Holm correction across alpha levels. Add S-NCP to Table 11.
4. Report sizes separately for n < 1600 and n >= 1600, and the Spearman association of the ratio with n_cal.
5. Restrict the efficiency claims to alpha = 0.1 and quote the CI in 00_front ("smaller on 22 of 31; 0.93, 95% CI 0.86-1.00").
6. Report the price of stratification as the geometric mean with its CI, alongside the median.
7. Delete "robust across miscoverage levels" and "smallest in median". Rewrite Section 7.2(iii) to name the regime: S-NCP or BCCP when n_cal per tail stratum is below about 50 or alpha <= 0.05.
8. Report the MLP result as supporting the direction, not as a confirmation.

**Action type:** re-analysis + text.

### C1-10 (major) The error-analysis prose contradicts its own statistics and hides that the price of stratification grows with skewness

**Raised by:** A2, A4, A5, A6, A9, A10.

**Arguments:**
- 04_results.md line 87 contains fixed template wording: "not associated" (rho = 0.47, p = 0.008) and "only weakly" (rho = 0.60, p = 0.0004). Both associations are significant, also after Holm across the 3 correlations (A4).
- Skewness is the stronger correlate. Skewed targets define imbalanced regression, so the method costs most exactly where it is meant to be used (A6).
- "p = < 0.001" is malformed.

**Corrective action:**
1. Rewrite the sentence: the price increases with relative RMSE (rho = 0.47) and with |skewness| (rho = 0.60), both significant after Holm.
2. Add a two-predictor rank regression or partial correlation (log price ~ |skew| + RMSE/sd + log n_cal), since the predictors are correlated.
3. Add a sentence to the Limitations.
4. Fix the "p = <" rendering in `code/scripts/render_manuscript.py`, and add a render-time check that flags qualitative words next to filled statistics.

**Action type:** text + code fix (renderer) + re-analysis (small).

### C1-11 (major) The efficiency and price claims rest mainly on the non-skewed datasets

**Raised by:** A5. Related evidence from A6.

**Arguments:**
- **Skewed datasets** (|skew| > 1, n = 15): SDLC vs BCCP 0.899 (p = 0.083); vs S-NCP 1.034 (p = 0.36); vs S-CQR 0.882 (p = 0.39). Price: geometric mean 1.386, median 1.20.
- **Non-skewed datasets** (n = 16): the advantages are significant, and the price is 1.11.
- The abstract frames the work as imbalanced regression but quotes the pooled numbers.

**Corrective action:**
1. Add a subgroup analysis using the |skew| > 1 cut already defined in Section 5.1: Table 4 and the H3 rows of Table 5 per subgroup, Holm within subgroup, with CIs.
2. Qualify the claims in 00_front and 06_conclusion for skewed targets, and report the larger price there.

**Action type:** re-analysis + text.

### C1-12 (major) The exclusion rule's rationale contradicts its threshold: discrete and atom-heavy targets were retained

**Raised by:** A5.

**Arguments:**
- **Eight retained datasets have count or heavily discretised targets:** abalone (28 values), geographical_origin_of_music (31 latitudes), naval (a 51-level grid), cpu_activity, health_insurance (65% of mass at 2 atoms), fifa, socmob (a count), forest_fires (48% zeros).
- **The text contradicts this.** Section 7.3 says count targets were excluded. Section 4.2 says size-optimality fails with atoms.
- **Excluding these 8 datasets changes the price:** the geometric mean falls from 1.237 to 1.144.

**Corrective action:**
1. Correct 03_setup Section 5.1 and 05_discussion Section 7.3 to say which count and discretised targets were retained.
2. Add a sensitivity analysis under a rule consistent with the rationale, for example fewer than 100 distinct values or a largest atom above 5%, defined from the targets only. Report Tables 3-5 for n = 23.
3. State that for the atom-heavy datasets only the coverage results (RQ1 and RQ4) are interpretable.

**Action type:** text + re-analysis.

### C1-13 (major) Theorem 2's novelty is overstated: it is a per-stratum application of classical level-set optimality, it states an oracle property, and Kiyani et al. (2024) is not cited

**Raised by:** A1, A8, A10.

**Arguments:**
- **The problem separates by stratum.** Theorem 2 is K copies of the classical Neyman-Pearson / level-set argument (Lei et al. 2013; Sadinle et al. 2019; Izbicki et al.) (A1, A10).
- **The closest modern precursor is uncited.** Kiyani, Pappas & Hassani (NeurIPS 2024, arXiv 2406.18814), Proposition 3.1, shows that length-optimal sets under conditional and group constraints are density level sets (A1, A8).
- **The paper oversells it.** It calls Theorem 2 "our main methodological contribution", and the highlight says the sets are "proven to be the smallest", although the result holds only for the oracle and plug-in consistency is not proved.
- **Proposition 1 and the RQ1 numbers are not evidence for SDLC.** They are properties of Mondrian/BCCP calibration (A10).

**Corrective action:**
1. Recast Theorem 2 as a Proposition, or keep it as a theorem and state explicitly that the problem separates and the proof is the standard Neyman-Pearson / level-set argument.
2. Cite Kiyani et al. (2024), after verifying it on the proceedings page, together with Lei et al., Sadinle et al. and Izbicki et al. Name the actual addition: label-indexed constraints with Lebesgue size, which give thresholds that are constant within each stratum.
3. Change "main methodological contribution" to "extension" in 06_conclusion and cover_letter. Change the highlight to "the oracle density level sets are the smallest".
4. Attribute the RQ1 numbers in 00_front to stratified (BCCP/Mondrian) calibration.
5. If the paper is to claim a theory contribution, add one of:
   - (a) asymptotic consistency and size-optimality of plug-in SDLC under consistency of f-hat and continuity of the law of f(Y|X) at each t_k;
   - (b) the size-optimal set under the joint constraints {marginal >= 1 - alpha, every stratum >= 1 - beta}, which does not separate and gives coupled thresholds; this would be a principled replacement for the floor rule;
   - (c) a bound on the size gap between C* and the oracle S-NCP set as a function of the dispersion of sigma(X).

   Otherwise, frame the paper as a benchmark and practice study.

**Action type:** text (+ optional new theory).

### C1-14 (major) Proposition 1 is a Gaussian result presented as a general mechanism, and the conclusion misstates it

**Raised by:** A1, A8, A10.

**Arguments:**
- **The general wording outruns the proof.** "The mechanism is general" (Section 3.2) and "even the oracle ... misses most extreme outcomes" (00_front, 06_conclusion) rest on a proof for jointly Gaussian (X, Y) only.
- **Counterexample** (A1, Monte Carlo): with a heavy-tailed signal and Gaussian noise, the oracle covers 0.816 / 0.896 of the top 10% / top 1% for S ~ t_1.5. Coverage rises toward 1 - alpha in the most extreme stratum.
- **The paper's own oracle over-covers a tail.** O-HDR-X covers the lower tail at 0.984.
- **"Misses most" contradicts Table 1:** 70.5% of the top decile is covered at R^2 = 0.5 (A8).
- **The phenomenon itself is not new.** It was shown empirically by Wang et al., Randahl et al. and Boruah (A1, A10).
- **Section 7.1 understates BCCP's evaluation:** it says "demonstrated for one application", although BCCP was also tested in simulations (A8).

**Corrective action:**
1. Limit the claims to the Gaussian model. Delete "the mechanism is general".
2. Replace "misses most extreme outcomes" with the quantitative statement (70.5% of the top decile and 37.5% of the top 1% at R^2 = 0.5).
3. Add the elementary general fact: exact X-conditional coverage implies sum_k p_k Cov_k = 1 - alpha, so some stratum is at or below 1 - alpha.
4. Either prove a sufficient condition for coverage to tend to 0 (for example, signal tails no heavier than noise tails), or present the heavy-tailed case as a counterexample.
5. Extend Table 1 with t_nu signals (nu in {1.5, 3, 30}, scaled to the same R^2) and a skewed-noise model. Report top-10%, top-1% and bottom-10% oracle coverage, by exact integration or Monte Carlo with 2 x 10^6 draws, using `code/experiments/prop1_gaussian.py`.
6. Fix the BCCP wording in Section 7.1 to "simulations and one application", and credit the earlier empirical reports.

**Action type:** text + new experiment (cheap Monte Carlo).

### C1-15 (major) Corollary 1 repackages known results without credit, and its bounds are near-vacuous for the shifts actually studied

**Raised by:** A1, A2, A8.

**Arguments:**
- **Prior results are uncredited.** Part (i) is the known label-shift robustness of label-conditional coverage (Angelopoulos, Barber & Bates; Podkopaev & Ramdas). Part (ii) is the total-variation coverage-gap bound of Barber, Candès, Ramdas & Tibshirani (2023, Ann. Stat. 51:816-845), which is not in the bib. Part (iii) is a standard bound for bounded likelihood ratios (A1, A8).
- **The bounds are weak for every stratum in the experiment** (A2). For the gamma = 1 / 2 tilts, d_TV for the upper stratum is 0.186 / 0.427, so part (ii) gives only >= 0.714 / 0.473 against observed coverage of about 0.88 / 0.83. Part (iii) has M/m = 11.4 / 131, which makes it vacuous, and even the bulk stratum has M/m = 3.9 / 14.8.
- **Two statements are wrong.** "Precise conditions for robustness" is overstated, and Section 7.3's "vacuous only for open tail strata" is incorrect.

**Corrective action:**
1. Cite Barber et al. (2023) after Crossref verification, Angelopoulos-Barber-Bates, and Podkopaev & Ramdas. State that (ii) is a within-stratum application of Barber et al., and that (iii) is the standard bounded-likelihood-ratio bound.
2. Reword the abstract and contribution 3 of 01_intro: "we state, for continuous outcomes, when the known label-shift robustness of label-conditional calibration holds exactly, and how it degrades".
3. Correct Section 7.3.
4. Add the Corollary 1(ii)/(iii) bounds as columns of Table 9, next to the observed coverage.
5. Add the sharper bound (sup kappa - inf kappa) x d_TV, with kappa estimated by isotonic regression of the coverage indicator on y, and report how often the observed coverage lies within it (A2).

**Action type:** text + re-analysis.

### C1-16 (major) The "BFQR-style" comparator is weaker than BFQR, and the headline uses five strata instead of the decile strata the paper itself defines

**Raised by:** A1, A3, A8.

**Arguments:**
- **The defining step of BFQR is missing** (A1). BFQR optimises per-bin levels beta_m to minimise width subject to mean(beta_m) = 1 - alpha, uses M = 10-20 bins, and has a per-bin finite-sample theorem (Wang et al. Thm 4.1). S-CQR has none of these, and it is also prior art for the floor variant.
- **The headline uses the wrong scheme** (A3). It uses S5, although Section 5.4 defines decile strata as "BFQR-style". Under S10 the ratio is 0.847 (25/31) instead of the reported 0.833.
- **Bin placement differs from BFQR.** Its bins come from calibration data; here they come from training quantiles (A3).
- **The abstract and cover letter's "binned quantile regression (0.83)" reads as a comparison with BFQR itself** (A8).

**Corrective action:**
1. Either implement BFQR faithfully, or rename S-CQR "stratified CQR" in 00_front, highlights, cover_letter and 06_conclusion and drop the "BFQR" label.
2. Use the S10 S-CQR wherever the BFQR-style label is kept. Add an H3 row SDLC-S10 vs S-CQR-S10, and list the remaining differences from Wang et al.
3. Describe BFQR's level optimisation in 015_related Section 2.2 and 02_theory Section 4.5, and cite Wang et al. Thm 4.1 next to Theorem 1.
4. **New experiment** (A1):
   - single-group BFQR with the CQR score, M in {10, 20} equal-mass bins, and beta_m optimised by subgradient on out-of-fold training predictions; union and hull forms;
   - compare with SDLC on size and worst-stratum coverage;
   - also compare SDLC-floor with a level-optimised SDLC (alpha_k chosen on training data to minimise estimated size subject to sum_k p_k alpha_k <= alpha and alpha_k <= beta).

**Action type:** text + new experiment.

### C1-17 (major) Kandinsky CP is mischaracterised as only "plausibly" covering stratified calibration

**Raised by:** A1 (moderate), A8 (major).

**Arguments:**
- **Kandinsky CP explicitly covers this setting** (arXiv 2502.17264, ICML 2025). It allows infinite Y, group functions on X x Y, overlapping and fractional groups, and it includes a regression (CQR) experiment. Stratified calibration with disjoint strata is a special case.
- **Overlapping groups address this paper's own granularity limitation** (worst decile 0.867).
- **Weighted groups can include y-tilts,** which addresses the shift setting where the paper's guarantee is only approximate.

**Corrective action:**
1. Rewrite 015_related Section 2.2 and 02_theory Section 4.1: Kandinsky CP covers regression with label-defined, overlapping and fractional groups. Position stratified calibration as the disjoint-group special case with an exact finite-sample guarantee, against Kandinsky's high-probability approximate guarantee over a richer class.
2. Discuss overlapping groups as an existing remedy in Section 7.3. Update `supplementary/literature_matrix.md`.
3. Recommended experiment: Kandinsky CP with the density and NCP scores, on 31 datasets x 10 seeds at alpha = 0.1.
   - Family A: {all data} + S5 strata + training deciles (+ top 5%). Report marginal, worst-stratum, worst-decile and top-5% coverage and size, against SDLC (S5, S10) and SDLC-floor (A1).
   - Family B: S5 strata + y-tilt functions exp(+/- gamma z), exp(gamma |z|), with gamma in {1, 2}, in Experiment 4 (A8).

**Action type:** text + new experiment.

### C1-18 (major) The target-shift experiment rests on tiny effective sample sizes, reports the wrong metric, has no positive control, and leaves null and below-nominal results untested

**Raised by:** A3, A4, A6, A9.

**Arguments:**
- **Tiny effective sample sizes.** At gamma = 2 the Kish ESS is 6.8-10.1 on energy_efficiency, forest_fires, geographical_origin_of_music and QSAR, and below 55 for every dataset with n < 4200. The 10 largest weights carry 50-78% of the total. The seed SD reaches 0.23 (A3, A4, A6).
- **Wrong metric.** RQ4 and Section 5.6 refer to stratum-wise (worst-stratum) coverage, but `metrics.py` and Table 9 report tilted marginal coverage. Corollary 1 is never checked (A4, A6, A9).
- **No positive control** for Corollary 1(i): every tilt re-weights within strata (A3).
- **Multiplicity.** Holm is applied within each tilt separately (28 tests) (A4).
- **Unreported null.** The lower-tilt result, where SDLC is not better than SCP (p_holm = 0.915), is not mentioned (A6).
- **Untested shortfall.** At gamma = 1 every stratified method is at 0.882-0.894, called "kept coverage" without a test (A4).
- **Re-weighting cannot place mass outside the observed test range** (A6).

**Corrective action:**
1. Report the ESS per dataset and tilt. Restrict the gamma = 2 summaries, the worst-dataset column and the tests to datasets with ESS >= 50 (or >= 100), and flag the rest.
2. Add CIs by bootstrapping datasets.
3. Compute the importance-weighted coverage of each stratum under each tilt from cache, and align RQ4 and Section 5.6 with the metric actually tested.
4. Apply Holm across all 28 shift tests, or declare up2 primary.
5. Test the gamma = 1 shortfall with a one-sample Wilcoxon, and discuss the lower-tilt null.
6. Positive control from cache: weights that are constant within strata (upper stratum x5, lower stratum x0.5). Optionally resample 200 replicates by rejection sampling.
7. Genuine label-shift experiment in the synthetic study: rejection-sample test points from a pool of 10^6 with acceptance proportional to exp(gamma Phi^{-1}(F_Y(y))), gamma in {0.5, 1, 2}. Report stratum-wise coverage and the Corollary 1(iii) bound computed from the known density ratio.

**Action type:** re-analysis + code fix (`metrics.py`, `analyze.py`) + new experiment (synthetic shift).

### C1-19 (major) The synthetic study uses only the one correctly specified location-scale DGP

**Raised by:** A2, A3, A6, A10.

**Arguments:**
- `synthetic.py` generates Y = mu + sigma x Gamma(2) noise, independent of X. This is exactly model (7), with n_cal = 5000 and alpha = 0.1 only.
- Even in this favourable case, estimated SDLC beats S-NCP by only 2.4%, and its size is 14% above the oracle (A6).
- The real-data failures involve misspecification: zero inflation (forest_fires), small n (socmob, cars) and heavy tails (brazilian_houses). Section 4.3's "affects size but never validity" is never quantified.

**Corrective action:**
1. Extend Table 6. Keep the current DGP (A) and add:
   - (B) covariate-dependent skewness (skew-normal with shape 4-5 x X_j);
   - (C) bimodal mixture noise (equal mixture N(+/-1.5, 0.5^2), or a mixing weight that depends on X);
   - (D) zero inflation (P(Y = 0) = logistic(X_1) or 0.4 + 0.3 x 1{X_2 > 0}, otherwise lognormal);
   - (E) t_2.5 or t_3 noise.
2. Cross each DGP with n_cal in {250, 1000, 5000} and alpha in {0.05, 0.1}, with 10 repetitions and the same pipeline.
3. Report oracle and estimated rows for SDLC, S-NCP, BCCP and S-HPD: size, stratum coverage, top-5% coverage, infinite thresholds and win counts. For (D), add an atom variant.
4. Use the results to delimit, in Section 7.2, when SDLC should be preferred.

**Action type:** new experiment (`code/experiments/synthetic.py`).

### C1-20 (major) The MLP replication uses an undocumented scale floor and imputation, and its explanation is contradicted by the data

**Raised by:** A3, A5, A6, A10.

**Arguments:**
- **Different floor.** `run_learner_generality.py` line 64 floors sigma at max(1e-3 sd, 0.05 x median|r_oof|), against 1e-3 sd in the main pipeline, and this is undisclosed.
- **Undisclosed imputation.** NaN is replaced by 0 with no missingness indicators (Moneyball 66% missing).
- **The "smoother scale" explanation is contradicted.** With the MLP, NCP/SCP is 1.114 and S-NCP/BCCP is 1.034, so normalisation hurts. That points to a worse scale model, not a smoother one (A6, A10). SDLC/S-NCP = 0.923 then reflects how fragile S-NCP is to a bad sigma-hat, not support for Theorem 2.
- **The scale MLP is unconstrained** and can output values <= 0 (A10).

**Corrective action:**
1. Document the floor and the imputation in Section 6.6 and the Table 12 caption.
2. Report the NCP/SCP and S-NCP/BCCP ratios next to the SDLC ratios, and the Spearman correlation of sigma-hat(X) with |Y - mu-hat| per learner.
3. Remove the "smoother scale" claim, and the "replicated with a neural learner" wording in 00_front, unless it survives the ablation.
4. **Floor ablation from cache:** GBM with the MLP floor (this needs z_LS recomputed with sg_tr), and the MLP with the GBM floor.
5. **Recommended re-run:** the MLP study (31 datasets x 5 seeds) with a positive scale model (softplus output or a log|r| target), training-only median imputation plus missingness indicators, and the same floor as the main benchmark.

**Action type:** text + re-analysis + new experiment (MLP re-run).

### C1-21 (major) The "more targeted tail alerts" claim holds only against BCCP

**Raised by:** A3, A6, A8, A9, A10.

**Arguments:**
- **Table 8 shows S-NCP and S-HPD alerting at least as precisely.** S-NCP: alert rate 0.366, precision 0.448. S-HPD: precision 0.448. SDLC: 0.384 and 0.439, with the lowest upper recall of the non-floor stratified methods (0.978).
- **Per-dataset tests find no SDLC advantage.** Against S-NCP, recall p = 0.064 and precision p = 0.22. At alpha = 0.2 S-NCP's precision is significantly higher (p = 0.018) (A6, A10).
- **Marginal methods already reach high recall.** SCP has recall 0.947 at precision 0.513, so SDLC buys about 3 points of recall for 7 points of precision (A9).
- **A crude tail classifier is comparable** (A3): a thresholded P(Y >= e_{K-1} | x) gives alert rate 0.394 at recall 0.965.
- **Conformal selection (Jin & Candès 2023, JMLR)** is the established method for flagging large outcomes and is not cited (A8).

**Corrective action:**
1. Qualify the claim in 00_front, 05_discussion Section 7.1 and 06_conclusion: "more targeted than BCCP and S-CQR, as also obtained by S-NCP, and at a precision cost relative to marginal methods".
2. Attribute the improvement to normalisation by sigma-hat (Section 6.4).
3. Add paired tests of alert rate, recall and precision against all stratified baselines.
4. Cite Jin & Candès (2023), and contrast recall control (stratified sets) with FDR control (conformal selection).
5. Add to Table 8:
   - (a) a calibrated tail classifier at matched recall, from the cached P_c_H/P_t_H;
   - (b) optionally, conformal selection with BH at q in {0.1, 0.2}.

**Action type:** text + re-analysis + new experiment (alert baselines; cheap).

### C1-22 (major) Weak fit with ESWA's applications emphasis: no decision-oriented case study

**Raised by:** A9.

**Arguments:**
- The paper is organised around Proposition 1 and Theorem 2. The only real-data illustration is Fig. 8, which its own caption calls "illustrative".
- `supplementary/eswa_paper_benchmark.md` itself recommends adding a case study.
- The decision view (Table 8) undercuts the claimed benefit (see C1-21).
- A9 estimates the desk-reject risk at about 35-40% as submitted.

**Corrective action:**
1. Add a cost-sensitive case study on 2-3 datasets with a decision context (for example kings_county or miami_housing, cps88wages, and health_insurance or diamonds).
2. Use the loss c_miss x 1{Y in upper stratum, Y not in C(X)} + c_width x |C(X)|, or a cost per false alert. Plot expected loss against c_miss/c_fa from 1 to 50 for SCP, CQR, HPD-split, BCCP, S-NCP, SDLC and SDLC-floor, using raw_eval.
3. Place the case study early in the Results, and lead the Introduction with the application problem.

**Action type:** re-analysis (no refit) + text.

### C1-23 (major) No imbalanced-regression base learners are compared, although the paper is positioned in the imbalanced-regression literature

**Raised by:** A9. Missing references from A8.

**Arguments:**
- All methods share an unweighted LightGBM. The ESWA imbalanced-regression literature (SMOGN, DenseWeight, SERA) would ask whether an imbalance-aware learner plus ordinary split conformal closes the tail gap.
- Proposition 1 argues that it cannot in the oracle limit, but this is never tested on data.
- 015_related Section 2.3 cites only Yang et al. (2021) for algorithm-level methods. It is missing DenseWeight (Steininger et al. 2021), Balanced MSE (Ren et al. 2022), and optionally RankSim and ConR.

**Corrective action:**
1. Refit the mean and scale models with DenseWeight sample weights (alpha = 1, training targets only) on 31 datasets x 10 seeds, optionally adding SMOGN for n < 25k.
2. Evaluate SCP, NCP, BCCP and SDLC on top of them: upper-tail and worst-stratum coverage and size, with Holm-corrected Wilcoxon tests against unweighted SDLC.
3. Discuss the result in Sections 6.1 and 7. Add the references after verifying them.

**Action type:** new experiment + text.

---

## 4. Moderate

### C1-24 (moderate) The shift experiment has no shift-aware competitor

**Raised by:** A8.

**Argument:** The tilt weights exp(gamma z) are known, so weighted split conformal is trivial to run. Without it, "robust to moderate shift" has no reference point.

**Corrective action:**
1. Add weighted split CP with label likelihood-ratio weights (absolute-residual and density scores) in two forms: oracle weights, and weights estimated by a logistic classifier that separates calibration targets from a tilted resample.
2. Report tilted marginal coverage, stratum-wise coverage and size in Table 9.
3. State in Section 7 that stratified calibration's advantage is that it needs no shift estimate.

**Action type:** new experiment (from cached outputs) + text.

### C1-25 (moderate) Strong covariate-conditional baselines are missing

**Raised by:** A3.

**Argument:** The adaptive baselines actually run are Mondrian-yhat and three methods that share the possibly mis-specified LS density (C1-05). Gibbs-Cherian-Candès conditional calibration, CHR and RLCP are cited but not run.

**Corrective action:** Add Gibbs et al. (the conditionalconformal package; function class = intercept + yhat and sigma-hat quintile indicators + a linear term), CHR on the 40-bin classifier, and RLCP on the absolute residual. Run on 31 datasets x 10 seeds at alpha = 0.1, and report them in Table 3.

**Action type:** new experiment (no base-model refit).

### C1-26 (moderate) The floor variant is presented as a contribution, and the hull and floor forms are compared only against BCCP

**Raised by:** A1, A10.

**Arguments:**
- C_floor is the union of two valid sets. It adds nothing unless beta > alpha, and it over-covers marginally (0.918).
- Prior art for joint marginal and group guarantees: Kandinsky CP, Gibbs et al. (2025), and BFQR's level optimisation.
- There is no S-NCP-hull, S-NCP-floor or BCCP-floor, so the hull and floor claims cannot be judged.

**Corrective action:**
1. Present the floor as a practical remark, and remove it from the contributions in 00_front and 01_intro. Cite the alternatives.
2. Compute S-NCP-hull, S-NCP-floor and BCCP-floor (beta = 2 alpha) from cache, for alpha in {0.05, 0.1, 0.2}. Add them to Tables 3, 5, 8 and 9 and to the H3 family.
3. The size-optimal joint-constraint rule is optional (see C1-13(b), C1-16).

**Action type:** text + re-analysis.

### C1-27 (moderate) The reported LS set geometry is not the set whose coverage is scored, and ls_exact.py is untested

**Raised by:** A2, A9.

**Arguments:**
- Size, pieces, hull and alerts come from a 2048-point grid, but coverage uses the exact rule.
- Cells that straddle a stratum edge take the centre's stratum. The comment "clip pieces to their stratum" is not implemented, and pieces beyond 12 are merged.
- Grid and exact membership disagree for 0.43% of test points overall and up to 3.5% (socmob). This produces an impossible result on auction_verification: alert recall (0.923) is below coverage (0.942).
- `tests/test_conformal.py` has no test of `ls_exact.py`.

**Corrective action:**
1. Compute the level sets exactly. g-hat is piecewise linear on its table, so the crossings can be solved for, then intersected with each B_k at its own threshold.
2. Add unit tests:
   - membership equals the exact rule (S[3]);
   - sizes match a brute-force fine-grid integral, including ties at cut points;
   - the floor variant's dual guarantee holds by Monte Carlo;
   - strata merging is correct with tied targets.
3. Re-evaluate the LS family from cache, and report whether any figure in Tables 3, 4, 5, 7 or 8 changes.

**Action type:** code fix + re-analysis.

### C1-28 (moderate) The development and diagnostic datasets are excluded only for H1, and two diagnostic datasets are unnamed

**Raised by:** A3, A4, A5.

**Arguments:**
- The exclusion matters for H3 (size), because the development datasets were used to choose the density estimator.
- The reviewers' recomputations show that H3 survives both exclusions: excluding the 3 development datasets, SDLC/BCCP is 0.922 (Holm p = 0.0089); excluding them plus the 5 named diagnostic datasets, 0.920 (Holm p = 0.0075). The manuscript does not show this.

**Corrective action:**
1. Name all 7 diagnostic datasets in Section 5.7 (from EXPERIMENT_LOG item 10).
2. Add T3b-style tables for H3 (6 tests plus the hull test) excluding (a) the development datasets and (b) the development plus diagnostic datasets.
3. Add one sentence to Section 6.3.

**Action type:** re-analysis + text.

### C1-29 (moderate) Table 5 sign conventions and several summary statements are wrong

**Raised by:** A3, A4, A9, A10.

**Arguments:**
- **(a) W/L are inverted for size.** `paired_wilcoxon` counts d > 0 as a win, so SDLC vs BCCP shows W = 9, L = 22, whereas the text says SDLC was smaller on 22. The r_rb sign convention is not explained.
- **(b) "r_rb >= 1.00" is impossible;** the minimum is 0.996.
- **(c) The stated ranges silently exclude the hull variants.** "90.7%-90.9%" upper-tail and "89.0%-89.3%" worst-stratum coverage leave out SDLC-hull (0.912, 0.900) and BCCP-hull (0.895).
- **(d) WSC is averaged over 27 datasets** (NaN for n_test < 200), but the caption says 31.
- **(e) The arithmetic "Size (mean)" column is dominated by forest_fires.**
- **(f) Percentages and decimals are mixed** in the conclusion.

**Corrective action:**
1. Define W as "SDLC better" with a direction per metric, regenerate Table 5 and the hull test (`code/src/statistics/tests.py`, `code/scripts/analyze.py`), and state the r_rb convention.
2. Write "r_rb >= 0.99" and define or widen the ranges.
3. State n = 27 for WSC and why four datasets are missing.
4. Replace or annotate the mean-size column (see C1-09), and harmonise number formats.

**Action type:** code fix + text.

### C1-30 (moderate) Statistical reporting refinements

**Raised by:** A4, A9.

**Points:**
- **(a) Inference from non-significance.** "Statistically indistinguishable (p = 1.000)" is used as evidence of equivalence. Add TOST equivalence on worst-stratum and marginal coverage, margin +/-0.01 stated in advance.
- **(b) Unstable CIs.** Percentile bootstrap CIs of medians are unstable and disagree in sign with r_rb. Replace them with Hodges-Lehmann estimates and exact Walsh-average CIs, and keep BCa only for geometric-mean ratios.
- **(c) The decile 7-9 dips are within sampling error** (p = 0.19-0.43), and decile 7 lies inside the bulk stratum. Add CIs to Fig. 1, and drop the "outer end" explanation for decile 7.
- **(d) Friedman/Nemenyi is promised in Section 5.6 but never reported.** Either report it as descriptive (sentence plus CD diagram in the supplement, `figures/F5_friedman_ranks.png`) or delete the promise.

**Action type:** re-analysis + text.

### C1-31 (moderate) The claim of independent observations with no repeated measures or temporal structure is false for several datasets

**Raised by:** A5.

**Arguments:**
- sarcos has 4,446 exact duplicates (its test set appended).
- video_transcoding has 68,784 rows from 1,099 videos.
- superconductivity: 40% of rows share a feature vector.
- Moneyball is a team x season panel; kings_county includes repeat sales; socmob is a contingency table.
- Theorem 1 still holds for exchangeable draws from the same finite population, but the guarantee does not transfer to new videos, new materials or future seasons.

**Corrective action:**
1. Rewrite 03_setup Section 5.2 and 05_discussion Section 7.3, and delete the sentence "no repeated measurements or temporal structure".
2. Robustness experiment (4 datasets x 10 seeds):
   - (a) sarcos de-duplicated;
   - (b) video_transcoding with GroupShuffleSplit by video;
   - (c) superconductivity grouped by feature vector;
   - (d) Moneyball with a temporal split (descriptive only).

**Action type:** text + new experiment.

### C1-32 (moderate) The domain D includes impossible negative values and inflates sizes unevenly; "immaterial" is wrong for forest_fires

**Raised by:** A5.

**Arguments:**
- **Below-zero share of mean set size:** forest_fires SCP 19.4%, DLS 22.5%; socmob SCP 27.3%, S-NCP 18.6%. The bias shrinks the marginal sizes most, so the price is understated: forest_fires 9.6 vs about 12.3 without negatives.
- **Out-of-domain targets.** forest_fires seed 8 has 2.3% of test targets outside D, all in the upper stratum, which caps its coverage at 0.85.

**Corrective action:**
1. Intersect D with the support declared per dataset before analysis (y >= 0; cpu_activity <= 100), in `strata.py`.
2. Recompute sizes, Table 4 and the error analysis from cache.
3. Report the maximum out-of-domain fraction per run and per tail stratum.
4. Soften "immaterial", or widen the upper margin by a pre-declared training-only rule.

**Action type:** code fix + re-analysis.

### C1-33 (moderate) Data-entry outliers (brazilian_houses) and SD normalisation distort dataset statistics

**Raised by:** A5.

**Arguments:**
- brazilian_houses has rows with total = 1.12M BRL where hoa = 1.117M. Across seeds y_train_sd ranges from 6,266 to 22,469, so Table 2's skewness of 58.95 and RMSE/sd of 1.00 are artefacts.
- forest_fires' training SD ranges from 26 to 87, depending on whether the 1,090.84 ha fire lands in training.
- nsize = size / sd per seed weights the seeds unevenly.

**Corrective action:**
1. Pre-declare a plausibility rule for implausible records, and report results with and without the flagged records.
2. In Table 2, report the median-over-seeds RMSE/sd and a robust skewness measure (Bowley or octile).
3. As a sensitivity check, normalise size by the training IQR or MAD, and recompute Fig. 7 and the Spearman analyses.

**Action type:** re-analysis.

### C1-34 (moderate) The calibration-size sensitivity confounds degenerate (infinite-threshold) strata with efficiency

**Raised by:** A6.

**Arguments:**
- At f = 0.25, about 86 of 310 runs have at least one stratum returned whole; at f = 0.5, about 28. Marginal coverage rises to 0.913-0.917.
- "Kept every stratified method valid" is trivially true when whole strata are returned.
- The text omits S-NCP (1.297).
- Only the calibration set is subsampled, so the experiment does not represent a genuinely small dataset.

**Corrective action:**
1. Record and report n_strata_inf for each alpha, scheme and calibration fraction (`evaluate_from_cache.py`).
2. Report sizes with and without the degenerate runs, and add S-NCP to the text.
3. Optional whole-data subsampling experiment: the 12 datasets with n >= 10k, n in {500, 1000, 2000}, 10 seeds each.

**Action type:** code fix + re-analysis (+ optional new experiment).

### C1-35 (moderate) Fit-time accounting is not like-for-like, and the cost-benefit trade-off is not discussed

**Raised by:** A7. A7 rated it major; it is moderate here because it does not affect any scientific conclusion.

**Arguments:**
- The `density_LS` timer also covers mu and sigma predictions on train, calibration and test, plus the legacy 200-cell tabulation. That accounts for 80-90% of the "density" time on large datasets.
- SDLC-2p therefore appears cheaper to fit than SDLC, although it fits two extra GBDTs.
- The fit times were measured with four concurrent tasks on four cores.

**Corrective action:**
1. Re-time each component in isolation: single process, BLAS/OMP threads = 1, LightGBM n_jobs = 1; seed 0 of all 31 datasets; 3 repetitions.
2. Report fitting only, prediction charged to every method that uses the model, the KDE as its own row, and no legacy `cells()` call.
3. Rewrite Table 13 and the Section 6.7 comparison of 2.04 s with 0.34 s.
4. Add the Pareto plot and cost-benefit paragraph of C1-02(5). Mention that one SDLC fit serves every alpha, whereas CQR needs new quantile models per alpha.

**Action type:** code fix (`run_benchmark.py`, `timing.py`) + new experiment (short re-timing).

### C1-36 (moderate) Excessive length, overloaded tables, inconsistent method names and unused figures

**Raised by:** A9.

**Arguments:**
- The body is about 15,000 words: 45 pages, 13 tables and 8 figures.
- Table 6 has 34 rows of internal codes (DLS-M-LS, MCP-yhat, S-Res, O-HDR-X).
- The method schematic F0 and the Proposition 1 figure F1 are unused.

**Corrective action:**
1. Cut the main text to about 10-11k words. Move Tables 7, 10, 11, 12 and 13 and most of Table 6 to the supplement, with one-line summaries in the text.
2. Use the paper's method names in every table (`code/scripts/tables_spec.py`).
3. Add F0 as Fig. 1.

**Action type:** text (+ table regeneration).

### C1-37 (moderate) The supplementary material cited in the text does not exist, and the licence table is missing

**Raised by:** A9, A5.

**Arguments:**
- "Table S3" is cited but does not exist.
- The v1 results and the licence/ID table exist only as loose files.
- S1 and S2 are never referenced.
- socmob is licensed for non-commercial use only, and ten datasets carry the uninformative licence string "Public".

**Corrective action:**
1. Assemble one Supplementary PDF:
   - S1 per-dataset results;
   - S2 leakage audit, re-run (C1-45);
   - S3 v1 pre-registered results and H3;
   - S4 OpenML ID, version, source, citation and licence;
   - the relocated tables.
2. Reference each item from the text.
3. Do not redistribute raw data (download via the API); note the socmob restriction.

**Action type:** text + re-analysis (table assembly).

### C1-38 (moderate) Submission readiness: placeholders, no reviewer access to the code, and the breadth of the AI-use declaration

**Raised by:** A9.

**Arguments:**
- Authors, affiliations, CRediT, competing interests, funding, acknowledgements and the repository URL are placeholders.
- Code is promised only "upon acceptance".
- The generative-AI declaration covers literature search, code, orchestration of experiments and drafting, which an editor may query against Elsevier policy.

**Corrective action:**
1. Fill all placeholders in 00_front and 07_declarations.
2. Deposit the code and raw_eval now, under a Zenodo DOI or an anonymised reviewer link, and cite it.
3. Check the AI declaration against the current Elsevier Guide for Authors. State truthfully and concretely what the human authors did (verifying proofs, analysis decisions and numbers). This is for the authors to confirm; do not invent author activities.

**Action type:** text (requires author input).

### C1-39 (moderate) Reference rendering and bibliographic formatting

**Raised by:** A8.

**Arguments:**
- Six @misc arXiv entries render with no identifier: boruah2026 x2, lee2026split, yi2025distribution, santos2026loboost and angelopoulos2024theoretical. LoBoost should be cited as TMLR.
- PMLR volumes and article numbers (PNAS, Stat, AIR) are missing, and the NeurIPS 2017-2021 entries lack pages and list editors.
- Capitalisation errors: {M}ondrian, {B}ayesian, McInerney, and "dAlché-Buc" without its apostrophe.
- The Bairaktari co-author is wrong (Zhiwei Steven Wu).
- Author names are inconsistent (Barber; Candes vs Candès), the sort order is wrong, and Vovk 2012 and 2013 are both cited for the same paper.

**Corrective action:**
1. Fix `supplementary/references_verified.bib`: arXiv DOIs (10.48550/arXiv.x) or journal = {arXiv preprint ...}, volumes and pages, braced capitals, names, the TMLR citation.
2. Fix the CSL mapping for PMLR volumes.
3. Cite only Vovk 2013 unless priority requires the 2012 version.
4. Re-render and check that every entry carries a DOI, an arXiv identifier or a stable URL.

**Action type:** text (bib/CSL).

---

## 5. Minor

### C1-40 (minor) Algorithm 1 cost statement, Table 13 statistics and timing environment

**Raised by:** A7.

**Points:**
- Algorithm 1 says 3 GBDT fits; the code runs 5 (mean, 3 OOF scale folds, final scale).
- The KDE costs O(n_tr x 4096); the stratum lookup costs O(G log K); memory peaks at O(chunk x G), about 200 MB.
- Table 13 pools repetitions and includes warm-up runs.
- Hardware, software and thread settings are unspecified.

**Corrective action:**
1. Correct Algorithm 1 in 02_theory and state the scaling to large n. Optionally use a binned or FFT KDE.
2. Recompute Table 13 as per-dataset medians, dropping the warm-up, with microseconds per test point and single-query latency.
3. Report the hardware and software versions, and set thread environment variables in `timing.py`.

**Action type:** text + re-analysis + code fix (small).

### C1-41 (minor) Theory statement fixes

**Raised by:** A2.

**Points:**
- **(a)** The Appendix A Remark attributes to Proposition 1 a property of stratified sets. State it as a corollary for C* in the Gaussian model, and call the pattern empirical for the estimated sets.
- **(b)** The "convexity argument" existence claim in Section 3.2 is vacuous, since C = R satisfies it. Delete it, or state and prove the nontrivial version.
- **(c)** HPD-split and S-HPD for the two-piece (LS2) density ignore the side-specific scales (`ls_exact.py` lines 28-33, 65-66). Compute H per x, or drop the HPD-LS2 variants.
- **(d)** The q_k = +inf exception is stated incompletely. It also occurs when the r_k-th score is +inf, coverage of out-of-domain targets is zero, and the upper bound requires P(Y not in D) = 0.

**Action type:** text (09_appendix, 02_theory) + code fix for (c).

### C1-42 (minor) Missing or under-credited related work

**Raised by:** A1, A8.

**Points:**
- **(a)** pintervals' `pinterval_ccp` (clustered Mondrian), which addresses the sparse-strata remedy mentioned in Section 7.3.
- **(b)** Conformal Thresholded Intervals (Luo & Zhou, AAAI 2025). Optionally add stratified CTI to the score ablation.
- **(c)** Wang et al. Thm 4.1 as the regression precedent for Theorem 1.
- **(d)** Rephrase "not studied within the imbalanced-regression literature" to acknowledge BCCP and BFQR.
- **(e)** Romano, Barber, Sabatti & Candès (2020, HDSR) on equalized coverage.

All of these, together with DenseWeight and Balanced MSE (C1-23), Jin & Candès (C1-21), Barber et al. (C1-15) and Kiyani et al. (C1-13), must be verified before they are added to `references_verified.bib` and `literature_matrix.md`.

**Action type:** text.

### C1-43 (minor) ESWA works characterised without being read, and the literature matrix is incomplete

**Raised by:** A8.

**Points:**
- Meng & Song (2024), Hajibabaee et al. (2025) and Johansson et al. (2018) are characterised but marked "Read: NONE".
- Eight cited ESWA entries are missing from `literature_matrix.md`.

**Corrective action:** Read the three papers and confirm the characterisations, or limit them to what the titles support. Add the 8 entries to the matrix with their read status.

**Action type:** text.

### C1-44 (minor) RQ2 has no matched-coverage comparison with marginal methods at a lower alpha

**Raised by:** A3.

**Corrective action:**
1. For each marginal method and dataset, find the alpha' at which its worst-stratum coverage matches SDLC's at alpha = 0.1, and compare sizes.
2. Re-evaluate from cache on alpha in {0.02, 0.03, 0.05, 0.07}. CQR needs new quantile models at these levels, so either omit it or fit them.
3. The top-1% evaluation is covered in C1-03.

**Action type:** re-analysis (+ optional fits for CQR).

### C1-45 (minor) Reproducibility package hygiene and a stale leakage audit

**Raised by:** A5, A9.

**Points:**
- `code/-` is a stray DOCX file.
- `code/scripts/review_cycle_workflow.js` is internal, with absolute paths.
- The README title differs from the manuscript title.
- `REPRODUCIBILITY_STATUS.md` is stale.
- The test suite has only 5 tests (extend as in C1-27).
- S2 was written before the data were regenerated (forest_fires missing_frac 0.167 vs 0).
- Deviation 1 misdescribes the FPS fix: the GPU column is 100% missing at source.

**Corrective action:**
1. Remove the stray files from the release, align the README title and update the status file.
2. Re-run `code/scripts/leakage_audit.py` and stamp S2 with the data hash and date.
3. Correct Deviation 1 in 03_setup Section 5.7, and add a check of parquet missingness against the source ARFF.

**Action type:** code fix + text.

### C1-46 (minor) Discontiguous sets with small spurious pieces hurt interpretability

**Raised by:** A9.

**Argument:** In Fig. 8, short isolated pieces appear near 380k. SDLC averages 1.48 pieces, and the hull costs 1.518 -> 1.703 in size.

**Corrective action:**
1. Report the share of sets with more than one piece and the median length of the smallest piece.
2. Discuss interpretability in Section 7.2.
3. Optionally evaluate a gap-filling rule that merges gaps smaller than a fraction of sigma-hat. Its output is a superset, so validity is preserved.

**Action type:** re-analysis + text.

---

## 6. Repeats

**None.** REVIEW_HISTORY.md has no entries, because this is the first review cycle, so no issue repeats an earlier fix.

Within this cycle, overlapping reports were merged instead of being marked as repeats. The most widely shared concerns:

| Concern | Issue | Reviewers |
|---|---|---|
| Error-analysis prose | C1-10 | 6 |
| No advantage over S-NCP / weak headline comparators | C1-02 | 6 |
| Pre-registration / post-hoc H3 | C1-01 | 5 |
| Realised strata and ties | C1-08 | 5 |
| Tail-alert claim | C1-21 | 5 |
| In-sample standardisation of g-hat | C1-05 | 3 |
| Synthetic study misspecification | C1-19 | 4 |
| MLP floor | C1-20 | 4 |
| Target-shift analysis | C1-18 | 4 |

---

## 7. Action plan

Action-type abbreviations: T = text, RA = re-analysis (cache or existing results), CF = code fix, NE = new experiment. Paths are relative to `Target_Journal_Submission/`, and `ms/` stands for `manuscript/src/`.

| ID | Priority | Action type | Files |
|---|---|---|---|
| C1-01 | critical | T + RA + NE (grid convergence from cache; confirmatory replication on new seeds/datasets) | ms/00_front.md, ms/highlights.md, ms/cover_letter.md, ms/03_setup.md, ms/04_results.md, ms/06_conclusion.md, code/scripts/analyze.py, code/experiments/evaluate_from_cache.py, supplementary/v1_preregistered_analysis, EXPERIMENT_LOG.md (read-only source) |
| C1-02 | critical | T + RA + NE (BCCP-het; score ablation; optional flexible density) | ms/00_front.md, ms/highlights.md, ms/cover_letter.md, ms/015_related.md, ms/03_setup.md, ms/04_results.md, ms/05_discussion.md, ms/06_conclusion.md, code/src/methods/conformal.py, code/src/methods/ls_exact.py, code/experiments/evaluate_from_cache.py, code/scripts/analyze.py |
| C1-03 | critical | T + RA + CF (top-1% stratum, extreme-strata scheme) | ms/00_front.md, ms/highlights.md, ms/04_results.md, ms/05_discussion.md, code/experiments/run_benchmark.py, code/experiments/evaluate_from_cache.py, code/src/methods/strata.py, code/scripts/analyze.py |
| C1-04 | major | T + RA | ms/04_results.md, ms/05_discussion.md, code/src/evaluation/metrics.py, code/scripts/analyze.py, tables/T2_main_results, tables/S1_per_dataset_results |
| C1-05 | major | CF + NE (cross-fitted scale refit, re-evaluate LS family) | code/experiments/run_benchmark.py, code/src/models/learners.py, code/src/models/density.py, ms/02_theory.md, ms/04_results.md |
| C1-06 | major | CF + RA (sensitivity grid from cache) | code/src/models/density.py, code/src/methods/ls_exact.py, code/experiments/run_benchmark.py, ms/02_theory.md, ms/04_results.md, ms/05_discussion.md |
| C1-07 | major | CF + RA | code/src/methods/conformal.py, code/src/evaluation/metrics.py, code/tests/test_conformal.py, ms/04_results.md |
| C1-08 | major | CF + RA + T | code/src/methods/strata.py, code/experiments/run_benchmark.py, code/scripts/analyze.py, ms/00_front.md, ms/03_setup.md, ms/04_results.md, tables/T1_datasets |
| C1-09 | major | RA + T | code/src/statistics/tests.py, code/scripts/analyze.py, ms/00_front.md, ms/03_setup.md, ms/04_results.md, ms/05_discussion.md, ms/06_conclusion.md |
| C1-10 | major | T + CF (renderer check) + RA | ms/04_results.md, ms/05_discussion.md, code/scripts/render_manuscript.py, code/scripts/analyze.py |
| C1-11 | major | RA + T | code/scripts/analyze.py, ms/00_front.md, ms/04_results.md, ms/06_conclusion.md |
| C1-12 | major | T + RA | ms/03_setup.md, ms/05_discussion.md, code/scripts/analyze.py |
| C1-13 | major | T (+ optional new theory) | ms/02_theory.md, ms/09_appendix.md, ms/highlights.md, ms/cover_letter.md, ms/06_conclusion.md, ms/00_front.md, supplementary/references_verified.bib, supplementary/literature_matrix.md |
| C1-14 | major | T + NE (Monte Carlo extension of Table 1) | ms/00_front.md, ms/02_theory.md, ms/05_discussion.md, ms/06_conclusion.md, code/experiments/prop1_gaussian.py |
| C1-15 | major | T + RA | ms/00_front.md, ms/01_intro.md, ms/02_theory.md, ms/09_appendix.md, ms/05_discussion.md, ms/04_results.md, supplementary/references_verified.bib |
| C1-16 | major | T + NE (faithful BFQR; level-optimised SDLC) | ms/00_front.md, ms/highlights.md, ms/cover_letter.md, ms/015_related.md, ms/02_theory.md, ms/03_setup.md, ms/06_conclusion.md, code/src/methods/conformal.py, code/scripts/analyze.py |
| C1-17 | major | T + NE (Kandinsky CP baseline) | ms/015_related.md, ms/02_theory.md, ms/05_discussion.md, supplementary/literature_matrix.md, new code/experiments script |
| C1-18 | major | RA + CF + NE (synthetic genuine label shift) | code/src/evaluation/metrics.py, code/experiments/run_benchmark.py, code/scripts/analyze.py, code/experiments/synthetic.py, ms/03_setup.md, ms/04_results.md, ms/05_discussion.md |
| C1-19 | major | NE | code/experiments/synthetic.py, ms/04_results.md, ms/05_discussion.md |
| C1-20 | major | T + RA + NE (MLP re-run) | code/experiments/run_learner_generality.py, ms/04_results.md, ms/05_discussion.md, ms/00_front.md |
| C1-21 | major | T + RA + NE (tail-classifier and conformal-selection baselines) | ms/00_front.md, ms/04_results.md, ms/05_discussion.md, ms/06_conclusion.md, ms/015_related.md, code/scripts/analyze.py, supplementary/references_verified.bib |
| C1-22 | major | RA + T | new code/scripts case-study script, ms/01_intro.md, ms/04_results.md |
| C1-23 | major | NE + T | code/experiments/run_benchmark.py, code/src/models/learners.py, ms/015_related.md, ms/04_results.md, ms/05_discussion.md, supplementary/references_verified.bib |
| C1-24 | moderate | NE + T | code/experiments/evaluate_from_cache.py, code/src/methods/conformal.py, ms/04_results.md, ms/05_discussion.md |
| C1-25 | moderate | NE | new code/experiments baseline script, code/src/methods/conformal.py, ms/03_setup.md, ms/04_results.md |
| C1-26 | moderate | T + RA | ms/00_front.md, ms/01_intro.md, ms/02_theory.md, code/src/methods/conformal.py, code/experiments/evaluate_from_cache.py, code/scripts/analyze.py |
| C1-27 | moderate | CF + RA | code/src/methods/ls_exact.py, code/tests/test_conformal.py, ms/02_theory.md |
| C1-28 | moderate | RA + T | code/scripts/analyze.py, ms/03_setup.md, ms/04_results.md |
| C1-29 | moderate | CF + T | code/src/statistics/tests.py, code/scripts/analyze.py, ms/04_results.md, ms/06_conclusion.md |
| C1-30 | moderate | RA + T | code/src/statistics/tests.py, code/scripts/analyze.py, ms/03_setup.md, ms/04_results.md, ms/05_discussion.md |
| C1-31 | moderate | T + NE | ms/03_setup.md, ms/05_discussion.md, code/experiments/run_benchmark.py (grouped/temporal split option) |
| C1-32 | moderate | CF + RA | code/src/methods/strata.py, code/src/data/openml_ctr23.py, ms/04_results.md |
| C1-33 | moderate | RA | code/scripts/analyze.py, code/src/data/openml_ctr23.py, ms/03_setup.md, ms/04_results.md, tables/T1_datasets |
| C1-34 | moderate | CF + RA (+ optional NE) | code/experiments/evaluate_from_cache.py, code/scripts/analyze.py, ms/04_results.md |
| C1-35 | moderate | CF + NE (isolated re-timing) | code/experiments/run_benchmark.py, code/experiments/timing.py, code/scripts/analyze.py, ms/04_results.md, ms/05_discussion.md |
| C1-36 | moderate | T | all ms/*.md, code/scripts/tables_spec.py, figures/F0_method_schematic.png |
| C1-37 | moderate | T + RA | supplementary/ (new Supplementary PDF), tables/, ms/04_results.md, ms/07_declarations.md |
| C1-38 | moderate | T (author input) | ms/00_front.md, ms/07_declarations.md |
| C1-39 | moderate | T | supplementary/references_verified.bib, manuscript CSL file, ms/08_references.md |
| C1-40 | minor | T + RA + CF | ms/02_theory.md, ms/04_results.md, code/experiments/timing.py, code/scripts/analyze.py |
| C1-41 | minor | T + CF | ms/02_theory.md, ms/09_appendix.md, code/src/methods/ls_exact.py |
| C1-42 | minor | T | ms/015_related.md, ms/02_theory.md, ms/05_discussion.md, supplementary/references_verified.bib, supplementary/literature_matrix.md |
| C1-43 | minor | T | ms/015_related.md, supplementary/literature_matrix.md, supplementary/eswa_paper_benchmark.md |
| C1-44 | minor | RA | code/experiments/evaluate_from_cache.py, code/scripts/analyze.py, ms/04_results.md |
| C1-45 | minor | CF + T | code/- (remove), code/scripts/review_cycle_workflow.js (exclude from release), code/README.md, REPRODUCIBILITY_STATUS.md, code/scripts/leakage_audit.py, tables/S2_leakage_audit, ms/03_setup.md |
| C1-46 | minor | RA + T | code/src/methods/ls_exact.py, code/scripts/analyze.py, ms/05_discussion.md |

### Suggested order of work

1. **Code fixes that change numbers.** C1-05, C1-06, C1-07, C1-08, C1-27 and C1-32, plus the hull/floor baselines of C1-26.
2. **Re-evaluate from cache.** Then the re-analyses: C1-02(b), C1-03, C1-04, C1-09, C1-11, C1-12, C1-15, C1-18, C1-28 to C1-30, C1-33 and C1-34.
3. **Run the new experiments by priority:**
   - **Required:** the grid-convergence check (C1-01), the score ablation and BCCP-het (C1-02), and the misspecified synthetic DGPs (C1-19).
   - **High:** faithful BFQR (C1-16), Kandinsky (C1-17), DenseWeight (C1-23) and the MLP re-run (C1-20).
   - **Recommended:** the confirmatory replication (C1-01), weighted CP (C1-24), the covariate-conditional baselines (C1-25), the grouped/temporal splits (C1-31) and the re-timing (C1-35).
4. **Reframe the text** (C1-01, C1-02, C1-03, C1-10, C1-13 to C1-17, C1-21) to match the new numbers.
5. **Editorial work:** length, supplement, bibliography and declarations (C1-36 to C1-39).

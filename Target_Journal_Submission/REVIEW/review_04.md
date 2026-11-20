# Review 04: Reviewer #4 (methodology, theory vs implementation, reproducibility)

**Journal:** Journal of King Saud University – Computer and Information Sciences (Springer Nature)
**Manuscript:** "Covering the rare outcomes: stratified conformal prediction with size-optimal density scores for imbalanced regression"
**Material inspected:** `manuscript/build/manuscript_filled.md` (Sections 3, 4, 5.3, 6.8 and Appendix A); `code/src/{models,methods,evaluation}`; `code/experiments/{run_benchmark,refit_scales,evaluate_from_cache3,run_learner_generality3,grid_convergence,timing,timing_fit,synthetic3}.py`; `code/tests/`; `code/run_all.py`; `code/README.md`; cached contexts in `results/raw_contexts{,_v3}` (seed 0); `results/raw_results_v3.csv.gz`.
**Not repeated:** the issues in `REVIEW/review_01.md`. Where an issue there was only partly fixed, I report only what is still wrong.

---

## Summary

The paper calibrates conformal thresholds within strata of the target (Mondrian/BCCP calibration). It argues that conditional-density level sets with per-stratum thresholds are size-optimal (Proposition 2), that their plug-in version is asymptotically optimal (Proposition 3), and it implements this as SDLC. SDLC uses a LightGBM location–scale model, a KDE noise density with a 1% Student-t2 defensive component fitted to cross-fitted standardised residuals, and an analytic, stratum-split set geometry.

I re-derived every proof in Appendix A. Proposition 1, Theorem 1, Proposition 2 and Corollary 1 are correct as stated. I checked the tanh total-variation bound algebraically and it holds. The proof of Proposition 3 is correct **under its own assumptions**. Those assumptions are not met by the estimator that is actually implemented, and the manuscript says the opposite (Section 4.3: "(8) can be consistent, so Proposition 3 applies").

The code mostly matches the manuscript. Eq. (3) rank, three folds, the floor ς, ε = 0.01, Silverman bandwidth, IQR/1.349 scale, the domain D, the strata quantiles, the LightGBM settings and the "eight regressions" all agree. I checked floating-point exactness of the rank formula for n ≤ 20,000 at α ∈ {0.05, 0.1, 0.2}: there are no off-by-one errors.

I found four substantive problems:
1. The noise density ĝ is measurably mis-calibrated for the residuals it is applied to at test time, and the paper's justification for the cross-fitting change is not supported by the data.
2. The "Gaussian" ablation SDLC-N is mis-scaled, and it differs from its description.
3. The geometry of the density-based sets still uses closed stratum pieces. On tied data it contradicts both Eq. (4) and the coverage rule.
4. The domain truncation caps tail coverage. It also falsifies the sentence that the Theorem 1 lower bound applies to the reported coverage.

The complexity statement in Section 4.5 does not describe the algorithm in the code.

Unit tests: `python -m pytest -q tests` ran **10 tests, all passed (32 s)**. The suite does not exercise the failure modes below. Each of issues 4 and 5 would be caught by a ten-line test.

## Recommendation

**Major revision.** Nothing I found invalidates the finite-sample stratum-wise coverage results: the coverage indicator uses the exact score rule, and Theorem 1 is sound. The efficiency story (RQ3, and the "a few per cent" advantage over S-NCP) rests on a density estimator whose calibration and ablation are flawed. The theoretical motivation (Proposition 3) is claimed for an estimator to which it does not apply. Both must be fixed before the size comparisons can be taken at face value.

---

## Issues

### 1. MAJOR: Proposition 3 is claimed for an estimator that cannot satisfy its assumption ε_N → 0

**Location:**
- Manuscript §4.3 (lines 179–181: "If Y = μ(X)+σ(X)ε … (8) can be consistent, so Proposition 3 applies"), Proposition 3 (line 154), Appendix A proof of Proposition 3.
- `code/src/models/density.py:135,160` (`eps=0.01` fixed).
- `code/experiments/refit_scales.py:49` (floor).
- `code/src/methods/ls_exact3.py:232` (score +∞ outside D).

**Evidence:** Proposition 3 requires ε_N = sup_{x,y}|f̂(y|x) − f(y|x)| → 0 in probability. The implemented f̂ violates this even under an exact location–scale model with independent noise:
- **(a) Fixed defensive weight.** ĝ = 0.99·KDE + 0.01·t₂(·/ŝ)/ŝ with ε fixed at 0.01 for every N. Hence sup|ĝ − g| ≥ 0.01·sup|t₂(·/ŝ)/ŝ − g|, which is bounded away from 0. On the 31 seed-0 datasets, the t₂ component makes up a median 0.9% (95th percentile up to 7.8%) of ĝ at the calibration residuals, so it is not asymptotically negligible.
- **(b) Fixed scale floor.** ς = max{10⁻³ sd(Y), 0.05·median|r|} does not vanish with N. Wherever σ(x) < ς on a set of positive P_X-mass, σ̂ is inconsistent.
- **(c) Score set to +∞ outside D.** Hence f̂ ≡ 0 outside a bounded D, while f(Y|X) > 0 a.s. is assumed. The sup over y ∉ D is not addressed.
- **(d) Strata.** The strata are data-dependent, and the proof explicitly "takes as given" that they converge. With the `method="lower"` quantiles and atoms used in the code (`strata.py:337`), they need not converge to the nominal cut points.
- **(e) Asymptotic regime.** The joint regime (N, n → ∞) is not stated.

I re-ran SDLC from cache with ε = 10⁻⁴ instead of 0.01 on all 31 datasets (seed 0). The geometric-mean size ratio was **1.0003** (range 0.9992–1.0055), with mean pieces 1.447 vs 1.446. The defensive component is therefore practically irrelevant, which makes the theory–implementation gap cheap to close.

**Fix:**
- Either let ε_N → 0 (e.g. ε_N = min(0.01, N^{-1/2})) and ς_N → 0, and add the assumption inf_x σ(x) > 0 together with a tail condition that makes sup_{y∉D_N} f(y|x) → 0 uniformly;
- or restate Proposition 3 for the target f_ε = (1−ε)f + ε·(defensive) and state the resulting O(ε) size bias.

In both cases:
- Replace the sentence "so Proposition 3 applies" with an accurate statement.
- State how data-dependent strata are handled: either a one-line argument that Ĉ ∩ B̂_k and Ĉ ∩ B_k differ by a set of vanishing expected measure when the cut points converge and P(Y = e_k) = 0, or an explicit restriction to continuous targets.

### 2. MAJOR: the noise density ĝ is mis-calibrated for the residuals it is applied to, and the stated reason for cross-fitting is not supported

**Location:**
- Manuscript §4.3 lines 181 ("Standardising by an in-sample scale fit shrinks the residuals … by a median factor of 1.14 … and makes ĝ too narrow"), §5.7 item (4), Algorithm 1 steps 1–3.
- `code/experiments/refit_scales.py:52–64`.
- `code/experiments/evaluate_from_cache3.py:140–149`.
- `code/src/models/learners.py:213–245`.

**Evidence:**
- **Where the mismatch comes from.** ĝ is fitted to z_cf = r_oof / σ̂_{−j}. Here:
  - r_oof comes from fold models μ̂_{−j}, trained on 2/3 of D_tr and then early-stopped on 10% of that, so about 30% of the full data.
  - σ̂_{−j} is trained on about 60% of the OOF residuals.

  At calibration and test time the standardisation is different: z = (Y − μ̂)/σ̂. Here μ̂ is trained on 90% of D_tr (about 45% of the data; it is never refitted after early stopping), and σ̂ on all OOF residuals.
- **The resulting distributions differ systematically.** Seed 0, all 31 datasets:
  - sd(z_cal) has median 1.30, while sd(z_cf) has median 1.44. The 1.14 shrinkage quoted in the paper compares the two *training* constructions, z_cf (1.39) vs in-sample (1.20) over all seeds, not either of them with the target distribution.
  - The central 90% interval of the cross-fitted ĝ covers a median **92.2%** of calibration z (10th–90th percentile 0.896–0.953). The rejected in-sample version covers **89.8%**. On central coverage, the version the paper calls "too narrow" is better calibrated than the one adopted.
  - The KS distance between the PIT of calibration z under ĝ and U(0,1) has median 0.050 and reaches 0.19–0.20 (forest_fires, brazilian_houses, socmob).
  - Mean log-likelihood favours cross-fitting on only 20 of 31 datasets.
- **Why it matters.** Validity is unaffected. But the paper's efficiency claim over S-NCP is "small, a few per cent" (§6.3, §7.1), and a 5–10% scale mis-specification of ĝ is the same order of magnitude. The direction of the bias is unknown, so the RQ3 ranking between SDLC and S-NCP is not interpretable as an effect of "the estimated noise shape".

**Fix:**
- Fit ĝ to residuals standardised by the *same* (μ̂, σ̂) used at test time. Two ways to do this:
  - split D_tr into a model part and a density part (sample splitting), or
  - fit fold models of the same effective size as the final models: refit μ̂ on all of D_tr after early stopping, with the number of rounds chosen on the validation split, and do the same for the fold models.
- Report, per dataset, the PIT/KS diagnostic and the central-coverage diagnostic on the calibration set for the adopted ĝ and for the alternatives.
- Recompute Tables 3–6 and the confirmatory ratios.
- Remove the "1.14" sentence or replace it with the calibration-set comparison.

### 3. MODERATE: the SDLC-N ablation is mis-scaled and differs from its description, so the BCCP → S-NCP → SDLC-N → SDLC decomposition is confounded

**Location:** Manuscript §4.3 line 183 ("SDLC-N replaces ĝ by the standard normal density (with the same defensive component)"), §5.4 line 248; `code/src/models/density.py:177–189`.

**Evidence:**
- σ̃ is an L2 regression of |r|, so it estimates E|r|. For Gaussian noise E|r| = 0.798·sd, so z = r/σ̂ has sd ≈ 1.25, not 1. On the cached data the median sd of calibration z is 1.30.
- `GaussianNoiseDensity` nevertheless uses N(0,1). The level set {φ(z) ≥ c·σ̂(x)} then trades z against σ̂(x) at the wrong rate, so SDLC-N is not "the normalised residual plus the factor 1/σ̂(x)".
- The defensive component is also not "the same": `GaussianNoiseDensity` sets s_t = 1 (line 184), whereas SDLC uses s_t = IQR/1.349 of z_cf.
- The step SDLC-N → SDLC therefore credits to "the estimated noise shape" what is partly a scale correction.

**Fix:** Use N(0, ŝ²) with ŝ the sd (or IQR/1.349) of the same standardised residuals, and the same s_t as SDLC. Re-run the ablation and correct the text in §4.3, §5.4 and §6.3.

### 4. MODERATE: density-based sets use closed stratum pieces, which contradicts Eq. (4) and the coverage rule on tied targets

**Location:**
- Manuscript §4.4 line 191 ("the reported geometry is therefore that of the stratum-exact set"; "Interval methods report half-open stratum pieces … as in (4)").
- `code/src/methods/ls_exact3.py:407–411` (`yhi = min(m + s·u, E[k+1])`, closed) and `:451` (coverage by exact score rule).
- README §5 (the public API returns `intervals`).

**Evidence:** The half-open fix from review cycle 1 (C1-07) was applied to `conformal.interval_method` only. In `build_sets`, the piece of stratum k ends at E[k+1] *inclusive*, so a target equal to a cut point is assigned geometrically to stratum k, but scored with the threshold of stratum k+1.

I rebuilt the SDLC sets from cache (seed 0, 31 datasets) and compared membership in the returned intervals with the exact indicator `S[6]`:
- 127 disagreements out of 134,141 test points overall.
- On **health_insurance**: **1.7%** of test points disagree. All are at y = 40, a cut point that carries 34% of the test targets, with realised strata [0,40), [40,41), [41,88.2]. In all of them the geometry says "covered" and the exact rule says "not covered".

Reported coverage is computed correctly. However, the reported sizes, hulls, pieces and alerts belong to a different set from the one that is scored, and a user of the README API (`intervals[i]`) gets sets whose empirical coverage differs from the paper's. The unit test `test_membership_matches_exact_rule` tolerates 0.2% disagreement and uses continuous data with no ties at cut points, so it cannot detect this.

**Fix:**
- Make the upper end of every non-final stratum piece open: use `nextafter(E[k+1], -inf)` as in `interval_method`, or carry an open/closed flag.
- Add a unit test with heavy ties at the cut points that requires exact agreement.
- Recompute sizes, pieces, hulls and alerts for the tied datasets (health_insurance, forest_fires, socmob, cars).

### 5. MODERATE: domain truncation caps tail coverage, and the statement that the Theorem 1 lower bound "applies to the reported coverage" is false

**Location:** Manuscript §4.4 line 189; Theorem 1 (line 131–133); `ls_exact3.py:232,451`; `metrics.py:10–20`; `strata.py:348–350`.

**Evidence:**
- **The rule creates an exception to Theorem 1.** Targets outside D = [min y − 0.05r, max y + 0.05r] receive the score +∞ and are counted as not covered even when q̂_k = +∞ (`cov = (sc ≤ thr) & in_domain`). Theorem 1's proof, by contrast, counts S_{n+1} = +∞ ≤ q̂_k = +∞ as covered. The correct guarantee for the reported coverage is P(cover | B_k) ≥ 1 − α_k − P(Y ∉ D | Y ∈ B_k). C1-41(d) raised the definition, but the sentence "so the lower bound of Theorem 1 applies to the reported coverage" was kept, and it is wrong.
- **The cap binds in practice, in the tail the paper is about.** On forest_fires, up to **2.3%** of the test targets in a split (seed 8) lie outside D. Since the upper stratum is nominally 10% (13 calibration points in that split), this is a sizeable fraction of the upper-tail test outcomes. No stratified method can cover them, whatever its threshold.
- **The truncation is not needed for SDLC.** The paper says ĝ has analytic Student-t tails so that "targets far outside the training residuals still receive a smooth, strictly decreasing density". `build_sets` already integrates the analytic tails. The upper truncation of D exists only for the convenience of the grid and interval baselines.

**Fix:**
- Either drop the upper (and, for real-valued targets, lower) truncation for the location–scale family: use B_K = [e_{K−1}, ∞), with the analytic tail, and report the infinite-threshold case as an unbounded set.
- Or keep D and restate the guarantee with the −P(Y ∉ D | B_k) term, reporting that term per dataset and per stratum, not only the overall fraction outside D.

### 6. MODERATE: the complexity and cost claims in §4.5 do not match the implementation

**Location:** Manuscript §4.5 line 208; `ls_exact3.py:359–369` (own docstring: "O(K R log G) per test point"); `experiments/refit_scales.py:44`; `experiments/timing_fit.py:109`.

**Evidence:**
- **Prediction cost.**
  - Claimed: O(G log K) per test point.
  - Implemented: for each of K strata and each of R monotone runs of the interpolant, one `np.interp` over the run, i.e. O(K·R·log G). The geometry construction also needs a sort of the KDE grid, O(G_g log G_g), when the table is built.

  R is bounded only by G. For heavy-tailed residuals the KDE has isolated bumps around outlying residuals: brazilian_houses has |z_cf| up to 336, with 1% above 72. So R can be large, which also explains the 13.5 µs vs 0.09 µs gap.
- **Number of regressions.** "Eight gradient-boosted regressions" is correct for the method. However, the released pipeline fits the four OOF/scale models twice: `refit_scales.py:44` re-runs `fit_scale` to recover r_oof, which was never cached. This doubles the scale-model cost relative to what is timed.
- **Timing set-up.** `timing_fit.py:109` fits the KDE to r/max(σ_cf, 10⁻¹²), i.e. without the floor ς used in production. The timed and the production pipelines therefore differ.

**Fix:**
- State the actual bound, O(K·R·log G) with R ≤ G, and report the median and maximum R across datasets.
- Cache r_oof in the fit stage, or say that the released pipeline fits 12 models.
- Use the production floor in `timing_fit.py`.

### 7. MINOR: the cross-fitted scale models are not fully independent of the residuals they standardise

**Location:** §4.3 line 181 ("neither μ̂ nor σ̂ has seen the residual it standardises"); `refit_scales.py:52–55`; `learners.py:240`.

**Evidence:** The OOF residuals r_a for folds a ≠ j come from mean models trained on folds that include fold j. The scale model σ̂_{−j} is trained on |r_a|, so its training targets depend on Y_j through μ̂_{−a}. The same KFold seed is used in both stages, so the folds coincide.

**Fix:** Either use nested cross-fitting, or soften the claim to "σ̂_{−j} was not trained on fold j's residuals".

### 8. MINOR: the learner protocol is described incompletely

**Location:** §5.3 line 240; `learners.py:213–223`.

**Evidence:**
- After early stopping, models are *not* refitted on the full training set. μ̂, σ̂ and the quantile and classifier models are all trained on 90% of D_tr, and the fold models on 90% of 2/3 of it. This interacts with issue 2.
- The early-stopping metric is LightGBM's default for each objective (L2 for σ̂ on |r|, pinball loss for the quantile models, multi-logloss for the classifier). This should be stated.
- `subsample_freq = 1` is needed for row subsampling to have any effect, and is not reported.

**Fix:** Add these facts to §5.3, or refit on the full D_tr with the selected number of rounds.

### 9. MINOR: small gaps in the statements of the theory

- **Theorem 1 (line 133).** The marginal statement 1 − Σ_k p_k α_k is not well defined when α_k depends on the random n_k, which the theorem allows. Write E[Σ_k p_k α_k(n_k)], or restrict this statement to fixed levels.
- **"Price of stratum-wise validity" (§4.2 line 162).** The "only if" direction, that t_1 = … = t_K is necessary for equality, needs the NP solution to be unique up to null sets. That requires strict monotonicity of the conditional law of f(Y|X) around the thresholds, which is an assumption of Proposition 3, not of Proposition 2. Add it.
- **Location–scale consequence (§4.2 line 164).** "It is empty whenever t_kσ(x) > max g" holds within stratum k only. Say so.
- **Proposition 3.** State the joint regime N, n → ∞ and that 𝔼_X refers to P_X restricted to D (see issue 1).

### 10. MINOR: the test suite checks the legacy path and misses the failure modes above

**Location:** `code/tests/test_conformal.py`, `code/tests/test_ls_exact3.py`.

**Evidence:** All 10 tests pass. However:
- `test_conformal.py` tests the v1/v2 `LocationScaleDensity` and `mask_method` path, which no longer produces any reported location–scale result.
- There is no test of:
  - ties at cut points for `build_sets` (issue 4);
  - targets outside D with q̂ = ∞ (issue 5);
  - `GaussianNoiseDensity` scaling (issue 3);
  - the cross-fitting and floor pipeline (`refit_scales`);
  - the floor variant's dual guarantee for the v3 path.
- The Monte-Carlo validity tests accept per-stratum coverage down to 1 − α − 3·SE − 0.01, which is loose, and use a fixed score that is independent of the data.

**Fix:** Add the tests listed above. Tighten the tolerance (for example by pooling more replications), and test the upper bound 1 − α + 1/(n_k + 1) as well.

### 11. MINOR: reproducibility and documentation details

- `code/README.md` line 5 says the paper was "submitted to *Expert Systems with Applications*". It should name the target journal.
- **σ̂ deciles.** The deciles of σ̂ used for the covariate-conditional diagnostic are cut at quantiles of the *test* σ̂ (`evaluate_from_cache3.py:196`), not the training σ̂ as requested in C1-04. Either state this or use training quantiles.
- **Strata construction.** Cut points use `np.quantile(..., method="lower")` and are kept only if they coincide with an edge of the 200-cell evaluation grid (`strata.py:337–338, 354–358`). Realised stratum masses are therefore systematically at or below nominal on the lower side. Neither the "lower" convention nor the grid dependence is stated in §4.4 or Algorithm 1 step 4.
- **Cache documentation.** The README says the cached contexts are not distributed, but `results/raw_contexts_v3` (310 files) and `results/raw_contexts` (32 files, seed 0 only) are present. Clarify which cache a reviewer needs in order to re-run `evaluate_from_cache3.py` for seeds 1–9; the answer is a full refit.

---

## Checklist: code vs manuscript

| Item | Manuscript | Code | Status |
|---|---|---|---|
| Rank formula Eq. (3), +∞ if r_k > n_k | ⌈(n_k+1)(1−α_k)⌉ | `conformal.py:18–22` | consistent; exact in floating point for n ≤ 20,000 |
| ε of defensive mixture | 0.01 | `density.py:135` | consistent (but see issue 1) |
| t-scale ŝ | IQR/1.349 | `density.py:143` | consistent for SDLC; **not** for SDLC-N (s_t = 1; issue 3) |
| Bandwidth | Silverman | `density.py:115–120` | consistent |
| Floor ς | max{10⁻³ sd, 0.05 median\|r_oof\|} | `refit_scales.py:49` (+10⁻¹²) | consistent; `timing_fit.py` omits it (issue 6) |
| Folds | 3 | `learners.py:235`, `refit_scales.py:52` | consistent |
| Strata quantiles | 0.10, 0.25, 0.75, 0.90 | `strata.py:291` | consistent; "lower" quantiles and grid snapping undocumented |
| Half-open strata | [e_{k−1}, e_k) | `strata.py:327–328` (assignment), `conformal.py:74` (interval pieces) | consistent for assignment and interval methods; **closed for density sets** (issue 4) |
| Domain D | [min − 0.05r, max + 0.05r] ∩ [0,∞) if y ≥ 0 | `strata.py:347–350` | consistent; consequences misstated (issue 5) |
| CQR quantile levels | α/2, 1 − α/2 | `run_benchmark.py:60–61` | consistent |
| LightGBM settings | lr 0.05, 31 leaves, 20 min leaf, 0.8/0.8, λ = 1, 2000/50 | `learners.py:206–210` | consistent; no refit after early stopping (issue 8) |
| Eight GBDT regressions | 1 + 3 + 1 + 3 | `learners.py`, `refit_scales.py` | consistent for the method; the pipeline fits 12 (issue 6) |
| Prediction cost | O(G log K) | O(K·R·log G) | **contradiction** (issue 6) |
| Prop. 3 "applies" | consistent estimator | fixed ε, fixed ς, truncated D | **contradiction** (issue 1) |

## Proof audit (Appendix A)

- **Proposition 1:** correct.
- **Theorem 1:** correct. The rank argument and the upper bound r_k/(n_k+1) < 1 − α_k + 1/(n_k+1) hold. The only gap is the marginal-statement wording (issue 9).
- **Corollary 1:** correct. I verified the chord bound and that its maximiser w̄ = √(m_k M_k) gives (√M − √m)/(√M + √m) = tanh(log(M/m)/4).
- **Proposition 2:** correct. The Neyman–Pearson integrand is non-negative pointwise. The extension to data-dependent sets follows by linearity.
- **Proposition 3:** correct as stated. Its hypotheses are not met by SDLC as implemented (issue 1).
- **Remark:** correct for C* in the Gaussian model.

# Pre-registered analysis plan: relevance-weighted density-level conformal prediction (RW-DLC)

Committed to the repository on 2026-11-20 **before** any RW method was evaluated on any real dataset. Motivation: review
round 2 (REVIEW/review_02.md) judged the stratified contribution incremental and pointed out that the open problems of
imbalanced regression (sparse extreme strata, choice of strata, the uncovered top 1 %) are not addressed; the
label-weighted "macro-coverage" approach of Bhattacharyya, Ding & Barber (arXiv:2606.28598, classification) has no
regression counterpart. This study adds one.

## 1. Method (fixed)
* Relevance function φ, fitted on the proper-training targets only: p̂_Y = Gaussian KDE of y_train with Silverman
  bandwidth (scipy.stats.gaussian_kde, bw_method="silverman"); τ = 0.01 · max_i p̂_Y(y_train,i).
  - **RW-U** ("uniform over the target range"): φ_U(y) = 1 / max(p̂_Y(y), τ).
  - **RW-H** ("half-way"): φ_H(y) = max(p̂_Y(y), τ)^(-1/2).
* Guarantee targeted: relevance-weighted coverage Cov_φ(C) = E[φ(Y) 1{Y ∈ C(X)}] / E[φ(Y)] ≥ 1 − α.
* Weighted split-conformal calibration: for a candidate y with calibration scores S_i and weights φ_i = φ(Y_i),
  q(y) = inf{s : Σ_i φ_i 1{S_i ≤ s} ≥ (1 − α)(Σ_i φ_i + φ(y))} (= +∞ if no such s); y ∈ C(x) iff s(x, y) ≤ q(y).
  Validity follows from weighted exchangeability with the known likelihood ratio dQ/dP ∝ φ(y) (Tibshirani et al. 2019).
* Scores (all use the same μ̂, σ̂, ĝ as SDLC, results/raw_contexts_v3 noise sample, same floor, same domain D):
  - **RW-DLC** (proposed; size-optimal for the weighted constraint): s(x, y) = −φ(y) f̂(y | x);
  - **RW-DLS** (ablation: weighting only in calibration): s = −f̂(y | x);
  - **RW-NCP** (ablation: weighted normalised residual): s = |y − μ̂(x)| / σ̂(x).
* Comparators recomputed on the same grid and the same splits: SCP, NCP, CQR (marginal intervals), DLS-M (marginal
  density level set), S-NCP and SDLC (five-stratum S5 design of the main benchmark).
* Geometry: y-grid of G = 4000 equally spaced points over D; a grid point is in the set iff its score ≤ its threshold;
  size = (number of included points) × (grid spacing). Coverage of each test target is decided exactly by the rule
  (not by the grid). α = 0.1 only.

## 2. Data
* Exploratory: all 31 OpenML-CTR23 datasets of the main benchmark, seeds 0–9 (same splits; contexts re-fitted by
  `experiments/run_benchmark.py --mode fitonly`, checked against the stored seed-0 contexts).
* Confirmatory: the 17 held-out datasets of the confirmatory replication, seeds 0–4 (stored contexts).
The same analysis is run on both; claims in the paper rest on the held-out data when the two disagree.

## 3. Metrics (per dataset × seed, then averaged over seeds)
Marginal coverage; Cov_φU and Cov_φH estimated on test points with φ evaluated at the test targets; coverage per
training-target decile → macro-decile coverage (mean of the ten) and worst-decile coverage; top-1 % and bottom-1 %
coverage (training-target 1 % quantiles); mean set size divided by sd(y_train); empty-set rate; Kish effective sample size
of the calibration weights (Σφ)²/Σφ²; share of test points with an infinite threshold.

## 4. Hypotheses and tests (unit of analysis = dataset; α_test = 0.05)
* **RW-1 (validity).** Dataset-mean Cov_φU of RW-DLC is equivalent to 0.90: TOST with two one-sided Wilcoxon
  signed-rank tests, margin 0.02. Supported if both one-sided p < 0.05.
* **RW-2 (marginal methods miss the weighted target).** Cov_φU of RW-DLC > that of each of SCP, NCP, CQR, DLS-M:
  one-sided Wilcoxon, Holm over the four. Supported if all four Holm p < 0.05.
* **RW-3 (extreme tail).** Top-1 % coverage of RW-DLC (φ_U) > that of SDLC: one-sided Wilcoxon. Reported with the
  mean difference and bootstrap CI.
* **RW-4 (score optimality).** Set size of RW-DLC < RW-DLS and < RW-NCP (φ_U): two-sided Wilcoxon on log sizes, Holm
  over the two; a size claim requires Holm p < 0.05 AND a 95 % bootstrap CI of the geometric-mean ratio excluding 1.
* Descriptive only (no hypothesis): RW-DLC vs SDLC and vs S-NCP in size, macro-decile and worst-decile coverage; the
  φ_H results; ESS and infinite-threshold shares.
Negative or null outcomes will be reported whatever their direction.

## 5. Deviations
Any change after this commit will be listed in the manuscript as a deviation with its reason.

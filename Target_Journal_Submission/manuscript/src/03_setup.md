# Experimental design {#sec:setup}

The study was designed to answer five research questions (RQs), each tied to one experiment. All design choices below were fixed in a configuration file before the full benchmark was run (Section [-@sec:protocol]).

* **RQ1 (tail coverage).** Do marginal and covariate-adaptive conformal methods under-cover rare target strata on real data, and does stratified calibration restore stratum-wise coverage? *Experiment 1: main benchmark.*
* **RQ2 (price).** How much larger are the sets when stratum-wise validity is required? *Experiment 2: paired comparison of each score under marginal vs. stratified calibration (ablation of the calibration component).*
* **RQ3 (score).** Does the density-level score suggested by Theorem 2 give smaller stratified sets than residual, normalised-residual, quantile and HPD scores? *Experiment 3: score ablation on real data and a synthetic study with known density.*
* **RQ4 (shift).** Do coverage guarantees survive shifts of the target distribution? *Experiment 4: importance-weighted evaluation under target tilting.*
* **RQ5 (robustness).** How sensitive are the conclusions to the miscoverage level, the number of strata, the calibration-set size, the density estimator and the base learner? *Experiment 5: sensitivity analyses.* Computational cost and an error analysis complete the evaluation.

## Datasets {#sec:data}

We use the OpenML-CTR23 suite, a curated benchmark of 35 tabular regression datasets with 500–100,000 observations, independent observations and documented provenance [@fischer2023openmlctr23]. Using a complete, externally curated suite avoids selecting datasets that favour the proposed method. We excluded, by a rule fixed in advance, the four datasets whose target takes fewer than 20 distinct values (red and white wine quality, solar flares, student performance): their outcomes are ordinal counts for which Lebesgue set size is not meaningful. The remaining {{n_datasets}} datasets (Table [-@tbl:datasets]) range from {{ds_n_min}} to {{ds_n_max}} observations and from {{ds_p_min}} to {{ds_p_max}} features after one-hot encoding; {{n_skewed}} have a target skewness above 1 in absolute value. Datasets were downloaded programmatically from OpenML; categorical features were one-hot encoded and missing values were passed to the gradient-boosting models, which handle them natively.

## Splitting, leakage control and repetitions

Each of the {{n_seeds}} predefined seeds (0–9, fixed before any result was seen) defines a random partition into proper training (50%), calibration (25%) and test (25%) sets. Every model, every stratum boundary, every density grid and every hyper-parameter decision uses the proper training set only; early stopping uses a 10% internal validation split of the proper training set. Calibration and test data are never used for fitting. The datasets in the suite were curated to contain independent observations [@fischer2023openmlctr23], so random splitting is the appropriate protocol; no dataset contains repeated measurements of the same subject or temporal structure that would require group or temporal splitting. Three small datasets (airfoil, concrete, QSAR fish toxicity) were used during development to choose the density estimator; all confirmatory statistics are also reported with these *development datasets* removed.

## Base learners

All methods share the same LightGBM models [@ke2017lightgbm] with a single fixed configuration (learning rate 0.05, 31 leaves, minimum 20 samples per leaf, row and column subsampling 0.8, $\ell_2$ penalty 1, up to 2000 rounds with early stopping after 50 rounds): a mean model $\hat\mu$, quantile models at $\alpha/2$ and $1-\alpha/2$ (for CQR), a scale model $\hat\sigma$ fitted on three-fold out-of-fold absolute residuals, and a multiclass model over 40 equal-mass target bins (histogram density). No method receives method-specific tuning, so differences between methods reflect the conformal procedures and not the base learners. A second learner family (a two-layer perceptron) is used in the robustness analysis.

## Compared methods

*Marginal or covariate-adaptive calibration (baselines).* Split conformal prediction with absolute residuals (SCP) [@papadopoulos2002inductive; @lei2018distribution]; normalised (locally weighted) conformal prediction (NCP) [@lei2018distribution]; conformalised quantile regression (CQR) [@romano2019conformalized]; Mondrian conformal regression with five bins of the point prediction (Mondrian-ŷ) [@bostrom2020mondrian]; distributional conformal prediction (DCP) [@chernozhukov2021distributional]; HPD-split [@izbicki2022cdsplit]; and density level sets with a single threshold (DLS). DCP, HPD-split and DLS use the same location–scale density as SDLC, so the comparison isolates the calibration rule.

*Stratified calibration (target-stratified conformal prediction).* The same scores with stratum-wise thresholds (3)–(4): S-SCP, S-NCP, S-CQR, S-HPD and the proposed SDLC, plus the variants SDLC-floor ($\beta=2\alpha$) and SDLC-hull. The histogram-density versions of DLS, HPD-split, DCP, S-HPD and SDLC are reported as secondary results.

## Evaluation metrics

For each test set we report marginal coverage; stratum-wise coverage (1) in each of the $K$ calibration strata; coverage in the training-target deciles and in the top and bottom 5% (strata *not* used for calibration, to test whether protection extends beyond the calibrated strata); mean set size divided by the training-target standard deviation (normalised size); the mean number of disjoint intervals per set; and worst-slab coverage (WSC) [@cauchois2021knowing] as a diagnostic of covariate-conditional coverage (slab selected on one half of the test set and evaluated on the other half, $\delta=0.1$). Stratum coverages are averaged over seeds before taking the minimum across strata ("worst-stratum coverage"), which avoids the downward bias of the minimum of noisy single-run estimates. Computing time is recorded for every fit and for calibration plus prediction.

## Statistical analysis

Following @demsar2006statistical, the unit of analysis is the dataset: metrics are averaged over seeds within each dataset and methods are compared across datasets. Paired comparisons use the Wilcoxon signed-rank test (no normality assumption; differences are paired by dataset), with Holm's step-down correction within each family of comparisons [@holm1979simple]. We report the median paired difference with a 95% bootstrap confidence interval (10,000 resamples of datasets) and the matched-pairs rank-biserial correlation as effect size. One-sided alternatives are used only for the pre-specified directional hypotheses of RQ1 and RQ4 (stratified calibration improves worst-stratum coverage); RQ3 uses two-sided tests. Multi-method rankings use the Friedman test with the Nemenyi critical difference. Size ratios are summarised by geometric means with bootstrap confidence intervals.

## Pre-registration and deviations {#sec:protocol}

The configuration (datasets, exclusion rule, seeds, split proportions, miscoverage levels $\alpha\in\{0.05,0.1,0.2\}$, strata, grid sizes, methods, sensitivity analyses) and the primary method (SDLC with the location–scale density) were fixed before running the benchmark; the hypotheses for RQ1–RQ5 were recorded at the same time. One deviation occurred: for the smallest dataset the stratified internal validation split of the histogram classifier failed (fewer validation points than classes); the affected runs were repeated with an unstratified split, a change that does not affect any other dataset.

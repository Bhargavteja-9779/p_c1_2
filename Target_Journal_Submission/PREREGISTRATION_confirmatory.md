# Pre-registered analysis plan: confirmatory replication on held-out datasets

**Status.** This document and `code/scripts/analyze_confirmatory.py` are committed to the public repository
(branch `claude/amazing-maxwell-i1mihd`) BEFORE any method has been evaluated on the confirmatory datasets. At the time of the
commit, no confirmatory evaluation file (`results/confirmatory/raw_eval_v3/`) exists. Model fitting for these
datasets (`results/confirmatory/raw_contexts*`) may be in progress; fitting produces only base-model outputs
(point, quantile, scale and histogram predictions) and no conformal-method result. The git history provides
the timestamps. Supplementary S6 of the manuscript reproduces this plan.

## 1. Motivation

On the 31 OpenML-CTR23 datasets, the implementation of the density-based methods was changed twice after
results had been seen (EXPERIMENT_LOG.md items 10–13). Every size comparison between SDLC and other stratified
methods on CTR23 is therefore exploratory. This replication tests those comparisons on data that played no role
in any design decision.

## 2. Data (fixed before this plan: `code/config/confirmatory.json`, commit 1762ec0)

* Source: the regression datasets of the tabular benchmark of Grinsztajn, Oyallon & Varoquaux (2022), OpenML
  suites 335/336.
* Removed: datasets that share source data with CTR23 (cpu_act, houses, house_sales, MiamiHousing2016,
  superconduct, diamonds, Brazilian_houses, abalone, wine_quality), duplicate versions, and targets with fewer
  than 20 distinct values (the main-study rule; analcatdata_supreme, pol).
* Remaining: 17 datasets (OpenML IDs 44056, 44061, 44068, 44069, 44134, 44137, 44139, 44142, 44143, 44145,
  44146, 45032, 45034, 45041, 45043, 45046, 45047). Datasets with more than 50,000 rows are subsampled once to
  50,000 rows with seed 2026.
* Seeds 0–4; split 50/25/25; alpha = 0.1; primary strata S5 (training quantiles 0.10, 0.25, 0.75, 0.90).
* Pipeline: exactly the final (v3) implementation of the main study, with no change to any setting:
  `experiments/run_benchmark.py --mode fitonly`, `experiments/refit_scales.py`,
  `experiments/evaluate_from_cache3.py` with `TSCP_CONFIG=confirmatory.json`.
* A dataset is dropped only if fitting or evaluation fails for software reasons. Any drop is reported with its
  reason. No dataset is dropped because of its results.

## 3. Hypotheses, tests and decision rules

Unit of analysis: the dataset (metrics averaged over the 5 seeds). SDLC = `SDLC-LS`. All tests are Wilcoxon
signed-rank tests over datasets, with Holm's correction within each family, at level 0.05.

| ID | Hypothesis | Test | Decision rule |
|---|---|---|---|
| C-H1 | SDLC has higher worst-stratum coverage than each marginal / covariate-adaptive method (SCP, NCP, CQR, Mondrian-ŷ, DCP, HPD-split, DLS) | one-sided, Holm over 7 | supported iff all 7 Holm p < 0.05 |
| C-H2 | SDLC's worst-stratum coverage is consistent with exact validity | count of datasets below the 5% quantile of the Beta–binomial null reference | consistent iff count ≤ 3 (95% quantile of Binomial(17, 0.05)); one-sided binomial test reported |
| C-H3 | SDLC's set size differs from BCCP, S-NCP, S-CQR and S-HPD | two-sided on log size ratios, Holm over 4 | "favours SDLC" iff Holm p < 0.05 and geometric-mean ratio < 1; "favours comparator" iff Holm p < 0.05 and ratio > 1; otherwise "no difference shown" |
| C-H4 | SDLC's worst-stratum coverage is equivalent to S-NCP's and BCCP's | TOST (two one-sided Wilcoxon tests), margin 0.02 | equivalent iff p_TOST < 0.05 |

Effect sizes are reported for every comparison: geometric-mean size ratio with a 95% bootstrap CI (10,000
resamples of datasets), the Hodges–Lehmann ratio with its 95% CI, wins/losses and the sign test.

## 4. Secondary, descriptive analyses (no decision rule)

Price of stratification (SDLC vs DLS); upper-tail, top-5% and top-1% coverage; empty-set rate; worst
sigma-hat-decile coverage; the C-H3 comparisons under decile strata (S10); hull variants.

## 5. Reporting

Results are reported in the manuscript (Section "Confirmatory replication") and in
`results/confirmatory/statistics_confirmatory.json`, whatever their direction. If C-H3 does not favour SDLC
against a comparator, the abstract and conclusions will say so.

# Comparison with the strongest related ESWA papers

Source for the ESWA papers: `supplementary/eswa_paper_benchmark.md` (32 ESWA papers verified on Crossref; content fields
only as far as the text could be read — FT = full text, PP = preprint, ABS = abstract, SNIP = summary). Papers whose
content could not be read are not used for comparison. Values for this manuscript come from the result files.

## 1. Evidence base

| Paper (ESWA) | Topic | Read | Datasets | Repetitions | Statistics | Ablation | Theory | Code | Held-out replication |
|---|---|---|---|---|---|---|---|---|---|
| Arteaga et al. (2023) | imbalanced regression | SNIP | 32 | > 3,000 partitions | yes (type n/a) | stratification analysis | no | n/a | no |
| Löfström et al. (2024) | Venn-Abers calibrated explanations | FT | 25 | 30 runs | none found | no | — | yes | no |
| Alahyari & Domaratzki (2026), SMOGAN | imbalanced regression | PP | 23 | 25 splits | Wilcoxon | GAN-only variant | no | not stated | no |
| Belhaouari et al. (2024) | oversampling for regression | FT | 18 + 2 image | single split | win counts | parameter sweep | no | yes | no |
| Ye et al. (2024), TSVQR | quantile regression | PP | 17 | MC-CV | Friedman + Nemenyi | no | yes (model) | yes | no |
| Shahbazi et al. (2026) | imbalanced regression | FT | 16 | 10-fold CV | none found | phase-wise | no | not stated | no |
| Sousa et al. (2024) | Mondrian-on-X CQR | PP | 3 | NN refit 100× | none found | no | no | not stated | no |
| **This manuscript** | stratified conformal regression | — | **31 (CTR23) + 17 held-out** | **10 predefined splits (+5 on held-out)** | **Wilcoxon + Holm, Hodges–Lehmann, sign test, TOST, bootstrap CIs, null reference** | **score decomposition, density estimators, strata, α, calibration size, learners** | **Props 1–3, Thm 1, Cor 1 with proofs** | **yes (one-command reproduction)** | **yes, pre-registered** |

## 2. Where the manuscript is stronger

* **Scale and rigour of the benchmark.** 31 + 17 = 48 datasets, more than any comparable ESWA conformal or
  imbalanced-regression paper identified (maximum 32, Arteaga et al. 2023), with a complete external suite (no dataset selection), predefined seeds,
  dataset-level non-parametric tests with family-wise correction, and effect sizes with confidence intervals.
* **Confirmatory replication.** No comparable ESWA paper replicates its main comparisons on held-out datasets under a
  pre-registered analysis plan. All four pre-registered hypotheses were supported.
* **Theory.** It analyses the oracle (Proposition 1 and Monte Carlo extensions), gives size-optimality (Proposition 2)
  and asymptotic optimality of the plug-in procedure (Proposition 3), explains the efficiency/coverage trade-off
  (coverage reallocation), and states the target-shift guarantee with credits (Corollary 1).
* **Honesty of reporting.** Small gains over the strongest stratified baseline, the coverage cost, and the cases where
  dedicated alert rules or simpler scores are preferable are reported in the abstract and conclusion.
* **Decision orientation.** The tail-alert study with expected-cost curves matches ESWA's applications emphasis.

## 3. Where the manuscript is weaker or at risk

* **Effect size against S-NCP is small** (geometric-mean ratio ≈ 0.98 on CTR23 and held-out data). A reviewer may judge
  the method's practical gain over a simple stratified normalised residual to be marginal. Mitigation: the paper
  presents the method within a broader contribution (theory, benchmark, decision study) and says so.
* **Stratified calibration itself is prior art** (BCCP, BFQR, Mondrian CP). Novelty rests on the score theory,
  the asymptotic result, the analysis of the trade-off and the evidence base.
* **No application-specific deployment.** The decision study uses public valuation data rather than a deployed
  expert system.
* **Length** (≈ 37 pages including appendix) is above the typical ESWA article, though within its limits.

## 4. Verdict

On evidence base, statistical rigour, reproducibility and theory, the manuscript exceeds the strongest comparable ESWA
papers identified. Its main weakness is the modest practical gain of the proposed score over the strongest stratified
baseline, which the manuscript reports openly.

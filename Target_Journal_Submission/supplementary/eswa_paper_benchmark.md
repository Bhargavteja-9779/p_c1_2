# ESWA historical paper benchmark

**Scope.** This file covers *Expert Systems with Applications* (ESWA, Elsevier, ISSN 0957-4174) papers on conformal prediction, prediction intervals and uncertainty quantification (UQ) for regression, imbalanced regression, and probabilistic regression and calibration.
**Prepared:** 2026-11-15, for the manuscript *Target-stratified conformal prediction for imbalanced regression*.
**Rule followed:** every paper below was verified to exist through `https://api.crossref.org/works/<DOI>`. Content fields are filled only to the extent the text could actually be read. Everything else is marked *not accessible* or *n/a*. No field was completed from memory.

---

## 0. How the set was built and what could be read

1. **Census of ESWA titles.** The full Crossref record list for ESWA journal articles published from 2017-01-01 onward was downloaded through the Crossref `/journals/0957-4174/works` cursor API: 21,400 records, the 2026-11-15 snapshot, including issues dated 2027. These titles were screened with regular expressions:
   - `conformal|conformali[sz]ed|mondrian|venn` matched 15 titles. Thirteen are genuinely about conformal prediction. One false positive, 10.1016/j.eswa.2026.135041 on "conformal laser wire additive manufacturing", was excluded.
   - An imbalanced-regression pattern matched 7 titles.
   - The pattern for prediction intervals, UQ, quantile regression, probabilistic and calibration work matched about 55 titles, mostly hybrid interval-forecasting pipelines for time series.
2. **Cross-checks.** Semantic Scholar relevance and bulk search with `venue = Expert Systems with Applications` was used, together with arXiv `jr:`/`co:` searches for "Expert Systems with Applications". These found no additional relevant ESWA paper.
3. **Citation counts.** Counts are Crossref `is-referenced-by-count` on 2026-11-15. They are lower than Google Scholar counts.
4. **Access limits.**
   - ScienceDirect returned HTTP 403.
   - The Elsevier API was not used.
   - The OpenAlex free daily budget was exhausted for this network.
   - SSRN, RCAAP (Lisbon), DiVA and the UGR repository returned bot challenges.
   - Content was therefore read only from arXiv versions, open-access PDFs on author sites, the Semantic Scholar abstract field, author or group pages, GitHub READMEs, and search-engine summaries.

**Reading-level codes used in the tables**

| Code | Meaning |
|---|---|
| **FT** | Full text read. Either the open-access published PDF, or an arXiv version whose journal-ref is the ESWA paper. |
| **PP** | Full text of a *preprint* read. The ESWA version may differ. |
| **ABS** | Abstract read, verbatim or from an author page or README. Experimental details come from the abstract only. |
| **SNIP** | Only a search-engine or repository summary of the abstract was available. Treat as weak. |
| **NONE** | No abstract or full text accessible. Only the Crossref bibliographic data are verified. |

---

## 1. Summary table (32 verified ESWA papers)

`#DS` is the number of datasets. "Stats" means formal statistical tests. "Seeds/rep." means repeated runs or splits.

### A1. Conformal prediction in ESWA (complete title-level census, 2017–2026)

| # | DOI | First author et al. (year) | Short title | Cites | Read | #DS | Stats | Seeds/rep. | Ablation | Code |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 10.1016/j.eswa.2017.12.041 | Johansson et al. (2018) | Interpretable regression trees using conformal prediction | 30 | NONE (+secondary) | n/a | n/a | n/a | n/a | n/a |
| 2 | 10.1016/j.eswa.2023.122322 | Sousa et al. (2024) | Improving CQR through cluster-based feature relevance | 17 | PP | 3 | none found | NN refit 100× | no | not stated |
| 3 | 10.1016/j.eswa.2023.123087 | Bastos (2024) | Conformal prediction of option prices | 11 | ABS | simulation + 1 empirical | n/a (abstract only) | n/a (abstract only) | n/a (abstract only) | n/a (abstract only) |
| 4 | 10.1016/j.eswa.2024.123743 | Meng & Song (2024) | Uncertainty forecasting system for tropical cyclone tracks based on CP | 13 | NONE | n/a | n/a | n/a | n/a | n/a |
| 5 | 10.1016/j.eswa.2024.126231 | Hajibabaee et al. (2025) | Carbonation depth of recycled aggregate concrete: CP intervals | 24 | NONE | n/a | n/a | n/a | n/a | n/a |
| 6 | 10.1016/j.eswa.2021.115942 | Oucheikh et al. (2022) | Product verification using OCR classification and Mondrian CP | 16 | ABS | 1 (grocery images) | n/a (abstract only) | n/a (abstract only) | n/a (abstract only) | n/a (abstract only) |
| 7 | 10.1016/j.eswa.2025.130417 | Wang et al. (2026) | Personalized FL with mixture of experts and CP for household energy | 9 | NONE | n/a | n/a | n/a | n/a | n/a |
| 8 | 10.1016/j.eswa.2025.130582 | La et al. (2026) | Inverse optimization of rice husk ash concrete via copula design spaces and conformal quantile surrogates | 19 | NONE | n/a | n/a | n/a | n/a | n/a |
| 9 | 10.1016/j.eswa.2026.134356 | Dey et al. (2027) | Robust conformal GP regression for CO2 laser engraving | 0 | PP (SSRN abstract, different title) | 1 (125-run factorial) | n/a | n/a | n/a | n/a |
| 10 | 10.1016/j.eswa.2026.135089 | Malik et al. (2026) | Uncertainty-aware CP of compressive strength in low-carbon UHPC | 0 | NONE | n/a | n/a | n/a | n/a | n/a |
| 11 | 10.1016/j.eswa.2026.135042 | Carvalho Silva et al. (2027) | Physics-informed KANs with CP for engine optimization | 0 | NONE | n/a | n/a | n/a | n/a | n/a |
| 12 | 10.1016/j.eswa.2026.132721 | Chen et al. (2026) | Heterogeneous autonomous vehicles at intersections using GNNs and CP | 0 | NONE | n/a | n/a | n/a | n/a | n/a |
| 13 | 10.1016/j.eswa.2021.116483 | Shanmugam et al. (2022) | Conformal isotonic separation for binary classification | 2 | NONE | n/a | n/a | n/a | n/a | n/a |
| 14 | 10.1016/j.eswa.2022.116864 | Farouq et al. (2022) | Conformal anomaly detection for fleet monitoring (district heating) | 6 | NONE | n/a | n/a | n/a | n/a | n/a |
| 15 | 10.1016/j.eswa.2024.123154 | Löfström et al. (2024) | Calibrated explanations: with uncertainty information and counterfactuals (Venn-Abers) | 21 | FT (arXiv, ESWA journal-ref) | 25 | none found | 30 runs/dataset | no | yes (GitHub) |

### A2. Imbalanced regression in ESWA

| # | DOI | First author et al. (year) | Short title | Cites | Read | #DS | Stats | Seeds/rep. | Ablation | Code |
|---|---|---|---|---|---|---|---|---|---|---|
| 16 | 10.1016/j.eswa.2024.124118 | Belhaouari et al. (2024) | Oversampling techniques for imbalanced data in regression | 49 | FT (OA, CC BY) | 18 tabular + 2 image | no (win counts, rank plots) | single 67/33 split; 243 configs/dataset | parameter sweep only | yes (GitHub) |
| 17 | 10.1016/j.eswa.2024.125526 | Dolar et al. (2025) | UQ-driven ML for improving accuracy in imbalanced regression | 16 | ABS (GitHub README) | "several benchmark" + 1 application | n/a | n/a | n/a | yes (GitHub `tubadolar/uqdir`) |
| 18 | 10.1016/j.eswa.2023.121011 | Arteaga et al. (2023) | Soft computing to actively address imbalanced regression | 8 | SNIP | 32 | yes (type not accessible) | >3,000 partitions | stratification analysis | n/a |
| 19 | 10.1016/j.eswa.2026.131908 | Shahbazi et al. (2026) | Hybrid imbalanced regression (data + algorithm level) | 0 | FT (arXiv, ESWA journal-ref) | 16 | none found | 10-fold CV (target-stratified) | yes (phase-wise) | not stated |
| 20 | 10.1016/j.eswa.2026.133032 | Alahyari & Domaratzki (2026) | SMOGAN: oversampling with GAN refinement for imbalanced regression | 0 | PP (arXiv v2) | 23 | Wilcoxon signed-rank | 25 random 80/20 splits | GAN-only variant | not stated |
| 21 | 10.1016/j.eswa.2026.132358 | Kim et al. (2026) | CenterIR: imbalance-aware deep regression for EEG depression severity | 0 | NONE | n/a | n/a | n/a | n/a | n/a |
| 22 | 10.1016/j.eswa.2025.127845 | Mo et al. (2025) | Learning from imbalance: cross-server power prediction via domain-adaptation regression | 1 | SNIP | 1 real-world | n/a | n/a | n/a | n/a |

### A3. Prediction intervals, probabilistic regression and quantile regression in ESWA

| # | DOI | First author et al. (year) | Short title | Cites | Read | #DS | Stats | Seeds/rep. | Ablation | Code |
|---|---|---|---|---|---|---|---|---|---|---|
| 23 | 10.1016/j.eswa.2017.01.054 | Xu et al. (2017) | Composite quantile regression neural network with applications | 99 | SNIP | n/a | n/a | n/a | n/a | n/a |
| 24 | 10.1016/j.eswa.2018.10.043 | Marín et al. (2019) | PI methodology based on fuzzy numbers (fuzzy systems and NNs) | 78 | ABS | 2 real (microgrid load, residential consumption) | n/a (abstract only) | n/a (abstract only) | n/a (abstract only) | n/a (abstract only) |
| 25 | 10.1016/j.eswa.2025.127728 | Nguinabé et al. (2025) | Bootstrap prediction intervals for LSTM | 25 | NONE | n/a | n/a | n/a | n/a | n/a |
| 26 | 10.1016/j.eswa.2023.121396 | Shi et al. (2024) | A distribution-free method for probabilistic prediction | 0 | ABS (author page, paraphrased) | n/a | n/a | n/a | n/a | none linked |
| 27 | 10.1016/j.eswa.2023.121239 | Ye et al. (2024) | Twin support vector quantile regression (TSVQR) | 14 | PP (arXiv v1) | 17 (6 synthetic + 11 real) | Friedman + Nemenyi | Monte Carlo CV mentioned | no | yes (author group site) |
| 28 | 10.1016/j.eswa.2023.122786 | Hu et al. (2024) | Asphalt pavement friction via IGWO-NGBoost | 30 | NONE | n/a | n/a | n/a | n/a | n/a |
| 29 | 10.1016/j.eswa.2023.121286 | Wang et al. (2024) | Causal carbon price interval prediction (LUBE + multi-objective EA + LSTM) | 37 | NONE | n/a | n/a | n/a | n/a | n/a |
| 30 | 10.1016/j.eswa.2025.127932 | Ochoa et al. (2025) | Probabilistic load forecasting with tailored-kernel mixture density networks | 11 | NONE | n/a | n/a | n/a | n/a | n/a |
| 31 | 10.1016/j.eswa.2022.119097 | Hao et al. (2023) | Data-augmentation estimation for censored QRNN | 12 | NONE | n/a | n/a | n/a | n/a | n/a |
| 32 | 10.1016/j.eswa.2024.124404 | Golnari et al. (2024) | Probabilistic deep learning and transfer learning for cryptocurrency prediction | 29 | NONE | n/a | n/a | n/a | n/a | n/a |

**Coverage of the request.**
- 32 verified ESWA papers in total.
- 26 published in 2023–2026, counting cover-dated 2027 issues.
- The most cited relevant items are included: Xu 2017 (99), Marín 2019 (78), Belhaouari 2024 (49), Wang 2024 (37), Johansson 2018 (30) and Hu 2024 (30).
- 15 of the 32 papers have readable content (FT, PP, ABS or SNIP), and 1 more has a secondary description only.

---

## 2. Paper cards (fields filled only from what was read)

### A1 — Conformal prediction

**[1] Johansson, U., Linusson, H., Löfström, T., Boström, H. (2018).** *Interpretable regression trees using conformal prediction.* ESWA 97, 394–404. DOI 10.1016/j.eswa.2017.12.041.
- **Read: NONE.** No abstract was accessible: ScienceDirect returned 403, and neither DiVA nor any preprint was reachable.
- **Secondary information only.** A 2026 arXiv paper (arXiv:2609.24528), seen through a search snippet, describes this work as conformal regression trees. The trees use leaf-wise normalisation, and Mondrian (per-leaf) calibration gives validity for each leaf rule at the cost of wider intervals.
- Datasets, baselines, metrics, seeds, tests and code: **not accessible**.
- **Relevance:** the closest ESWA precedent for *Mondrian* conformal regression. Its categories are defined by X (tree leaves), not by Y.

**[2] Sousa, M., Tomé, A. M., Moreira, J. (2024).** *Improving conformalized quantile regression through cluster-based feature relevance.* ESWA 238, 122322. DOI 10.1016/j.eswa.2023.122322.
- **Read: PP.** arXiv:2207.02808v8 (Nov 2022), titled "Improved conformalized quantile regression". The ESWA version may differ.
- **Problem:** the single conformal correction in CQR is not adaptive.
- **Method:** cluster the covariates, weighted by permutation importance, with an optimised K-means, then apply k conformal steps (one per cluster). This is a Mondrian-on-X CQR.
- **Datasets:** 3 (BlogFeedback, Boston housing, Bike sharing).
- **Baselines:** CQR, QR, naive split CP.
- **Metrics:** coverage and width summary statistics (mean, median, quantiles of width).
- **Protocol:** three-way split with 50% training. The FFNN is trained 100 times. No statistical tests, no ablation, and no code statement in the preprint.

**[3] Bastos, J. A. (2024).** *Conformal prediction of option prices.* ESWA 245, 123087. DOI 10.1016/j.eswa.2023.123087.
- **Read: ABS** (Semantic Scholar abstract).
- **Problem:** quantify the uncertainty of option-price predictions.
- **Method:** split-conformal prediction intervals around gradient boosting machines. Evaluated on simulated option prices and then on American call and put options on individual stocks.
- **Baselines:** "non-conformal prediction intervals", which under-cover.
- **Metrics:** empirical coverage and interval width, including by moneyness and time to maturity, and as a function of training size.
- **Seeds, tests, ablation, code:** n/a (abstract only).

**[4] Meng, F., Song, T. (2024).** *Uncertainty forecasting system for tropical cyclone tracks based on conformal prediction.* ESWA 249, 123743. DOI 10.1016/j.eswa.2024.123743.
- **Read: NONE.** A 2025 arXiv paper (2506.06638) states only that this work applied CP to cyclone-track forecasting.
- All other fields: not accessible.

**[5] Hajibabaee, P., Behnood, A., Ngo, T., Mohammadi Golafshani, E. (2025).** *Carbonation depth assessment of recycled aggregate concrete: An application of conformal prediction intervals.* ESWA 268, 126231. DOI 10.1016/j.eswa.2024.126231.
- **Read: NONE.** An SSRN preprint exists (10.2139/ssrn.4971568), but Crossref holds no abstract and SSRN returned 403.
- **Genre (from the title):** an application of CP intervals to one material-science prediction task.

**[6] Oucheikh, R., Pettersson, T., Löfström, T. (2022).** *Product verification using OCR classification and Mondrian conformal prediction.* ESWA 188, 115942. DOI 10.1016/j.eswa.2021.115942.
- **Read: ABS.**
- **Problem:** fraud and miss-scan detection at self-checkout (barcode switching, miss-scan).
- **Method:** a three-component system: OCR reading, then NLP text classification, then product verification with Mondrian (class-conditional) CP.
- **Data:** image data from existing grocery stores. The number of datasets was not stated in the abstract.
- **Baselines, metrics, seeds, code:** n/a (abstract only).
- **Relevance:** Mondrian or label-conditional CP already appears in ESWA, but for classification.

**[7] Wang, J. et al. (2026).** *Personalized federated learning with mixture of experts and conformal prediction for household energy forecasting.* ESWA 300, 130417. DOI 10.1016/j.eswa.2025.130417.
- **Read: NONE.**

**[8] La, H., Uddin, M., Nguyen, T. (2026).** *Reliable inverse optimization of rice husk ash concrete via copula-based design spaces and conformal quantile surrogates.* ESWA 301, 130582. DOI 10.1016/j.eswa.2025.130582.
- **Read: NONE.**

**[9] Dey, N., Khan, M. M. A., Sayem, A. (2027).** *Robust conformal Gaussian process regression for CO2 laser engraving: distribution-free uncertainty quantification and automated quality gating.* ESWA 333, 134356. DOI 10.1016/j.eswa.2026.134356.
- **Read: PP-abstract only.** The abstract is the Crossref record of SSRN preprint 10.2139/ssrn.6881388, which has a different title ("Surrogate modelling for CO2 laser ablation response in PMMA with interval-calibrated uncertainty estimation"). That abstract does not mention conformal prediction, so the ESWA version evidently adds it.
- **Preprint content:**
  - Models: GPR, SVR, MLP, RF and polynomial ridge, tuned with the Grey Wolf Optimizer.
  - Data: a 125-run full-factorial experiment.
  - Analysis: VIF multicollinearity diagnostics.
  - Results: R² ≈ 0.999 and 0.998.
  - Calibration metrics: PICP ≥ 0.94 and NLPD at the 95% level.
- Seeds, tests and code: n/a.

**[10] Malik, U. J., Mohotti, D., Mo, H., Lee, C. K. (2026).** *Uncertainty-aware conformal prediction of compressive strength in low-carbon UHPC.* DOI 10.1016/j.eswa.2026.135089. No volume was assigned in Crossref at the time of the check.
- **Read: NONE.**

**[11] Carvalho Silva, M. H. et al. (2027).** *Physics-informed Kolmogorov-Arnold networks with conformal prediction for multi-objective engine optimization.* ESWA 335, 135042. DOI 10.1016/j.eswa.2026.135042.
- **Read: NONE.**

**[12] Chen, Y. et al. (2026).** *Cooperative optimization of heterogeneous autonomous vehicles at intersections using graph neural networks and conformal prediction.* ESWA 326, 132721. DOI 10.1016/j.eswa.2026.132721.
- **Read: NONE.**

**[13] Shanmugam, P. et al. (2022).** *Conformal isotonic separation for binary classification.* ESWA 193, 116483. DOI 10.1016/j.eswa.2021.116483.
- **Read: NONE.**

**[14] Farouq, S., Byttner, S., Bouguelia, M.-R., Gadd, H. (2022).** *A conformal anomaly detection based industrial fleet monitoring framework: a case study in district heating.* ESWA 201, 116864. DOI 10.1016/j.eswa.2022.116864.
- **Read: NONE.**

**[15] Löfström, H., Löfström, T., Johansson, U., Sönströd, C. (2024).** *Calibrated explanations: with uncertainty information and counterfactuals.* ESWA 246, 123154. DOI 10.1016/j.eswa.2024.123154.
- **Read: FT** (arXiv:2305.02305v3, whose journal-ref is this ESWA paper).
- **Problem:** unstable and uncalibrated local feature-importance explanations that carry no uncertainty.
- **Method:** Calibrated Explanations, built on Venn-Abers. It gives calibrated probabilities, feature weights with uncertainty intervals, and counterfactual rules.
- **Datasets:** 25 binary-classification datasets (UCI, PROMISE).
- **Baselines:** LIME and SHAP.
- **Metrics:** stability and robustness (variance of feature weights over runs) and calibration.
- **Protocol:** 30 runs per dataset with only the seed varied.
- **Statistical tests:** none found in the text scan.
- **Code:** GitHub (`Moffran/calibrated_explanations`).

### A2 — Imbalanced regression

**[16] Belhaouari, S. B., Islam, A., Kassoul, K., Al-Fuqaha, A., Bouzerdoum, A. (2024).** *Oversampling techniques for imbalanced data in regression.* ESWA 252, 124118. DOI 10.1016/j.eswa.2024.124118.
- **Read: FT** (open-access CC BY PDF from the author site).
- **Problem:** skewed continuous targets.
- **Method:**
  - KNNOR-Reg: KNN oversampling adapted to regression.
  - KNNOR-DeepReg: target-aware autoencoders.
  - Auto-Inflater: an autoencoder with an exponential loss.
  - Multi-level conv/FC autoencoders for images.
- **Datasets:** 18 tabular datasets from Branco's IR repository and KEEL: ANACALT, bank8FM, baseball, boston, compactiv, concrete, cpuSm, ele-1, ele-2, forestFires, friedman, laser, machineCPU, mortgage, quake, stock, treasury, wankara. Plus 2 image datasets: AgeDB and IMDB-WIKI.
- **Baselines:** no augmentation and SMOTER, across 19 regressors.
- **Metrics:**
  - RMSE.
  - A new relative-max error (RMaxE).
  - MAE, MSE, R², explained variance and MedAE.
  - Win counts.
- **Protocol:** a single 67/33 train/test split per dataset. A grid of 243 augmentation configurations per dataset gives 53,217 experiments in total.
- **Statistical tests:** none (rank plots only). No robustness study.
- **Code:** GitHub.

**[17] Dolar, T., Chen, J., Chen, W. (2025).** *Uncertainty quantification driven machine learning for improving model accuracy in imbalanced regression tasks.* ESWA 261, 125526. DOI 10.1016/j.eswa.2024.125526.
- **Read: ABS** (abstract reproduced in the public GitHub README `tubadolar/uqdir`).
- **Problem:** imbalanced regression degrades accuracy.
- **Method:** UQDIR. Epistemic UQ identifies rare samples, and a new weight function then resamples the existing training samples.
- **Datasets:** "several benchmark datasets", plus a metamaterial-design application.
- **Baselines:** "similar imbalanced regression methods".
- **Metrics, seeds, tests:** n/a (abstract only).
- **Code:** yes.
- **Relevance:** it uses UQ *for* imbalanced regression, but to improve point accuracy. It gives no coverage guarantee.

**[18] Arteaga, M., Gacto, M. J., Galende, M., Alcalá-Fdez, J., Alcalá, R. (2023).** *Enhancing soft computing techniques to actively address imbalanced regression problems.* ESWA 234, 121011. DOI 10.1016/j.eswa.2023.121011.
- **Read: SNIP** (paraphrased abstract from the SIMIDAT group page; the UGR open-access PDF was blocked by a bot check).
- **Method:** two multi-objective evolutionary fuzzy-rule-based algorithms that handle imbalance *during learning* ("active", as opposed to "passive" preprocessing).
- **Datasets:** 32, with more than 3,000 partitions.
- **Baseline:** SMOGN, described as the best passive method.
- **Findings:** stratifying the partitions had no clearly significant effect. The methods improve accuracy statistically on most metrics; on the imbalance metric they are only slightly better than SMOGN.
- **Code:** n/a.

**[19] Shahbazi, S., Mohammadi, H., Afsharchi, M. (2026).** *Hybrid imbalanced regression through unified data-level and algorithm-level balancing.* ESWA 322, 131908. DOI 10.1016/j.eswa.2026.131908.
- **Read: FT** (arXiv:2606.01221v1, whose journal-ref is this ESWA paper).
- **Method:** a five-phase pipeline:
  1. Adaptive target-bin partitioning.
  2. A conditional VAE.
  3. Cluster-wise SMOGN.
  4. A latent-density weighted loss.
  5. Gated fusion.
- **Datasets:** 16: california, compactiv, cpu_small, heat, wine_quality, abalone, space_ga, debutanizer, available_power, maximal_torque, fuel_consumption_country, acceleration, airfoil, mortgage, treasury, concreteStrength.
- **Baselines:** MLP, XGBoost, linear regression, KNN, SVR and ridge without imbalance handling. In the ablations, each phase is replaced by quantile binning, SMOGN, MSE or concatenation.
- **Metrics:** RMSE, MAE, R².
- **Protocol:** 10-fold CV with folds stratified by target bins, and a fixed `random_state` of 42.
- **Statistical tests:** none found. A phase-wise ablation is included, plus a skewness-versus-gain analysis.
- **Code:** not stated.

**[20] Alahyari, S., Domaratzki, M. (2026).** *SMOGAN: Synthetic minority oversampling with GAN refinement for imbalanced regression.* ESWA 329, 133032. DOI 10.1016/j.eswa.2026.133032.
- **Read: PP** (arXiv:2504.21152v2).
- **Method:** SMOGN-generated samples are refined by DistGAN, which uses an adversarial loss plus an MMD loss.
- **Datasets:** 23, from KEEL, Branco et al. and Avelino et al.
- **Baselines:** SMOGN, GAN-only, no oversampling, random oversampling, G-SMOTE, WSMOTER.
- **Metrics:** RMSE, SERA, and precision, recall and F-measure for regression.
- **Protocol:** 25 random 80/20 splits per dataset.
- **Statistical tests:** Wilcoxon signed-rank (α = 0.05), reported as significant wins.
- **Code:** not stated in the preprint.

**[21] Kim, N. et al. (2026).** *CenterIR: an imbalance-aware deep regression framework for EEG-based depression severity estimation in older adults.* ESWA 323, 132358. DOI 10.1016/j.eswa.2026.132358.
- **Read: NONE.** Listed as open access, but it could not be retrieved.

**[22] Mo, R., Lin, W., Liu, G., Liu, H., He, L. (2025).** *Learning from imbalance: cross-server power prediction in large data centers via domain adaptation regression.* ESWA 287, 127845. DOI 10.1016/j.eswa.2025.127845.
- **Read: SNIP** (abstract summary from a search engine).
- **Problem:** semi-supervised domain-adaptation regression where server heterogeneity creates distribution shift and the power labels are imbalanced.
- **Method:** ICSP, which aligns the joint distributions of source and target servers with unbalanced optimal transport.
- **Data:** one real-world data-centre dataset.
- **Baselines:** existing domain-adaptation regression methods.
- Other fields: n/a.

### A3 — Prediction intervals, probabilistic regression and calibration

**[23] Xu, Q., Deng, K., Jiang, C., Sun, F., Huang, X. (2017).** *Composite quantile regression neural network with applications.* ESWA 76, 129–139. DOI 10.1016/j.eswa.2017.01.054.
- **Read: SNIP.**
- **Method:** a composite quantile regression neural network (CQRNN) that combines composite QR with ANNs. It is reported to outperform standard ANNs.
- Other fields: n/a.
- The most cited paper in this set (99).

**[24] Marín, L. G., Cruz, N., Sáez, D., Sumner, M., Núñez, A. (2019).** *Prediction interval methodology based on fuzzy numbers and its extension to fuzzy systems and neural networks.* ESWA 119, 128–141. DOI 10.1016/j.eswa.2018.10.043.
- **Read: ABS.**
- **Method:** prediction intervals from affine combinations of fuzzy numbers. Fuzzy and NN interval models are trained on a criterion that combines coverage probability and normalised average width, with no distributional assumption.
- **Baseline:** a covariance-based PI method.
- **Data:** load of the Huatacondo microgrid (Chile) and residential consumption in Loughborough (UK), forecast up to two days ahead.
- **Metrics:** coverage (PICP) and normalised width.
- Seeds, tests, code: n/a (abstract only).

**[25] Nguinabé, J., Rockefeller, R., Mamode Khan, N., Canas Rodrigues, P. (2025).** *Bootstrap prediction intervals for the LSTM recurrent neural network.* ESWA 284, 127728. DOI 10.1016/j.eswa.2025.127728.
- **Read: NONE.**

**[26] Shi, Q. et al. (2024).** *A distribution-free method for probabilistic prediction.* ESWA 237, 121396. DOI 10.1016/j.eswa.2023.121396.
- **Read: ABS** (paraphrased from the co-author's publication page).
- **Method:** distribution-free probabilistic prediction for real-valued regression, trained by boosting, with a variant that gives unbiased mean estimation.
- Datasets and other fields: n/a.
- **Code:** none linked.

**[27] Ye, Y., Xu, Z., Zhang, J., Chen, W., Shao, Y. (2024).** *Twin support vector quantile regression.* ESWA 237, 121239. DOI 10.1016/j.eswa.2023.121239.
- **Read: PP** (arXiv:2305.03894v1).
- **Method:** two smaller QPPs that produce non-parallel quantile planes, solved by dual coordinate descent.
- **Datasets:** 6 synthetic, 5 UCI benchmark, 2 large-scale, 2 time-series and 2 imbalanced.
- **Baselines:** SVQR, ε-SVQR, Online-SVQR, GPQR.
- **Metrics:** pinball risk, RMSE, MAE, MAPE and CPU time.
- **Statistical tests:** Friedman with Nemenyi post-hoc, citing Demšar (2006).
- **Code:** code and synthetic data on the authors' group site.

**[28]–[32]** Hu et al. (2024, IGWO-NGBoost, 10.1016/j.eswa.2023.122786), Wang et al. (2024, LUBE carbon-price intervals, 10.1016/j.eswa.2023.121286), Ochoa et al. (2025, mixture density networks, 10.1016/j.eswa.2025.127932), Hao et al. (2023, censored QRNN, 10.1016/j.eswa.2022.119097) and Golnari et al. (2024, probabilistic DL for cryptocurrency, 10.1016/j.eswa.2024.124404).
- **Read: NONE** for all five. Only the Crossref metadata are verified.
- Titles indicate application-driven hybrid interval or probabilistic forecasting.

---

## 3. Synthesis: what ESWA publishes in this area

These conclusions rest on the **15 papers with readable content**. Fields marked NONE were not used. They are signals, not a full census of experimental practice.

### 3.1 Two distinct genres

1. **Application papers that use CP or PIs as a UQ layer.** Examples: option prices [3], cyclone tracks [4], concrete [5][8][10], laser engraving [9], engines [11], energy FL [7], autonomous vehicles [12], microgrid load [24].
   - **Novelty:** bringing a known UQ method (split CP, CQR, LUBE, bootstrap, fuzzy PIs) into a new domain pipeline, often alongside metaheuristic tuning (Grey Wolf Optimizer, whale optimisation) or a hybrid model.
   - **Data:** typically **one** domain dataset or simulation study.
   - **Metrics:** PICP or coverage plus mean or normalised width, sometimes NLPD.
   - **Baselines:** "non-conformal" or parametric intervals and several ML regressors.
   - **Statistical testing:** rarely visible.
   - Most of the 13 ESWA conformal papers belong to this genre. Only [1], [2] and arguably [3] are method-centred.
2. **Method papers with multi-dataset benchmarks.** This is mostly imbalanced regression and quantile regression: [16], [18], [19], [20] and [27]. Their evaluation depth is markedly higher.
   - **Datasets:** **16–32** public datasets (16, 18+2, 23, 32; 17 for TSVQR), drawn mostly from the Branco/Torgo IR collection, KEEL and UCI.
   - **Repetition:** 10-fold CV [19], 25 random splits [20], or >3,000 partitions [18]. A single split [16] was still accepted.
   - **Statistical tests:** used in 3 of the 5 readable method papers. Wilcoxon signed-rank in [20], Friedman + Nemenyi in [27], and unspecified tests in [18]. None in [16] or [19].
   - **Ablation:** appears mainly in the newest (2026) papers [19][20].
   - **Code:** released in [15], [16], [17] and [27]. That is 4 of the 7 papers whose full text or README could be read.

### 3.2 What the strongest and most cited ones share

- **A general method plus a clear practical story.** The most cited items either introduced a reusable model class with applications (CQRNN [23], 99 cites; fuzzy-number PIs [24], 78), or a broad open benchmark with code (KNNOR-Reg [16], 49 cites in about 2.5 years).
- **Breadth over depth of theory.** None of the readable ESWA papers in this area proves finite-sample guarantees beyond citing standard CP results. ESWA rewards methodology plus empirical breadth and application value more than new theory.
- **Imbalanced-regression baselines are standard.** SMOTER, SMOGN, G-SMOTE, WSMOTER and random oversampling recur. The standard metrics are SERA and the precision, recall and F-measure for regression of Torgo & Ribeiro, with RMSE and MAE.
- **Mondrian or category-conditional CP has ESWA precedent,** in [1] (tree leaves in X), [2] (X-clusters) and [6] (classes in classification). None of the 32 papers calibrates within **strata of the target Y** for regression. No ESWA paper was found that combines conformal coverage guarantees with imbalanced regression; [17] uses UQ but not coverage.

### 3.3 Implications for the manuscript, benchmarked against ESWA practice

| Dimension | ESWA typical (readable subset) | Manuscript as described | Recommendation |
|---|---|---|---|
| Datasets | 1 (application genre); 16–32 (method genre) | 31 OpenML-CTR23 datasets | At the top of the ESWA range. Add 1 application case study to fit ESWA's applications emphasis. |
| Repetitions | 10-fold CV, 25 random splits, or a single split | ? | Use ≥ 10–25 random splits per dataset and report mean ± s.e. |
| Statistical tests | Wilcoxon or Friedman + Nemenyi in 3 of 5 readable method papers | ? | Use Friedman + Holm-corrected Wilcoxon (Demšar 2006; Holm 1979), or the Bayesian signed-rank test (Benavoli et al. 2017). |
| Baselines | Domain or ML baselines; SMOGN-family for IR | ? | Required: split CP, CQR, CHR, DCP, CD-split/HPD-split, Mondrian-on-X (Boström & Johansson 2020) and **bin-conditional CP (BCCP; Randahl et al. 2026)**. Recommended: EOC/BFQR (Wang et al. 2023), and LoBoost or regression-tree local CP for the LightGBM setting. |
| Metrics | Coverage and width; SERA and F1 for IR | Per-stratum coverage and set size | Add worst-stratum coverage, interval score (Gneiting & Raftery 2007), and rare-region coverage weighted by SERA-style relevance. |
| Ablation and robustness | Present in 2026 method papers | Label-shift robustness | Add ablations on number of strata, binning rule, density estimator, and calibration size per stratum. |
| Code | 4 of 7 checkable papers release code | ? | Release code and the seeds and splits. ESWA does not mandate it, but the strongest papers do. |

**Novelty positioning.** ESWA accepts application-level novelty, but a method paper is judged on whether the algorithm is new. Y-stratified (bin-conditional) conformal calibration for regression has direct prior art outside ESWA: Randahl, Williams & Hegre, *Political Analysis* 2026 (arXiv 2024), and the binned fair quantile regression of Wang et al. (NeurIPS 2023). See `literature_matrix.md` §1. The manuscript's defensible contributions are therefore:
1. The conditional-density level-set score with **size-optimality under per-stratum coverage**, a regression analogue of Sadinle et al. (2019).
2. The finite-sample per-stratum analysis and the label-shift robustness statement.
3. The large-scale 31-dataset LightGBM benchmark against all conditional-coverage competitors.

These need to be framed accordingly.

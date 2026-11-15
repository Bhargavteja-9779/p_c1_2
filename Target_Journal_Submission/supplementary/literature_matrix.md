# Literature matrix: target-stratified conformal prediction for imbalanced regression

**Prepared:** 2026-11-15
**Entries:** 65 verified references. Matching BibTeX is in `references_verified.bib`, and the keys below are the BibTeX keys.

**Verification protocol**
- **DOI entries:** `https://api.crossref.org/works/<DOI>`, plus BibTeX from `doi.org` content negotiation.
- **arXiv entries:** the arXiv API (`export.arxiv.org/api/query?id_list=`).
- **Entries without a DOI:** the official proceedings pages (PMLR `citation_*` metadata, JMLR `.bib` files, NeurIPS proceedings pages and BibTeX) or the OpenReview API.
- **Year:** the print or issue year is used where Crossref reports an earlier online-first year. The online year is noted.
- **Limit:** nothing below was filled from memory except the one-line descriptions of canonical papers. These are deliberately generic, and the abstracts of all newer or threat papers were read through arXiv.

---

## 1. PRIOR-ART THREATS: Y-stratified, label-conditional and bin-conditional conformal methods for regression

Sources searched:
- arXiv full-text abstract search: `conformal` combined with `imbalanced regression`, `label-conditional`, `Mondrian` + `regression`, `bin-conditional`, `outcome space`, `target-conditional`, `response-conditional`, `label shift` + `regression`, `extreme` + `coverage`, `skewed`, `long-tailed`.
- Semantic Scholar relevance search for "conformal prediction imbalanced regression" and "label-conditional conformal prediction regression".
- Web search.
- A Crossref title census of ESWA.

Result: **no paper titled or framed as "conformal prediction for imbalanced regression" was found.** arXiv returns zero abstracts containing both "conformal" and "imbalanced regression". However, the **core mechanism has been published**.

| Threat | Reference (verified) | What it does | Overlap with the manuscript | Honest assessment |
|---|---|---|---|---|
| **HIGH: direct prior art** | Randahl, Williams & Hegre (2026). *Bin-conditional conformal prediction of fatalities from armed conflict.* Political Analysis 34(1):96–108. DOI 10.1017/pan.2025.10010 (online 2025); arXiv:2410.14507 (Oct 2024). Key `randahl2026bin` | "Bin-conditional conformal prediction (BCCP)". The calibration scores are partitioned by user-defined **bins of the observed outcome y**. At test time, split CP is run per bin over a grid of hypothetical y in that bin, and the per-bin sets are combined: either their union (discontiguous) or the hull ("contiguized"). The authors state it guarantees coverage in each bin under within-bin exchangeability, and call it a hybrid of label-conditional (Mondrian) CP and split CP. Evaluated on simulations and one heavily skewed outcome (conflict fatalities). R package `pintervals` on CRAN. | **Same calibration principle:** Mondrian calibration on Y-bins, per-stratum coverage, motivated by skewed outcomes and under-coverage of the sparse upper range. | The **Y-stratified calibration step is not novel** and must be cited and positioned against BCCP. BCCP uses a residual score with no optimality result, user-chosen bins, no label-shift analysis, and one real application rather than a benchmark. The manuscript can still claim: (i) the density level-set score and its size-optimality under per-stratum coverage; (ii) formal finite-sample per-stratum guarantees with label-shift robustness; (iii) a 31-dataset benchmark. **BCCP must be a baseline.** |
| **HIGH: partial prior art** | Wang, Cheng, Guo, Liu & Yu (2023). *Equal opportunity of coverage in fair regression.* NeurIPS 36:7743–7755. DOI 10.52202/075280-0340; arXiv:2311.02243. Key `wang2023equal` | Defines Equal Opportunity of Coverage: coverage equal across groups *conditional on the true label Y*. The method, Binned Fair Quantile Regression (BFQR), splits **Y into M equal-mass bins** on the calibration set and calibrates per (group, bin), then uses conformal prediction to maintain coverage. Its motivating figure shows standard methods mis-cover the head and tail salary bins. Code is public. | Y-binned conformal calibration in regression, and the observation that tails of Y are mis-covered. | Goal is fairness across a sensitive attribute A, not imbalanced regression, but the binning-on-Y device is the same. Cite it as prior art for Y-conditional coverage in regression, and consider it as a baseline with A ≡ constant. |
| **MEDIUM: conceptual prior art** | Vovk, Gammerman & Shafer (2005; 2nd ed. 2022), Mondrian conformal predictors; Vovk (2012/2013) on label-conditional validity; Toccaceli & Gammerman (2019) | Mondrian taxonomies may depend on the label; label-conditional validity is a standard ICP property. | Finite-sample per-stratum validity of Mondrian ICP with Y-defined categories follows from the general Mondrian theorem. | The per-stratum finite-sample guarantee should be presented as an *instance* of Mondrian validity, with the novelty in the score and optimality. Do not claim it as a new type of guarantee. |
| **MEDIUM: optimality theorem** | Sadinle, Lei & Wasserman (2019) JASA 114:223–234; Lei (2014) Biometrika 101:755–769; Lei, Robins & Wasserman (2013) JASA 108:278–287; Izbicki, Shimizu & Stern (2022) JMLR 23(87) (HPD-split) | Sadinle et al. derive the minimum-ambiguity set-valued classifiers under total or **class-specific** coverage; the class-specific solution thresholds p(y\|x) with class-specific cut-offs. Lei et al. (2013) and HPD-split (Izbicki et al.) give level-set or HPD optimality under marginal or conditional coverage. | A "conditional-density level-set score that is size-optimal among sets with per-stratum coverage" is the **continuous-Y, stratified analogue** of Sadinle et al.'s class-specific result, combined with HPD-split. | Present the theorem as an extension: Lebesgue-measure objective, strata of a continuous Y, stratum-specific level thresholds. Cite Sadinle et al. explicitly. Reviewers familiar with this literature will otherwise object. |
| **MEDIUM: generalising framework** | Bairaktari, Wu & Wu (2025) ICML, PMLR 267:2581–2602 (Kandinsky CP) | The abstract (read) says the framework "handles overlapping and fractional group memberships defined jointly on covariates and labels". It encompasses covariate-group-conditional, class-conditional and **Mondrian** CP as special cases, with a minimax-optimal high-probability conditional coverage bound. | Disjoint Y-bins are label-defined groups, so Y-stratified calibration is plausibly a special case of this framework. | Whether its theory or experiments explicitly treat a *continuous* Y was **not verified** (abstract only). Cite it as the general framework containing label-defined groups, and position the manuscript's contribution as the optimal score plus the regression-specific analysis. |
| **LOW–MEDIUM: label-conditional coverage in classification** | Ding et al. (2023) NeurIPS; Guan & Tibshirani (2022) JRSSB | Clustered conformal prediction that pools classes with similar score distributions when there are few labelled points per class (Ding; abstract read). Label-conditional sets via density estimation (BCOPS). | Few calibration points per class mirrors the "rare stratum" problem. Ding's clustering of classes is analogous to merging sparse Y-strata. | Classification papers, so not direct threats. Cite them for the small-stratum and merging design choices. |
| **LOW–MEDIUM: same motivation, X-measurable strata** | Boruah (2026a) arXiv:2608.07589; Boruah (2026b) arXiv:2611.14521 | Applied CP for steel fatigue strength and 5 materials datasets, with 7 interval methods and 50 splits. Shows split CP holds marginal coverage but **drops to 0.758 in the highest-strength quartile**. Mondrian CP is calibrated on quartiles of **predicted** (out-of-fold) values, not the true y. The second paper corrects worst-bin statistics for finite-sample bias. | Same failure mode (under-coverage of extreme targets); Mondrian CP as remedy. | Strata are defined on ŷ (X-measurable), so the guarantee is not Y-conditional. These are recent arXiv-only preprints (2026): cite as concurrent evidence of the problem, and adopt the null-corrected worst-bin evaluation advice. |
| **LOW–MEDIUM: label shift in regression** | Yi, Tang & Wang (2025) arXiv:2510.10985; Lee et al. (2026) arXiv:2609.12386; Podkopaev & Ramdas (2021) UAI | Conformal sets under **target or label shift in regression**: likelihood-ratio weighting plus HPD sets from a weight-adjusted conditional density (Yi et al.); a label-shift-adjusted Bayesian score (Lee et al.). Weighted or label-conditional CP under label shift in classification (Podkopaev & Ramdas). | The manuscript's robustness to label shift. | Prior work handles label shift by *reweighting*. The manuscript's claim must be stated precisely: per-stratum coverage is invariant to shifts that re-weight strata, i.e. when the within-stratum distribution of (X,Y) is unchanged. Under a continuous density ratio that varies inside a stratum it holds only approximately. Cite these as the reweighting alternatives. |
| **LOW: same application area, different mechanism** | Dolar, Chen & Chen (2025) ESWA 261:125526 (UQDIR); Pasche, Lam & Engelke (2026) Extremes 29:129–155; Wang & Wang (2023) NeurIPS (VIR) | UQ used to resample rare samples in imbalanced regression (no coverage guarantee); extreme-value theory combined with CP for very high-confidence intervals; probabilistic imbalanced regression giving uncertainty as a by-product. | UQ in imbalanced or extreme regression. | No threat to the coverage mechanism. These are must-cite related work. Dolar et al. is an ESWA paper. |

**Bottom line for the authors.**
- **Do not claim** to introduce label-conditional or Y-stratified conformal calibration for regression. BCCP (2024/2026) and EOC/BFQR (2023) already do this, and Mondrian theory covers its validity.
- **The novelty can rest on:**
  - the optimal level-set score under per-stratum coverage, with a proof that generalises Sadinle et al. (2019);
  - finite-sample analysis, including small-stratum effects and data-driven stratum construction;
  - the precise label-shift statement;
  - systematic evidence on 31 datasets that even oracle X-conditional intervals under-cover rare targets, consistent with Barber et al. (2021) and Boruah (2026).
- **Required baselines:** BCCP and, where possible, BFQR.

---

## 2. Literature matrix

**Relation codes:**
- **F** = theory foundation
- **B** = baseline (should be run)
- **C** = competitor or prior art (discuss; run if feasible)
- **R** = related work
- **E** = evaluation and benchmarking methodology

### 2.1 Conformal prediction foundations

| Key | Verified citation | DOI / arXiv | One-line contribution | Rel. | Verification source |
|---|---|---|---|---|---|
| vovk2005alrw | Vovk, V., Gammerman, A., Shafer, G. (2005). *Algorithmic Learning in a Random World.* Springer. | 10.1007/b106715 | Monograph introducing conformal predictors, including Mondrian (category-conditional) conformal predictors. | F | api.crossref.org/works/10.1007/b106715 (Crossref record has no authors; authors from Open Library, ISBN 0387001522) |
| vovk2022alrw | Vovk, V., Gammerman, A., Shafer, G. (2022). *Algorithmic Learning in a Random World* (2nd ed.). Springer. | 10.1007/978-3-031-06649-8 | Updated monograph (conformal predictive distributions, conditional validity). | F | api.crossref.org/works/10.1007/978-3-031-06649-8 |
| vovk2012conditional | Vovk, V. (2012). Conditional validity of inductive conformal predictors. *ACML*, PMLR 25:475–490. | — (PMLR) | Types of conditional validity (object-, label- and training-conditional); Mondrian ICPs give category-conditional validity. | F | proceedings.mlr.press/v25/vovk12.html |
| vovk2013conditional | Vovk, V. (2013). Conditional validity of inductive conformal predictors. *Machine Learning* 92(2–3):349–376. | 10.1007/s10994-013-5355-6 | Journal version of the above. | F | api.crossref.org/works/10.1007/s10994-013-5355-6 |
| papadopoulos2002inductive | Papadopoulos, H., Proedrou, K., Vovk, V., Gammerman, A. (2002). Inductive confidence machines for regression. *ECML 2002*, LNCS 2430, 345–356. | 10.1007/3-540-36755-1_29 | Inductive (split) conformal prediction for regression. | F | api.crossref.org/works/10.1007/3-540-36755-1_29 |
| lei2018distribution | Lei, J., G'Sell, M., Rinaldo, A., Tibshirani, R. J., Wasserman, L. (2018). Distribution-free predictive inference for regression. *JASA* 113(523):1094–1111. | 10.1080/01621459.2017.1307116 | Split, full and locally weighted conformal regression with finite-sample marginal coverage. | F/B | api.crossref.org/works/10.1080/01621459.2017.1307116 |
| lei2013distribution | Lei, J., Robins, J., Wasserman, L. (2013). Distribution-free prediction sets. *JASA* 108(501):278–287. | 10.1080/01621459.2012.751873 | Conformalised density level sets; finite-sample validity plus asymptotic (minimax) optimality of level-set prediction regions. | F | api.crossref.org/works/10.1080/01621459.2012.751873 |
| lei2014bands | Lei, J., Wasserman, L. (2014). Distribution-free prediction bands for non-parametric regression. *JRSSB* 76(1):71–96 (online 2013). | 10.1111/rssb.12021 | Local conformal bands with asymptotic conditional validity. | F/R | api.crossref.org/works/10.1111/rssb.12021 |
| toccaceli2019combination | Toccaceli, P., Gammerman, A. (2019). Combination of inductive Mondrian conformal predictors. *Machine Learning* 108(3):489–510 (online 2018). | 10.1007/s10994-018-5754-9 | Inductive Mondrian (label-conditional) CP and the combination of such predictors. | F | api.crossref.org/works/10.1007/s10994-018-5754-9 |
| vovk2019nonparametric | Vovk, V., Shen, J., Manokhin, V., Xie, M. (2019). Nonparametric predictive distributions based on conformal prediction. *Machine Learning* 108(3):445–474 (online 2018). | 10.1007/s10994-018-5755-8 | Conformal predictive distributions for regression. | R | api.crossref.org/works/10.1007/s10994-018-5755-8 |
| angelopoulos2023gentle | Angelopoulos, A. N., Bates, S. (2023). Conformal prediction: a gentle introduction. *Foundations and Trends in ML* 16(4):494–591. | 10.1561/2200000101 (arXiv:2107.07511) | Tutorial and survey of CP, including class-conditional and group-conditional variants. | F | api.crossref.org/works/10.1561/2200000101 |
| angelopoulos2024theoretical | Angelopoulos, A. N., Barber, R. F., Bates, S. (2024). *Theoretical Foundations of Conformal Prediction.* arXiv:2411.11824 (v5, 2026; to be published by CUP). | arXiv:2411.11824 | Book-length theory, including Mondrian or group-conditional guarantees. | F | export.arxiv.org/api/query?id_list=2411.11824 |
| barber2021jackknife | Barber, R. F., Candès, E. J., Ramdas, A., Tibshirani, R. J. (2021). Predictive inference with the jackknife+. *Annals of Statistics* 49(1):486–507. | 10.1214/20-AOS1965 | Jackknife+ and CV+ intervals with distribution-free coverage. | R/B | api.crossref.org/works/10.1214/20-AOS1965 |

### 2.2 Conditional coverage, Mondrian and label-conditional calibration

| Key | Verified citation | DOI / arXiv | One-line contribution | Rel. | Verification source |
|---|---|---|---|---|---|
| barber2021limits | Foygel Barber, R., Candès, E. J., Ramdas, A., Tibshirani, R. J. (2021). The limits of distribution-free conditional predictive inference. *Information and Inference* 10(2):455–482 (online 2020). | 10.1093/imaiai/iaaa017 | Impossibility of exact X-conditional distribution-free coverage; relaxations. | F | api.crossref.org/works/10.1093/imaiai/iaaa017 |
| sadinle2019least | Sadinle, M., Lei, J., Wasserman, L. (2019). Least ambiguous set-valued classifiers with bounded error levels. *JASA* 114(525):223–234 (online 2018). | 10.1080/01621459.2017.1395341 | Size-optimal set-valued classifiers under total or class-specific coverage. | **F/C** (optimality analogue) | api.crossref.org/works/10.1080/01621459.2017.1395341 |
| lei2014classification | Lei, J. (2014). Classification with confidence. *Biometrika* 101(4):755–769. | 10.1093/biomet/asu038 | Set-valued classification with class-specific error control; plug-in optimality. | F | api.crossref.org/works/10.1093/biomet/asu038 |
| guan2022prediction | Guan, L., Tibshirani, R. (2022). Prediction and outlier detection in classification problems. *JRSSB* 84(2):524–546. | 10.1111/rssb.12443 | BCOPS: label-conditional conformal sets built from density estimates. | R | api.crossref.org/works/10.1111/rssb.12443 |
| bostrom2020mondrian | Boström, H., Johansson, U. (2020). Mondrian conformal regressors. *COPA 2020*, PMLR 128:114–133. | — (PMLR) | Mondrian conformal regression with categories formed from X-based difficulty estimates. | **B** (Mondrian-on-X) | proceedings.mlr.press/v128/bostrom20a.html |
| bostrom2021mondrian | Boström, H., Johansson, U., Löfström, T. (2021). Mondrian conformal predictive distributions. *COPA 2021*, PMLR 152:24–38. | — (PMLR) | Mondrian taxonomies applied to conformal predictive distributions. | R | proceedings.mlr.press/v152/bostrom21a.html |
| johansson2018interpretable | Johansson, U., Linusson, H., Löfström, T., Boström, H. (2018). Interpretable regression trees using conformal prediction. *ESWA* 97:394–404. | 10.1016/j.eswa.2017.12.041 | Conformal regression trees with per-leaf (Mondrian) calibration (ESWA precedent; abstract not accessible, see benchmark file). | R | api.crossref.org/works/10.1016/j.eswa.2017.12.041 |
| ding2023class | Ding, T., Angelopoulos, A. N., Bates, S., Jordan, M. I., Tibshirani, R. J. (2023). Class-conditional conformal prediction with many classes. *NeurIPS 36*:64555–64576. | 10.52202/075280-2817 (arXiv:2306.09335) | Clustered CP: pools classes with similar score distributions so that rare classes get approximately class-conditional coverage. | R/C | api.crossref.org/works/10.52202/075280-2817; arXiv |
| gibbs2025conformal | Gibbs, I., Cherian, J. J., Candès, E. J. (2025). Conformal prediction with conditional guarantees. *JRSSB* 87(4):1100–1126. | 10.1093/jrsssb/qkaf008 (arXiv:2305.12616) | Finite-sample coverage over user-specified function classes (groups, covariate shifts) via augmented quantile regression. | R/B (X-groups) | api.crossref.org/works/10.1093/jrsssb/qkaf008 |
| cauchois2021knowing | Cauchois, M., Gupta, S., Duchi, J. C. (2021). Knowing what you know: valid and validated confidence sets in multiclass and multilabel prediction. *JMLR* 22(81):1–42. | — (JMLR); arXiv:2004.10181 | Conditional-coverage-oriented confidence sets and worst-slab coverage as a validation metric. | E/R | jmlr.org/papers/v22/20-753.html |
| bairaktari2025kandinsky | Bairaktari, K., Wu, J., Wu, Z. S. (2025). Kandinsky conformal prediction: beyond class- and covariate-conditional coverage. *ICML 2025*, PMLR 267:2581–2602. | arXiv:2502.17264 | Conditional coverage for overlapping or fractional groups defined jointly on covariates and labels; contains Mondrian and class-conditional CP as special cases. | **C** | proceedings.mlr.press/v267/bairaktari25a.html; arXiv |
| randahl2026bin | Randahl, D., Williams, J. P., Hegre, H. (2026). Bin-conditional conformal prediction of fatalities from armed conflict. *Political Analysis* 34(1):96–108 (online 2025). | 10.1017/pan.2025.10010 (arXiv:2410.14507) | **Y-bin-conditional (Mondrian) split CP for skewed regression outcomes** (see §1). | **C/B (top threat)** | api.crossref.org/works/10.1017/pan.2025.10010; arXiv |
| wang2023equal | Wang, F., Cheng, L., Guo, R., Liu, K., Yu, P. S. (2023). Equal opportunity of coverage in fair regression. *NeurIPS 36*:7743–7755. | 10.52202/075280-0340 (arXiv:2311.02243) | Y-binned calibration (BFQR) for label-conditional, group-fair coverage in regression. | **C/B** | api.crossref.org/works/10.52202/075280-0340; arXiv |
| boruah2026distribution | Boruah, I. (2026). Distribution-free conformal prediction for steel fatigue strength: marginal validity is not enough. arXiv:2608.07589v2. | arXiv:2608.07589 | Shows top-quartile under-coverage of split CP; Mondrian on predicted-value quartiles. | C/R | export.arxiv.org/api/query?id_list=2608.07589 |
| boruah2026null | Boruah, I. (2026). Null-corrected conditional coverage in materials property prediction: a five-dataset replication. arXiv:2611.14521v1. | arXiv:2611.14521 | Worst-bin conditional-coverage statistics are biased downward; null correction for evaluation. | E/R | export.arxiv.org/api/query?id_list=2611.14521 |

### 2.3 Conformal regression scores and adaptive or local methods (baselines and competitors)

| Key | Verified citation | DOI / arXiv | One-line contribution | Rel. | Verification source |
|---|---|---|---|---|---|
| romano2019conformalized | Romano, Y., Patterson, E., Candès, E. (2019). Conformalized quantile regression. *NeurIPS 32*. | arXiv:1905.03222 | CQR: conformal calibration of quantile-regression intervals. | **B** | proceedings.neurips.cc/paper/2019/hash/5103c3584b063c431bd1268e9b5e76fb-Abstract.html |
| sesia2020comparison | Sesia, M., Candès, E. J. (2020). A comparison of some conformal quantile regression methods. *Stat* 9(1):e261. | 10.1002/sta4.261 | Empirical comparison of CQR variants. | B/E | api.crossref.org/works/10.1002/sta4.261 |
| chernozhukov2021distributional | Chernozhukov, V., Wüthrich, K., Zhu, Y. (2021). Distributional conformal prediction. *PNAS* 118(48):e2107794118. | 10.1073/pnas.2107794118 | DCP: conformity via the estimated conditional CDF (probability integral transform). | **B** | api.crossref.org/works/10.1073/pnas.2107794118 |
| izbicki2020flexible | Izbicki, R., Shimizu, G., Stern, R. (2020). Flexible distribution-free conditional predictive bands using density estimators. *AISTATS*, PMLR 108:3068–3077. | — (PMLR) | Dist-split and CD-split: conformal bands from conditional density estimators. | B/F | proceedings.mlr.press/v108/izbicki20a.html |
| izbicki2022cdsplit | Izbicki, R., Shimizu, G., Stern, R. B. (2022). CD-split and HPD-split: efficient conformal regions in high dimensions. *JMLR* 23(87):1–32. | — (JMLR); arXiv:2007.12778 | HPD-split: conditional-density level-set (HPD) conformal regions. The closest score to the manuscript's level-set score. | **B/F** | jmlr.org/papers/v23/20-797.html |
| sesia2021conformal | Sesia, M., Romano, Y. (2021). Conformal prediction using conditional histograms. *NeurIPS 34*:6304–6315. | arXiv:2105.08747 | CHR: intervals from conditional histograms, adaptive to skewness. | **B** | proceedings.neurips.cc/paper/2021/hash/31b3b31a1c2f8a370206f111127c0dbd-Abstract.html |
| guha2024conformal | Guha, E., Natarajan, S., Möllenhoff, T., Khan, M. E., Ndiaye, E. (2024). Conformal prediction via regression-as-classification. *ICLR 2024* (venue per arXiv journal-ref). | arXiv:2404.08168 | R2CCP: discretise Y into bins, learn a classifier-based density, conformalise. | **B** | export.arxiv.org/api/query?id_list=2404.08168 |
| xie2024boosted | Xie, R., Barber, R. F., Candès, E. J. (2024). Boosted conformal prediction intervals. *NeurIPS 37*:71868–71899. | 10.52202/079017-2296 (arXiv:2406.07449) | Gradient boosting of the conformity score toward conditional coverage or shorter length. | B/R | api.crossref.org/works/10.52202/079017-2296 |
| guan2023localized | Guan, L. (2023). Localized conformal prediction: a generalized inference framework for conformal prediction. *Biometrika* 110(1):33–50 (online 2022). | 10.1093/biomet/asac040 | LCP: kernel-localised calibration in X. | B/R | api.crossref.org/works/10.1093/biomet/asac040 |
| hore2025local | Hore, R., Barber, R. F. (2025). Conformal prediction with local weights: randomization enables robust guarantees. *JRSSB* 87(2):549–578 (online 2024). | 10.1093/jrsssb/qkae103 (arXiv:2310.07850) | RLCP: randomly localised CP with local and covariate-shift-robust guarantees. The arXiv v5 title ends "…enables local guarantees". | R/B | api.crossref.org/works/10.1093/jrsssb/qkae103 |
| cabezas2025regression | Cabezas, L. M. C., Otto, M. P., Izbicki, R., Stern, R. B. (2025). Regression trees for fast and adaptive prediction intervals. *Information Sciences* 686:121369. | 10.1016/j.ins.2024.121369 | Tree-based partitions of X for locally calibrated conformal intervals. | B/R | api.crossref.org/works/10.1016/j.ins.2024.121369 |
| santos2026loboost | Santos, V., Coscrato, V., Cabezas, L., Izbicki, R., Ramos, T. (2026). LoBoost: model-native local conformal prediction for gradient-boosted trees. arXiv:2602.22432v3 (TMLR 11/2026 per arXiv journal-ref). | arXiv:2602.22432 | Local CP from GBDT leaf-path partitions. Directly relevant to the LightGBM base models. | **B** | export.arxiv.org/api/query?id_list=2602.22432 |
| gao2024adjusting | Gao, R., Yin, M., McInerney, J., Kallus, N. (2024). Adjusting regression models for conditional uncertainty calibration. *Machine Learning* 113(11–12):8347–8370. | 10.1007/s10994-024-06627-7 (arXiv:2409.17466) | Trains the regressor to reduce the conditional miscoverage gap after split CP. | R | api.crossref.org/works/10.1007/s10994-024-06627-7 |
| sousa2024improving | Sousa, M., Tomé, A. M., Moreira, J. (2024). Improving conformalized quantile regression through cluster-based feature relevance. *ESWA* 238:122322. | 10.1016/j.eswa.2023.122322 | CQR with per-cluster (X) conformal steps (ESWA precedent). | R | api.crossref.org/works/10.1016/j.eswa.2023.122322 |
| kuleshov2018accurate | Kuleshov, V., Fenner, N., Ermon, S. (2018). Accurate uncertainties for deep learning using calibrated regression. *ICML*, PMLR 80:2796–2804. | — (PMLR) | Quantile recalibration of probabilistic regressors (marginal calibration). | R | proceedings.mlr.press/v80/kuleshov18a.html |

### 2.4 Distribution shift (covariate and label)

| Key | Verified citation | DOI / arXiv | One-line contribution | Rel. | Verification source |
|---|---|---|---|---|---|
| tibshirani2019conformal | Tibshirani, R. J., Foygel Barber, R., Candès, E., Ramdas, A. (2019). Conformal prediction under covariate shift. *NeurIPS 32*. | arXiv:1904.06019 | Weighted CP using likelihood ratios under covariate shift. | F/R | proceedings.neurips.cc/paper/2019/hash/8fb21ee7a2207526da55a679f0332de2-Abstract.html |
| podkopaev2021distribution | Podkopaev, A., Ramdas, A. (2021). Distribution-free uncertainty quantification for classification under label shift. *UAI*, PMLR 161:844–853. | arXiv:2103.03323 | Label-shift-robust (weighted, label-conditional) CP for classification. | **F/C** (label-shift argument) | proceedings.mlr.press/v161/podkopaev21a.html |
| yi2025distribution | Yi, M., Tang, Y., Wang, H. J. (2025). Distribution-free prediction sets for regression under target shift. arXiv:2510.10985v1. | arXiv:2510.10985 | Regression target shift: likelihood-ratio identification plus HPD sets from a weight-adjusted conditional density. | C/R | export.arxiv.org/api/query?id_list=2510.10985 |
| lee2026split | Lee, H., Kim, J., Jadamba, E., Choi, S., Shin, H. (2026). Split conformal prediction with label-shift-adjusted Bayesian scores. arXiv:2609.12386v1. | arXiv:2609.12386 | Label-shift-adjusted score plus importance weighting for regression CP. | R | export.arxiv.org/api/query?id_list=2609.12386 |

### 2.5 Extremes and rare events

| Key | Verified citation | DOI / arXiv | One-line contribution | Rel. | Verification source |
|---|---|---|---|---|---|
| pasche2026extreme | Pasche, O. C., Lam, H., Engelke, S. (2026). Extreme conformal prediction: reliable intervals for high-impact events. *Extremes* 29(2):129–155. | 10.1007/s10687-026-00536-9 (arXiv:2505.08578) | Extreme-value theory combined with CP for very high-confidence intervals. | R | api.crossref.org/works/10.1007/s10687-026-00536-9 |

### 2.6 Imbalanced regression

| Key | Verified citation | DOI / arXiv | One-line contribution | Rel. | Verification source |
|---|---|---|---|---|---|
| torgo2007utility | Torgo, L., Ribeiro, R. (2007). Utility-based regression. *PKDD 2007*, LNCS, 597–604. | 10.1007/978-3-540-74976-9_63 | Relevance and utility framework for regression with non-uniform importance of targets. | F | api.crossref.org/works/10.1007/978-3-540-74976-9_63 |
| torgo2009precision | Torgo, L., Ribeiro, R. (2009). Precision and recall for regression. *Discovery Science 2009*, LNCS, 332–346. | 10.1007/978-3-642-04747-3_26 | Precision and recall for rare-target regression. | E | api.crossref.org/works/10.1007/978-3-642-04747-3_26 |
| torgo2013smote | Torgo, L., Ribeiro, R. P., Pfahringer, B., Branco, P. (2013). SMOTE for regression. *EPIA 2013*, LNCS, 378–389. | 10.1007/978-3-642-40669-0_33 | SMOTER oversampling for regression. | R | api.crossref.org/works/10.1007/978-3-642-40669-0_33 |
| branco2016survey | Branco, P., Torgo, L., Ribeiro, R. P. (2017). A survey of predictive modeling on imbalanced domains. *ACM Computing Surveys* 49(2):1–50 (online 2016). | 10.1145/2907070 | Survey of imbalanced classification and regression. | F | api.crossref.org/works/10.1145/2907070 |
| branco2017smogn | Branco, P., Torgo, L., Ribeiro, R. P. (2017). SMOGN: a pre-processing approach for imbalanced regression. *LIDTA 2017*, PMLR 74:36–50. | — (PMLR) | SMOTER plus Gaussian-noise oversampling. | R | proceedings.mlr.press/v74/branco17a.html |
| ribeiro2020imbalanced | Ribeiro, R. P., Moniz, N. (2020). Imbalanced regression and extreme value prediction. *Machine Learning* 109(9–10):1803–1835. | 10.1007/s10994-020-05900-9 | Formalises imbalanced regression; relevance functions; SERA metric. | F/E | api.crossref.org/works/10.1007/s10994-020-05900-9 |
| yang2021delving | Yang, Y., Zha, K., Chen, Y., Wang, H., Katabi, D. (2021). Delving into deep imbalanced regression. *ICML*, PMLR 139:11842–11851. | arXiv:2102.09554 | Deep imbalanced regression benchmarks; label and feature distribution smoothing (LDS/FDS). | R | proceedings.mlr.press/v139/yang21m.html |
| wang2023variational | Wang, Z., Wang, H. (2023). Variational imbalanced regression: fair uncertainty quantification via probabilistic smoothing. *NeurIPS 36*:30429–30452. | 10.52202/075280-1326 (arXiv:2306.06599) | Probabilistic imbalanced regression with uncertainty estimates (no coverage guarantee). | R/C | api.crossref.org/works/10.52202/075280-1326 |
| avelino2024resampling | Avelino, J. G., Cavalcanti, G. D. C., Cruz, R. M. O. (2024). Resampling strategies for imbalanced regression: a survey and empirical analysis. *Artificial Intelligence Review* 57(4):82. | 10.1007/s10462-024-10724-3 | Recent survey and benchmark of resampling for imbalanced regression. | R | api.crossref.org/works/10.1007/s10462-024-10724-3 |
| dolar2025uncertainty | Dolar, T., Chen, J., Chen, W. (2025). Uncertainty quantification driven machine learning for improving model accuracy in imbalanced regression tasks. *ESWA* 261:125526. | 10.1016/j.eswa.2024.125526 | Epistemic-UQ-guided resampling for imbalanced regression (ESWA). | R | api.crossref.org/works/10.1016/j.eswa.2024.125526 |

### 2.7 Benchmark, base learner and statistical evaluation

| Key | Verified citation | DOI / arXiv | One-line contribution | Rel. | Verification source |
|---|---|---|---|---|---|
| fischer2023openml | Fischer, S. F., Feurer, M., Bischl, B. (2023). OpenML-CTR23: a curated tabular regression benchmarking suite. *AutoML Conference 2023, Workshop Track* (OpenReview). | — (OpenReview HebAOoMm94) | Curated OpenML regression benchmark suite used for the 31 datasets. | E | api2.openreview.net (note HebAOoMm94); openreview.net/forum?id=HebAOoMm94 |
| ke2017lightgbm | Ke, G., Meng, Q., Finley, T., Wang, T., Chen, W., Ma, W., Ye, Q., Liu, T.-Y. (2017). LightGBM: a highly efficient gradient boosting decision tree. *NeurIPS 30*. | — (NeurIPS) | The base learner. | E | papers.nips.cc/paper/2017/hash/6449f44a102fde848669bdd9eb6b76fa-Abstract.html |
| demsar2006statistical | Demšar, J. (2006). Statistical comparisons of classifiers over multiple data sets. *JMLR* 7:1–30. | — (JMLR) | Friedman and Nemenyi (and Wilcoxon) protocol for multi-dataset comparisons. | E | jmlr.org/papers/v7/demsar06a.html |
| benavoli2016should | Benavoli, A., Corani, G., Mangili, F. (2016). Should we really use post-hoc tests based on mean-ranks? *JMLR* 17(5):1–10. | — (JMLR) | Critique of mean-rank post-hoc tests; recommends pairwise tests. | E | jmlr.org/papers/v17/benavoli16a.html |
| benavoli2017time | Benavoli, A., Corani, G., Demšar, J., Zaffalon, M. (2017). Time for a change: a tutorial for comparing multiple classifiers through Bayesian analysis. *JMLR* 18(77):1–36. | — (JMLR) | Bayesian signed-rank and hierarchical tests. | E | jmlr.org/papers/v18/16-305.html |
| holm1979simple | Holm, S. (1979). A simple sequentially rejective multiple test procedure. *Scandinavian Journal of Statistics* 6(2):65–70. | **no DOI** (JSTOR stable 4615733) | Holm step-down multiple-testing correction. | E | Secondary only: bibbase record with JSTOR stable URL, vol. 6, pp. 65–70. Crossref has no record, `doi.org/10.2307/4615733` returns 404, and JSTOR returned a bot challenge. **Flag: verified via secondary index only.** |
| gneiting2007strictly | Gneiting, T., Raftery, A. E. (2007). Strictly proper scoring rules, prediction, and estimation. *JASA* 102(477):359–378. | 10.1198/016214506000001437 | Proper scoring rules, including the interval (Winkler) score for evaluating prediction intervals. | E | api.crossref.org/works/10.1198/016214506000001437 |

---

## 3. Coverage of the requested list

| Requested item | Status |
|---|---|
| Vovk, Gammerman & Shafer book (2005 and 2022) | Verified, both editions. |
| Vovk 2012 ACML and 2013 Machine Learning | Verified, both. |
| Papadopoulos et al. 2002 | Verified. |
| Lei et al. 2018 JASA | Verified. |
| Lei, Robins & Wasserman 2013 JASA | Verified. |
| Romano et al. 2019 CQR | Verified (NeurIPS page plus arXiv; no DOI). |
| Sesia & Candès 2020 Stat | Verified: 9(1):e261. |
| Chernozhukov et al. 2021 PNAS | Verified. |
| Izbicki et al. 2022 JMLR | Verified: 23(87). The 2020 AISTATS precursor was added. |
| Sesia & Romano 2021 NeurIPS | Verified. |
| Sadinle et al. JASA | Verified. Print year **2019** (online 2018). |
| Boström & Johansson 2020 COPA | Verified: PMLR 128:114–133. |
| Ding et al. 2023 NeurIPS | Verified: DOI 10.52202/075280-2817. |
| Gibbs et al. | Verified: **JRSSB 87(4):1100–1126 (2025)**, plus arXiv 2023. |
| Barber et al. 2021 Information and Inference | Verified: 10(2):455–482 (online 2020). |
| Barber et al. 2021 jackknife+ | Verified. |
| Tibshirani et al. 2019 NeurIPS | Verified. |
| Podkopaev & Ramdas 2021 UAI | Verified: PMLR 161:844–853. |
| Cauchois et al. 2021 JMLR | Verified: 22(81). |
| Angelopoulos & Bates FnT ML 2023 | Verified. |
| Guha et al. ICLR 2024 | Verified as arXiv:2404.08168. **The ICLR venue comes from the arXiv journal-ref; the OpenReview ICLR record could not be retrieved.** |
| Kandinsky CP | Verified: arXiv:2502.17264, and published at ICML 2025 (PMLR 267). |
| Torgo & Ribeiro 2007 and 2009 | Verified, both. |
| Ribeiro & Moniz 2020 | Verified. |
| Branco et al. ACM Computing Surveys | Verified. **Volume 49(2) is dated 2017; Crossref online date 2016.** |
| SMOGN 2017 | Verified: PMLR 74. |
| Yang et al. 2021 ICML | Verified: PMLR 139. |
| Wang & Wang 2023 NeurIPS | Verified: DOI 10.52202/075280-1326. |
| OpenML-CTR23 | Verified: AutoML 2023 **Workshop Track** (OpenReview); no DOI. |
| LightGBM | Verified (NeurIPS page; no DOI). |
| Demšar 2006 | Verified. |
| Benavoli et al. 2016 and 2017 | Verified, both. |
| Holm 1979 | **Secondary verification only; no DOI exists.** |
| Pasche, Lam & Engelke | **Now published:** *Extremes* 29(2):129–155 (2026). |
| Gao et al. arXiv:2409.17466 | **Now published:** *Machine Learning* 113:8347–8370 (2024). |
| LoBoost arXiv:2602.22432 | Verified. Accepted to TMLR (11/2026) per arXiv journal-ref. |
| Cabezas et al. 2025 Information Sciences | Verified: 686:121369. |
| Hore & Barber RLCP | Verified: JRSSB 87(2):549–578 (2025). |
| Guan 2023 Biometrika | Verified. |
| Xie, Barber & Candès boosted CP | Verified: NeurIPS 2024, DOI 10.52202/079017-2296. |

**References that could NOT be fully verified (do not cite without manual check):**
- *Holm (1979)*: real and canonical, but no DOI exists and only secondary indexes could be reached. Check the JSTOR page manually before submission.
- *Guha et al. (2024)*: the ICLR 2024 venue is taken from the arXiv journal-ref only. Check that the OpenReview or ICLR proceedings entry exists, or cite as arXiv.

No requested reference was found to be non-existent.

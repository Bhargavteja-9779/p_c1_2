[Corresponding author name]
[Affiliation, full postal address]
[E-mail address]

[Date]

The Editor-in-Chief
*Journal of King Saud University – Computer and Information Sciences*
Springer Nature

**Submission of an original research article**

Dear Editor-in-Chief,

We are pleased to submit the manuscript entitled **"Covering rare outcomes in imbalanced regression: stratified and relevance-weighted conformal prediction with density scores"** for consideration as an original research article in the *Journal of King Saud University – Computer and Information Sciences*.

**What the paper addresses.** Intelligent systems that predict prices, wages, loads or physical quantities are increasingly asked to report prediction intervals with a coverage guarantee. Conformal prediction provides such guarantees, but only on average over all outcomes. In imbalanced regression, the outcomes that matter most are rare, and standard (marginal or covariate-adaptive) conformal intervals systematically miss them: in our benchmark, they covered only 63.0%–78.3% of their worst-covered target stratum at a nominal 90%.

**Contributions.** We state each contribution with explicit reference to the closest prior work:

1. *The size-optimal score for stratum-wise coverage.* Calibrating within target strata is an established technique (Mondrian conformal prediction), recently applied to a skewed outcome as bin-conditional conformal prediction (Randahl et al. 2026) and used for fair regression (Wang et al. 2023); we credit it as such. We show which score makes stratum-valid sets smallest and implement it as stratified density-level conformal prediction (SDLC).
2. *Relevance-weighted coverage.* We study relevance-weighted coverage for continuous outcomes, a criterion for imbalanced regression analogous to macro-coverage for long-tailed classification and obtained by weighted conformal calibration with known weights, with a finite-sample guarantee, the size-optimal score and a method (RW-DLC) that shares SDLC's density model.

*Evidence.* 31 OpenML-CTR23 datasets with 10 predefined splits (exploratory size comparisons, because the implementation changed after results were seen) and 17 held-out datasets analysed under two pre-specified plans. Standard conformal methods covered only 63.0%–78.3% of their worst-covered stratum; SDLC's sets were smaller than those of bin-conditional conformal prediction, and RW-DLC covered 88.4% of the top 1% of held-out outcomes, against 76.0% for SDLC with five strata; a post hoc check shows that dedicated 1% tail strata achieve this coverage as well, so RW-DLC's value lies in its range-wide guarantee. We also report where gains are small (a few percent against a stratified normalised residual) and where a pre-specified hypothesis was not supported. A tail-alert study with expected-cost curves shows when prediction sets, conformal tail classifiers or conformal selection are preferable.

**Fit with the journal.** The paper addresses imbalanced learning and uncertainty quantification for intelligent systems, two topics of the journal's readership, and extends the journal's recent work on conformal classification (Zhang et al. 2025) and on quantile-regression ensembles for long-tailed prediction (Zhu et al. 2026) to prediction intervals for regression whose coverage is guaranteed for the rare outcomes that imbalanced-learning methods target. The evaluation is reproducible and multi-dataset, of a kind the journal's readers can reuse.

**Reproducibility.** All data are public (OpenML study 353 and suites 335/336). The complete code, configuration, raw per-run results, the pre-specified confirmatory analysis plan, and the scripts that generate every table, figure and number in the manuscript are provided as supplementary material and will be deposited in a public repository upon acceptance.

**Declarations.** This manuscript is original, has not been published previously, and is not under consideration for publication elsewhere. All authors have approved the manuscript and agree with its submission. The authors have no relevant financial or non-financial interests to disclose. The study uses only publicly available, de-identified benchmark data, so no ethical approval was required. As required by the journal, the use of a large language model is documented in the Methods section (Section "Use of a large language model"): it assisted with literature search, code development, experiment orchestration and drafting; it generated no data or results, and the authors reviewed all content and take full responsibility for it. The manuscript has been anonymised for double-blind review; author information is given on the separate title page.

Thank you for considering our manuscript. We look forward to hearing from you.

Yours sincerely,

[Corresponding author name], on behalf of all authors

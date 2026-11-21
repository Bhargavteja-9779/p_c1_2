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

**What the paper addresses.** Intelligent systems that predict prices, wages, loads or physical quantities are increasingly asked to report prediction intervals with a coverage guarantee. Conformal prediction provides such guarantees, but only on average over all outcomes. In imbalanced regression, the outcomes that matter most are rare, and standard (marginal or covariate-adaptive) conformal intervals systematically miss them: in our benchmark, they covered only {{marg.worst_stratum.min}}–{{marg.worst_stratum.max}} of their worst-covered target stratum at a nominal 90%.

**Contributions.** We state each contribution with explicit reference to the closest prior work:

1. *Two guarantees and their optimal sets.* Calibrating within target strata is an established Mondrian device, recently applied to a skewed outcome as bin-conditional conformal prediction (Randahl et al., 2026) and used for fair regression (Wang et al., 2023); we credit it as such. We show which score makes stratum-valid sets smallest, and we introduce relevance-weighted coverage for continuous outcomes, the regression counterpart of recent macro-coverage results for long-tailed classification, with a finite-sample guarantee and the size-optimal score.
2. *Two methods.* SDLC (stratified) and RW-DLC (relevance-weighted, no strata), sharing one semiparametric density model with linear-time prediction.
3. *Evidence under analysis plans fixed before evaluation.* {{n_datasets}} OpenML-CTR23 datasets with {{n_seeds}} predefined splits and {{conf.n_eval}} held-out datasets. Marginal methods covered only {{marg.worst_stratum.min}}–{{marg.worst_stratum.max}} of their worst stratum; SDLC's sets were smaller than those of bin-conditional conformal prediction, and RW-DLC covered {{J:rw_statistics.json|confirmatory/RW-3/rw|pct}} of the top 1% of held-out outcomes, against {{J:rw_statistics.json|confirmatory/RW-3/sdlc|pct}} for SDLC. We also report where gains are small (a few per cent against a stratified normalised residual) and where a pre-specified hypothesis was not supported.
4. *Decisions.* A tail-alert study with expected-cost curves shows when prediction sets, conformal tail classifiers or conformal selection are preferable.

**Fit with the journal.** The journal regularly publishes machine-learning methodology for imbalanced and long-tailed data (for example, SMOTE variants, imbalance-aware classifiers and a review of class overlap) and for uncertainty quantification, including conformal prediction for classification with deep forests and quantile-regression ensembles for long-tailed prediction. Our manuscript brings these two lines together for regression: it gives prediction intervals whose coverage is guaranteed for the rare outcomes that imbalanced-learning methods target, and it does so with a reproducible, multi-dataset evaluation of the kind the journal's readers can reuse. To our knowledge the journal has not yet published work on conformal prediction intervals for regression, so the paper adds a new but closely related topic.

**Reproducibility.** All data are public (OpenML study 353 and suites 335/336). The complete code, configuration, raw per-run results, the pre-specified confirmatory analysis plan, and the scripts that generate every table, figure and number in the manuscript are provided as supplementary material and will be deposited in a public repository upon acceptance.

**Declarations.** This manuscript is original, has not been published previously, and is not under consideration for publication elsewhere. All authors have approved the manuscript and agree with its submission. The authors declare no competing interests [to be confirmed by all authors]. The study uses only publicly available, de-identified benchmark data, so no ethical approval was required. As required by the journal, the use of a large language model is documented in the Methods section (Section "Use of a large language model"): it assisted with literature search, code development, experiment orchestration and drafting; it generated no data or results, and the authors reviewed all content and take full responsibility for it. The manuscript has been anonymised for double-blind review; author information is given on the separate title page.

[Optional: suggested reviewers with no conflict of interest, or reviewers to exclude, as permitted by the journal's submission system.]

Thank you for considering our manuscript. We look forward to hearing from you.

Yours sincerely,

[Corresponding author name], on behalf of all authors

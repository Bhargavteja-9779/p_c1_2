[Corresponding author name]
[Affiliation, full postal address]
[E-mail address]

[Date]

The Editor-in-Chief
*Expert Systems with Applications*
Elsevier

**Submission of an original research article**

Dear Editor-in-Chief,

We are pleased to submit the manuscript entitled **"Covering the rare outcomes: stratified conformal prediction with size-optimal density scores for imbalanced regression"** for consideration as a full-length research article in *Expert Systems with Applications*.

**What the paper addresses.** Intelligent systems that predict prices, wages, loads or physical quantities are increasingly asked to report prediction intervals with a coverage guarantee. Conformal prediction provides such guarantees, but only on average over all outcomes. In imbalanced regression, the outcomes that matter most are rare, and standard (marginal or covariate-adaptive) conformal intervals systematically miss them: in our benchmark, they covered only {{marg.worst_stratum.min}}–{{marg.worst_stratum.max}} of their worst-covered target stratum at a nominal 90%.

**Contributions.** We state each contribution with explicit reference to the closest prior work:

1. *Theory.* We quantify how far even the oracle interval with exact covariate-conditional coverage falls short in the tails, so that covariate adaptivity cannot replace calibration conditional on the target. Calibrating within target strata is an established Mondrian device, recently applied to a skewed outcome as bin-conditional conformal prediction (Randahl et al., 2026, *Political Analysis*) and used for fair regression (Wang et al., 2023, NeurIPS); we credit it as such. Our contribution concerns the score: conditional-density level sets with stratum-specific thresholds are the smallest stratum-valid sets (the per-stratum form of known level-set results), their plug-in conformal version is asymptotically optimal, and in a location–scale model the gain over a normalised residual comes from reallocating coverage across inputs.
2. *Method.* Stratified density-level conformal prediction (SDLC), with a semiparametric density estimated from cross-fitted residuals and an exact implementation whose cost is linear in the number of test points.
3. *Evidence.* A benchmark on {{n_datasets}} public datasets (OpenML-CTR23) with {{n_seeds}} predefined splits and {{n_methods_main}} conformal procedures sharing identical base models, with dataset-level non-parametric statistics, a null reference for worst-stratum coverage, and ablations that isolate each component of the score. Because the implementation was revised after earlier results had been seen, we label the size comparisons on this benchmark exploratory. We then replicated them on {{conf.n_eval}} held-out datasets under an analysis plan that was made public before evaluation, and all pre-registered hypotheses were supported.
4. *Decisions.* A tail-alert study with expected-cost curves shows when prediction sets, dedicated conformal tail classifiers or conformal selection are preferable. We report openly where simpler scores remain competitive: the gain over a stratified normalised residual is small and costs coverage of the noisiest inputs.

**Fit with the journal.** *Expert Systems with Applications* regularly publishes both conformal-prediction methods for applied intelligent systems and methods for imbalanced regression. Our work connects these two lines with a decision-oriented perspective: the paper evaluates stratified sets as tail alerts with guaranteed recall against dedicated alert rules under explicit cost models, which is directly relevant to the expert and decision-support systems that the journal's readers build.

**Reproducibility.** All data are public (OpenML study 353 and suites 335/336). The complete code, configuration, raw per-run results, the pre-registered confirmatory analysis plan, and the scripts that generate every table, figure and number in the manuscript are provided as supplementary material and will be deposited in a public repository upon acceptance.

**Declarations.** This manuscript is original, has not been published previously, and is not under consideration for publication elsewhere. All authors have approved the manuscript and agree with its submission. The authors declare no competing interests [to be confirmed by all authors]. The study uses only publicly available, de-identified benchmark data, so no ethical approval was required. In accordance with Elsevier's policy, the manuscript contains a declaration on the use of generative AI: an AI system was used to assist with literature search, code development, experiment orchestration, and drafting, and the authors reviewed and edited all content and take full responsibility for it.

[Optional: suggested reviewers with no conflict of interest, or reviewers to exclude, as permitted by the journal's submission system.]

Thank you for considering our manuscript. We look forward to hearing from you.

Yours sincerely,

[Corresponding author name], on behalf of all authors

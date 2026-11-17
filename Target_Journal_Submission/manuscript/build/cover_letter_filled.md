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

**What the paper addresses.** Intelligent systems that predict prices, wages, loads, or physical quantities are increasingly asked to report prediction intervals with a coverage guarantee. Conformal prediction provides such guarantees, but only on average over all outcomes. In imbalanced regression, the outcomes that matter most are rare, and standard (marginal or covariate-adaptive) conformal intervals systematically miss them. In our benchmark, marginal and covariate-adaptive methods covered only 69.0%–81.9% of upper-tail outcomes at a nominal 90%.

**Contributions.** We make four contributions, stated with explicit reference to closely related prior work:

1. We prove that even the oracle interval with exact covariate-conditional coverage under-covers extreme outcomes (in a Gaussian model it covers 70.5% of the top decile when the predictor explains half of the variance), so covariate adaptivity cannot replace calibration conditional on the target.
2. Calibrating thresholds within target strata is an established Mondrian device, recently applied to a skewed outcome as bin-conditional conformal prediction (Randahl et al., 2026, *Political Analysis*); we credit it as such. Our methodological contribution is the score: we prove that conditional-density level sets with stratum-specific thresholds are the smallest sets with stratum-wise coverage, which yields the SDLC procedure, together with a floor variant that guarantees marginal and stratum-wise coverage simultaneously and a precise characterisation of robustness to target shift.
3. A pre-registered benchmark on 31 public datasets (OpenML-CTR23) with 10 random splits each, 15 conformal procedures sharing identical base models, dataset-level non-parametric statistics, a null reference for worst-stratum coverage, and documented deviations from the pre-registered protocol.
4. Evidence that SDLC restores stratum-wise coverage at a quantified cost in set size and produces smaller stratum-valid sets than bin-conditional conformal prediction (geometric-mean ratio 0.93) and binned quantile-regression calibration (0.83), with the gains replicated using a neural base learner, together with an honest account of where simpler scores remain competitive.

**Fit with the journal.** *Expert Systems with Applications* regularly publishes both conformal-prediction methods for applied intelligent systems and methods for imbalanced regression. Our work connects these two lines with a decision-oriented perspective: the paper shows how stratified sets can serve as tail alerts with guaranteed recall for rare outcomes, which is directly relevant to the expert and decision-support systems that the journal's readers build.

**Reproducibility.** All data are public (OpenML study 353). The complete code, configuration, raw per-run results, and the scripts that generate every table, figure, and number in the manuscript are provided as supplementary material and will be deposited in a public repository upon acceptance.

**Declarations.** This manuscript is original, has not been published previously, and is not under consideration for publication elsewhere. All authors have approved the manuscript and agree with its submission. The authors declare no competing interests [to be confirmed by all authors]. The study uses only publicly available, de-identified benchmark data, so no ethical approval was required. In accordance with Elsevier's policy, the manuscript contains a declaration on the use of generative AI: an AI system was used to assist with literature search, code development, experiment orchestration, and drafting, and the authors reviewed and edited all content and take full responsibility for it.

[Optional: suggested reviewers with no conflict of interest, or reviewers to exclude, as permitted by the journal's submission system.]

Thank you for considering our manuscript. We look forward to hearing from you.

Yours sincerely,

[Corresponding author name], on behalf of all authors

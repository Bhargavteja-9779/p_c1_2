# Review 02: Reviewer #2 (novelty, prior art and positioning)

**Manuscript:** "Covering the rare outcomes: stratified conformal prediction with size-optimal density scores for imbalanced regression"
**Journal:** Journal of King Saud University – Computer and Information Sciences (Springer Nature)
**Reviewed version:** `manuscript/build/manuscript_filled.md` (rendered, all numbers filled), with `cover_letter_filled.md`, `highlights_filled.md` and `supplementary/references_verified.bib`
**Scope of this review:** novelty, prior art, how the contribution is set apart from earlier work, whether the research gap is real, how the paper presents itself to a desk editor, and whether Table 1 is fair. Issues already raised in `REVIEW/review_01.md` (C1-01 to C1-46) are not repeated. Where an issue here touches one of them, the overlap is named and only the new point is argued.
**Literature check:** I verified every external paper cited below on its arXiv abstract page or in its HTML full text on 2026-11-20. Where I could read only the abstract, I say so.

---

## 1. Summary

The paper studies *stratum-wise* coverage, $P\{Y\in C(X)\mid Y\in B_k\}$, for prediction sets in regression. Its main findings are:

- an analytic calculation in a Gaussian model, extended by Monte Carlo, showing that even the oracle set with exact $X$-conditional coverage under-covers tail strata of $Y$ (Prop. 1, Table 2);
- calibration within outcome strata, which the paper credits to Mondrian conformal prediction, BCCP (Randahl et al.) and BFQR (Wang et al.) (Theorem 1);
- a per-stratum Neyman–Pearson characterisation of the smallest stratum-valid sets as conditional-density level sets with stratum-specific thresholds (Prop. 2);
- a plug-in consistency result (Prop. 3);
- a remark that, in a location–scale model, the density score gains over the normalised residual by moving coverage from noisy to quiet inputs;
- a corollary on label shift (Cor. 1);
- a method, SDLC: Mondrian calibration of a location–scale KDE density score;
- a 31-dataset benchmark (CTR23) and a pre-registered 17-dataset replication.

The writing is careful, and the paper now credits Mondrian, BCCP and BFQR openly. That openness, however, shows how little is left. Every theoretical statement is either:

- a direct specialisation of a known result (Neyman–Pearson / Sadinle et al. 2019 / Lei et al. 2013; Podkopaev & Ramdas 2021; Barber et al. 2023); or
- an illustrative calculation of a phenomenon that is already documented.

The method plugs a known score into a known calibration. Against the comparator that uses the same information (S-NCP), the empirical gain is about 2–3% in geometric-mean size, and the 95% CI includes 1 on both the exploratory and the confirmatory data. That gain is paid for with lower coverage of the noisiest inputs and of the top 1%.

The paper also misses a closely related 2025–2026 body of work on optimal conformal sets under label-conditional and label-group coverage for long-tailed (imbalanced) classification:

- Ding, Fermanian & Salmon, ICLR 2026;
- Bhattacharyya, Ding & Barber, 2026.

Those papers contain the discrete-label version of Prop. 2, including grouped-label constraints. They also study the same "price of class-conditional validity" trade-off that RQ2 studies.

Table 1 favours the proposed method. It lists as contributions of SDLC properties that belong to the calibration step the paper concedes to BCCP, and it leaves out the most relevant competitors (Kandinsky CP, Podkopaev & Ramdas, the long-tail CP literature).

## 2. Recommendation (as a JKSU-CIS reviewer)

**Reject in the present form (novelty insufficient for this journal), with encouragement to resubmit as a re-framed paper.**

At a journal where editors desk-reject rather than ask for major revision, a desk editor who reads the title, abstract and highlights will see four things:

- the calibration is explicitly "not new";
- the optimality result is "the per-stratum form of known level-set results";
- the asymptotic result follows "the plug-in arguments of" earlier work;
- the gain over the simplest strong baseline is "small".

A one-minute read therefore yields "incremental". There are two credible routes to publication:

- **(a)** Re-frame the paper honestly as an evidence and practice paper on outcome-stratified conformal regression for rare outcomes, centred on the benchmark, the price of stratification, the decision study and practitioner guidance, with the theory compressed into a short section.
- **(b)** Add one genuinely new methodological result that addresses a problem specific to imbalanced regression (see Issue 5).

In either case Table 1, the title, the abstract and the highlights must be rewritten (Issues 3 and 4).

---

## 3. Issues

### FATAL

#### R2-01 (FATAL). Once known results are taken out, the paper's own contribution is a combination of known pieces plus a benchmark. The paper does not say so, and the size gain that would justify a "method" paper is within noise against the information-matched baseline.

**Location:** Abstract; Section 1, contributions 1–2; Section 2.2 last paragraph; "Positioning of this work"; Sections 4.1–4.3; cover letter "Contributions"; highlights 2–4.

**Evidence.** Each claimed element has a precursor, most of which the manuscript itself names:

| Claimed element | Status | Precursor |
|---|---|---|
| Stratum-wise coverage via calibration within outcome bins (Theorem 1) | Conceded as known (Section 2.2, 4.1) | Vovk et al. 2005; Vovk 2013; Randahl et al. (PAN 2026); Wang et al. (NeurIPS 2023, Thm 4.1) |
| Oracle covariate-conditional sets under-cover tails (Prop. 1) | Gaussian calculation of a phenomenon the paper itself says was "reported empirically". The general fact behind it ($\sum_k p_k\mathrm{Cov}_k=1-\alpha$) is elementary (Section 3.1) | Wang et al. 2023; Randahl et al. 2026 |
| Size-optimal stratum-valid sets are density level sets with per-stratum thresholds (Prop. 2) | "Per-stratum form of known level-set results". The problem separates by stratum, so the proof is $K$ copies of Neyman–Pearson | Sadinle, Lei & Wasserman (JASA 2019), class-specific coverage; Lei, Robins & Wasserman (JASA 2013); Kiyani et al. (NeurIPS 2024); **and, missed:** Ding, Fermanian & Salmon (ICLR 2026, arXiv:2507.06867) and Bhattacharyya, Ding & Barber (arXiv:2606.28598, 2026), see R2-02 |
| Plug-in asymptotic optimality (Prop. 3) | "Follows the plug-in arguments of Lei et al. and Izbicki et al." | Lei et al. 2013; Izbicki et al. 2022; Sadinle et al. 2019 also study the plug-in/conformal estimator of class-specific-coverage sets (their Sec. 4, on my reading) |
| The gain comes from reallocating coverage across $x$ | This is the reason, known since Izbicki et al. (2020, 2022), why the single-threshold density level set of Lei et al. lacks conditional coverage. HPD-split and CD-split were introduced to fix it. Kiyani et al. (2024) make the same point: $x$-dependent levels are needed for conditional constraints | Izbicki, Shimizu & Stern 2020, 2022; Kiyani et al. 2024 |
| Label-shift robustness (Cor. 1) | "Collects known facts" (Section 4.1) | Podkopaev & Ramdas (UAI 2021); Barber et al. (AoS 2023); Angelopoulos, Barber & Bates (2024) |
| SDLC = Mondrian calibration + location–scale KDE density score | A plug-in combination. The paper itself states that the stratified guarantee "holds for any score" | Location–scale density with KDE noise is a standard semiparametric estimator; HPD/density scores are standard (HPD-split, CHCDS: Sampson & Chan, arXiv:2406.18052) |

The empirical case for the method is weak where it matters:

- **SDLC vs S-NCP, exploratory:** geometric-mean ratio 0.975 [0.941, 1.020].
- **SDLC vs S-NCP, confirmatory:** 0.977 [0.940, 1.028].
- **SDLC vs S-HPD, confirmatory:** 0.984 [0.963, 1.014].
- **Costs of the gain:** lower top-1% coverage (0.736 vs 0.789 for S-NCP), lower worst-$\hat\sigma$-decile coverage, and 5× more empty sets.

The advantage over BCCP (ratio about 0.90) mostly reflects adding a scale model $\hat\sigma(x)$ to an unscaled residual, which is not an advance in 2026. The decomposition (Table 6) confirms this. The noise-shape estimate that is distinctive of SDLC adds 0.7% (0.993, $p=0.068$).

C1-02 and C1-13 raised the S-NCP gap and the novelty of Theorem 2 separately for an earlier version. The new point is cumulative: after the revisions every element is now credited to prior work, and nothing in the remaining contribution is new.

**Fix.** Choose one of:

- **(a) Re-frame as a benchmark and practice paper.** Possible title: "Conformal prediction intervals that cover rare outcomes: how much does outcome-stratified calibration cost, and which score should be used? A 48-dataset study".
  - State plainly in the abstract that the calibration and the optimality principle are known.
  - Make the contributions:
    - (i) the first large, pre-registered quantification of tail under-coverage and of the price of stratification;
    - (ii) a comparison of scores under stratified calibration;
    - (iii) the decision study;
    - (iv) guidance.
  - Compress Section 4.2 to one proposition, labelled as a corollary of Sadinle et al. and Ding et al., plus a remark.
  - Drop "method" language for SDLC, or present it as "the density score in the stratified family".
- **(b) Keep the method framing only if a genuinely new result is added.** See R2-05 for candidates that address problems specific to imbalanced regression.

### MAJOR

#### R2-02 (MAJOR). Missed prior art: optimal conformal sets under label-conditional and label-group coverage for long-tailed classification. This is the direct discrete counterpart of Prop. 2, of RQ2 and of the floor variant.

**Location:** Section 2.2 ("Closest to our optimality result is ... Sadinle"); Section 4.2 before Prop. 2; Section 4.6 floor variant; Section 6.2 / RQ2; Table 1.

**Evidence (verified).**

1. **Ding, T., Fermanian, J.-B., Salmon, J. (2026). "Conformal Prediction for Long-Tailed Classification." ICLR 2026.** arXiv:2507.06867 (v3, 26 Feb 2026; ICLR 2026 listing at mlanthology.org/iclr/2026/ding2026iclr-conformal).
   - Section 2.1 restates that minimising expected set size under class-conditional coverage is solved by thresholding $p(y\mid x)$ (Neyman–Pearson / Sadinle).
   - Props. 1, 2 and 6 characterise the size-optimal sets for (weighted) macro-coverage as thresholds on $\omega(y)p(y\mid x)/p(y)$.
   - "Interp-Q" linearly interpolates marginal and class-wise thresholds, with a marginal guarantee of $1-2\alpha$.
   - The paper's motivation is exactly RQ2: class-conditional validity for rare labels is expensive, and the authors propose principled ways to trade it off.
2. **Bhattacharyya, A., Ding, T., Barber, R. F. (2026). "Conformal Prediction with Macro-Coverage Guarantees."** arXiv:2606.28598 (26 Jun 2026).
   - Groups are functions of the *label*, $g:\mathcal Y\to\mathcal K$ (a stratification of the label space).
   - The paper proves a finite-sample macro-coverage guarantee for label-weighted CP.
   - It characterises the smallest sets under one or several group-coverage constraints. Prop. 5 gives the multi-constraint optimum $\{y: [p(y\mid x)/p(y)]\sum_j\lambda_j\tilde w_j(y)\ge t\}$ by Lagrangian duality.
   - With one constraint per label group, this is the discrete-label version of Prop. 2 with strata = label groups.
3. **Chzhen, E., Denis, C., Hebiri, M., Lorieul, T. (2021). "Set-valued classification – overview via a unified framework."** arXiv:2102.12318. This gives a unified treatment of the optimal set-valued rules under coverage constraints, including class-specific ones.
4. **Guha et al. (ICLR 2024, arXiv:2404.08168)** is cited, but not in this role. Once $Y$ is discretised into bins treated as classes ("regression-as-classification"), Sadinle et al.'s class-specific-coverage result applies directly. The "regression analogue" in Prop. 2 is then a change from counting measure to Lebesgue measure. That change is not a conceptual advance.
5. **Liu, S., Huang, J., Ong, L. (2025). "Conformal Prediction Meets Long-tail Classification" (TACP).** arXiv:2508.11345 (listed as AAAI 2026 on ojs.aaai.org). It addresses the head–tail coverage gap that RQ1 documents for regression.

**What these undercut:**

- the claim in Section 2.2 and Table 1 that the closest optimality result is Sadinle (2019);
- the implicit claim that the "price of stratum-wise validity" (RQ2) is a new question;
- the description of the floor variant (Section 4.6) as having only BFQR and Kiyani et al. as principled alternatives. Interp-Q and macro-coverage targets are direct, published alternatives.

The paper also positions itself inside imbalanced learning (keywords, cover letter: "the journal regularly publishes ... imbalanced and long-tailed data"). It cannot ignore the long-tailed conformal classification literature it most closely mirrors.

**Fix.**

- Cite 1, 2 and 5, and re-cite 3 and 4 in this role. Add a paragraph to Section 2.2 ("Long-tailed and label-group conformal classification").
- Re-state Prop. 2 as "the continuous-label, Lebesgue-measure counterpart of the class-specific results of Sadinle et al. (2019) and the label-group results of Ding et al. (2026) and Bhattacharyya et al. (2026)".
- Add a macro-coverage-over-strata or Interp-Q-style comparator next to SDLC-floor in Section 6.8. At least discuss it as the principled alternative to the max rule.
- Add the long-tailed CP row to Table 1.

#### R2-03 (MAJOR). Table 1 is not fair to prior work. It credits SDLC with properties of the calibration step it concedes to BCCP, it puts unlike methods in one row, and it leaves out the most relevant comparators.

**Location:** Table 1 and its caption; "Positioning of this work".

**Evidence.**

1. **The label-shift column credits the calibration step to SDLC.** It reads "exact under stratum re-weighting, quantified otherwise (Cor. 1)" for SDLC and "not analysed" for BCCP. Cor. 1 is a property of the Mondrian calibration step, which is *identical* in BCCP and SDLC (Section 4.1: "it collects known facts"). The same holds for BFQR, whose row reads "not addressed". The caption then says the contribution "lies in the last three columns", which presents an inherited property as new.
2. **The Sadinle row says "Label shift: not addressed".** Class-specific (label-conditional) sets are the textbook label-shift-robust construction (Podkopaev & Ramdas, UAI 2021, which the paper cites in Section 2.4 but not in the table). The row implies a limitation that does not exist.
3. **The Gibbs et al. (2025) and Kiyani et al. (2024) row is a merger of unlike methods.**
   - It credits "length-optimal over the class" to the merged row, but Gibbs et al. make no length-optimality claim.
   - It puts "covariate shift" in a column headed "Label (target) shift". That is a category error. Either the column means "shift robustness", or Kiyani/Gibbs should read "not addressed".
4. **Missing rows:**
   - Kandinsky CP (Bairaktari et al., ICML 2025). It is discussed in the text as covering label-defined groups in regression, and it is the most general existing framework for this guarantee.
   - Lei et al. (2013) and Lei & Wasserman (2014). These are the conformal density level sets with asymptotic optimality, the direct ancestor of the "Score" and "Size optimality" columns.
   - Long-tailed / macro-coverage CP (R2-02).
   - Podkopaev & Ramdas (2021), the label-shift column's origin.
5. **The SDLC "Size optimality" cell overstates.** It reads "exact for the oracle (Prop. 2); asymptotic for the plug-in (Prop. 3)". It omits that Prop. 3 requires uniform consistency of $\hat f$, which the SDLC estimator has only under a correctly specified location–scale model with $x$-independent noise shape (Section 7.3). It also omits that this property is the same for any stratified density plug-in (S-HPD's oracle is not optimal, but a "stratified HPD-split with a different level" would be). The CD-split/HPD-split row reads "asymptotic (marginal / X-conditional)", which applies the same kind of qualification to prior work that is missing from SDLC's row.

**Fix.**

- Re-build Table 1 with these columns: "conditioning event", "finite-sample guarantee", "score", "optimality result (oracle / plug-in, with assumption)", "label-shift property (source)".
- Fill the label-shift cell identically for every label-conditional method (Sadinle, BFQR, BCCP, SDLC), citing Podkopaev & Ramdas and Cor. 1(i) as a restatement.
- Split the Gibbs and Kiyani row.
- Add rows for Kandinsky CP, Lei et al. 2013, and Ding et al. / Bhattacharyya et al.
- Change the caption to: "The calibration step and its validity and label-shift properties are shared with BCCP; the contribution of this paper is the analysis of the score (Prop. 2–3, a continuous-label counterpart of Sadinle et al. 2019 and Ding et al. 2026) and the empirical study."

#### R2-04 (MAJOR). The title, abstract and highlights fail the one-minute desk test. They lead with prior art, overclaim optimality, and leave the differentiating contribution unclear.

**Location:** Title; abstract; highlights; Section 1, contributions list.

**Evidence.**

- **The title promises "size-optimal density scores".** The method is size-optimal only for the oracle, and its plug-in is asymptotically optimal only under a uniformly consistent density estimate, which SDLC's location–scale estimator is not in general (Section 7.3, and the bimodal design C: estimated SDLC 53.2% larger than the oracle). "Size-optimal" in a title is a claim about the method, and it is false for the method as implemented.
- **Highlights mostly restate known or oracle-only results:**
  - Highlight 1 ("Even oracle covariate-conditional intervals under-cover") is the Gaussian illustration.
  - Highlight 2 ("Calibrating within target strata guarantees coverage of rare, extreme outcomes") is BCCP/Mondrian, which the paper itself concedes.
  - Highlight 3 ("Stratum-wise density level sets are the smallest stratum-valid prediction sets") is oracle-only and is the Sadinle/Neyman–Pearson result.

  Only highlight 4 is the paper's own empirical result. A desk editor reading the highlights will see two known results and one oracle statement presented as contributions.
- **The abstract (250 words, at the journal limit) is hard to parse quickly:**
  - It spends its first 100 words on the problem and the known calibration.
  - It says "compared with 13 procedures" but does not say that 6 of them are the authors' own stratified variants and ablations.
  - It ends with hedges ("Gains ... were small and came with lower coverage of the noisiest inputs").

  The honesty is commendable. But the abstract never says in one sentence *what is new relative to BCCP*. The answer would be: "the choice of score, its optimality principle, its cost, and a pre-registered multi-dataset evaluation".
- **Contribution 1 ("Theory of stratum-wise coverage") bundles five items:**
  - a Gaussian calculation;
  - an oracle optimality result described in the same sentence as known;
  - a consistency result;
  - a location–scale remark;
  - a corollary of "known" facts.

  Bundling them makes the theory look like a block of new results. Section 2.2 and Section 4 then undo that impression.

**Fix.**

- **Title.** Remove "size-optimal". Possible alternatives:
  - "Conformal intervals that cover rare outcomes: the price and the best score for outcome-stratified calibration in imbalanced regression";
  - "Outcome-stratified conformal regression for rare outcomes: which score, at what price? A pre-registered multi-dataset study".
- **Abstract.** Use this order:
  - (1) problem, one sentence;
  - (2) what is known: "Calibrating within outcome strata (Mondrian/BCCP) guarantees stratum-wise coverage for any score";
  - (3) the question: "which score, and at what cost?";
  - (4) the answers, with numbers, stating the 2–3% vs S-NCP;
  - (5) the replication;
  - (6) the practical message.
- **Highlights.** Replace highlights 2 and 3 with the paper's own findings. For example:
  - "Stratum-valid sets cost 1.17–1.27× marginal sets but beat lowering α";
  - "Density score beats residual score by ~10%, normalised residual by ~2%".
- **Contributions list.** Re-state contribution 1 as "Analysis" with sub-bullets, each tagged *new* or *restated*.

#### R2-05 (MAJOR). The stated research gap is narrow and largely closed by theory already. The gaps that are real and specific to imbalanced regression are left open.

**Location:** Section 1 paragraph 4 ("the open questions concern the score"); Section 2.2 last paragraph; Section 7.3.

**Evidence.** Section 1 says "BCCP leaves open which score yields the smallest bin-valid sets". Under the paper's own formulation (per-stratum coverage constraints, Lebesgue size) this question is answered as soon as it is posed: the constraints separate, and Neyman–Pearson gives the density level set. The paper's own Proposition 2 proof is half a page. The empirical question ("how much does it help in practice?") has the answer "a few per cent over a normalised residual, with costs".

The problems that make outcome-stratified conformal regression hard *in imbalanced regression* are visible in the paper's own results but are not addressed:

1. **Sparse tail strata.** With $n_k<1/\alpha_k-1$ the threshold is $+\infty$ and the whole stratum is returned. With a quarter of the calibration set this happened in 87 runs, and sizes grew from 0.874 to 1.243 (Section 6.8). This is the defining difficulty of rare targets, and it is deferred to "natural remedies that we did not evaluate" (Section 7.3).
2. **Choosing strata (number and cut points) to optimise size subject to validity.** Strata are fixed at training quantiles 0.10/0.25/0.75/0.90 without justification. No data-driven or relevance-function-driven rule is proposed.
3. **Coverage beyond the calibrated strata.** The top 1% is covered at 0.736 for SDLC, against a nominal 0.9 (Table 3). This is exactly the "rare outcomes" the title promises to cover.
4. **The joint marginal + per-stratum constraint problem.** Review 01 suggested this (C1-13(b)) and it was not done. It does not separate, so it would give a genuinely new optimal set with coupled thresholds and a principled replacement for the floor rule. The multi-constraint Lagrangian of Bhattacharyya et al. (2026, Prop. 5) shows how it is done in the discrete case.

**Fix.** Either:

- add a result on one of points 1–4, for example:
  - a finite-sample size bound as a function of $n_k$ with a data-driven stratum-merging rule chosen on training data;
  - the optimal set under {marginal ≥ 1−α, each stratum ≥ 1−β} with a conformal implementation and guarantee;
  - an extrapolation device (e.g. EVT-based, cf. Pasche 2026) for the uncalibrated extreme; or
- state explicitly in Section 1 that the score question is answered in principle by Neyman–Pearson, and that the paper's contribution is to quantify the answer empirically (route (a) of R2-01).

#### R2-06 (MAJOR). Fit with JKSU-CIS: the paper is a long statistics-methodology paper with a thin computer-science contribution and no application study, and it is far over typical length for the journal.

**Location:** Whole manuscript; cover letter "Fit with the journal".

**Evidence.**

- **Length and density.** The rendered manuscript is about 17,600 words including tables. It contains 10 main-text tables, 8 figures, one theorem, three propositions, one corollary and a proofs appendix.
- **Thin computer-science content.** The cover letter argues fit through SMOTE and class-overlap papers and one conformal-classification paper. The present manuscript, however, contains no system, no application-driven case study (Fig. 7's three valuation datasets are benchmark rows, not a case study), and no algorithmic contribution beyond a grid evaluation of a density.
- **Self-assessed risk.** The project's own journal-selection note (`journal_selection/selected_journal.md`, "Key rejection risks") lists "desk rejection as too statistical/theoretical" and "novelty challenge" as the top two risks.

C1-22 raised the absence of an application case study for ESWA. The present point is different: readership fit and length for JKSU-CIS, combined with R2-01.

**Fix.**

- Cut to about 9,000–10,000 words. Move to the supplement:
  - Section 6.4 (synthetic);
  - most of Section 6.6 (shift);
  - Section 6.8 (sensitivity), keeping one paragraph;
  - the grouped-split study;
  - Appendix A proofs of Thm 1 and Cor 1, which are known.
- Lead with an applied scenario, e.g. a valuation or grid-load use case with a stated cost of missing an extreme, and carry it through the paper.

### MODERATE

#### R2-07 (MODERATE). Label-shift literature for continuous outcomes is incomplete, and Cor. 1 is presented as an SDLC contribution although it is a property of all label-conditional calibration.

**Location:** Section 2.4; Cor. 1 and the paragraph after it; Section 1 contribution 1 (last sentence); Table 1.

**Evidence.** C1-15 covered crediting Podkopaev & Ramdas and Barber et al. The new points are:

- **(i) Attribution in Table 1 and contribution 1.** Cor. 1(i) holds verbatim for BCCP, BFQR and every stratified baseline in the paper. Table 9 shows the positive-control result is identical across all stratified methods. It is therefore not a property of SDLC and should not appear in SDLC's row or contribution list.
- **(ii) Missing directly relevant work on continuous label shift in regression** (verified on arXiv):
  - **Choi, S. (2026). "Conformal Bayes under Continuous Label Shift: Sensitivity Analysis and the Limits of Exact Validity."** arXiv:2609.27976 (v2, 1 Nov 2026). It studies exactly when validity can be exact under continuous label shift with exponential tilts, the same tilt family as Experiment 4. It shows that linear exponential tilts make exact candidate-weighted sets unbounded. This is directly relevant to the paper's statement that its tilts have "unbounded density ratios" and to the claimed contribution "when the guarantee survives label shift".
  - **Lee, H., Kim, J., Jadamba, E., Choi, S., Shin, H. (2026). "Conformal Prediction for Molecular Properties under Label Shift."** arXiv:2608.17678.
  - **Choi, S. (2026). "Conformal Bayes under Label Shift: Post-Hoc Calibration vs. In-Training Adaptation."** arXiv:2606.11865 (EIML@ICML 2026).

  The paper cites the sibling paper by the same group (lee2026split, arXiv:2609.12386) but not these.
- **(iii) Overstated novelty.** Section 4.1 calls "exactness requires that the joint law of (X,Y) inside each stratum be unchanged" "the point specific to a continuous outcome". This is an immediate consequence of Mondrian validity, which conditions on the category and is exchangeable within it. It is a remark, not a result.

**Fix.**

- Remove label-shift robustness from SDLC's claimed contributions and from SDLC's Table 1 row; attribute it to stratified calibration.
- Cite Choi (2026, arXiv:2609.27976) in Section 2.4 and in the discussion of the tilt experiment, and the other two in Section 2.4.
- Demote Cor. 1 to a Remark.

#### R2-08 (MODERATE). The "imbalanced regression" framing is not matched by the imbalanced-regression notion of rarity or by its benchmarks.

**Location:** Title; Section 1 paragraph 1; Section 2.3; Section 4.4 "Strata"; Section 5.1.

**Evidence.**

- **The field's own definition of rarity is not used.** In the imbalanced-regression literature the paper cites (Torgo & Ribeiro 2007; Ribeiro & Moniz 2020; Branco et al. 2016), rare targets are defined by a *relevance function* $\phi(y)$, typically derived from the boxplot or adjusted boxplot of $Y$. Here they are defined by fixed training quantiles (10%/90%), which make every dataset "10% rare" in each tail whatever its distribution. Mild-skew datasets therefore get the same "rare" tails as heavy-tailed ones.
- **Standard imbalanced-regression benchmarks are not used.** Examples are the DIR suites of Yang et al. (ICML 2021): AgeDB-DIR, IMDB-WIKI-DIR, STS-B-DIR, NYUD2-DIR. The tabular data in Branco/Ribeiro's imbalanced-regression collections are not used either.
- **Evaluation metrics.** Nothing is evaluated with SERA or relevance-weighted coverage, which the paper itself introduces in Section 2.3 as the evaluation standard of the field.

Without this link, "imbalanced regression" in the title is positioning rather than substance. A JKSU-CIS reviewer from the imbalanced-learning community will notice. C1-11 and C1-23 concern skewness subsets and imbalance-aware learners. This point concerns the definition of the target event and the benchmarks.

**Fix.**

- Add a relevance-function-based stratification as a variant: strata $\{\phi(y)\ge\tau\}$ on each side, with cut points from the adjusted boxplot.
- Report relevance-weighted coverage.
- Either run on the tabular imbalanced-regression datasets used by Branco et al. or Avelino et al. 2024 (which the paper cites), or tone the title down to "skewed and heavy-tailed regression targets".

#### R2-09 (MODERATE). Neighbouring 2026 "tail" conformal papers are not distinguished. Editors and reviewers will find them with the obvious keyword search.

**Location:** Section 2.3 (paragraph on extreme conformal prediction); Section 1.

**Evidence (verified abstracts).**

- **Cuonzo, S., Deliu, N. (2026). "Conformal Prediction Intervals with Tail-Specific Guarantees."** arXiv:2606.18199. It constructs one-sided intervals with separately calibrated upper- and lower-tail guarantees. These are marginal, not conditional on $Y$.
- **Wang, T. (2026). "Geometry of tail allocation in conformal prediction intervals."** arXiv:2604.25202. It studies the optimal split of the miscoverage budget between the two tails, with regularly varying tails.
- **Sampson, M., Chan, K.-S. "Flexible Conformal Highest Predictive Conditional Density Sets" (CHCDS).** arXiv:2406.18052 (v3, 2025). It conformalises estimated conditional HDRs, i.e. the density-score family that SDLC belongs to.
- **Le Bars, B., Humbert, P. (2025). "On Volume Minimization in Conformal Regression."** arXiv:2502.09985. It studies length-optimal split conformal regression and bounds the excess length over the oracle interval.

None of these does what the paper does. But "tail-specific guarantees" and "volume minimisation" are exactly the phrases a desk editor would search, and the paper must say in one sentence why they differ. The tail papers guarantee the *direction* of misses, not coverage given $Y$ in a tail. The volume papers address marginal coverage.

**Fix.** Add two sentences to Section 2.1 and 2.3 citing and distinguishing these works. Add CHCDS to the density-based row of Table 1.

#### R2-10 (MODERATE). Some prior work is cited for claims it does not make.

**Location:** Section 2.2 ("@randahl2026bin note that it holds for any score"); Section 4.1 ("@randahl2026bin ... note that the bin-wise guarantee holds for any score"); Section 3.2 ("Tail under-coverage ... reported empirically [@wang2023equal; @randahl2026bin; @boruah2026distribution]").

**Evidence.**

- **Randahl et al.** In the arXiv version of BCCP (arXiv:2410.14507v2), the bin-wise guarantee is stated "assuming exchangeability of the data within each bin". The paper uses the absolute error as the score, and I could not find a statement that the guarantee holds for any score. Nor could I find any discussion of score choice for efficiency or of distribution/label shift. If the published PAN version (10.1017/pan.2025.10010) adds such a statement, quote it with a page number. Otherwise the attribution is unsupported. This matters for positioning: the paper uses that attribution to argue that "BCCP leaves open which score" while crediting BCCP with the any-score insight.
- **Boruah (arXiv:2608.07589).** The bins are predicted-strength quartiles, which are functions of $X$, as the paper itself says correctly in Section 2.2. Citing it in Section 3.2 as evidence of *outcome-tail* under-coverage is inaccurate.

**Fix.**

- Verify the PAN text and quote it, or rephrase as "the bin-wise argument does not depend on the score (Vovk et al. 2005)".
- Remove Boruah from the outcome-tail sentence in Section 3.2, or qualify it ("in the top quartile of predicted values").

#### R2-11 (MODERATE). The "asymptotically optimal" claim is stated without its condition in the abstract and conclusion, and it is not differentiated from Sadinle et al.'s plug-in analysis.

**Location:** Abstract ("their plug-in conformal version is asymptotically optimal"); Section 8 paragraph 2; Prop. 3.

**Evidence.**

- Prop. 3 assumes $\sup_{x,y}|\hat f-f|\to0$ in probability. The authors themselves state that this holds for SDLC's estimator only under a location–scale model with $x$-independent noise shape (Sections 4.3 and 7.3), and the synthetic design C shows a 53% gap. The abstract and conclusion state the result unconditionally.
- Prop. 3 gives consistency without a rate. Lei et al. (2013) and Sadinle et al. (2019) give rates for their plug-in procedures. A consistency-only plug-in result for a separable problem adds little.

**Fix.**

- Abstract and conclusion: "... asymptotically optimal when the density estimate is uniformly consistent".
- Either add a rate (e.g. excess size $O_P(\varepsilon_N+n_{\min}^{-1/2})$ under a margin condition on $f(Y\mid X)$ near $t_k$, as in Lei et al. 2013 / Sadinle et al. 2019), or label Prop. 3 a "consistency check".

### MINOR

#### R2-12 (MINOR). Duplicated BFQR description in Section 2.2.

**Location:** Section 2.2, paragraph "We are aware of two regression methods ...".

**Evidence.** "their binned fair quantile regression (BFQR) splits $Y$ into equal-mass bins ..." is followed two sentences later by "Their binned fair quantile regression (BFQR) forms equal-mass bins ...". This looks like a merge artefact.

**Fix.** Keep one description (the second, more precise one).

#### R2-13 (MINOR). "Compared with 13 procedures" inflates the comparison.

**Location:** Abstract; Section 1 contribution 3.

**Evidence.** Of the 13 procedures, SDLC-N, S-NCP, S-CQR, S-HPD and the hull variants are the authors' own stratified constructions or ablations. Only SCP, NCP, CQR, Mondrian-ŷ, DCP, HPD-split and BCCP are published methods (DLS is a single-threshold variant of Lei et al.). No published stratified method other than BCCP is run: neither BFQR (C1-16) nor Kandinsky (C1-17).

**Fix.** Write "against 7 published conformal methods, BCCP, and 5 stratified variants and ablations".

#### R2-14 (MINOR). "We are aware of two regression methods that calibrate within bins of the outcome itself" should be qualified by date and scope.

**Location:** Section 2.2.

**Evidence.** Kandinsky CP covers label-defined groups in regression; the same section discusses it a paragraph earlier. Bhattacharyya et al. (2026) cover label-group calibration in classification. Regression-as-classification (Guha et al. 2024) combined with class-conditional CP gives outcome-bin calibration directly.

**Fix.** Write "Besides general frameworks that include label-defined groups (Kandinsky CP) and class-conditional CP applied to a discretised outcome, two regression methods ...".

#### R2-15 (MINOR). Table 2 placement and labelling.

**Location:** Section 3.2, Table 2.

**Evidence.** The non-Gaussian rows are Monte Carlo illustrations, but they sit in a "Preliminaries" section next to a proposition. A reader may take Table 2 as theory.

**Fix.** Label the non-Gaussian rows "illustration (Monte Carlo)". Consider moving them to the supplement, which also serves R2-06.

---

## 4. Verified references the authors should consider (not in `references_verified.bib`)

| # | Reference | Identifier (verified) | Bears on |
|---|---|---|---|
| 1 | Ding, T., Fermanian, J.-B., Salmon, J. Conformal Prediction for Long-Tailed Classification. ICLR 2026. | arXiv:2507.06867 | Prop. 2 positioning; RQ2; floor variant (Interp-Q) |
| 2 | Bhattacharyya, A., Ding, T., Barber, R. F. Conformal Prediction with Macro-Coverage Guarantees. 2026. | arXiv:2606.28598 | Prop. 2 (label-group constraints, multi-constraint optimum); alternative to strict per-stratum coverage |
| 3 | Chzhen, E., Denis, C., Hebiri, M., Lorieul, T. Set-valued classification – overview via a unified framework. 2021. | arXiv:2102.12318 | Optimal set-valued rules under class-specific constraints |
| 4 | Liu, S., Huang, J., Ong, L. Conformal Prediction Meets Long-tail Classification (TACP). 2025 (AAAI 2026 per ojs.aaai.org). | arXiv:2508.11345 | RQ1 analogue in long-tailed classification |
| 5 | Choi, S. Conformal Bayes under Continuous Label Shift: Sensitivity Analysis and the Limits of Exact Validity. 2026. | arXiv:2609.27976 | Cor. 1, Experiment 4 (exponential tilts) |
| 6 | Lee, H., Kim, J., Jadamba, E., Choi, S., Shin, H. Conformal Prediction for Molecular Properties under Label Shift. 2026. | arXiv:2608.17678 | Section 2.4 |
| 7 | Choi, S. Conformal Bayes under Label Shift: Post-Hoc Calibration vs. In-Training Adaptation. 2026 (EIML@ICML 2026). | arXiv:2606.11865 | Section 2.4 |
| 8 | Cuonzo, S., Deliu, N. Conformal Prediction Intervals with Tail-Specific Guarantees. 2026. | arXiv:2606.18199 | Section 2.3 differentiation |
| 9 | Wang, T. Geometry of tail allocation in conformal prediction intervals. 2026. | arXiv:2604.25202 | Section 2.3 differentiation |
| 10 | Sampson, M., Chan, K.-S. Flexible Conformal Highest Predictive Conditional Density Sets. 2024/2025. | arXiv:2406.18052 | Density-score family, Table 1 |
| 11 | Le Bars, B., Humbert, P. On Volume Minimization in Conformal Regression. 2025. | arXiv:2502.09985 | Size optimality in conformal regression |

Already cited but needed in a new role: Guha et al. 2024 (R2-02 item 4, R2-14); Podkopaev & Ramdas 2021 (R2-03, R2-07); Izbicki et al. 2020/2022 (R2-01, reallocation mechanism); Sadinle et al. 2019 Sec. 4 (R2-11).

**Search outcome for the four requested areas.**

- **(a) Conformal calibration within bins of $Y$ in regression.** Beyond BCCP and BFQR, I found no further regression method that does this explicitly. Kandinsky CP (cited) and regression-as-classification combined with class-conditional CP subsume it. The paper's statement that the device is not new is correct, and the novelty space is correspondingly small.
- **(b) Size-optimal sets under label- or group-conditional coverage.** The 2025–2026 long-tailed classification papers (refs 1–2) are the important omissions.
- **(c) Conformal prediction for imbalanced regression / extreme targets.** I found no paper that combines conformal coverage guarantees with imbalanced regression in the relevance-function sense. This is the paper's best genuine niche, and it is under-exploited (R2-05, R2-08).
- **(d) Label-shift robustness of label-conditional conformal regression.** I found no paper stating Cor. 1(i) for continuous outcomes. It is, however, an immediate corollary of Mondrian validity, and the recent continuous-label-shift work (refs 5–7) must be discussed.

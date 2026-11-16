---
title: "Covering the rare outcomes: stratified conformal prediction with size-optimal density scores for imbalanced regression"
author:
  - "[Author 1]^a,\\*^, [Author 2]^b^"
  - "^a^ [Affiliation 1, full postal address]; ^b^ [Affiliation 2, full postal address]"
  - "^\\*^ Corresponding author: [e-mail address]"
abstract: |
  Prediction intervals for regression are usually calibrated to hold on average over all outcomes, so they can systematically miss the rare, extreme outcomes that matter most in imbalanced regression. We study stratum-wise coverage, the probability that a prediction set contains the outcome given that the outcome lies in a target stratum such as the upper tail. We prove that even the oracle interval with exact covariate-conditional coverage under-covers extreme outcomes: in a Gaussian model with half of the variance explained it covers only 70.5% of the top decile. Calibrating conformal thresholds within target strata, as in bin-conditional conformal prediction, guarantees stratum-wise coverage for any score; we show that the score then determines only the set size and that conditional-density level sets with stratum-specific thresholds are size-optimal. This yields stratified density-level conformal prediction (SDLC), a floor variant with simultaneous marginal and stratum-wise guarantees, and precise conditions for robustness to target shift. In a pre-registered benchmark on 31 OpenML-CTR23 datasets with 10 random splits each, marginal and covariate-adaptive conformal methods covered only 69.0%–81.9% of upper-tail outcomes at a nominal 90%, whereas stratified methods covered 90.7%–90.9%, consistent with exact validity, at a median size increase of 1.05–1.14-fold. SDLC produced smaller stratum-valid sets than bin-conditional conformal prediction (geometric-mean ratio 0.93) and binned quantile regression (0.83), replicated with a neural base learner, and more targeted alerts for extreme outcomes. Code and all raw results are released.
---

**Keywords:** Conformal prediction; Imbalanced regression; Prediction intervals; Uncertainty quantification; Mondrian calibration; Extreme values; Distribution shift


# 1. Introduction

Many regression problems that intelligent systems are asked to solve are judged by how they handle the *rare* outcomes: the unusually expensive property, the exceptional salary, the extreme load on a power grid, the very toxic compound. These outcomes are rare by definition, so they are under-represented in training data, and models trained by minimising average loss shrink their predictions towards the bulk of the target distribution. This is the setting of *imbalanced regression* [@branco2016survey; @ribeiro2020imbalanced; @yang2021delving], where a growing literature re-weights, re-samples or re-parameterises models so that point predictions for rare targets become more accurate.

Point predictions are only half of what a decision maker needs. Prediction *sets* (or intervals) with a coverage guarantee state how far the truth may be from the prediction, and conformal prediction delivers such guarantees in finite samples for any model, under exchangeability only [@vovk2005alrw; @lei2018distribution; @angelopoulos2023gentle]. Its standard guarantee, however, is *marginal*: the set contains the outcome with probability $1-\alpha$ *on average over all outcomes*. When rare outcomes are what matter, the relevant question is different: **when the outcome is extreme, how often does the set contain it?** A marginal guarantee is silent on this question, because the frequent bulk of the distribution can be over-covered while the rare tails are under-covered and the average still equals $1-\alpha$.

A large body of work makes conformal sets adapt to the covariates, so that coverage holds approximately conditionally on $X$ [@romano2019conformalized; @chernozhukov2021distributional; @izbicki2022cdsplit; @gibbs2025conformal]. A natural expectation is that such covariate-adaptive sets also protect rare outcomes. We show, in a Gaussian model where everything is explicit, that they do not, and that this is not a matter of estimation quality: even the *oracle* set with exact coverage $1-\alpha$ at every $x$ covers only a fraction of the extreme outcomes, because an extreme outcome typically combines an extreme signal with an extreme, unpredictable noise realisation that no $X$-measurable set can anticipate. Coverage *conditional on the target*, which we call stratum-wise coverage, is therefore a different property that must be targeted explicitly.

Calibrating conformal thresholds separately within bins of the observed outcome is the natural device for this purpose, and it is not new. @randahl2026bin proposed it as bin-conditional conformal prediction (BCCP) for the heavily skewed distribution of conflict fatalities, and it is the binning step of the binned fair quantile regression of @wang2023equal, which targets equal coverage across groups conditionally on the outcome. Its finite-sample bin-wise validity is an instance of Mondrian (label-conditional) validity [@vovk2005alrw; @vovk2013conditional; @toccaceli2019combination]. What has been missing is an explanation of *why* such calibration is unavoidable, guidance on *which* conformity score it should be combined with, a precise account of *what* it guarantees when the target distribution shifts, and evidence of *how much* it costs and gains across many problems. This paper supplies these four elements:

1. **Why covariate adaptivity is not enough.** We formalise stratum-wise coverage, $P\{Y\in C(X)\,|\, Y\in B_k\}\ge 1-\alpha_k$, for target strata $B_k$ such as the lower and upper tails; it is the regression analogue of class-conditional coverage. We prove that covariate-conditional validity does not imply it, even for the oracle: in a Gaussian model the shortest interval with coverage $1-\alpha$ at every $x$ covers only 70.5% of the top-decile outcomes when the predictor explains half of the variance, and its coverage at $y$ vanishes as $|y|$ grows (Proposition 1). Tail under-coverage of standard conformal sets has been reported empirically [@randahl2026bin; @wang2023equal; @boruah2026distribution]; Proposition 1 shows that it persists with a perfect model.
2. **Which score to stratify.** Stratified calibration is valid for any score, so the score determines only how large the sets are. We prove that, among all prediction sets with coverage at least $1-\alpha_k$ in every stratum, expected Lebesgue measure is minimised by conditional-density level sets with stratum-specific thresholds (Theorem 2). This extends the Neyman–Pearson characterisation of least-ambiguous set-valued classifiers with class-specific coverage [@sadinle2019least; @lei2014classification] from finitely many labels to strata of a continuous outcome, and, when $K=1$, reduces to single-threshold conditional-density level sets, the continuous counterpart of the total-coverage solution of @sadinle2019least.
3. **SDLC and a precise account of its guarantees.** Stratified density-level conformal prediction (SDLC) combines stratified calibration with an estimate of the optimal score of Theorem 2, a semiparametric location–scale conditional density whose noise density is estimated by a kernel. A *floor* variant guarantees marginal coverage $1-\alpha$ and stratum-wise coverage $1-\beta$ simultaneously in finite samples. We make the robustness of stratified calibration to target shift precise (Corollary 1), which, unlike re-weighting approaches [@podkopaev2021distribution; @yi2025distribution; @lee2026split], requires no estimate of the shift: stratum-wise coverage is preserved exactly when a shift re-weights whole strata, and otherwise it can degrade by at most the total-variation distance between the within-stratum laws, which we bound for label shift.
4. **A pre-registered benchmark.** On all 31 eligible datasets of the OpenML-CTR23 suite [@fischer2023openml], each with 10 predefined random splits, we compare 15 conformal procedures that share identical base models, including BCCP in its union and hull forms, a BFQR-style binned conformalised quantile regression and seven marginal or covariate-adaptive methods. Dataset-level non-parametric statistics quantify tail coverage, the price of stratum-wise validity in set size, whether the size advantage predicted by Theorem 2 survives estimation of the density, robustness to target shift, sensitivity to design choices, a second learner family and computational cost. Deviations from the pre-registered protocol are documented, and code, configuration and all raw results are released.

The remainder of the paper is organised as follows. Section 2 reviews related work. Section 3 formalises the problem and proves Proposition 1. Section 4 presents stratified calibration, its guarantees and the optimal score, and introduces SDLC. Section 5 describes the experimental design, Section 6 reports the results, Section 7 discusses implications and limitations, and Section 8 concludes.


# 2. Related work

Four lines of work meet in this paper: conformal regression with covariate-adaptive coverage, calibration within categories defined by the label, imbalanced regression, and conformal prediction under distribution shift.

## 2.1 Conformal regression and covariate-conditional coverage

Split (inductive) conformal prediction calibrates a nonconformity score of an arbitrary fitted regressor on held-out data and guarantees marginal coverage in finite samples under exchangeability [@papadopoulos2002inductive; @vovk2005alrw; @lei2018distribution]. Much subsequent work changes the score so that the sets adapt to the covariates. Locally weighted (normalised) conformal prediction divides absolute residuals by an estimate of their spread [@lei2018distribution]; conformalised quantile regression (CQR) calibrates the interval between two estimated conditional quantiles [@romano2019conformalized; @sesia2020comparison]; and distributional conformal prediction (DCP) uses the probability integral transform of an estimated conditional distribution function [@chernozhukov2021distributional]. Conformal predictive distributions [@vovk2019nonparametric] and jackknife+/CV+ intervals, which reuse all data at higher computational cost [@barber2021jackknife], are further alternatives. A family of methods builds sets from density estimates: density level sets, conformalised without covariates and asymptotically optimal [@lei2013distribution] and extended to regression by local conformal bands [@lei2014bands]; Dist-split and CD-split [@izbicki2020flexible]; HPD-split, which conformalises highest-density regions of an estimated conditional density [@izbicki2022cdsplit]; conformal sets from conditional histograms, which adapt to skewness [@sesia2021conformal]; and regression-as-classification, which learns a density over a discretised target [@guha2024conformal]. SDLC uses a score from this family but calibrates it with stratum-specific thresholds.

These methods target approximate covariate-conditional coverage, $P\{Y\in C(X)\,|\, X=x\}\approx 1-\alpha$, which cannot be guaranteed in finite samples without further assumptions [@barber2021limits]. The literature has therefore pursued relaxed guarantees and approximations: local conformal bands with asymptotic conditional validity [@lei2014bands]; conditional calibration, which guarantees coverage over a user-specified class of covariate groups or shifts [@gibbs2025conformal]; localised calibration, which weights calibration points by their proximity to the test point in covariate space [@guan2023localized; @hore2025local]; calibration within the cells of covariate partitions learned by regression trees [@cabezas2025regression] or by the leaf paths of gradient-boosted trees [@santos2026loboost]; and learned scores or adjusted regressors that reduce conditional miscoverage [@xie2024boosted; @gao2024adjusting]. In applied expert systems, conformal prediction serves as an uncertainty layer, for example for option prices [@bastos2024conformal], tropical-cyclone track forecasts [@meng2024uncertainty] and the carbonation depth of recycled-aggregate concrete [@hajibabaee2025carbonation]. All of these approaches are marginal or condition, exactly or approximately, on functions of $X$, and Proposition 1 (Section 3) shows that, in a Gaussian model, even exact covariate-conditional coverage leaves extreme outcomes under-covered. Covariate-adaptive scores are therefore complementary to stratified calibration rather than a substitute for it.

## 2.2 Category-, label- and bin-conditional calibration

Mondrian conformal predictors [@vovk2005alrw; @vovk2022alrw] assign each example to a category through a taxonomy that may depend on both the object and its label, and calibrate separately within each category; this yields finite-sample coverage conditional on the category [@angelopoulos2024theoretical]. @vovk2012conditional distinguished object-, label- and training-conditional validity and showed that Mondrian inductive conformal predictors achieve category-conditional, and in particular label-conditional, validity [see also @vovk2013conditional]; @toccaceli2019combination studied label-conditional inductive Mondrian predictors and their combination.

In classification, the corresponding property is class-conditional coverage. When classes are many and calibration examples per class are few, clustered conformal prediction pools classes with similar score distributions [@ding2023class], a device analogous to merging sparse target strata; BCOPS constructs label-conditional sets from density estimates [@guan2022prediction]; and class-conditional Mondrian conformal prediction has been applied in this journal to product verification [@oucheikh2022product]. Closest to our optimality result is work on set-valued classifiers with class-specific error control [@lei2014classification], in particular @sadinle2019least, who showed that the least ambiguous classifier under class-specific coverage thresholds the conditional class probabilities $p(y\,|\, x)$ with class-specific cut-offs. Theorem 2 transfers this characterisation from a finite label set to a continuous outcome, with Lebesgue measure as the size and target strata in place of classes. Kandinsky conformal prediction [@bairaktari2025kandinsky] provides conditional coverage for overlapping or fractional groups defined jointly on covariates and labels, contains covariate-group-conditional, class-conditional and Mondrian conformal prediction as special cases, and comes with a minimax-optimal high-probability bound on conditional coverage; disjoint target strata are, formally, label-defined groups, so stratified calibration plausibly falls within this framework.

In regression, Mondrian categories have mostly been defined through the covariates or the fitted model: by binning difficulty estimates [@bostrom2020mondrian], by the leaves of regression trees [@johansson2018interpretable], by clusters of the covariates [@sousa2024improving] and by quartiles of out-of-fold point predictions [@boruah2026distribution]; Mondrian taxonomies have also been applied to conformal predictive distributions [@bostrom2021mondrian]. The last study reports that split conformal intervals for steel fatigue strength, although marginally valid, under-cover the highest-strength quartile; a follow-up shows that worst-bin coverage statistics are biased downwards and proposes a null correction [@boruah2026null]. Because the categories are functions of $X$, the resulting guarantees do not extend to coverage conditional on $Y$.

We are aware of two regression methods that calibrate within bins of the outcome itself. @wang2023equal define equal opportunity of coverage, which requires coverage to be equal across groups of a sensitive attribute conditionally on the true outcome; their binned fair quantile regression (BFQR) splits $Y$ into equal-mass bins and calibrates within each combination of group and bin, with a conformal step that maintains coverage, and they illustrate that standard methods mis-cover the head and tail bins of the outcome. Their aim is fairness, but the binning device is the same. The most closely related work is the bin-conditional conformal prediction (BCCP) of @randahl2026bin, motivated by the heavily skewed distribution of fatalities from armed conflict. BCCP partitions the calibration scores by user-defined bins of the observed outcome, runs split conformal prediction with a residual score within each bin over a grid of candidate outcomes, and returns either the union of the per-bin sets, which may be discontiguous, or its hull ("contiguized" sets). The authors state that BCCP guarantees coverage within each bin under within-bin exchangeability, describe it as a hybrid of label-conditional (Mondrian) and split conformal prediction, and evaluate it on simulations and on conflict fatalities.

The stratified calibration step of the present paper (Section 4, Eqs. 3–4) coincides with BCCP: with the absolute-residual score and the strata as bins it is BCCP, and taking the convex hull, as in our hull variant, gives its contiguized form. Its finite-sample validity (Theorem 1) is an instance of Mondrian validity and is not claimed as new. BCCP leaves open which score yields the smallest bin-valid sets and how the guarantee behaves under label shift. The contributions of the present paper lie elsewhere: the impossibility result for covariate-conditional sets (Proposition 1), the size-optimal score under per-stratum coverage (Theorem 2) and the SDLC procedure built on it, the floor variant with simultaneous marginal and per-stratum guarantees, the label-shift analysis, and large-scale evidence in which BCCP and a single-group, BFQR-style binned CQR serve as baselines.

## 2.3 Imbalanced regression and its uncertainty

Imbalanced regression concerns problems in which the target values that matter most are rare in the training data [@branco2016survey; @ribeiro2020imbalanced]. Utility-based regression encodes the non-uniform importance of targets through relevance and utility functions [@torgo2007utility], and precision and recall for regression [@torgo2009precision] and the SERA metric [@ribeiro2020imbalanced] evaluate point predictions on the relevant, typically extreme, part of the target range. Data-level methods re-balance the training set: SMOTER [@torgo2013smote] and SMOGN, which adds Gaussian noise [@branco2017smogn], synthesise examples with rare targets, and @avelino2024resampling survey and benchmark such re-sampling strategies. Recent contributions in this journal include oversampling with nearest neighbours and autoencoders [@belhaouari2024oversampling], the refinement of SMOGN samples by a generative adversarial network [@alahyari2026smogan], a hybrid of data-level and algorithm-level balancing [@shahbazi2026hybrid] and soft-computing techniques that actively address imbalance [@arteaga2023enhancing]. For deep models, @yang2021delving propose label and feature distribution smoothing, which exploit the similarity of nearby targets.

Uncertainty has entered this literature mainly as a means to better point predictions or as a by-product of probabilistic modelling. Variational imbalanced regression obtains uncertainty estimates through probabilistic smoothing [@wang2023variational], and UQDIR identifies rare samples through epistemic uncertainty and re-samples them with a weight function to improve accuracy [@dolar2025uncertainty]; neither provides a coverage guarantee. Extreme conformal prediction addresses a different difficulty, very high confidence levels, by combining extreme-value theory with conformal prediction [@pasche2026extreme]. To our knowledge, guarantees on how often prediction sets contain the rare targets themselves, the uncertainty counterpart of the relevance-based evaluation above, have not been studied within the imbalanced-regression literature; the closest methods come from conflict forecasting and fair regression (Section 2.2).

## 2.4 Distribution shift

Weighted conformal prediction restores validity under covariate shift by re-weighting calibration scores with the likelihood ratio of the covariate distributions [@tibshirani2019conformal]. Under label shift, also called target shift, the marginal distribution of $Y$ changes while the conditional distribution of $X$ given $Y$ does not. For classification, @podkopaev2021distribution study conformal prediction under label shift, using re-weighted and label-conditional calibration. For regression, @yi2025distribution identify the likelihood ratio under target shift and construct highest-density sets from a weight-adjusted conditional density, and @lee2026split combine a label-shift-adjusted Bayesian score with importance weighting. The re-weighting approaches estimate the shift [@yi2025distribution; @lee2026split]; label-conditional calibration in classification needs no estimate, because a label shift re-weights whole classes [@podkopaev2021distribution].

Stratified calibration carries this property over to regression: it needs no estimate of the shift, because a guarantee that holds within every stratum is unaffected by changes in the stratum probabilities. This invariance is exact when the shift re-weights whole strata, that is, when the conditional distribution of $(X,Y)$ within each stratum is unchanged (Corollary 1). If the density ratio varies inside a stratum, the within-stratum distribution changes and the guarantee holds only approximately, which our experiments quantify under target tilting (Section 5).

**Positioning of this work.** Calibration within outcome strata [@randahl2026bin; @wang2023equal] and its per-stratum validity [@vovk2005alrw; @vovk2013conditional; @randahl2026bin] are established, and the present paper takes them as given. It asks instead why such calibration is needed even when covariate-conditional coverage is exact (Proposition 1), how small stratum-valid sets can be and how their cost can be limited (Theorem 2, SDLC and its floor variant), and when the guarantee survives label shift (Corollary 1). It then examines them empirically in a pre-registered comparison on 31 OpenML-CTR23 datasets [@fischer2023openml], with 10 repetitions each, against BCCP, a BFQR-style binned CQR and marginal and covariate-adaptive conformal methods. For imbalanced regression, this complements methods that improve accuracy on rare targets with a guarantee on how often prediction sets contain them.


# 3. Problem formulation

## 3.1 Target-conditional coverage

Let $(X,Y)\in\mathcal{X}\times\mathbb{R}$ have joint law $P$, with marginal law $P_X$ of the covariates. A *prediction set* is a map $C$ from $\mathcal{X}$ to subsets of $\mathbb{R}$ whose graph $\{(x,y):y\in C(x)\}$ is jointly measurable. Split conformal prediction [@papadopoulos2002inductive; @lei2018distribution] guarantees *marginal* coverage $P\{Y\in C(X)\}\ge 1-\alpha$, and much recent work targets approximate *covariate-conditional* coverage $P\{Y\in C(X)\,|\, X=x\}\approx 1-\alpha$ [@romano2019conformalized; @izbicki2022cdsplit; @gibbs2025conformal], which cannot be guaranteed in finite samples without further assumptions [@barber2021limits].

In imbalanced regression the outcomes of interest are rare target values. Let $e_1<\dots<e_{K-1}$ be cut points and $B_1=(-\infty,e_1)$, $B_k=[e_{k-1},e_k)$ for $1<k<K$, $B_K=[e_{K-1},\infty)$ the resulting *target strata*, for instance the lower tail, the bulk and the upper tail, with $p_k=P(Y\in B_k)>0$. We call
$$\operatorname{Cov}_k(C)=P\{Y\in C(X)\,|\, Y\in B_k\},\qquad k=1,\ldots,K, \qquad (1)$$
the *stratum-wise* (target-conditional) coverage of $C$. It answers the question that matters when extremes are costly: *when the outcome is extreme, how often does the prediction set contain it?* It is the regression analogue of class-conditional coverage in classification [@vovk2005alrw; @vovk2013conditional; @sadinle2019least]. Because $\sum_k p_k\,\operatorname{Cov}_k(C)=P\{Y\in C(X)\}$, marginal coverage only constrains a $p$-weighted average of the $\operatorname{Cov}_k$: rare strata can be under-covered while the bulk is over-covered. The next proposition shows that this is not merely a defect of estimation that better covariate-conditional methods would remove.

## 3.2 Covariate-conditional validity does not imply target-conditional validity

**Proposition 1.** *Let $X\sim N(0,\tau^2)$ and $Y\,|\, X\sim N(X,\sigma^2)$ with $\tau^2+\sigma^2=1$ and $0<\tau^2<1$, so that $R^2=\tau^2$ is the fraction of variance explained by the optimal predictor. Let $z=\Phi^{-1}(1-\alpha/2)$ and $C^{\mathrm{cov}}(x)=[x-z\sigma,\,x+z\sigma]$, which is, up to Lebesgue-null sets, the unique set of minimal length with $P\{Y\in C(x)\,|\, X=x\}\ge 1-\alpha$ for every $x$. Then*
$$P\{Y\in C^{\mathrm{cov}}(X)\,|\, Y=y\}=\Phi\!\left(\frac{z\sigma-(1-R^2)y}{s}\right)-\Phi\!\left(\frac{-z\sigma-(1-R^2)y}{s}\right),\qquad s=\sigma\sqrt{R^2}, \qquad (2)$$
*an even function of $y$ that is strictly decreasing in $|y|$ and tends to $0$ as $|y|\to\infty$.*

*Proof.* $(X,Y)$ is bivariate normal with $\operatorname{Var}(Y)=1$ and $\operatorname{Cov}(X,Y)=\tau^2$, hence $X\,|\, Y=y\sim N(\tau^2y,\tau^2\sigma^2)$ and $Y-X\,|\, Y=y\sim N((1-\tau^2)y,\tau^2\sigma^2)$. Since $Y\in C^{\mathrm{cov}}(X)$ iff $|Y-X|\le z\sigma$, (2) follows. Write $a=z\sigma>0$ and $m=(1-R^2)y$. The function $h(m)=\Phi((a-m)/s)-\Phi((-a-m)/s)$ is even because $\Phi(-u)=1-\Phi(u)$, and for $m>0$, $h'(m)=-\{\phi((a-m)/s)-\phi((a+m)/s)\}/s<0$ because $|a-m|<a+m$. As $1-R^2>0$, (2) is strictly decreasing in $|y|$ and vanishes as $|y|\to\infty$. Minimality and uniqueness of $C^{\mathrm{cov}}(x)$ follow because the $N(x,\sigma^2)$ density is symmetric and strictly unimodal. $\square$

Table 1 integrates (2) over strata of $Y$. For a predictor that explains half of the variance, the oracle covariate-conditional interval covers only 70.5% of the top-10% outcomes and 37.5% of the top-1% outcomes, while it covers 94.9% of the central 80%; even with $R^2=0.9$ it covers 86.2% of the top decile. The mechanism is general: an extreme outcome is typically the sum of an extreme signal and an extreme noise realisation, and the shortest covariate-conditionally valid set spends its coverage in the bulk of each conditional distribution, where such outcomes rarely fall. Covariate-conditional validity does not *rule out* stratum-wise validity (in the model of Proposition 1 a convexity argument shows that sets with both properties exist), but the two criteria select different sets, and to guarantee coverage in rare strata a set must be calibrated against the distribution of $(X,Y)$ *given* $Y\in B_k$. This is what stratified calibration does.

**Table 1.** Proposition 1: coverage of the oracle covariate-conditional interval $C^{\mathrm{cov}}$ ($\alpha=0.1$) within strata of the target, in the Gaussian model. Analytic values from Eq. (2); Monte Carlo with $2\times10^6$ draws. The marginal coverage is 0.900 in every row.

| R²   | Top 10% (analytic)   | Top 10% (Monte Carlo)   | Top 1% (analytic)   | Central 80% (analytic)   |
|:-----|:---------------------|:------------------------|:--------------------|:-------------------------|
| 0.30 | 0.621                | 0.621                   | 0.166               | 0.970                    |
| 0.50 | 0.705                | 0.706                   | 0.375               | 0.949                    |
| 0.70 | 0.784                | 0.784                   | 0.586               | 0.929                    |
| 0.90 | 0.862                | 0.861                   | 0.795               | 0.910                    |
| 0.95 | 0.881                | 0.881                   | 0.848               | 0.905                    |


# 4. Stratified calibration and the optimal score

## 4.1 Stratified (Mondrian) calibration

Data are split into a proper training set $\mathcal{D}_{\mathrm{tr}}$ and a calibration set $\mathcal{D}_{\mathrm{cal}}=\{(X_i,Y_i)\}_{i=1}^n$. Using $\mathcal{D}_{\mathrm{tr}}$ only, we fit a nonconformity score $s:\mathcal{X}\times\mathbb{R}\to\mathbb{R}\cup\{+\infty\}$ (small values = conforming) and choose the cut points, e.g. at quantiles of the training targets. Let $k(y)$ be the stratum containing $y$, $I_k=\{i:Y_i\in B_k\}$, $n_k=|I_k|$, and, for levels $\alpha_k\in(0,1)$,
$$\hat q_k=\text{the }\lceil (n_k+1)(1-\alpha_k)\rceil\text{-th smallest value of }\{s(X_i,Y_i):i\in I_k\}, \qquad (3)$$
with $\hat q_k=+\infty$ if that rank exceeds $n_k$, which happens exactly when $n_k<1/\alpha_k-1$ (i.e. $n_k\le 8$ for $\alpha_k=0.1$ and $n_k\le 18$ for $\alpha_k=0.05$). The stratified prediction set is
$$\hat C(x)=\{y\in\mathbb{R}: s(x,y)\le \hat q_{k(y)}\}=\bigcup_{k=1}^K\{y\in B_k: s(x,y)\le\hat q_k\}. \qquad (4)$$
The threshold applied to a candidate value $y$ is that of the stratum *of that candidate*, not of a prediction; this is what makes the guarantee target-conditional. Equation (4) is an inductive Mondrian conformal predictor whose taxonomy assigns each example to the stratum of its label [@vovk2005alrw; @vovk2013conditional; @toccaceli2019combination], and it is not new for regression: with the absolute-residual score it is the bin-conditional conformal prediction (BCCP) of @randahl2026bin, who report either the union (4) or its convex hull, and @wang2023equal calibrate within equal-mass bins of $Y$ in a method that targets equal coverage across groups conditionally on the outcome. Kandinsky conformal prediction [@bairaktari2025kandinsky] extends group-conditional guarantees to overlapping groups defined jointly on covariates and labels. What this paper adds to (3)–(4) is the choice of score (Theorem 2), the floor variant, and a precise account of the guarantee under target shift (Corollary 1). When every sub-level set $\{y:s(x,y)\le q\}$ is an interval, as for residual or quantile scores, $\hat C(x)$ is a union of at most $K$ intervals; density scores with a multimodal estimate can produce more pieces.

The following guarantee is the standard label-conditional Mondrian property, restated for an arbitrary score with the edge cases used later; its proof is given in Appendix A for completeness.

**Theorem 1 (stratum-wise validity of Mondrian calibration).** *Suppose that, conditionally on $\mathcal{D}_{\mathrm{tr}}$, the points $(X_1,Y_1),\ldots,(X_n,Y_n),(X_{n+1},Y_{n+1})$ are exchangeable, and let $p_k=P(Y_{n+1}\in B_k\,|\,\mathcal{D}_{\mathrm{tr}})$. Then for every $k$ with $p_k>0$,*
$$P\{Y_{n+1}\in\hat C(X_{n+1})\,|\, Y_{n+1}\in B_k,\mathcal{D}_{\mathrm{tr}}\}\ \ge\ 1-\alpha_k, \qquad (5)$$
*and consequently $P\{Y_{n+1}\in\hat C(X_{n+1})\,|\,\mathcal{D}_{\mathrm{tr}}\}\ge 1-\sum_kp_k\alpha_k\ge 1-\max_k\alpha_k$. If the scores within stratum $k$ are almost surely distinct, then also $P\{Y_{n+1}\in\hat C(X_{n+1})\,|\, Y_{n+1}\in B_k,n_k,\mathcal{D}_{\mathrm{tr}}\}\le 1-\alpha_k+1/(n_k+1)$. The levels $\alpha_k$ may depend on $n_k$, and the score and strata may be any functions of $\mathcal{D}_{\mathrm{tr}}$.*

The guarantee holds for *any* score. A useful consequence concerns shifts of the target distribution between calibration and deployment.

**Corollary 1 (target shift).** *Let $\mathcal{D}_{\mathrm{cal}}$ be i.i.d. from $P$ and let the test point be drawn from $Q$, independently of $\mathcal{D}_{\mathrm{cal}}$ and $\mathcal{D}_{\mathrm{tr}}$. Write $P_k=P(\cdot\,|\, Y\in B_k)$ and $Q_k=Q(\cdot\,|\, Y\in B_k)$ for the within-stratum laws of the pair $(X,Y)$ and $\pi_k=Q(Y\in B_k)$; assume $p_k>0$ whenever $\pi_k>0$.*
*(i) If $Q_k=P_k$ for every $k$ with $\pi_k>0$ (the shift re-weights whole strata), then $Q\{Y\in\hat C(X)\,|\, Y\in B_k\}\ge 1-\alpha_k$ for every such $k$, and $Q\{Y\in\hat C(X)\}\ge 1-\sum_k\pi_k\alpha_k$ whatever the $\pi_k$.*
*(ii) For an arbitrary shift, $Q\{Y\in\hat C(X)\,|\, Y\in B_k\}\ge 1-\alpha_k-d_{\operatorname{TV}}(Q_k,P_k)$.*
*(iii) Under label shift, $Q(\cdot\,|\, Y=y)=P(\cdot\,|\, Y=y)$ with density ratio $w=dQ_Y/dP_Y$; let $m_k$ and $M_k$ be the essential infimum and supremum of $w$ on $B_k$, $0<m_k\le M_k<\infty$. Then $Q\{Y\notin\hat C(X)\,|\, Y\in B_k\}\le(M_k/m_k)\,\alpha_k$ and $d_{\operatorname{TV}}(Q_k,P_k)\le\tanh\{\log(M_k/m_k)/4\}$.*

The proof is in Appendix A. Part (i) is the stratified analogue of the fact that class-conditional coverage survives label shift in classification [cf. @podkopaev2021distribution]. With a continuous outcome, however, a label shift generally also changes the distribution of $Y$ *within* a stratum, and exactness then requires that the joint law of $(X,Y)$ inside each stratum be unchanged; a stable covariate distribution alone is not sufficient. Parts (ii)–(iii) quantify the degradation otherwise: it is small when the density ratio varies little across each stratum, which favours narrow strata at the price of fewer calibration points per stratum, and the bound in (iii) becomes vacuous for an open tail stratum under an unbounded tilt. Marginally calibrated sets enjoy no analogue of (i): their coverage under $Q$ is $\sum_k\pi_k\operatorname{Cov}_k$, which can be as low as $\min_k\operatorname{Cov}_k$. Unlike re-weighting approaches [@podkopaev2021distribution; @yi2025distribution; @lee2026split; for covariate shift @tibshirani2019conformal], stratified calibration needs no estimate of the shift, but it is exact only for shifts that act on the stratum probabilities. Experiment 4 examines continuous tilts, which also re-weight within strata.

## 4.2 The smallest sets with stratum-wise coverage

Theorem 1 leaves the score free, so validity is never the issue; the score determines how large the sets are. For a prediction set $C$ let $|C(x)|$ be its Lebesgue measure and $\mathbb{E}|C(X)|=\int|C(x)|\,P_X(dx)$ its expected size.

**Theorem 2 (size-optimal stratum-wise sets).** *Suppose the conditional law of $Y$ given $X$ has a Lebesgue density $f(y\,|\, x)$, that $f(Y\,|\, X)>0$ almost surely, and that for each $k$ the random variable $f(Y\,|\, X)$ has a continuous distribution conditionally on $Y\in B_k$. Fix $\alpha_1,\ldots,\alpha_K\in(0,1)$. Then there are thresholds $t_k>0$ with $P\{f(Y\,|\, X)\ge t_k\,|\, Y\in B_k\}=1-\alpha_k$, and the set*
$$C^\star(x)=\bigcup_{k=1}^K\{y\in B_k: f(y\,|\, x)\ge t_k\} \qquad (6)$$
*satisfies $\operatorname{Cov}_k(C^\star)=1-\alpha_k$ for all $k$. Every prediction set $C$ with $\operatorname{Cov}_k(C)\ge 1-\alpha_k$ for all $k$ satisfies $\mathbb{E}|C(X)\cap B_k|\ge\mathbb{E}|C^\star(X)\cap B_k|$ for every $k$, and hence $\mathbb{E}|C(X)|\ge\mathbb{E}|C^\star(X)|$.*

*Proof.* Existence: $G_k(t)=P\{f(Y\,|\, X)\ge t\,|\, Y\in B_k\}$ is continuous and non-increasing with $G_k(0^+)=1$ and $G_k(t)\to0$ as $t\to\infty$, so the intermediate value theorem gives $t_k>0$ with $G_k(t_k)=1-\alpha_k$. Optimality: write $A=\{(x,y):y\in C(x)\}$, $A^\star$ likewise, $A_k=A\cap(\mathcal{X}\times B_k)$, $A_k^\star=A^\star\cap(\mathcal{X}\times B_k)$ and $|A|_P=\iint\mathbf{1}_A(x,y)\,dy\,P_X(dx)$, so that $\mathbb{E}|C(X)\cap B_k|=|A_k|_P$ and $p_k\operatorname{Cov}_k(C)=\iint\mathbf{1}_{A_k}f(y\,|\, x)\,dy\,P_X(dx)$. Since $|\{y:f(y\,|\, x)\ge t_k\}|\le 1/t_k$, $|A_k^\star|_P<\infty$; if $|A_k|_P=\infty$ there is nothing to prove. Otherwise the integrand of
$$\Delta_k=\iint\left(\mathbf{1}_{A_k^\star}-\mathbf{1}_{A_k}\right)\left(f(y\,|\, x)-t_k\right)dy\,P_X(dx)$$
is non-negative pointwise: on $A_k^\star\setminus A_k$ we have $f\ge t_k$, and on $A_k\setminus A_k^\star$, where $y\in B_k$, we have $f<t_k$. Hence $\Delta_k\ge 0$, i.e. $t_k(|A_k^\star|_P-|A_k|_P)\le p_k\{\operatorname{Cov}_k(C^\star)-\operatorname{Cov}_k(C)\}\le 0$, and $t_k>0$ gives $|A_k^\star|_P\le|A_k|_P$. $\square$

Theorem 2 is the regression counterpart of the Neyman–Pearson argument behind least-ambiguous set-valued classifiers with class-specific error levels [@sadinle2019least; @lei2014classification]; with $K=1$ it reduces to a single-threshold conditional-density level set, the continuous counterpart of the total-coverage solution of @sadinle2019least and, without covariates, of conformal density level sets [@lei2013distribution]; HPD-split [@izbicki2022cdsplit] instead uses an $x$-specific threshold, whose oracle is the highest-density region of each conditional distribution. Since the inequality $\Delta_k\ge0$ holds for every realisation of a set built from data independent of the test point, $C^\star$ also minimises expected size among data-dependent (e.g. conformal) sets whose stratum-wise coverage, averaged over the data, is at least $1-\alpha_k$. Four consequences guide the method.

*The optimal score.* The size-optimal score is the conditional density, $s(x,y)=-f(y\,|\, x)$, combined with stratum-specific thresholds; a single threshold is optimal only for marginal coverage.

*The price of stratum-wise validity.* Every set that satisfies the stratum constraints has marginal coverage at least $1-\bar\alpha$, $\bar\alpha=\sum_kp_k\alpha_k$. Hence $\mathbb{E}|C^\star(X)|$ is at least the expected size of the size-optimal marginal set at level $1-\bar\alpha$, a single-threshold density level set; under the assumptions of Theorem 2 the two coincide if and only if $t_1=\dots=t_K$, i.e. if and only if that marginal set already has coverage $1-\alpha_k$ in every stratum. With a common level $\alpha_k=\alpha$ this difference is the price, in size, of stratum-wise validity.

*Shape.* $C^\star(x)$ need not be an interval even when $f(\cdot\,|\, x)$ is unimodal: thresholds differ across strata (typically $t_k$ is smaller in a rare tail stratum), so $C^\star(x)$ can contain a piece of a tail stratum while excluding part of an adjacent stratum.

*Scope.* The optimality refers to size averaged over the covariate law $P_X$ of the calibration population; under a shifted $Q$, $C^\star$ remains valid in the sense of Corollary 1(i) but is no longer size-optimal. For targets with atoms (ties, zero inflation) Theorem 1 is unaffected, whereas Lebesgue size is degenerate at an atom and the size-optimal set contains every atom; on such data a smooth density score is valid but not size-optimal.

## 4.3 The proposed method: stratified density-level conformal prediction (SDLC)

SDLC instantiates (3)–(4) with the plug-in score $s(x,y)=-\hat f(y\,|\, x)$, where $\hat f$ is estimated on $\mathcal{D}_{\mathrm{tr}}$. By Theorem 1 the guarantee (5) holds for any $\hat f$; Theorem 2 motivates the score. With $\hat f=f$ and growing strata, $-\hat q_k\to t_k$ and $\hat C$ approaches $C^\star$; we expect, but do not prove, the same for a consistent $\hat f$ (a result in the spirit of @lei2013distribution and @izbicki2022cdsplit would require continuity of the law of $f(Y\,|\, X)$ at each $t_k$). We use the semiparametric location–scale estimator
$$\hat f(y\,|\, x)=\frac{1}{\hat\sigma(x)}\,\hat g\!\left(\frac{y-\hat\mu(x)}{\hat\sigma(x)}\right), \qquad (7)$$
where $\hat\mu$ is a gradient-boosted regression of $Y$ on $X$, $\hat\sigma(x)=\max\{\tilde\sigma(x),10^{-3}\,\operatorname{sd}(Y_{\mathrm{tr}})\}$ with $\tilde\sigma$ a gradient-boosted regression of the absolute *out-of-fold* residuals $|Y-\hat\mu_{-j}(X)|$ (three folds; $\tilde\sigma$ plays the role of the spread estimate of locally weighted conformal prediction [@lei2018distribution]), and $\hat g$ is a Gaussian kernel density estimate (Silverman bandwidth) of the standardised out-of-fold residuals. The noise density $\hat g$ is nonparametric, so (7) captures skewness and heavy tails of the error distribution, while heteroscedasticity enters through $\hat\sigma$. If $Y=\mu(X)+\sigma(X)\varepsilon$ with $\varepsilon$ independent of $X$, (7) can be consistent; otherwise SDLC targets the optimal sets of the best location–scale approximation, which affects size but never validity. Two alternative estimators are evaluated as secondary results: an exploratory *two-piece* variant that replaces $\hat\sigma$ by $\hat\sigma_-(x)$ below $\hat\mu(x)$ and $\hat\sigma_+(x)$ above it (separate scale models for negative and positive out-of-fold residuals, with $\hat g$ the kernel estimate of the side-wise standardised residuals; this is a normalised density that captures covariate-dependent asymmetry of scale), and a fully nonparametric histogram density from a multiclass gradient-boosted classifier over 40 equal-mass target bins (a "regression-as-classification" density, cf. @sesia2021conformal and @guha2024conformal).

## 4.4 Implementation

*Strata.* The primary stratification uses the training-target quantiles $0.10, 0.25, 0.75, 0.90$ ($K=5$: lower tail, lower shoulder, bulk, upper shoulder, upper tail). With tied targets coinciding cut points are merged and empty strata removed, so the realised number of strata and their masses can differ from the nominal values; realised values are reported per dataset.

*Exact scores.* Calibration scores are computed exactly at the observed target, $S_i=-\hat g(\hat Z_i)/\hat\sigma(X_i)$ with $\hat Z_i=(Y_i-\hat\mu(X_i))/\hat\sigma(X_i)$. Sets are restricted to a bounded domain $D=[\min y-0.05r,\max y+0.05r]$ of the training targets ($r$ the training range): a point with $Y\notin D$ receives the score $+\infty$, stays in its stratum, and counts as not covered. Membership of a test target is decided by the same exact rule, $Y_{n+1}\in\hat C(X_{n+1})$ iff $s(X_{n+1},Y_{n+1})\le\hat q_{k(Y_{n+1})}$, so Theorem 1 applies to the implemented procedure, with one exception: when $\hat q_k=+\infty$ the reported set is $B_k\cap D$ rather than $B_k$. We report the fraction of test targets outside $D$ and how often $\hat q_k=+\infty$ occurs.

*Set geometry.* Only the size, the number of pieces and the hull of a set are computed numerically. Because $\hat C(x)\cap B_k=\{\hat\mu(x)+\hat\sigma(x)u:\hat g(u)\ge-\hat q_k\hat\sigma(x)\}\cap B_k$, the level sets are evaluated on a per-$x$ grid $y=\hat\mu(x)+\hat\sigma(x)u_j$ of 2048 standardised points, i.e. at a resolution relative to the conditional scale, with the regions beyond the tabulated range of $\hat g$ treated analytically. The same exact construction is used for every location–scale-family baseline (DLS, DCP, HPD-split, S-HPD). Histogram-density methods are evaluated on the grid of the histogram itself. (The pre-registered implementation evaluated all density-based sets on a fixed grid of 200 equal-mass cells of the *marginal* target distribution; Section 5.7 explains why it was replaced.)

> **Algorithm 1 (SDLC).** *Input:* $\mathcal{D}_{\mathrm{tr}}$, $\mathcal{D}_{\mathrm{cal}}$, levels $\alpha_k$, strata probabilities. (i) Fit $\hat\mu$, out-of-fold residuals, $\hat\sigma$ and $\hat g$ on $\mathcal{D}_{\mathrm{tr}}$; build the strata from training targets. (ii) For each calibration point compute $S_i=-\hat f(Y_i\,|\, X_i)$ (or $+\infty$ outside $D$) and its stratum $k(Y_i)$. (iii) Compute $\hat q_k$ by (3) within each stratum. (iv) For a test $x$, return $\{y\in D:\hat f(y\,|\, x)\ge-\hat q_{k(y)}\}$. *Cost:* fitting is that of three gradient-boosted regressions; calibration is $O(n\log n)$; prediction is $O(G)$ per test point for $G$ grid points.

## 4.5 Two practical variants

*Floor variant (SDLC-floor).* Practitioners may want the efficiency of a single marginal threshold while protecting rare strata at a lower level $1-\beta$. Define $\hat C_{\mathrm{floor}}(x)=\{y: s(x,y)\le\max(\hat q^{\mathrm{marg}}_\alpha,\hat q_{k(y)}(\beta))\}$, where $\hat q^{\mathrm{marg}}_\alpha$ is the ordinary split-conformal quantile at level $\alpha$ and $\hat q_k(\beta)$ the stratified quantile (3) at level $\beta$. Since $\hat C_{\mathrm{floor}}$ contains both the marginal set and the stratified set at level $\beta$, it has marginal coverage $\ge 1-\alpha$ and stratum-wise coverage $\ge 1-\beta$ simultaneously, in finite samples and for any $\beta\in(0,1)$; we use $\beta=2\alpha$. The rule is conservative: the size-optimal set under both constraints lowers the stratum thresholds only where a floor binds and would raise the common threshold to restore exact marginal coverage.

*Hull variant (SDLC-hull).* When an interval is required, the convex hull of $\hat C(x)$ is reported. It contains $\hat C(x)$ and therefore inherits (5); the upper bound of Theorem 1 and the optimality of Theorem 2 do not carry over, and when some $\hat q_k=+\infty$ the hull spans most of $D$.


# 5. Experimental design

The study was designed to answer five research questions (RQs), each tied to one experiment. All design choices below were fixed in a configuration file before the full benchmark was run (Section 5.7).

* **RQ1 (tail coverage).** Do marginal and covariate-adaptive conformal methods under-cover rare target strata on real data, and does stratified calibration restore stratum-wise coverage? *Experiment 1: main benchmark.*
* **RQ2 (price).** How much larger are the sets when stratum-wise validity is required? *Experiment 2: paired comparison of each score under marginal vs. stratified calibration (ablation of the calibration component).*
* **RQ3 (score).** Does the density-level score suggested by Theorem 2 give smaller stratified sets than residual, normalised-residual, quantile and HPD scores? *Experiment 3: score ablation on real data and a synthetic study with known density.*
* **RQ4 (shift).** How robust is stratum-wise coverage when the target distribution shifts? Corollary 1 guarantees exactness only for shifts that re-weight whole strata; the experiment uses continuous tilts that also re-weight *within* strata, so it is an empirical robustness test. *Experiment 4: importance-weighted evaluation under target tilting.*
* **RQ5 (robustness).** How sensitive are the conclusions to the miscoverage level, the number of strata, the calibration-set size, the density estimator and the base learner? *Experiment 5: sensitivity analyses.* Computational cost and an error analysis complete the evaluation.

## 5.1 Datasets

We use the OpenML-CTR23 suite, a curated benchmark of 35 tabular regression datasets with 500–100,000 observations, independent observations and documented provenance [@fischer2023openml]. Using a complete, externally curated suite avoids selecting datasets that favour the proposed method. We excluded, by a rule fixed in advance, the four datasets whose target takes fewer than 20 distinct values (red and white wine quality, solar flares, student performance): their outcomes are ordinal counts for which Lebesgue set size is not meaningful. The remaining 31 datasets (Table 2) range from 517 to 72,000 observations and from 5 to 971 features after one-hot encoding; 15 have a target skewness above 1 in absolute value. Datasets were downloaded programmatically from OpenML; categorical features were one-hot encoded and missing values were passed to the gradient-boosting models, which handle them natively.

## 5.2 Splitting, leakage control and repetitions

Each of the 10 predefined seeds (0–9, fixed before any result was seen) defines a random partition into proper training (50%), calibration (25%) and test (25%) sets. Every model, every stratum boundary, every density grid and every hyper-parameter decision uses the proper training set only; early stopping uses a 10% internal validation split of the proper training set. Calibration and test data are never used for fitting. The datasets in the suite were curated to contain independent observations [@fischer2023openml], so random splitting is the appropriate protocol; no dataset contains repeated measurements of the same subject or temporal structure that would require group or temporal splitting. Three small datasets (airfoil, concrete, QSAR fish toxicity) were used during development to choose the density estimator; all confirmatory statistics are also reported with these *development datasets* removed.

## 5.3 Base learners

All methods share the same LightGBM models [@ke2017lightgbm] with a single fixed configuration (learning rate 0.05, 31 leaves, minimum 20 samples per leaf, row and column subsampling 0.8, $\ell_2$ penalty 1, up to 2000 rounds with early stopping after 50 rounds): a mean model $\hat\mu$, quantile models at $\alpha/2$ and $1-\alpha/2$ (for CQR), a scale model $\hat\sigma$ fitted on three-fold out-of-fold absolute residuals, and a multiclass model over 40 equal-mass target bins (histogram density). No method receives method-specific tuning, so differences between methods reflect the conformal procedures and not the base learners. A second learner family (a two-layer perceptron) is used in the robustness analysis.

## 5.4 Compared methods

*Marginal or covariate-adaptive calibration (baselines).* Split conformal prediction with absolute residuals (SCP) [@papadopoulos2002inductive; @lei2018distribution]; normalised (locally weighted) conformal prediction (NCP) [@lei2018distribution]; conformalised quantile regression (CQR) [@romano2019conformalized]; Mondrian conformal regression with five equal-mass bins of the point prediction (Mondrian-ŷ), in the spirit of @bostrom2020mondrian and @boruah2026distribution; distributional conformal prediction (DCP) [@chernozhukov2021distributional]; HPD-split [@izbicki2022cdsplit]; and density level sets with a single threshold on the conditional density (DLS) [cf. @lei2013distribution; @izbicki2020flexible]. DCP, HPD-split and DLS use the same location–scale density as SDLC, so the comparison with SDLC isolates the calibration rule.

*Stratified calibration.* BCCP [@randahl2026bin], i.e. the absolute-residual score with stratum-wise thresholds, in its union form and its hull ("contiguized") form (BCCP-hull); the normalised-residual score with stratum-wise thresholds (S-NCP); the CQR score with stratum-wise thresholds (S-CQR), which with decile strata is a single-group, BFQR-style analogue of the binned fair quantile regression of @wang2023equal (strata from training-target deciles rather than calibration-set bins); the HPD score with stratum-wise thresholds (S-HPD); and the proposed SDLC with its floor ($\beta=2\alpha$) and hull variants.

*Density estimators.* The primary estimator is the location–scale density (7). Two alternatives are reported as secondary results: the multiclass histogram density, and an exploratory two-piece location–scale density that allows the scale to differ below and above $\hat\mu(x)$ (separate gradient-boosted scale models for negative and positive out-of-fold residuals), which can represent covariate-dependent skewness.

*Implementation.* For all location–scale-family methods (DLS, DCP, HPD-split, S-HPD, SDLC and variants) scores are evaluated exactly at the observed targets and sets are constructed on a per-$x$ grid $y=\hat\mu(x)+\hat\sigma(x)z$ of 2048 standardised points, i.e. at a resolution relative to the conditional scale (Section 4.4). Histogram-density methods are evaluated on the grid of the histogram itself. All methods are fitted once per dataset and seed; model outputs are cached and every method is evaluated from the same cached outputs.

## 5.5 Evaluation metrics

For each test set we report marginal coverage; stratum-wise coverage (1) in each of the $K$ calibration strata; coverage in the training-target deciles and in the top and bottom 5% (strata *not* used for calibration, to test whether protection extends beyond the calibrated strata); mean set size divided by the training-target standard deviation (normalised size); the mean number of disjoint intervals per set; and worst-slab coverage (WSC) [@cauchois2021knowing] as a diagnostic of covariate-conditional coverage (slab selected on one half of the test set and evaluated on the other half, $\delta=0.1$). Stratum coverages are averaged over seeds before taking the minimum across strata ("worst-stratum coverage"). This reduces, but does not remove, the downward bias of a minimum over noisy estimates [cf. @boruah2026null]; we therefore also report a *null reference*, the worst-stratum coverage expected under exact conformal validity given the realised calibration and test stratum sizes (Monte Carlo over the Beta–binomial law of split-conformal coverage). Computing time is recorded for every fit and for calibration plus prediction.

## 5.6 Statistical analysis

Following @demsar2006statistical, the unit of analysis is the dataset: metrics are averaged over seeds within each dataset and methods are compared across datasets. Paired comparisons use the Wilcoxon signed-rank test (no normality assumption; differences are paired by dataset), with Holm's step-down correction within each family of comparisons [@holm1979simple]. We report the median paired difference with a 95% bootstrap confidence interval (10,000 resamples of datasets) and the matched-pairs rank-biserial correlation as effect size. One-sided alternatives are used only for the pre-specified directional hypotheses of RQ1 and RQ4 (stratified calibration improves worst-stratum coverage); RQ3 uses two-sided tests. Multi-method rankings use the Friedman test with the Nemenyi critical difference [@demsar2006statistical]; because mean-rank post-hoc comparisons depend on which other methods are included [@benavoli2016should], all confirmatory pairwise conclusions rest on the Holm-corrected Wilcoxon tests and the rankings are descriptive. Size ratios are summarised by geometric means with bootstrap confidence intervals.

## 5.7 Pre-registration and deviations

The configuration (datasets, exclusion rule, seeds, split proportions, miscoverage levels $\alpha\in\{0.05,0.1,0.2\}$, strata, grid sizes, base learners, the original method list and sensitivity analyses), the primary method (SDLC with the location–scale density) and the hypotheses for RQ1–RQ5 were fixed in a configuration file before the benchmark was run. Four deviations occurred and are reported transparently; the original (pre-registered) run is archived with the code.

1. *Data loading.* An audit found that two string-typed features of two datasets (forest fires; FPS benchmark) had been parsed as missing values; the loader was corrected and both datasets were recomputed for all seeds. For the smallest dataset the stratified internal validation split of the histogram classifier failed; it was replaced by an unstratified split.
2. *Additional comparators.* After the run we learned of BCCP [@randahl2026bin] and BFQR [@wang2023equal]. BCCP (union) was already part of the design as the residual-score stratified method; its hull form and the decile-stratified variants (BFQR-style) were added, together with tail-alert metrics.
3. *Exact implementation.* The pre-registered implementation evaluated all density-based sets on a fixed grid of 200 equal-mass cells of the *marginal* training-target distribution. Diagnostics showed that this grid inflates set sizes whenever the *conditional* density is narrower than a cell (high-$R^2$ datasets) and when targets have many ties, for baselines and proposed method alike. All location–scale-family methods are therefore reported with the exact implementation described above. Pre-registered grid-based results are given in the supplementary material; the conclusions on coverage (RQ1) are identical, and the comparison of scores (RQ3) is affected as discussed in Section 6.
4. *Exploratory density.* The two-piece location–scale density was added after the pre-registered run; it is labelled exploratory throughout and never replaces the primary method.


# 6. Results

All 310 runs (31 datasets × 10 splits) completed. The fraction of test targets outside the bounded domain $D$ was at most 0.38% for any dataset (mean 0.0%), so the domain restriction is immaterial. Infinite stratum thresholds ($n_k<1/\alpha-1$, Eq. 3) occurred in 2 of the 310 runs at $\alpha=0.1$, in 32 runs (7 small datasets) at $\alpha=0.05$ and never at $\alpha=0.2$. Table 2 summarises the datasets and Table 3 the main results at $\alpha=0.1$.

**Table 2.** Datasets (OpenML-CTR23, 31 datasets after the pre-registered exclusion rule): number of observations $n$, number of features $p$ after one-hot encoding, skewness of the target, mean calibration-set size, realised number of strata $K$ (median over splits; tied targets merge cut points) and test RMSE of the mean model relative to the target standard deviation.

| Dataset                       | n      | p   | Skewness of y   | Calibration size   | K   | RMSE / sd(y)   |
|:------------------------------|:-------|:----|:----------------|:-------------------|:----|:---------------|
| forest_fires                  | 517    | 31  | 12.81           | 129                | 3   | 0.78           |
| energy_efficiency             | 768    | 8   | 0.36            | 192                | 5   | 0.08           |
| cars                          | 804    | 17  | 1.57            | 201                | 5   | 0.28           |
| QSAR_fish_toxicity            | 908    | 6   | 0.25            | 227                | 5   | 0.63           |
| concrete_compressive_strength | 1,030  | 8   | 0.42            | 258                | 5   | 0.29           |
| geographical_origin_of_music  | 1,059  | 116 | -0.99           | 265                | 5   | 0.88           |
| socmob                        | 1,156  | 43  | 4.43            | 289                | 4   | 0.49           |
| Moneyball                     | 1,232  | 78  | 0.17            | 308                | 5   | 0.27           |
| airfoil_self_noise            | 1,503  | 5   | -0.42           | 376                | 5   | 0.29           |
| auction_verification          | 2,043  | 18  | 1.50            | 511                | 5   | 0.17           |
| space_ga                      | 3,107  | 6   | -1.02           | 777                | 5   | 0.59           |
| abalone                       | 4,177  | 11  | 1.11            | 1,044              | 5   | 0.67           |
| cpu_activity                  | 8,192  | 21  | -3.42           | 2,048              | 5   | 0.13           |
| pumadyn32nh                   | 8,192  | 32  | -0.05           | 2,048              | 5   | 0.61           |
| kin8nm                        | 8,192  | 8   | 0.09            | 2,048              | 5   | 0.47           |
| grid_stability                | 10,000 | 12  | 0.02            | 2,500              | 5   | 0.22           |
| brazilian_houses              | 10,692 | 53  | 58.95           | 2,673              | 5   | 1.00           |
| naval_propulsion_plant        | 11,934 | 14  | -0.00           | 2,984              | 5   | 0.06           |
| miami_housing                 | 13,932 | 15  | 3.22            | 3,483              | 5   | 0.29           |
| fifa                          | 19,178 | 191 | 6.47            | 4,794              | 4   | 0.48           |
| california_housing            | 20,640 | 8   | 0.98            | 5,160              | 5   | 0.41           |
| superconductivity             | 21,263 | 81  | 0.86            | 5,316              | 5   | 0.29           |
| kings_county                  | 21,613 | 136 | 4.02            | 5,403              | 5   | 0.33           |
| health_insurance              | 22,272 | 32  | -0.34           | 5,568              | 2   | 0.78           |
| fps_benchmark                 | 24,624 | 971 | 1.05            | 6,156              | 5   | 0.02           |
| cps88wages                    | 28,155 | 16  | 6.50            | 7,039              | 5   | 0.83           |
| physiochemical_protein        | 45,730 | 9   | 0.57            | 11,432             | 5   | 0.61           |
| sarcos                        | 48,933 | 21  | 0.15            | 12,233             | 5   | 0.13           |
| diamonds                      | 53,940 | 29  | 1.62            | 13,485             | 5   | 0.14           |
| video_transcoding             | 68,784 | 26  | 4.25            | 17,196             | 5   | 0.07           |
| wave_energy                   | 72,000 | 36  | 0.14            | 18,000             | 5   | 0.40           |


**Table 3.** Main results at $\alpha=0.1$ (means over 31 datasets of per-dataset means over 10 splits). Lower/upper tail: coverage in the lowest/highest calibration stratum; worst stratum: minimum over strata of the split-averaged stratum coverage; top-5%: coverage of test targets above the 95% training quantile (not a calibration stratum); size: set size divided by the training-target standard deviation; pieces: mean number of disjoint intervals; WSC: worst-slab coverage. The null reference for the worst stratum under exact validity is 0.893.

| Method          | Marginal cov.   | Lower-tail cov.   | Upper-tail cov.   | Worst stratum   | Top-5% cov.   | Size (median)   | Size (mean)   | Pieces   | WSC   |
|:----------------|:----------------|:------------------|:------------------|:----------------|:--------------|:----------------|:--------------|:---------|:------|
| SCP             | 0.903           | 0.865             | 0.690             | 0.630           | 0.598         | 0.921           | 1.081         | 1.000    | 0.768 |
| NCP             | 0.903           | 0.854             | 0.812             | 0.765           | 0.757         | 0.934           | 1.063         | 1.000    | 0.872 |
| CQR             | 0.903           | 0.808             | 0.759             | 0.720           | 0.671         | 1.013           | 1.182         | 1.000    | 0.867 |
| Mondrian-ŷ      | 0.905           | 0.827             | 0.811             | 0.770           | 0.735         | 0.946           | 1.086         | 1.000    | 0.834 |
| DCP             | 0.902           | 0.852             | 0.819             | 0.780           | 0.765         | 0.941           | 1.073         | 1.000    | 0.872 |
| HPD-split       | 0.903           | 0.857             | 0.811             | 0.766           | 0.757         | 0.947           | 1.109         | 1.119    | 0.872 |
| DLS             | 0.903           | 0.860             | 0.735             | 0.681           | 0.640         | 0.933           | 1.028         | 1.138    | 0.815 |
| BCCP            | 0.905           | 0.906             | 0.908             | 0.890           | 0.863         | 1.037           | 1.509         | 1.466    | 0.829 |
| BCCP-hull       | 0.916           | 0.908             | 0.908             | 0.895           | 0.863         | 1.099           | 1.638         | 1.000    | 0.838 |
| S-NCP           | 0.905           | 0.906             | 0.907             | 0.891           | 0.880         | 1.044           | 1.369         | 1.290    | 0.886 |
| S-CQR           | 0.908           | 0.907             | 0.907             | 0.893           | 0.854         | 1.155           | 1.532         | 1.494    | 0.874 |
| S-HPD           | 0.904           | 0.907             | 0.908             | 0.893           | 0.881         | 1.029           | 1.541         | 1.494    | 0.884 |
| SDLC (proposed) | 0.904           | 0.903             | 0.909             | 0.891           | 0.874         | 0.976           | 1.518         | 1.480    | 0.857 |
| SDLC-floor      | 0.918           | 0.892             | 0.852             | 0.823           | 0.789         | 0.933           | 1.271         | 1.304    | 0.864 |
| SDLC-hull       | 0.920           | 0.910             | 0.912             | 0.900           | 0.877         | 1.043           | 1.703         | 0.997    | 0.871 |


## 6.1 RQ1: Marginal and covariate-adaptive methods under-cover rare targets

All methods attained their nominal marginal coverage (Table 3). Coverage in the target strata, however, differed sharply. The seven marginal or covariate-adaptive methods covered between 69.0% and 81.9% of the upper-tail targets (the top 10% of the training distribution) and their worst-stratum coverage ranged from 63.0% to 78.0%; split conformal prediction with absolute residuals covered only 69.0% of the upper tail, and CQR only 75.9%. Fig. 1 shows the mechanism: marginal methods over-cover the central deciles and pay for it in the outer ones, exactly the pattern predicted by Proposition 1. Every stratified method, in contrast, covered 90.7%–90.9% of the upper tail, with worst-stratum coverage between 89.0% and 89.3%.

![**Fig. 1.** Coverage by decile of the training-target distribution, averaged over 31 datasets ($\alpha=0.1$). Marginal methods over-cover the bulk and under-cover both tails; stratified methods stay close to $1-\alpha$ in every decile.](/home/user/p_c1_2/Target_Journal_Submission/figures/F3_decile_coverage_profile.png){width=100%}


The improvement is consistent across datasets (Fig. 2). SDLC had a higher worst-stratum coverage than every marginal or covariate-adaptive baseline on at least 30/31 datasets (Holm-adjusted Wilcoxon $p$ < 0.001 for all seven comparisons; median gains 0.047–0.221; rank-biserial correlation $\ge$1.00; Table 5), and the same held after removing the three development datasets (28 datasets; all Holm-adjusted $p$ < 0.001). For the upper tail alone the gains were also significant for every comparison, with SDLC better than SCP on 26/31 datasets and better than CQR on 30/31.

![**Fig. 2.** Coverage of the upper-tail stratum (top 10% of training targets) for each dataset, averaged over splits ($\alpha=0.1$). The vertical line marks $1-\alpha$.](/home/user/p_c1_2/Target_Journal_Submission/figures/F4_upper_tail_per_dataset.png){width=100%}


Are the stratified methods' worst-stratum values of about 0.891, slightly below 0.90, a sign of invalidity? No: the minimum over strata of finite-sample coverages is biased downwards even when every stratum is exactly valid. Under exact split-conformal validity, given the realised stratum sizes, the expected worst-stratum coverage is 0.893 on average. SDLC fell below the 5% quantile of this null distribution on 1 of 31 datasets and BCCP on 2, close to the $\approx 1.5$ expected by chance, whereas the marginal methods fell below it on 27–30 datasets. Fig. 7 (right) shows the deviation from the null mean against calibration size.

Protection extends beyond the calibrated strata only partly. For the top 5% of targets, which lie inside the upper calibration stratum, SDLC covered 87.4%, against 59.8%–76.5% for the marginal methods. At the resolution of deciles, which cut across the calibration strata, SDLC dipped slightly below the nominal level in deciles 7–9 (Fig. 1): the guarantee is per calibrated stratum, not per arbitrary sub-range, a point we return to in Section 6.6.

## 6.2 RQ2: The price of stratum-wise validity

Stratum-wise validity is not free. Relative to the same score with a single marginal threshold, stratified calibration increased the set size by a geometric mean of 1.24 [1.12, 1.43] for the density score and between 1.16 and 1.23 for the other scores (Table 4); the median increase was smaller (1.05–1.14), because a few datasets carry most of the cost. In exchange, worst-stratum coverage rose by 0.126–0.260 on average. Fig. 3 places all methods on this coverage–size plane. The floor variant sits in between: with $\beta=2\alpha$ it kept marginal coverage at 0.918 and guaranteed at least $1-\beta=0.8$ in every stratum (observed worst stratum 0.823, upper tail 0.852) at a median size of 0.933, against 0.976 for SDLC and 0.933 for the marginal density level set.

**Table 4.** Price of stratum-wise validity ($\alpha=0.1$): ratio of the mean set size of each stratified method to that of the same score with a single marginal threshold (geometric mean over datasets with 95% bootstrap confidence interval; median ratio; number of datasets with ratio $>1.5$) and the corresponding mean gain in worst-stratum coverage.

| Marginal method   | Stratified counterpart   | Size ratio (geo. mean)   | 95% CI low   | 95% CI high   | Median ratio   | Gain in worst-stratum cov.   | Datasets with ratio > 1.5   |
|:------------------|:-------------------------|:-------------------------|:-------------|:--------------|:---------------|:-----------------------------|:----------------------------|
| SCP               | BCCP                     | 1.23                     | 1.09         | 1.44          | 1.10           | 0.260                        | 4                           |
| NCP               | S-NCP                    | 1.16                     | 1.05         | 1.33          | 1.05           | 0.126                        | 1                           |
| CQR               | S-CQR                    | 1.19                     | 1.08         | 1.35          | 1.08           | 0.173                        | 2                           |
| HPD-split         | S-HPD                    | 1.19                     | 1.08         | 1.33          | 1.06           | 0.127                        | 3                           |
| DLS               | SDLC (proposed)          | 1.24                     | 1.12         | 1.43          | 1.14           | 0.210                        | 2                           |
| DLS-2p            | SDLC-2p                  | 1.26                     | 1.13         | 1.48          | 1.14           | 0.202                        | 4                           |
| DLS (hist.)       | SDLC (hist.)             | 1.51                     | 1.27         | 1.84          | 1.24           | 0.259                        | 9                           |


![**Fig. 3.** Coverage–size trade-off at $\alpha=0.1$: worst-stratum coverage (mean over datasets) against normalised set size (geometric mean). Grey: marginal or covariate-adaptive; green: stratified baselines; blue: SDLC; orange: SDLC variants.](/home/user/p_c1_2/Target_Journal_Submission/figures/F2_coverage_size_tradeoff.png){width=100%}


## 6.3 RQ3: Which score should be stratified?

Theorem 2 predicts that, among stratum-valid sets, density level sets are the smallest. Among the pre-registered stratified procedures, SDLC produced the smallest sets in median (Table 3): its sets were smaller than those of BCCP on 22 of 31 datasets (geometric-mean ratio 0.932, 95% CI [0.862, 1.003]; Holm-adjusted $p$ = 0.017), smaller than those of the BFQR-style S-CQR on 26 (ratio 0.833; $p$ = 0.004) and smaller than those of S-HPD on 30 (ratio 0.949; $p$ < 0.001); when intervals are required, SDLC-hull was smaller than BCCP-hull on 22 datasets (ratio 0.930; $p$ = 0.013). The comparison with the normalised-residual score is more nuanced. SDLC was smaller than S-NCP on 24 datasets ($p$ = 0.035), but the geometric-mean ratio was 1.004 (0.963–1.059), because on a few datasets SDLC was considerably larger (Section 6.8): SDLC is typically, not uniformly, more efficient than S-NCP. All stratified methods had statistically indistinguishable worst-stratum coverage (all Holm-adjusted $p$ = 1.000), so the size differences are not bought with coverage.

**Table 5.** Paired Wilcoxon signed-rank tests across datasets ($\alpha=0.1$; unit of analysis: dataset). H1: one-sided, SDLC better than each marginal or covariate-adaptive method; H3: two-sided comparisons of SDLC with the other stratified methods on log set size and worst-stratum coverage. Median paired difference with 95% bootstrap CI, matched-pairs rank-biserial correlation $r_{rb}$, wins (W) and losses (L) of SDLC, Holm-adjusted $p$ within each family.

| H   | Metric        | Comparison           | Median diff.   | 95% CI low   | 95% CI high   | r_rb   | W   | L   | p (Holm)   |
|:----|:--------------|:---------------------|:---------------|:-------------|:--------------|:-------|:----|:----|:-----------|
| H1  | worst_stratum | SDLC vs SCP          | 0.221          | 0.187        | 0.389         | 1.00   | 31  | 0   | < 0.001    |
| H1  | worst_stratum | SDLC vs NCP          | 0.048          | 0.028        | 0.150         | 1.00   | 30  | 1   | < 0.001    |
| H1  | worst_stratum | SDLC vs CQR          | 0.142          | 0.066        | 0.215         | 1.00   | 31  | 0   | < 0.001    |
| H1  | worst_stratum | SDLC vs Mondrian-ŷ   | 0.083          | 0.053        | 0.141         | 1.00   | 30  | 1   | < 0.001    |
| H1  | worst_stratum | SDLC vs DCP          | 0.049          | 0.030        | 0.127         | 1.00   | 30  | 1   | < 0.001    |
| H1  | worst_stratum | SDLC vs HPD-split    | 0.047          | 0.028        | 0.151         | 1.00   | 30  | 1   | < 0.001    |
| H1  | worst_stratum | SDLC vs DLS          | 0.179          | 0.142        | 0.238         | 1.00   | 31  | 0   | < 0.001    |
| H1  | upper_tail    | SDLC vs SCP          | 0.204          | 0.085        | 0.272         | 0.90   | 26  | 5   | < 0.001    |
| H1  | upper_tail    | SDLC vs NCP          | 0.044          | 0.020        | 0.107         | 0.71   | 23  | 8   | < 0.001    |
| H1  | upper_tail    | SDLC vs CQR          | 0.132          | 0.077        | 0.187         | 0.98   | 30  | 1   | < 0.001    |
| H1  | upper_tail    | SDLC vs Mondrian-ŷ   | 0.060          | 0.043        | 0.101         | 0.97   | 29  | 2   | < 0.001    |
| H1  | upper_tail    | SDLC vs DCP          | 0.053          | 0.026        | 0.102         | 0.77   | 24  | 7   | < 0.001    |
| H1  | upper_tail    | SDLC vs HPD-split    | 0.051          | 0.014        | 0.100         | 0.73   | 23  | 8   | < 0.001    |
| H1  | upper_tail    | SDLC vs DLS          | 0.087          | 0.044        | 0.202         | 0.87   | 27  | 4   | < 0.001    |
| H3  | log_size      | SDLC vs BCCP         | -0.042         | -0.100       | -0.015        | -0.56  | 9   | 22  | 0.017      |
| H3  | log_size      | SDLC vs S-NCP        | -0.030         | -0.049       | -0.011        | -0.48  | 7   | 24  | 0.035      |
| H3  | log_size      | SDLC vs S-CQR        | -0.121         | -0.219       | -0.089        | -0.65  | 5   | 26  | 0.004      |
| H3  | log_size      | SDLC vs S-HPD        | -0.047         | -0.064       | -0.030        | -0.89  | 1   | 30  | < 0.001    |
| H3  | log_size      | SDLC vs SDLC-2p      | -0.005         | -0.018       | 0.004         | -0.16  | 13  | 18  | 0.456      |
| H3  | log_size      | SDLC vs SDLC (hist.) | -0.519         | -0.669       | -0.343        | -0.90  | 3   | 28  | < 0.001    |
| H3  | worst_stratum | SDLC vs BCCP         | 0.000          | -0.001       | 0.003         | 0.17   | 17  | 14  | 1.000      |
| H3  | worst_stratum | SDLC vs S-NCP        | -0.000         | -0.002       | 0.001         | -0.11  | 15  | 16  | 1.000      |
| H3  | worst_stratum | SDLC vs S-CQR        | 0.001          | -0.003       | 0.002         | -0.15  | 16  | 15  | 1.000      |
| H3  | worst_stratum | SDLC vs S-HPD        | -0.000         | -0.001       | 0.001         | -0.11  | 15  | 16  | 1.000      |
| H3  | worst_stratum | SDLC vs SDLC-2p      | 0.001          | -0.002       | 0.003         | 0.11   | 18  | 13  | 1.000      |
| H3  | worst_stratum | SDLC vs SDLC (hist.) | 0.001          | -0.003       | 0.004         | -0.02  | 16  | 15  | 1.000      |


The synthetic study isolates the role of the density estimate (Table 6). With the true density, oracle SDLC gave the smallest stratum-valid sets in 10 of 10 repetitions (mean size 1.762, against 1.820 for the oracle HPD score, 1.839 for the oracle normalised residual and 2.132 for the oracle residual), as Theorem 2 predicts, while the exactly covariate-conditional oracle interval covered only 69.4% of the upper stratum, as Proposition 1 predicts for a skewed, heteroscedastic model. With estimated models, SDLC was smaller than BCCP in 10 and smaller than S-NCP in 9 of the 10 repetitions.

**Table 6.** Synthetic study with known conditional density ($Y=\mu(X)+\sigma(X)\varepsilon$, standardised Gamma(2) noise, $n_{\mathrm{train}}=n_{\mathrm{cal}}=5000$, 20,000 test points, 10 repetitions, $\alpha=0.1$). Oracle rows use the true $\mu$, $\sigma$ and density; estimated rows use the benchmark pipeline.

| Scores    | Method                        | Marginal cov.   | Lower-tail cov.   | Upper-tail cov.   | Worst stratum   | Mean size   | Pieces   |
|:----------|:------------------------------|:----------------|:------------------|:------------------|:----------------|:------------|:---------|
| estimated | DLS-M-LS                      | 0.900           | 0.951             | 0.696             | 0.696           | 1.810       | 1.000    |
| estimated | DLS-M-LS2                     | 0.900           | 0.953             | 0.712             | 0.712           | 1.832       | 1.000    |
| estimated | HPD-split-LS                  | 0.900           | 0.952             | 0.703             | 0.703           | 1.854       | 1.000    |
| estimated | NCP                           | 0.900           | 0.961             | 0.694             | 0.694           | 1.854       | 1.000    |
| estimated | HPD-split-LS2                 | 0.901           | 0.948             | 0.736             | 0.736           | 1.878       | 1.000    |
| estimated | SDLC-LS-floor                 | 0.912           | 0.951             | 0.808             | 0.808           | 1.911       | 1.068    |
| estimated | SDLC-LS2-floor                | 0.910           | 0.953             | 0.805             | 0.805           | 1.923       | 1.059    |
| estimated | DCP-LS                        | 0.900           | 0.900             | 0.759             | 0.759           | 1.928       | 1.000    |
| estimated | DCP-LS2                       | 0.900           | 0.910             | 0.783             | 0.783           | 1.980       | 1.000    |
| estimated | SDLC-LS                       | 0.901           | 0.895             | 0.906             | 0.895           | 2.003       | 1.222    |
| estimated | SCP                           | 0.901           | 0.925             | 0.715             | 0.715           | 2.006       | 1.000    |
| estimated | MCP-yhat                      | 0.901           | 0.922             | 0.719             | 0.719           | 2.008       | 1.000    |
| estimated | SDLC-LS2                      | 0.901           | 0.899             | 0.905             | 0.899           | 2.015       | 1.208    |
| estimated | S-HPD-LS                      | 0.900           | 0.895             | 0.908             | 0.895           | 2.047       | 1.211    |
| estimated | S-NCP                         | 0.899           | 0.894             | 0.908             | 0.894           | 2.051       | 1.195    |
| estimated | S-HPD-LS2                     | 0.901           | 0.899             | 0.903             | 0.899           | 2.054       | 1.180    |
| estimated | SDLC-LS2-hull                 | 0.908           | 0.901             | 0.905             | 0.901           | 2.087       | 1.000    |
| estimated | SDLC-LS-hull                  | 0.909           | 0.896             | 0.907             | 0.896           | 2.090       | 1.000    |
| estimated | CQR                           | 0.899           | 0.830             | 0.700             | 0.700           | 2.116       | 1.000    |
| estimated | S-Res                         | 0.903           | 0.897             | 0.908             | 0.897           | 2.228       | 1.236    |
| estimated | S-CQR                         | 0.901           | 0.899             | 0.909             | 0.899           | 2.299       | 1.267    |
| estimated | S-Res-hull                    | 0.910           | 0.897             | 0.908             | 0.897           | 2.324       | 1.000    |
| estimated | DCP-H                         | 0.902           | 0.725             | 0.643             | 0.643           | 2.833       | 1.000    |
| estimated | DLS-M-H                       | 0.901           | 0.856             | 0.654             | 0.654           | 2.971       | 3.092    |
| estimated | HPD-split-H                   | 0.901           | 0.879             | 0.691             | 0.691           | 3.138       | 3.722    |
| estimated | SDLC-H-floor                  | 0.915           | 0.856             | 0.798             | 0.798           | 3.181       | 3.204    |
| estimated | SDLC-H                        | 0.903           | 0.903             | 0.903             | 0.900           | 3.476       | 3.807    |
| estimated | S-HPD-H                       | 0.903           | 0.901             | 0.906             | 0.900           | 3.844       | 4.485    |
| estimated | SDLC-H-hull                   | 0.974           | 0.917             | 0.905             | 0.905           | 4.559       | 1.000    |
| oracle    | O-DLS-M                       | 0.899           | 0.985             | 0.679             | 0.679           | 1.584       | 1.000    |
| oracle    | O-HDR-X (exact X-conditional) | 0.899           | 0.984             | 0.694             | 0.694           | 1.632       | 1.000    |
| oracle    | O-SDLC                        | 0.898           | 0.889             | 0.906             | 0.889           | 1.762       | 1.235    |
| oracle    | O-S-HPD                       | 0.900           | 0.894             | 0.906             | 0.894           | 1.820       | 1.214    |
| oracle    | O-S-NCP                       | 0.899           | 0.889             | 0.906             | 0.889           | 1.839       | 1.169    |
| oracle    | O-S-Res                       | 0.902           | 0.894             | 0.908             | 0.894           | 2.132       | 1.224    |


The density estimate matters as much as the theory suggests. The fully nonparametric histogram density produced stratified sets about twice as large as the location–scale density (geometric-mean ratio of SDLC to its histogram version 0.517), and the exploratory two-piece density was statistically indistinguishable from the symmetric one (ratio 0.992, $p$ = 0.456; Table 7). The implementation also matters: with the pre-registered fixed-grid implementation, which discretised all density-based sets on a 200-cell grid of the marginal target distribution, SDLC was *not* smaller than BCCP (Holm-adjusted $p$ = 0.809; supplementary Table S3). Section 5.7 documents why that implementation was replaced; the coverage results (RQ1) were identical under both implementations.

**Table 7.** Secondary density estimators ($\alpha=0.1$): exploratory two-piece location–scale density (2p) and multiclass histogram density (hist.), each with marginal and stratified calibration.

| Method             | Marginal cov.   | Upper-tail cov.   | Worst stratum   | Size (median)   | Size (mean)   | Pieces   |
|:-------------------|:----------------|:------------------|:----------------|:----------------|:--------------|:---------|
| SDLC-2p            | 0.903           | 0.909             | 0.891           | 0.955           | 1.503         | 1.508    |
| SDLC-2p-floor      | 0.917           | 0.851             | 0.826           | 0.927           | 1.225         | 1.245    |
| SDLC-2p-hull       | 0.920           | 0.913             | 0.899           | 0.967           | 1.698         | 0.999    |
| DLS-2p             | 0.902           | 0.732             | 0.688           | 0.876           | 1.010         | 1.095    |
| HPD-split-2p       | 0.901           | 0.810             | 0.773           | 0.913           | 1.063         | 1.089    |
| DCP-2p             | 0.902           | 0.823             | 0.792           | 0.923           | 1.128         | 1.000    |
| S-HPD-2p           | 0.904           | 0.909             | 0.892           | 0.974           | 1.525         | 1.537    |
| SDLC (hist.)       | 0.904           | 0.909             | 0.893           | 1.818           | 2.414         | 3.658    |
| DLS (hist.)        | 0.903           | 0.679             | 0.633           | 1.299           | 1.404         | 2.731    |
| HPD-split (hist.)  | 0.902           | 0.742             | 0.719           | 1.594           | 1.710         | 3.270    |
| DCP (hist.)        | 0.903           | 0.740             | 0.677           | 1.441           | 1.564         | 1.000    |
| S-HPD (hist.)      | 0.904           | 0.910             | 0.893           | 2.125           | 5.040         | 4.246    |
| SDLC-floor (hist.) | 0.925           | 0.839             | 0.822           | 1.515           | 1.891         | 2.851    |
| SDLC-hull (hist.)  | 0.974           | 0.934             | 0.914           | 2.397           | 2.928         | 1.000    |


## 6.4 A decision view: tail alerts

A prediction set that reaches into the upper stratum can be read as an alert that the outcome may be extreme. By Theorem 1, the recall of such alerts, $P\{\hat C(X)\cap B_K\neq\emptyset\,|\, Y\in B_K\}\ge P\{Y\in\hat C(X)\,|\, Y\in B_K\}\ge 1-\alpha$, is guaranteed for stratified methods. Table 8 and Fig. 4 show the price in false alarms. BCCP raised an upper-tail alert for 47.1% of all test points, with precision 0.379; SDLC alerted for 38.4% with precision 0.439, at a recall of 0.978 versus 0.986. The density score thus concentrates the extra coverage on the observations for which an extreme outcome is plausible, whereas the residual score of BCCP extends the upper-tail piece to many observations whose point prediction is far from the tail. S-NCP behaved like SDLC (alert rate 36.6%).

**Table 8.** Tail alerts ($\alpha=0.1$): recall $P\{\hat C(X)\cap B\neq\emptyset\,|\, Y\in B\}$, alert rate $P\{\hat C(X)\cap B\neq\emptyset\}$ and precision $P\{Y\in B\,|\, \hat C(X)\cap B\neq\emptyset\}$ for the upper and lower calibration strata $B$ (means over datasets).

| Method          | Upper recall   | Upper alert rate   | Upper precision   | Lower recall   | Lower alert rate   | Lower precision   |
|:----------------|:---------------|:-------------------|:------------------|:---------------|:-------------------|:------------------|
| SCP             | 0.947          | 0.273              | 0.513             | 0.961          | 0.395              | 0.387             |
| NCP             | 0.954          | 0.281              | 0.497             | 0.963          | 0.358              | 0.423             |
| CQR             | 0.951          | 0.286              | 0.496             | 0.960          | 0.328              | 0.461             |
| Mondrian-ŷ      | 0.952          | 0.279              | 0.491             | 0.958          | 0.363              | 0.421             |
| DCP             | 0.956          | 0.280              | 0.494             | 0.962          | 0.350              | 0.427             |
| HPD-split       | 0.950          | 0.279              | 0.497             | 0.964          | 0.363              | 0.421             |
| DLS             | 0.910          | 0.268              | 0.505             | 0.960          | 0.367              | 0.413             |
| BCCP            | 0.986          | 0.471              | 0.379             | 0.975          | 0.402              | 0.404             |
| BCCP-hull       | 0.986          | 0.471              | 0.379             | 0.975          | 0.402              | 0.404             |
| S-NCP           | 0.984          | 0.366              | 0.448             | 0.981          | 0.413              | 0.395             |
| S-CQR           | 0.989          | 0.431              | 0.405             | 0.984          | 0.428              | 0.413             |
| S-HPD           | 0.984          | 0.378              | 0.448             | 0.983          | 0.427              | 0.387             |
| SDLC (proposed) | 0.978          | 0.384              | 0.439             | 0.978          | 0.411              | 0.396             |
| SDLC-floor      | 0.963          | 0.331              | 0.471             | 0.976          | 0.392              | 0.403             |
| SDLC-hull       | 0.978          | 0.384              | 0.439             | 0.978          | 0.411              | 0.396             |
| SDLC-2p         | 0.984          | 0.387              | 0.435             | 0.979          | 0.406              | 0.398             |
| SDLC (hist.)    | 0.992          | 0.576              | 0.296             | 0.992          | 0.644              | 0.276             |


![**Fig. 4.** Upper-tail alerts: recall against precision (means over datasets, $\alpha=0.1$). Points with identical values are labelled jointly.](/home/user/p_c1_2/Target_Journal_Submission/figures/F10_tail_alerts.png){width=100%}


## 6.5 RQ4: Robustness to target shift

Table 9 and Fig. 5 report coverage when the test distribution is tilted towards the upper tail, towards both tails or towards the lower tail by importance weights $\exp(\gamma z)$, where $z$ is the normal score of the target under the training distribution. These tilts also re-weight targets *within* strata, so Corollary 1(i) does not apply exactly. Under a moderate upward tilt ($\gamma=1$) the stratified methods kept coverage between 88.2% and 89.4%, whereas the marginal methods dropped to 80.7%–86.2%. Under a strong upward tilt ($\gamma=2$) all methods lost coverage, but the stratified methods much less: SDLC retained 82.6% and S-NCP 84.7%, against 63.7% for SCP and 66.8% for CQR (one-sided Holm-adjusted $p$ for SDLC versus each marginal method at most 0.011). The residual loss is the within-stratum effect described after Corollary 1: a strong tilt moves mass towards the outer end of the upper stratum, where every set is less likely to reach. The density score is somewhat more exposed to this effect than the normalised residual, because it spends less coverage on the most extreme part of a tail stratum.

**Table 9.** Coverage under target tilting (means over datasets and, for $\gamma=2$, the worst dataset). Importance weights $\exp(\gamma z)$ (upper tilt), $\exp(\gamma|z|)$ (two-tail) or $\exp(-\gamma z)$ (lower tilt), with $z$ the normal score of $y$ under the training distribution.

| Method          | Lower tilt γ=1   | Two-tail tilt γ=1   | Upper tilt γ=1   | Upper tilt γ=2   | Upper γ=2 (worst dataset)   |
|:----------------|:-----------------|:--------------------|:-----------------|:-----------------|:----------------------------|
| SCP             | 0.899            | 0.832               | 0.807            | 0.637            | 0.326                       |
| NCP             | 0.884            | 0.858               | 0.859            | 0.766            | 0.365                       |
| CQR             | 0.869            | 0.829               | 0.830            | 0.668            | 0.431                       |
| Mondrian-ŷ      | 0.873            | 0.848               | 0.853            | 0.717            | 0.384                       |
| DCP             | 0.881            | 0.859               | 0.862            | 0.770            | 0.415                       |
| HPD-split       | 0.885            | 0.859               | 0.859            | 0.766            | 0.350                       |
| DLS             | 0.892            | 0.839               | 0.823            | 0.668            | 0.324                       |
| BCCP            | 0.897            | 0.885               | 0.882            | 0.803            | 0.587                       |
| BCCP-hull       | 0.906            | 0.896               | 0.894            | 0.809            | 0.603                       |
| S-NCP           | 0.897            | 0.892               | 0.893            | 0.847            | 0.624                       |
| S-CQR           | 0.897            | 0.885               | 0.884            | 0.798            | 0.601                       |
| S-HPD           | 0.897            | 0.891               | 0.892            | 0.846            | 0.617                       |
| SDLC (proposed) | 0.896            | 0.888               | 0.888            | 0.826            | 0.614                       |
| SDLC-floor      | 0.906            | 0.877               | 0.870            | 0.754            | 0.498                       |


![**Fig. 5.** Coverage under target tilting, means over datasets ($\alpha=0.1$).](/home/user/p_c1_2/Target_Journal_Submission/figures/F6_label_shift.png){width=100%}


## 6.6 RQ5: Sensitivity analyses

*Miscoverage level.* The conclusions held at $\alpha=0.05$ and $\alpha=0.2$ (Table 10). At $\alpha=0.05$ the marginal methods' worst-stratum coverage ranged from 0.772 to 0.878 against 0.947 for SDLC; the price of stratification increased because rare strata contain few calibration points, and S-NCP was then smaller than SDLC (normalised size 1.299 versus 1.364). At $\alpha=0.2$ SDLC gave the smallest stratified sets (0.631 versus 0.652 for BCCP).

**Table 10.** Sensitivity to the miscoverage level $\alpha$ (means over datasets; size: geometric mean of normalised size).

| α    | Method          | Marginal cov.   | Worst stratum   | Upper-tail cov.   | Size (geo. mean)   |
|:-----|:----------------|:----------------|:----------------|:------------------|:-------------------|
| 0.05 | SCP             | 0.952           | 0.772           | 0.814             | 1.111              |
| 0.05 | CQR             | 0.951           | 0.808           | 0.845             | 1.379              |
| 0.05 | HPD-split       | 0.952           | 0.863           | 0.893             | 1.074              |
| 0.05 | BCCP            | 0.955           | 0.947           | 0.955             | 1.447              |
| 0.05 | S-NCP           | 0.954           | 0.946           | 0.955             | 1.299              |
| 0.05 | SDLC (proposed) | 0.954           | 0.947           | 0.955             | 1.364              |
| 0.05 | SDLC-floor      | 0.962           | 0.916           | 0.929             | 1.130              |
| 0.10 | SCP             | 0.903           | 0.630           | 0.690             | 0.798              |
| 0.10 | CQR             | 0.903           | 0.720           | 0.759             | 0.929              |
| 0.10 | HPD-split       | 0.903           | 0.766           | 0.811             | 0.815              |
| 0.10 | BCCP            | 0.905           | 0.890           | 0.908             | 0.984              |
| 0.10 | S-NCP           | 0.905           | 0.891           | 0.907             | 0.913              |
| 0.10 | SDLC (proposed) | 0.904           | 0.891           | 0.909             | 0.917              |
| 0.10 | SDLC-floor      | 0.918           | 0.823           | 0.852             | 0.841              |
| 0.20 | SCP             | 0.802           | 0.470           | 0.544             | 0.528              |
| 0.20 | CQR             | 0.804           | 0.593           | 0.644             | 0.633              |
| 0.20 | HPD-split       | 0.802           | 0.620           | 0.685             | 0.565              |
| 0.20 | BCCP            | 0.804           | 0.787           | 0.817             | 0.652              |
| 0.20 | S-NCP           | 0.806           | 0.790           | 0.812             | 0.649              |
| 0.20 | SDLC (proposed) | 0.802           | 0.787           | 0.811             | 0.631              |
| 0.20 | SDLC-floor      | 0.823           | 0.637           | 0.695             | 0.582              |


*Number of strata.* Coarser or finer stratifications preserved coverage in the calibrated strata (Table 11). They differ in how far protection extends: with three strata (tails at 10%) the worst *decile* was covered at only 0.781 by SDLC, with the primary five strata at 0.867, and with ten decile strata at 0.889, at a modest increase in size (0.898, 0.917 and 0.938). SDLC was smaller than BCCP under every scheme.

**Table 11.** Sensitivity to the stratification (S3: cut points at training quantiles 0.1 and 0.9; S5: primary; S10: deciles). Worst decile: minimum over training-target deciles of split-averaged coverage.

| Strata   | K   | Method          | Marginal cov.   | Worst calibrated stratum   | Worst decile   | Size (geo. mean)   |
|:---------|:----|:----------------|:----------------|:---------------------------|:---------------|:-------------------|
| S3       | 3   | BCCP            | 0.904           | 0.895                      | 0.786          | 0.967              |
| S3       | 3   | DLS             | 0.903           | 0.679                      | 0.676          | 0.742              |
| S3       | 3   | SDLC (proposed) | 0.902           | 0.894                      | 0.781          | 0.898              |
| S3       | 3   | DLS (hist.)     | 0.903           | 0.628                      | 0.623          | 1.178              |
| S3       | 3   | SDLC (hist.)    | 0.902           | 0.895                      | 0.741          | 1.715              |
| S5       | 5   | BCCP            | 0.905           | 0.890                      | 0.861          | 0.984              |
| S5       | 5   | DLS             | 0.903           | 0.681                      | 0.676          | 0.742              |
| S5       | 5   | SDLC (proposed) | 0.904           | 0.891                      | 0.867          | 0.917              |
| S5       | 5   | DLS (hist.)     | 0.903           | 0.633                      | 0.623          | 1.178              |
| S5       | 5   | SDLC (hist.)    | 0.904           | 0.893                      | 0.844          | 1.775              |
| S10      | 10  | BCCP            | 0.908           | 0.887                      | 0.888          | 1.011              |
| S10      | 10  | DLS             | 0.903           | 0.677                      | 0.676          | 0.742              |
| S10      | 10  | SDLC (proposed) | 0.907           | 0.889                      | 0.889          | 0.938              |
| S10      | 10  | DLS (hist.)     | 0.903           | 0.623                      | 0.623          | 1.178              |
| S10      | 10  | SDLC (hist.)    | 0.906           | 0.886                      | 0.886          | 1.824              |


*Calibration-set size.* Using a quarter of the calibration set (mean 1,082 points) kept every stratified method valid but enlarged their sets markedly (SDLC 1.265, BCCP 1.388, versus 0.917 and 0.984 with the full set; Fig. 6), whereas the marginal methods' sizes hardly changed. Stratified calibration therefore needs enough calibration points in each rare stratum; with fewer than about $1/\alpha$ points per stratum it degenerates to returning the whole stratum.

![**Fig. 6.** Effect of the calibration-set size (fraction of the 25% calibration split used): worst-stratum coverage (left) and normalised set size (right), means over datasets ($\alpha=0.1$).](/home/user/p_c1_2/Target_Journal_Submission/figures/F7_calibration_size.png){width=100%}


*Base learner.* To check that the conclusions are not specific to gradient boosting, all location–scale and residual methods were re-run with a two-layer perceptron (128 and 64 units, early stopping) as mean and scale model on all 31 datasets with 5 splits each (CQR and the histogram density were omitted because they require quantile or multiclass models). The picture was the same (Table 12): marginal and covariate-adaptive methods covered 70.8%–86.7% of the upper tail, every stratified method reached a worst-stratum coverage of about 0.889 (SDLC better than every marginal method, all Holm-adjusted $p$ < 0.001), and SDLC gave the smallest stratified sets: smaller than BCCP on 23 of 31 datasets (geometric-mean ratio 0.954, $p$ = 0.025), than S-NCP on 29 (ratio 0.923, $p$ < 0.001) and than S-HPD on 30 (ratio 0.911, $p$ < 0.001). With the perceptron, whose scale estimates are smoother than those of gradient boosting, the advantage of the density score over the normalised residual was therefore clearer than in the main benchmark.

**Table 12.** Learner generality: the conformal procedures with a multilayer perceptron as mean and scale model (31 datasets × 5 splits, $\alpha=0.1$; size: geometric mean of normalised size).

| Method          | Marginal cov.   | Lower-tail cov.   | Upper-tail cov.   | Worst stratum   | Size (geo. mean)   |
|:----------------|:----------------|:------------------|:------------------|:----------------|:-------------------|
| SCP             | 0.902           | 0.879             | 0.708             | 0.648           | 0.932              |
| NCP             | 0.903           | 0.856             | 0.857             | 0.805           | 1.038              |
| Mondrian-ŷ      | 0.904           | 0.840             | 0.808             | 0.764           | 0.918              |
| DCP             | 0.902           | 0.851             | 0.867             | 0.820           | 1.055              |
| HPD-split       | 0.903           | 0.857             | 0.860             | 0.809           | 1.048              |
| DLS             | 0.903           | 0.866             | 0.779             | 0.737           | 0.924              |
| BCCP            | 0.905           | 0.902             | 0.913             | 0.891           | 1.111              |
| S-NCP           | 0.906           | 0.904             | 0.912             | 0.890           | 1.149              |
| S-HPD           | 0.905           | 0.902             | 0.912             | 0.889           | 1.164              |
| SDLC (proposed) | 0.905           | 0.901             | 0.910             | 0.889           | 1.060              |
| SDLC-floor      | 0.913           | 0.886             | 0.853             | 0.825           | 0.991              |
| SDLC-hull       | 0.920           | 0.909             | 0.914             | 0.897           | 1.118              |


## 6.7 Computational cost

Table 13 separates the cost of fitting the underlying models (recorded during the benchmark, four single-threaded tasks running concurrently on a four-core CPU) from the cost of calibration and prediction (seed 0 of every dataset, timed in isolation, median of three repetitions, for the whole test set). SDLC needs the mean model, the scale model with three out-of-fold refits and a one-dimensional kernel density estimate: a median of 2.04 s per dataset (maximum 61.0 s), against 0.34 s for the mean model alone and 4.33 s for the multiclass histogram density. Calibration and prediction with residual or quantile scores took well under a millisecond for an entire test set; density-level sets took a median of 0.24 s (maximum 1.56 s for test sets of up to 18,000 points), almost all of it spent computing the geometry of the sets (their size and pieces) on the per-$x$ grid. Deciding whether a given value belongs to an SDLC set requires a single evaluation of $\hat f$, so the method is cheap enough for interactive and batch deployment; its overhead relative to BCCP is the scale model and the density evaluation.

**Table 13.** Computational cost. Fit: seconds to fit the models a method requires (median and maximum over datasets; CQR per miscoverage level). Calibrate+predict: seconds for calibration and prediction sets on the whole test set (seed 0, median of three repetitions; median and maximum over datasets).

| Method          | Fit (s, median)   | Fit (s, max)   | Calibrate+predict (s, median)   | Calibrate+predict (s, max)   |
|:----------------|:------------------|:---------------|:--------------------------------|:-----------------------------|
| SCP             | 0.342             | 10.527         | 0.000                           | 0.001                        |
| NCP             | 1.344             | 46.359         | 0.000                           | 0.001                        |
| CQR             | 0.552             | 12.571         | 0.000                           | 0.000                        |
| Mondrian-ŷ      | 0.342             | 10.527         | 0.001                           | 0.004                        |
| DCP             | 2.039             | 60.958         | 0.001                           | 0.005                        |
| HPD-split       | 2.039             | 60.958         | 0.216                           | 1.436                        |
| DLS             | 2.039             | 60.958         | 0.240                           | 1.678                        |
| BCCP            | 0.342             | 10.527         | 0.000                           | 0.002                        |
| BCCP-hull       | 0.342             | 10.527         | 0.000                           | 0.003                        |
| S-NCP           | 1.344             | 46.359         | 0.000                           | 0.003                        |
| S-CQR           | 0.552             | 12.571         | 0.000                           | 0.002                        |
| S-HPD           | 2.039             | 60.958         | 0.218                           | 1.543                        |
| SDLC (proposed) | 2.039             | 60.958         | 0.237                           | 1.563                        |
| SDLC-2p         | 2.037             | 52.872         | 0.248                           | 1.515                        |
| SDLC (hist.)    | 4.334             | 131.770        | 0.001                           | 0.010                        |


## 6.8 Error analysis

Where does stratification cost the most, and where does SDLC lose to simpler scores? The price of stratum-wise validity (SDLC relative to DLS) was not associated with the predictability of the target (Spearman $\rho$ = 0.47 with RMSE/sd($y$), $p$ = 0.008) and only weakly with its skewness ($\rho$ = 0.60, $p$ = < 0.001); it was concentrated on a few datasets (Fig. 7, left). The largest price occurred for forest fires, whose burned area is zero for 47.8% of the fires: the atom at zero merges the nominal lower strata into a single stratum holding about three quarters of the training targets, and covering the heavy upper tail of an almost unpredictable target conditionally on the target requires very long sets. Here SDLC, whose smooth density cannot represent the atom, was also less efficient than BCCP and S-NCP (size ratios 1.71 relative to S-NCP), as anticipated by the scope remark after Theorem 2. The other datasets on which SDLC was clearly larger than S-NCP (socmob, cars, concrete) are among the smallest in the suite (804–1,156 observations), where the scale model that enters the density score through the factor $1/\hat\sigma(x)$ is estimated from few points; on socmob SDLC was nevertheless much smaller than BCCP. On the target with the most ties (weekly working hours in the health-insurance data), coinciding quantiles reduced the realised number of strata to two or three, so the nominal "tails" were not tails; validity was unaffected. Small calibration sets also explain the lowest worst-stratum coverages (Fig. 7, right), which remain within the range expected under exact validity.

![**Fig. 7.** Error analysis ($\alpha=0.1$). Left: price of stratum-wise validity (SDLC/DLS size ratio, log scale) against the relative test RMSE of the mean model; labelled datasets have ratios above 1.4. Right: SDLC worst-stratum coverage minus its null mean under exact validity, against calibration size; the shaded area is the null 5% band.](/home/user/p_c1_2/Target_Journal_Submission/figures/F8_error_analysis.png){width=100%}


![**Fig. 8.** Prediction sets for 70 test points of the California housing data (seed 0; 14 points sampled per stratum, so the miss counts are illustrative, not coverage estimates). Dashed lines are stratum edges; crosses mark targets outside the set. Stratified sets (BCCP, SDLC) add separate upper-tail pieces where an extreme value is plausible; the target is top-coded at 500,001, an atom at the upper edge.](/home/user/p_c1_2/Target_Journal_Submission/figures/F9_example_sets_california.png){width=100%}



# 7. Discussion

## 7.1 What the evidence supports

Three findings are robust across datasets, miscoverage levels, stratifications and learner families. First, marginal and covariate-adaptive conformal methods systematically under-cover rare targets: their worst-stratum coverage at a nominal 90% was 63.0%–78.0% on average, and the null reference shows that this is not sampling noise. Proposition 1 and the synthetic study show that the shortfall is structural; better covariate adaptivity alone cannot remove it. Second, calibrating within target strata restores stratum-wise coverage for every score, as Mondrian theory guarantees and as BCCP [@randahl2026bin] demonstrated for one application; our benchmark shows that the guarantee holds in practice across 31 datasets, is robust to moderate target shift, and costs a median 1.05–1.14-fold increase in set size. Third, the choice of score matters for efficiency in the direction predicted by Theorem 2: the density-level score gave smaller stratum-valid sets than the residual score of BCCP, the quantile score of BFQR-style calibration and the HPD score, with both gradient-boosted and neural base models, and gave more targeted tail alerts.

Two qualifications are equally well supported. The advantage of the density score over the normalised residual depends on the quality of the scale model: it was clear with the perceptron, typical but not uniform with gradient boosting, and absent at $\alpha=0.05$, where few calibration points fall in the tail strata. And the efficiency of any density score depends on its implementation: evaluating density sets on a coarse grid of the marginal target distribution, as in our pre-registered implementation, inflated them enough to erase the advantage. Density-based conformal methods should therefore be evaluated at a resolution relative to the conditional scale.

## 7.2 Practical guidance

For practitioners who must report how often extreme outcomes are covered, our results suggest the following. (i) Use stratified calibration whenever coverage of rare targets is a requirement; marginal coverage, however adaptive the score, does not deliver it. (ii) Choose strata from training-target quantiles so that each stratum receives at least several times $1/\alpha$ calibration points; otherwise the method returns whole strata. Finer strata extend protection to finer target ranges (Table 11) at a modest cost in size. (iii) Use a density-level score: SDLC with a location–scale density is a robust default, and S-NCP is a close and simpler alternative when the scale model is noisy. (iv) When an interval is mandatory, report the hull; when marginal efficiency matters more than full stratum-wise validity, the floor variant protects every stratum at level $1-\beta$ while keeping marginal coverage $1-\alpha$. (v) Treat the sets as tail alerts: whenever the set reaches into the upper stratum, an extreme outcome is plausible, and the recall of such alerts is guaranteed.

## 7.3 Limitations

*Size cost and data requirements.* Stratum-wise validity is paid for in set size, and the payment grows when tail strata are small: at $\alpha=0.05$ or with a quarter of the calibration set, sets became considerably larger, and with fewer than $1/\alpha_k-1$ calibration points the method returns the whole stratum. Cross-fitted or jackknife+-type calibration [@barber2021jackknife] and pooling of sparse strata in the spirit of clustered conformal prediction [@ding2023class] are natural remedies that we did not evaluate; any pooling rule must be decided from training data only to preserve validity.

*Granularity of the guarantee.* The guarantee holds for the calibrated strata, not for arbitrary sub-ranges: within a stratum, coverage can be lower near its outer end (deciles 7–9 in Fig. 1), and continuous tilts that move mass within a stratum reduce coverage (Table 9). Corollary 1 quantifies this, but the bound is vacuous for open tail strata under unbounded tilts.

*Density estimation.* The optimality of Theorem 2 is an oracle property. The location–scale density cannot represent atoms (zero inflation), multimodality or covariate-dependent shape beyond scale, and the exploratory two-piece variant did not improve on it. On the zero-inflated forest-fire data SDLC was less efficient than BCCP. Flexible conditional density estimators (mixture density networks, normalising flows, distributional boosting) may close the gap to the oracle and are an obvious next step.

*Evaluation scope.* The benchmark covers independent tabular data with targets having at least 20 distinct values; ordinal, count and temporally dependent targets were excluded. Several datasets contain duplicate rows (up to 9.1% for sarcos); random splitting keeps the data exchangeable, so the guarantees are unaffected, but point accuracy may be optimistic. All results are for split calibration with a 50/25/25 split and a single fixed configuration of the base learners, chosen without tuning to avoid favouring any method. Finally, three implementation decisions were changed after pre-registration (Section 5.7); the pre-registered results are reported in the supplementary material, the coverage conclusions are identical, and only the size comparison of density-based scores depended on the implementation.

*Applicability of the guarantee.* Like all conformal guarantees, stratum-wise coverage requires exchangeability of calibration and test data; it holds on average over calibration sets and test points of a stratum, not conditionally on a particular covariate value, and it does not protect against shifts of the covariate distribution within strata.


# 8. Conclusion

Prediction intervals that are valid on average can fail exactly where imbalanced regression needs them: on the rare outcomes. We showed that this failure is structural, since even the oracle interval with exact covariate-conditional coverage misses most extreme outcomes, and that calibrating conformal thresholds within strata of the target, an established Mondrian device, restores coverage for rare outcomes in finite samples and under shifts of the stratum frequencies. Our main methodological contribution concerns efficiency: among all sets with stratum-wise coverage, conditional-density level sets with stratum-specific thresholds are the smallest, which leads to SDLC. In a pre-registered benchmark on 31 datasets with 10 splits each, stratified calibration raised the worst-stratum coverage from 63.0%–78.0% to about 0.891 (consistent with exact validity), at a median set-size increase of 1.05–1.14-fold; SDLC gave smaller stratum-valid sets than bin-conditional conformal prediction with residual scores (geometric-mean ratio 0.93) and than binned quantile-regression calibration (0.83), and more targeted tail alerts, with gains that replicated with a neural base learner. Its advantage over a stratified normalised residual was smaller and depended on the quality of the scale model. Future work should combine stratified calibration with more flexible conditional density estimators, data-efficient cross-fitted calibration for sparse strata, and dependent data.


<!-- End matter. Every heading carries {-} so that it stays unnumbered in any build (render_manuscript.py does not exempt "Ethics statement" by name). The generative AI declaration comes last so that it immediately precedes the References, as Elsevier's policy requires. Bracketed text marks placeholders for the authors. -->

# Declaration of competing interest

The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper. [Placeholder: to be confirmed by every author before submission.]

# CRediT authorship contribution statement

[Placeholder: to be completed by the authors using the CRediT taxonomy, for example:] **[Author 1]:** Conceptualization, Methodology, Software, Formal analysis, Investigation, Visualization, Writing – original draft. **[Author 2]:** Conceptualization, Validation, Supervision, Writing – review & editing.

# Data and code availability

*Data.* All datasets analysed in this study are publicly available on OpenML as study 353, the OpenML-CTR23 benchmark suite [@fischer2023openml]. They were downloaded programmatically through the OpenML API by the scripts in the code package; the OpenML identifier and licence of each dataset are listed in the supplementary material.

*Code.* All code, the configuration files, the raw per-run results and the analysis scripts are provided in the supplementary code package and will be deposited in a public repository [repository URL] upon acceptance.

# Funding

[Placeholder: funding sources, grant numbers and the role of each funder; if there was no funding: "This research did not receive any specific grant from funding agencies in the public, commercial, or not-for-profit sectors."]

# Acknowledgements

[Placeholder: to be completed by the authors; delete this section if there is nothing to acknowledge.]

# Ethics statement

This study used only publicly available, de-identified benchmark data. It involved no human participants and no animals, and no personal data were collected; ethical approval was therefore not required.

# Declaration of generative AI and AI-assisted technologies in the manuscript preparation process

During the preparation of this work the authors used Claude (Anthropic), a generative AI system, in order to assist with literature search, code development, orchestration of the computational experiments and drafting of the manuscript. After using this tool, the authors reviewed and edited the content as needed and take full responsibility for the content of the publication.


# References

::: {#refs}
:::


# Appendix A. Proofs

**Proof of Theorem 1.** Condition on $\mathcal{D}_{\mathrm{tr}}$, which fixes the score $s$ and the strata. Let $E_k=\{Y_{n+1}\in B_k\}$ and $J=\{i\le n+1: Y_i\in B_k\}$, so that $|J|=n_k+1$ on $E_k$. Membership of a point in $B_k$ is a function of that point alone, so any permutation of $\{1,\ldots,n+1\}$ that maps $J$ onto itself leaves the event $\{J=j,\ n+1\in J\}$ unchanged; by exchangeability, conditionally on $J=j\ni n+1$ and on the multiset $\{(X_i,Y_i):i\in j\}$, the index $n+1$ is uniformly distributed over $j$. Let $R$ be the rank of $S_{n+1}=s(X_{n+1},Y_{n+1})$ among $\{S_i\}_{i\in J}$, with ties broken uniformly at random; conditionally as above, $R$ is uniform on $\{1,\ldots,n_k+1\}$. By (3)–(4), $Y_{n+1}\in\hat C(X_{n+1})$ iff $S_{n+1}\le\hat q_k$, which holds whenever $R\le r_k=\lceil(n_k+1)(1-\alpha_k)\rceil$ (if $r_k>n_k$, then $\hat q_k=+\infty$ and coverage is one). Hence the conditional coverage is at least $r_k/(n_k+1)\ge 1-\alpha_k$. Averaging over $J$ and the multiset gives (5); since the argument conditions on $J$, the level $\alpha_k$ may depend on $n_k$. If scores are almost surely distinct, coverage is exactly $\min\{r_k,n_k+1\}/(n_k+1)<1-\alpha_k+1/(n_k+1)$ given $n_k$. The marginal statement follows from the law of total probability, $\sum_kp_k(1-\alpha_k)=1-\sum_kp_k\alpha_k$. Finally, the conditioning on $\mathcal{D}_{\mathrm{tr}}$ allows any score and strata that are measurable functions of $\mathcal{D}_{\mathrm{tr}}$ alone. $\square$

**Proof of Corollary 1.** Given $\mathcal{D}_{\mathrm{tr}}$ and $\mathcal{D}_{\mathrm{cal}}$ the set $A=\{(x,y):y\in\hat C(x)\}$ is fixed. Because the test point is independent of the calibration data, $Q\{Y\in\hat C(X)\,|\, Y\in B_k\}=\mathbb{E}\,Q_k(A)$ and the left-hand side of (5) equals $\mathbb{E}\,P_k(A)$, where $\mathbb{E}$ averages over $\mathcal{D}_{\mathrm{cal}}\sim P^n$ (i.i.d. data are exchangeable, so (5) applies). (i) If $Q_k=P_k$ the two expectations coincide, and the law of total probability gives the marginal statement. (ii) $|Q_k(A)-P_k(A)|\le d_{\operatorname{TV}}(Q_k,P_k)$ for every fixed $A$; average and use (5). (iii) Under label shift the likelihood ratio of $Q_k$ to $P_k$ is $\lambda_k(y)=w(y)/\bar w_k$ with $\bar w_k=\pi_k/p_k=\mathbb{E}_{P_k}w(Y)\ge m_k$. Hence $Q_k(A^c)=\mathbb{E}_{P_k}\{\lambda_k(Y)\mathbf{1}_{A^c}(X,Y)\}\le(M_k/\bar w_k)P_k(A^c)\le(M_k/m_k)P_k(A^c)$; averaging over $\mathcal{D}_{\mathrm{cal}}$ and using (5) gives the multiplicative bound. For the total-variation bound, $\lambda_k\in[a,b]$ with $a=m_k/\bar w_k\le1\le b=M_k/\bar w_k$ and $\mathbb{E}_{P_k}\lambda_k=1$; since $d_{\operatorname{TV}}(Q_k,P_k)=\mathbb{E}_{P_k}(\lambda_k-1)_+$ and, by convexity, $(\lambda-1)_+\le(b-1)(\lambda-a)/(b-a)$ on $[a,b]$, we obtain $d_{\operatorname{TV}}\le(b-1)(1-a)/(b-a)=(M_k-\bar w_k)(\bar w_k-m_k)/\{\bar w_k(M_k-m_k)\}$. The right-hand side is maximised at $\bar w_k=\sqrt{m_kM_k}$, where it equals $(\sqrt{M_k}-\sqrt{m_k})/(\sqrt{M_k}+\sqrt{m_k})=\tanh\{\log(M_k/m_k)/4\}$. $\square$

**Remark (within-stratum coverage profile).** Under label shift, let $\kappa(y)=P\{y\in\hat C(X_{n+1})\,|\, Y_{n+1}=y\}$, which is the same under $P$ and $Q$. Then the change in stratum-wise coverage equals the within-stratum covariance $\mathbb{E}_{P_k}[\{\kappa(Y)-c\}\{\lambda_k(Y)-1\}]$ for any constant $c$, so coverage is lost only if the shift moves mass within $B_k$ towards values that are covered less often than the stratum average. By Proposition 1 such profiles decrease towards the outer end of a tail stratum, which is why a tilt towards more extreme outcomes can lower tail-stratum coverage even after stratified calibration.

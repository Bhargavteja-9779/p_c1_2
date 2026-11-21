---
title: "Covering rare outcomes in imbalanced regression: stratified and relevance-weighted conformal prediction with density scores"
author:
  - "[Anonymised for double-blind review: author names and affiliations are given on the separate title page]"
abstract: |
  Prediction intervals for regression are usually calibrated to hold on average over all outcomes, so they can systematically miss the rare, extreme outcomes that matter most in imbalanced regression. Even the oracle interval with exact covariate-conditional coverage covers only 70.5% of the top decile in a Gaussian model with half of the variance explained. We study two guarantees for rare outcomes and the prediction sets that meet them most efficiently. For coverage within every stratum of the target, calibration within strata is an established Mondrian device; we show that conditional-density level sets with stratum-specific thresholds are the smallest such sets and evaluate the resulting method, stratified density-level conformal prediction (SDLC). For coverage weighted by an imbalanced-regression relevance function, we propose relevance-weighted density-level conformal prediction (RW-DLC), which needs no strata, has a finite-sample guarantee and uses the size-optimal score. On 31 OpenML-CTR23 datasets, marginal and covariate-adaptive methods covered only 63.0%–78.3% of their worst-covered stratum at a nominal 90%, whereas stratified methods were consistent with exact validity. SDLC gave smaller sets than bin-conditional conformal prediction and stratified quantile regression, which a pre-specified replication on 17 held-out datasets confirmed, but stayed within a few per cent of a stratified normalised residual. In a second pre-specified study on the held-out datasets, RW-DLC met its relevance-weighted target and covered 87.2% of the top 1% of outcomes, against 68.8% for SDLC, at a cost in coverage of the bulk. Code and raw results are released.
---

**Keywords:** Conformal prediction; Imbalanced regression; Prediction intervals; Uncertainty quantification; Relevance function; Extreme values


# 1. Introduction

Many regression problems that intelligent systems solve are judged by how they handle *rare* outcomes: the unusually expensive property, the exceptional salary, the extreme load on a power grid, the very toxic compound. Rare outcomes are under-represented in training data, and models trained by minimising average loss shrink their predictions towards the bulk of the target distribution. This is the setting of *imbalanced regression* [@branco2016survey; @ribeiro2020imbalanced; @yang2021delving], where a growing literature re-weights, re-samples or re-parameterises models so that point predictions for rare targets become more accurate.

Point predictions are only half of what a decision maker needs. Prediction *sets* with a coverage guarantee state how far the truth may be from the prediction, and conformal prediction delivers such guarantees in finite samples for any model, under exchangeability only [@vovk2005alrw; @lei2018distribution; @angelopoulos2023gentle]. Its standard guarantee, however, is *marginal*: the set contains the outcome with probability $1-\alpha$ *on average over all outcomes*. When rare outcomes matter, the relevant question is different: **when the outcome is extreme, how often does the set contain it?** A marginal guarantee is silent on this, because the frequent bulk can be over-covered while the rare tails are under-covered.

Much work makes conformal sets adapt to the covariates, so that coverage holds approximately conditionally on $X$ [@romano2019conformalized; @chernozhukov2021distributional; @izbicki2022cdsplit; @gibbs2025conformal]. Such sets do not protect rare outcomes, and better estimation would not change this: even the *oracle* set with exact coverage $1-\alpha$ at every $x$ under-covers the tails, because an extreme outcome typically combines a large signal with a large, unpredictable noise realisation that no $X$-measurable set can anticipate. Coverage *conditional on the target*, which we call stratum-wise coverage, must be targeted explicitly.

Calibrating conformal thresholds separately within bins of the observed outcome is the natural device, and it is not new. @randahl2026bin proposed it as bin-conditional conformal prediction (BCCP) for conflict fatalities, and @wang2023equal calibrate within outcome bins to equalise coverage across groups. Its bin-wise validity is an instance of Mondrian (label-conditional) validity [@vovk2005alrw; @vovk2013conditional]. Two questions remain open. First, the guarantee holds for any score, so efficiency is decided by the score, and it is not known which score makes stratum-valid sets smallest or what that efficiency costs. Second, strata protect rare outcomes only at their own resolution: the most extreme outcomes lie inside a tail stratum and are covered only on average with it, while finer strata leave too few calibration points. Imbalanced regression usually describes the importance of an outcome by a continuous *relevance function* [@torgo2007utility; @ribeiro2020imbalanced; @steininger2021denseweight], and long-tailed classification has obtained conformal guarantees that average coverage over classes [@ding2025longtailed; @bhattacharyya2026macro]; a regression counterpart has been missing. This paper makes four contributions.

1. **Two guarantees for rare outcomes and their optimal sets.** We quantify how far the oracle covariate-conditional set falls short in the tails (Proposition 1: 70.5% of the top decile in a Gaussian model with half of the variance explained). For coverage within strata, conditional-density level sets with stratum-specific thresholds are the smallest valid sets (Proposition 2, the per-stratum form of known level-set results [@lei2013distribution; @sadinle2019least]), and their plug-in version is asymptotically optimal under conditions on the density estimate (Proposition 3). For *relevance-weighted coverage*, the average of coverage weighted by a relevance function, we prove finite-sample validity of relevance-weighted calibration (Theorem 2) and show that level sets of relevance times conditional density are the smallest valid sets (Proposition 4).
2. **Two methods with one density model.** Stratified density-level conformal prediction (SDLC) and the new relevance-weighted density-level conformal prediction (RW-DLC) share a semiparametric location–scale density whose noise distribution is estimated from cross-fitted residuals; both have exact implementations whose cost is linear in the number of test points.
3. **Evidence under pre-specified plans.** On all 31 eligible OpenML-CTR23 datasets with 10 predefined splits, we compare the stratified methods with BCCP, stratified normalised-residual, quantile and HPD scores and seven marginal or covariate-adaptive methods, with ablations of each score component. The size comparisons are replicated on 17 held-out datasets under an analysis plan fixed before evaluation, and RW-DLC is evaluated on both collections under a second such plan. We report where the gains are small: among scores that use the estimated scale, the choice changes set sizes by only a few per cent.
4. **Decision-oriented guidance.** We compare tail alerts derived from prediction sets with dedicated conformal tail classifiers and conformal selection [@jin2023selection] under explicit cost models, analyse robustness to target shift, imbalance-aware training, a second learner family, grouped splits and design choices, and state which guarantee and which score suit which requirement.

Section 2 reviews related work (Table 1). Section 3 formalises the problem, Section 4 presents SDLC and RW-DLC, Section 5 describes the experiments, Section 6 reports the results, Section 7 discusses them, and Section 8 concludes.


# 2. Related work

Four lines of work meet in this paper: covariate-adaptive conformal regression, calibration within label-defined categories, imbalanced regression, and conformal prediction under distribution shift.

## 2.1 Conformal regression and covariate-conditional coverage

Split conformal prediction calibrates a nonconformity score of any fitted regressor on held-out data and guarantees marginal coverage in finite samples under exchangeability [@papadopoulos2002inductive; @vovk2005alrw; @lei2018distribution]. Much subsequent work changes the score so that sets adapt to the covariates: normalised residuals [@lei2018distribution], conformalised quantile regression (CQR) [@romano2019conformalized; @sesia2020comparison], distributional conformal prediction (DCP) [@chernozhukov2021distributional], conformal predictive distributions [@vovk2019nonparametric] and jackknife+ [@barber2021jackknife]. A family of methods builds sets from density estimates: conformal density level sets [@lei2013distribution; @lei2014bands], Dist-split and CD-split [@izbicki2020flexible], HPD-split [@izbicki2022cdsplit], conditional histograms [@sesia2021conformal], regression-as-classification [@guha2024conformal] and conformal thresholded intervals [@luo2025cti]. Under coverage constraints indexed by covariate shifts, length-optimal sets are conditional-density level sets with a covariate-dependent level [@kiyani2024length]. SDLC uses a score from this family but calibrates it with stratum-specific thresholds.

These methods target approximate covariate-conditional coverage, which cannot be guaranteed in finite samples without further assumptions [@barber2021limits]. Relaxations include conditional calibration over classes of covariate groups or shifts [@gibbs2025conformal], localised calibration [@guan2023localized; @hore2025local], calibration within partitions learned by trees [@cabezas2025regression; @santos2026loboost], and learned scores that reduce conditional miscoverage [@xie2024boosted; @gao2024adjusting]. In intelligent systems, conformal prediction serves as an uncertainty layer, for example for option prices [@bastos2024conformal] and tropical-cyclone tracks [@meng2024uncertainty]. All these approaches condition, at most, on functions of $X$, and Proposition 1 shows that even exact covariate-conditional coverage leaves extreme outcomes under-covered. Covariate-adaptive scores are therefore complementary to stratified calibration, not a substitute.

## 2.2 Category-, label- and bin-conditional calibration

Mondrian conformal predictors [@vovk2005alrw; @vovk2022alrw] assign each example to a category that may depend on its label and calibrate within each category, which yields finite-sample category-conditional and, in particular, label-conditional validity [@vovk2013conditional; @toccaceli2019combination; @angelopoulos2024theoretical]. In classification, clustered conformal prediction pools classes with similar score distributions [@ding2023class], a device analogous to merging sparse strata. Conformal uncertainty measures have also been built into classifiers such as deep forests [@zhang2025conformal]. Closest to our optimality result is @sadinle2019least, who showed that the least ambiguous classifier under class-specific coverage thresholds $p(y\,|\, x)$ with class-specific cut-offs [see also @lei2014classification; @chzhen2021setvalued]; Proposition 2 is the same characterisation for a continuous outcome. For long-tailed classification, @ding2025longtailed and @liu2025longtail interpolate between marginal and class-conditional coverage, and @bhattacharyya2026macro show that label-weighted conformal prediction guarantees macro-coverage and characterise its smallest sets. RW-DLC carries this idea to continuous outcomes, with a relevance function in place of class weights (Section 4.7). Kandinsky conformal prediction [@bairaktari2025kandinsky] covers overlapping or fractional groups defined jointly on covariates and labels, with a high-probability guarantee; disjoint target strata are its simplest case, for which Mondrian calibration is exact.

In regression, Mondrian categories have mostly been functions of $X$ or of the fitted model: binned difficulty estimates [@bostrom2020mondrian], regression trees [@johansson2018interpretable], covariate clusters [@sousa2024improving] and quartiles of point predictions [@boruah2026distribution], which reports under-coverage of the highest-strength quartile for steel fatigue; worst-bin coverage statistics are biased downwards [@boruah2026null]. Such guarantees do not extend to coverage conditional on $Y$.

Two regression methods calibrate within bins of the outcome itself. @wang2023equal require coverage to be equal across groups of a sensitive attribute conditionally on the outcome; their binned fair quantile regression (BFQR) calibrates within each group and equal-mass outcome bin at bin-specific levels chosen to minimise width, so coverage is equalised across groups but traded across bins. The closest work is BCCP [@randahl2026bin], which runs split conformal prediction with a residual score within user-defined outcome bins and returns the union of the per-bin sets or its hull; it guarantees coverage within each bin. Our stratified calibration step (Eqs. 3–4) coincides with BCCP when the absolute-residual score is used, and its validity (Theorem 1) is not claimed as new. BCCP leaves open which score yields the smallest bin-valid sets, where the efficiency comes from, and how the guarantee behaves under label shift; these are the questions we address.

## 2.3 Imbalanced regression and its uncertainty

Imbalanced regression concerns problems in which the most important targets are rare [@branco2016survey; @ribeiro2020imbalanced]. Utility-based regression encodes their importance through relevance functions [@torgo2007utility], and precision, recall [@torgo2009precision] and SERA [@ribeiro2020imbalanced] evaluate point predictions on the relevant range. Data-level methods synthesise rare examples, such as SMOTER [@torgo2013smote], SMOGN [@branco2017smogn] and their successors [@avelino2024resampling; @belhaouari2024oversampling; @alahyari2026smogan; @shahbazi2026hybrid]. Algorithm-level methods re-weight the loss, for example DenseWeight [@steininger2021denseweight], label distribution smoothing [@yang2021delving] and Balanced MSE [@ren2022balanced].

Uncertainty has entered this literature mainly as a means to better point predictions: quantile ensembles [@zhu2026swarm], variational imbalanced regression [@wang2023variational] and UQDIR [@dolar2025uncertainty] give no coverage guarantee, and extreme conformal prediction [@pasche2026extreme] addresses very high confidence levels instead. Guarantees on how often sets contain rare targets have so far come from conflict forecasting and fair regression [@randahl2026bin; @wang2023equal]. For yes/no decisions about extremes, conformal selection [@jin2023selection] and class-conditional conformal tail classifiers exist; we use both as baselines.

## 2.4 Distribution shift

Weighted conformal prediction handles covariate shift with likelihood-ratio weights [@tibshirani2019conformal]. Under label (target) shift, the law of $Y$ changes while that of $X$ given $Y$ does not. Re-weighting approaches for classification [@podkopaev2021distribution] and regression [@yi2025distribution; @lee2026split] estimate the shift, and exact validity is lost when it is misspecified [@choi2026continuous]. Label-conditional calibration needs no estimate, because a label shift re-weights whole classes [@podkopaev2021distribution]. Stratified calibration carries this property over to regression exactly when the shift re-weights whole strata (Corollary 1), and only approximately otherwise, which our experiments quantify.

**Table 1.** Positioning of the present work against the closest conformal approaches (qualitative summary of the cited papers; Sections 2.1–2.4). *Finite-sample guarantee*: the event for which coverage $\ge 1-\alpha$ is guaranteed under exchangeability. The stratified calibration step of SDLC coincides with BCCP and is not claimed as new; the contribution lies in the last three columns.

| Approach                                                                                                              | Coverage guaranteed for                                    | Score                                           | Size optimality                                                                                          | Label (target) shift                                                            |
|:----------------------------------------------------------------------------------------------------------------------|:-----------------------------------------------------------|:------------------------------------------------|:---------------------------------------------------------------------------------------------------------|:--------------------------------------------------------------------------------|
| Split, normalised, CQR, DCP [@lei2018distribution; @romano2019conformalized; @chernozhukov2021distributional]         | all outcomes (marginal)                                    | residual, quantile or CDF                       | no                                                                                                       | not addressed                                                                   |
| Density level sets, CD-split, HPD-split [@lei2013distribution; @izbicki2020flexible; @izbicki2022cdsplit]             | all outcomes (marginal)                                    | conditional density                             | smallest marginal sets (oracle)                                                                          | not addressed                                                                   |
| Conditional calibration [@gibbs2025conformal]                                                                         | a class of covariate groups or shifts                      | any                                             | no                                                                                                       | covariate shifts in the class                                                   |
| Length-optimal sets [@kiyani2024length]                                                                               | a class of covariate shifts                                | density with an X-dependent level               | smallest over the class (oracle)                                                                         | covariate shifts in the class                                                   |
| Mondrian on X or ŷ [@bostrom2020mondrian; @sousa2024improving; @boruah2026distribution]                               | bins of covariates or predictions                          | any                                             | no                                                                                                       | not addressed                                                                   |
| Kandinsky CP [@bairaktari2025kandinsky]                                                                               | overlapping or weighted groups of (X, Y), high probability | any                                             | no                                                                                                       | group re-weightings (approximate)                                               |
| Class-conditional and long-tailed classification [@sadinle2019least; @podkopaev2021distribution; @ding2025longtailed] | each class (discrete Y)                                    | class probabilities                             | smallest class-valid sets (oracle)                                                                       | exact under label shift                                                         |
| Macro-coverage [@bhattacharyya2026macro]                                                                              | weighted average over classes (discrete Y)                 | label-weighted probabilities                    | smallest sets characterised (oracle)                                                                     | re-weighting of classes                                                         |
| BFQR [@wang2023equal]                                                                                                 | group × bin of Y, levels traded across bins                | conformalised quantiles                         | width-minimising bin levels                                                                              | not addressed                                                                   |
| BCCP [@randahl2026bin]                                                                                                | each bin of Y                                              | absolute residual (any score admissible)        | not analysed                                                                                             | exact under bin re-weighting (Mondrian property)                                |
| SDLC (this paper; calibration step = BCCP)                                                                            | each stratum of Y                                          | conditional density with per-stratum thresholds | smallest stratum-valid sets (oracle, Prop. 2); plug-in asymptotically optimal under conditions (Prop. 3) | inherited from stratified calibration; within-stratum shift quantified (Cor. 1) |
| RW-DLC (this paper)                                                                                                   | relevance-weighted average over continuous Y (no strata)   | relevance × conditional density                 | smallest relevance-valid sets (oracle, Prop. 4)                                                          | exact under a target shift proportional to the relevance                        |


**Positioning.** Table 1 summarises the comparison. We take calibration within outcome strata, its validity and its robustness to shifts of whole strata as given. Our contributions are (i) the oracle analysis showing why such calibration is needed even under exact covariate-conditional coverage; (ii) the size-optimal score for stratum-wise coverage, its plug-in asymptotics and an analysis of its efficiency and costs; (iii) relevance-weighted coverage for continuous outcomes, with a finite-sample guarantee, its size-optimal score and RW-DLC; and (iv) evidence on 31 OpenML-CTR23 datasets [@fischer2023openml] and 17 held-out datasets under two analysis plans fixed before evaluation.


# 3. Preliminaries and problem formulation

## 3.1 Target-conditional coverage

Let $(X,Y)\in\mathcal{X}\times\mathbb{R}$ have joint law $P$, with marginal law $P_X$ of the covariates. A *prediction set* is a map $C$ from $\mathcal{X}$ to subsets of $\mathbb{R}$ whose graph $\{(x,y):y\in C(x)\}$ is jointly measurable. Split conformal prediction [@papadopoulos2002inductive; @lei2018distribution] guarantees *marginal* coverage $P\{Y\in C(X)\}\ge 1-\alpha$, and much recent work targets approximate *covariate-conditional* coverage $P\{Y\in C(X)\,|\, X=x\}\approx 1-\alpha$ [@romano2019conformalized; @izbicki2022cdsplit; @gibbs2025conformal], which cannot be guaranteed in finite samples without further assumptions [@barber2021limits].

In imbalanced regression the outcomes of interest are rare target values. Let $e_1<\dots<e_{K-1}$ be cut points and $B_1=(-\infty,e_1)$, $B_k=[e_{k-1},e_k)$ for $1<k<K$, $B_K=[e_{K-1},\infty)$ the resulting *target strata*, for instance the lower tail, the bulk and the upper tail, with $p_k=P(Y\in B_k)>0$. We call
$$\operatorname{Cov}_k(C)=P\{Y\in C(X)\,|\, Y\in B_k\},\qquad k=1,\ldots,K, \qquad (1)$$
the *stratum-wise* (target-conditional) coverage of $C$, the regression analogue of class-conditional coverage [@vovk2013conditional; @sadinle2019least] and the notion behind BCCP [@randahl2026bin] and equal opportunity of coverage [@wang2023equal]. Because $\sum_k p_k\,\operatorname{Cov}_k(C)=P\{Y\in C(X)\}$, marginal coverage only constrains a $p$-weighted average of the $\operatorname{Cov}_k$. In particular, a set with *exact* coverage $1-\alpha$, marginally or at every $x$, has $\min_k\operatorname{Cov}_k(C)\le 1-\alpha$, with equality only if all strata are covered at exactly the same rate; any over-coverage of the bulk is paid for in some other stratum.

## 3.2 Covariate-conditional validity does not imply target-conditional validity

How large can the shortfall be for the best covariate-conditional set? The simplest model gives an answer.

**Proposition 1 (Gaussian model).** *Let $X\sim N(0,\tau^2)$ and $Y\,|\, X\sim N(X,\sigma^2)$ with $\tau^2+\sigma^2=1$ and $0<\tau^2<1$, so that $R^2=\tau^2$ is the fraction of variance explained by the optimal predictor. Let $z=\Phi^{-1}(1-\alpha/2)$ and $C^{\mathrm{cov}}(x)=[x-z\sigma,\,x+z\sigma]$, which is, up to Lebesgue-null sets, the unique set of minimal length with $P\{Y\in C(x)\,|\, X=x\}\ge 1-\alpha$ for every $x$. Then*
$$P\{Y\in C^{\mathrm{cov}}(X)\,|\, Y=y\}=\Phi\!\left(\frac{z\sigma-(1-R^2)y}{s}\right)-\Phi\!\left(\frac{-z\sigma-(1-R^2)y}{s}\right),\qquad s=\sigma\sqrt{R^2}, \qquad (2)$$
*an even function of $y$ that is strictly decreasing in $|y|$ and tends to $0$ as $|y|\to\infty$.*

*Proof.* $(X,Y)$ is bivariate normal with $\operatorname{Var}(Y)=1$ and $\operatorname{Cov}(X,Y)=\tau^2$, hence $X\,|\, Y=y\sim N(\tau^2y,\tau^2\sigma^2)$ and $Y-X\,|\, Y=y\sim N((1-\tau^2)y,\tau^2\sigma^2)$. Since $Y\in C^{\mathrm{cov}}(X)$ iff $|Y-X|\le z\sigma$, (2) follows. Write $a=z\sigma>0$ and $m=(1-R^2)y$. The function $h(m)=\Phi((a-m)/s)-\Phi((-a-m)/s)$ is even because $\Phi(-u)=1-\Phi(u)$, and for $m>0$, $h'(m)=-\{\phi((a-m)/s)-\phi((a+m)/s)\}/s<0$ because $|a-m|<a+m$. As $1-R^2>0$, (2) is strictly decreasing in $|y|$ and vanishes as $|y|\to\infty$. Minimality and uniqueness of $C^{\mathrm{cov}}(x)$ follow because the $N(x,\sigma^2)$ density is symmetric and strictly unimodal. $\square$

Integrating (2) over strata of $Y$ (Table 2): for a predictor that explains half of the variance, the oracle covariate-conditional interval covers 70.5% of the top-10% outcomes and 37.5% of the top-1% outcomes, against 94.9% of the central 80%; with $R^2=0.9$ it covers 86.2% of the top decile. The shape of this profile is specific to the Gaussian model, so Table 2 also reports Monte Carlo values for heavy-tailed signals and skewed noise. With a Student-$t_3$ signal the top decile is still under-covered at $R^2=0.5$ (0.648), but the top 1% is covered at 0.625, because extreme outcomes then mostly come from extreme signals, which a covariate-conditional set follows. With right-skewed Gamma noise the oracle *over*-covers the lower decile (0.987) and covers only 0.418 of the top decile and 0.029 of the top 1%. In every case at least one tail stratum is covered well below $1-\alpha$. Tail under-coverage of standard conformal sets has been reported empirically [@wang2023equal; @randahl2026bin; @boruah2026distribution]; it persists for the oracle, so better covariate adaptivity cannot remove it. Coverage in rare strata requires calibration against the law of $(X,Y)$ *given* $Y\in B_k$, which is what stratified calibration does.

**Table 2.** Coverage of the oracle covariate-conditional set ($\alpha=0.1$) within strata of the target. Gaussian rows (Proposition 1): analytic values from Eq. (2) with a Monte Carlo check ($2\times10^6$ draws). Other rows: $Y=S+\varepsilon$ with signal $S$ (standardised Student-$t_\nu$ or Gaussian) and noise $\varepsilon$ (Gaussian or standardised Gamma(2)), scaled to the stated $R^2$; the oracle set is the shortest set with conditional coverage 0.9 given $S$; Monte Carlo with $2\times10^6$ draws. Strata are defined by quantiles of $Y$. Marginal coverage is 0.900 in every row.

| Model                                     | R²   | Bottom 10%   | Central 80%   | Top 10%   | Top 1%   |
|:------------------------------------------|:-----|:-------------|:--------------|:----------|:---------|
| t3 signal, Gaussian noise                 | 0.50 | 0.646        | 0.964         | 0.648     | 0.625    |
| t5 signal, Gaussian noise                 | 0.50 | 0.685        | 0.954         | 0.684     | 0.549    |
| t30 signal, Gaussian noise                | 0.50 | 0.704        | 0.949         | 0.702     | 0.396    |
| Gaussian signal, Gamma(2) noise           | 0.50 | 0.987        | 0.949         | 0.418     | 0.029    |
| Gaussian signal, Gaussian noise (Prop. 1) | 0.50 | 0.705        | 0.949         | 0.705     | 0.375    |
| t3 signal, Gaussian noise                 | 0.90 | 0.839        | 0.915         | 0.838     | 0.869    |
| t5 signal, Gaussian noise                 | 0.90 | 0.854        | 0.911         | 0.855     | 0.860    |
| t30 signal, Gaussian noise                | 0.90 | 0.860        | 0.910         | 0.860     | 0.803    |
| Gaussian signal, Gamma(2) noise           | 0.90 | 0.973        | 0.912         | 0.733     | 0.554    |
| Gaussian signal, Gaussian noise (Prop. 1) | 0.90 | 0.862        | 0.910         | 0.862     | 0.795    |


# 4. Proposed method: stratified density-level conformal prediction

## 4.1 Stratified (Mondrian) calibration

Data are split into a proper training set $\mathcal{D}_{\mathrm{tr}}$ and a calibration set $\mathcal{D}_{\mathrm{cal}}=\{(X_i,Y_i)\}_{i=1}^n$. On $\mathcal{D}_{\mathrm{tr}}$ we fit a nonconformity score $s:\mathcal{X}\times\mathbb{R}\to\mathbb{R}\cup\{+\infty\}$ (small values = conforming) and choose the cut points, e.g. at quantiles of the training targets. Let $k(y)$ be the stratum containing $y$, $I_k=\{i:Y_i\in B_k\}$, $n_k=|I_k|$, and, for levels $\alpha_k\in(0,1)$,
$$\hat q_k=\text{the }r_k\text{-th smallest value of }\{s(X_i,Y_i):i\in I_k\},\qquad r_k=\lceil (n_k+1)(1-\alpha_k)\rceil, \qquad (3)$$
with $\hat q_k=+\infty$ if $r_k>n_k$, which happens exactly when $n_k<1/\alpha_k-1$ (i.e. $n_k\le 8$ for $\alpha_k=0.1$). The stratified prediction set is
$$\hat C(x)=\{y\in\mathbb{R}: s(x,y)\le \hat q_{k(y)}\}=\bigcup_{k=1}^K\{y\in B_k: s(x,y)\le\hat q_k\}. \qquad (4)$$
The threshold applied to a candidate value $y$ is that of the stratum *of that candidate*, not of a prediction; this makes the guarantee target-conditional. Equation (4) is an inductive Mondrian conformal predictor whose taxonomy assigns each example to the stratum of its label [@vovk2005alrw; @vovk2013conditional]; with the absolute-residual score it is BCCP [@randahl2026bin]. When every sub-level set $\{y:s(x,y)\le q\}$ is an interval, as for residual or quantile scores, $\hat C(x)$ is a union of at most $K$ intervals; density scores with a multimodal estimate can produce more pieces.

The following guarantee is the standard label-conditional Mondrian property [@vovk2013conditional], stated for outcome bins by @wang2023equal [Thm. 4.1] and @randahl2026bin. We restate it for an arbitrary score, with the edge cases used later (proof in Appendix A).

**Theorem 1 (stratum-wise validity of Mondrian calibration).** *Suppose that, conditionally on $\mathcal{D}_{\mathrm{tr}}$, the points $(X_1,Y_1),\ldots,(X_n,Y_n),(X_{n+1},Y_{n+1})$ are exchangeable, and let $p_k=P(Y_{n+1}\in B_k\,|\,\mathcal{D}_{\mathrm{tr}})$. Then for every $k$ with $p_k>0$,*
$$P\{Y_{n+1}\in\hat C(X_{n+1})\,|\, Y_{n+1}\in B_k,\mathcal{D}_{\mathrm{tr}}\}\ \ge\ 1-\alpha_k, \qquad (5)$$
*and consequently $P\{Y_{n+1}\in\hat C(X_{n+1})\,|\,\mathcal{D}_{\mathrm{tr}}\}\ge 1-\sum_kp_k\alpha_k\ge 1-\max_k\alpha_k$. If the scores within stratum $k$ are almost surely distinct and finite, then also $P\{Y_{n+1}\in\hat C(X_{n+1})\,|\, Y_{n+1}\in B_k,n_k,\mathcal{D}_{\mathrm{tr}}\}\le 1-\alpha_k+1/(n_k+1)$. The levels $\alpha_k$ may depend on $n_k$, and the score and strata may be any functions of $\mathcal{D}_{\mathrm{tr}}$.*

The guarantee holds for *any* score. For target shift between calibration and deployment, known facts specialise as follows.

**Corollary 1 (target shift).** *Let $\mathcal{D}_{\mathrm{cal}}$ be i.i.d. from $P$ and let the test point be drawn from $Q$, independently of $\mathcal{D}_{\mathrm{cal}}$ and $\mathcal{D}_{\mathrm{tr}}$. Write $P_k=P(\cdot\,|\, Y\in B_k)$ and $Q_k=Q(\cdot\,|\, Y\in B_k)$ for the within-stratum laws of the pair $(X,Y)$ and $\pi_k=Q(Y\in B_k)$; assume $p_k>0$ whenever $\pi_k>0$.*
*(i) If $Q_k=P_k$ for every $k$ with $\pi_k>0$ (the shift re-weights whole strata), then $Q\{Y\in\hat C(X)\,|\, Y\in B_k\}\ge 1-\alpha_k$ for every such $k$, and $Q\{Y\in\hat C(X)\}\ge 1-\sum_k\pi_k\alpha_k$ whatever the $\pi_k$.*
*(ii) For an arbitrary shift, $Q\{Y\in\hat C(X)\,|\, Y\in B_k\}\ge 1-\alpha_k-d_{\operatorname{TV}}(Q_k,P_k)$.*
*(iii) Under label shift, $Q(\cdot\,|\, Y=y)=P(\cdot\,|\, Y=y)$ with density ratio $w=dQ_Y/dP_Y$; let $m_k$ and $M_k$ be the essential infimum and supremum of $w$ on $B_k$, $0<m_k\le M_k<\infty$. Then $Q\{Y\notin\hat C(X)\,|\, Y\in B_k\}\le(M_k/m_k)\,\alpha_k$ and $d_{\operatorname{TV}}(Q_k,P_k)\le\tanh\{\log(M_k/m_k)/4\}$.*

The proof is in Appendix A. Part (i) is the continuous-outcome form of the label-shift robustness of label-conditional coverage [@podkopaev2021distribution; @angelopoulos2024theoretical]. For a continuous outcome, a label shift generally also changes the law of $Y$ *within* a stratum, so exactness requires an unchanged joint law of $(X,Y)$ inside each stratum. Part (ii) applies the coverage-gap bounds of @barber2023beyond [Sec. 4.5] within a stratum, and part (iii) follows from a bounded likelihood ratio. Both bounds are loose for the tilts of Experiment 4, whose density ratios are unbounded on the open tail strata; they explain the direction of the effect, not its size. Marginally calibrated sets have no analogue of (i): their coverage under $Q$ is $\sum_k\pi_k\operatorname{Cov}_k$, which can be as low as $\min_k\operatorname{Cov}_k$. Stratified calibration needs no estimate of the shift, but it is exact only for shifts that act on the stratum probabilities.

## 4.2 The smallest sets with stratum-wise coverage

Theorem 1 leaves the score free; the score determines how large the sets are. For a prediction set $C$ let $|C(x)|$ be its Lebesgue measure and $\mathbb{E}|C(X)|=\int|C(x)|\,P_X(dx)$ its expected size. By the Neyman–Pearson argument behind conformal density level sets [@lei2013distribution], least-ambiguous classifiers [@sadinle2019least] and covariate-indexed length-optimal sets [@kiyani2024length], size-optimal sets are density level sets. The constraints in (1) are indexed by the *label*, so the problem separates by stratum and the thresholds are constant within each stratum.

**Proposition 2 (size-optimal stratum-wise sets).** *Suppose the conditional law of $Y$ given $X$ has a Lebesgue density $f(y\,|\, x)$, that $f(Y\,|\, X)>0$ almost surely, and that for each $k$ the random variable $f(Y\,|\, X)$ has a continuous distribution conditionally on $Y\in B_k$. Fix $\alpha_1,\ldots,\alpha_K\in(0,1)$. Then there are thresholds $t_k>0$ with $P\{f(Y\,|\, X)\ge t_k\,|\, Y\in B_k\}=1-\alpha_k$, and the set*
$$C^\star(x)=\bigcup_{k=1}^K\{y\in B_k: f(y\,|\, x)\ge t_k\} \qquad (6)$$
*satisfies $\operatorname{Cov}_k(C^\star)=1-\alpha_k$ for all $k$. Every prediction set $C$ with $\operatorname{Cov}_k(C)\ge 1-\alpha_k$ for all $k$ satisfies $\mathbb{E}|C(X)\cap B_k|\ge\mathbb{E}|C^\star(X)\cap B_k|$ for every $k$, and hence $\mathbb{E}|C(X)|\ge\mathbb{E}|C^\star(X)|$.*

The proof (Appendix A) is the per-stratum Neyman–Pearson argument; it also covers data-dependent (e.g. conformal) sets whose stratum-wise coverage, averaged over the data, is at least $1-\alpha_k$. With $K=1$ it reduces to a single-threshold density level set, whereas HPD-split [@izbicki2022cdsplit] uses an $x$-specific threshold. Proposition 2 is an oracle statement. The next result shows that stratified calibration of a consistent density estimate attains it asymptotically (with fixed strata); its proof follows the plug-in arguments of @lei2013distribution and @izbicki2022cdsplit.

**Proposition 3 (asymptotic size-optimality of the plug-in procedure).** *Let the assumptions of Proposition 2 hold, and suppose in addition that the distribution function of $f(Y\,|\, X)$ given $Y\in B_k$ is strictly increasing at $t_k$ for every $k$. Let $\hat f$ be estimated from $\mathcal{D}_{\mathrm{tr}}$ of size $N$, let $\varepsilon_N=\sup_{x,y}|\hat f(y\,|\, x)-f(y\,|\, x)|\to0$ in probability, and let $\hat C$ be the stratified set (3)–(4) with score $s=-\hat f$, fixed strata $B_1,\ldots,B_K$ and $n\to\infty$ calibration points. Then $-\hat q_k\to t_k$ in probability for every $k$, and*
$$\mathbb{E}_X\big|\hat C(X)\,\triangle\,C^\star(X)\big|\ \to\ 0\quad\text{in probability,} \qquad (7)$$
*where $\mathbb{E}_X$ averages over a new $X\sim P_X$ given the data. In particular $\mathbb{E}_X|\hat C(X)|\to\mathbb{E}|C^\star(X)|$ while (5) holds for every $n$.*

Four consequences guide the method.

*The optimal score* is the conditional density, $s(x,y)=-f(y\,|\, x)$, with stratum-specific thresholds; a single threshold is optimal only for marginal coverage.

*The price of stratum-wise validity.* Every set that meets the stratum constraints has marginal coverage at least $1-\bar\alpha$, $\bar\alpha=\sum_kp_k\alpha_k$, so $\mathbb{E}|C^\star(X)|$ is at least the size of the optimal marginal set at that level, a single-threshold density level set. The two coincide if and only if $t_1=\dots=t_K$. With a common level $\alpha_k=\alpha$ the difference is the price, in size, of stratum-wise validity.

*Coverage is reallocated across inputs.* In a location–scale model $f(y\,|\, x)=g\{(y-\mu(x))/\sigma(x)\}/\sigma(x)$ the optimal set is, in standardised units $u=(y-\mu(x))/\sigma(x)$, $\{u: g(u)\ge t_k\sigma(x)\}$ within stratum $k$. Its standardised width *shrinks* as $\sigma(x)$ grows, and it is empty when $t_k\sigma(x)>\max g$: the oracle spends coverage where it is cheap. The stratified normalised residual (S-NCP), whose standardised width does not depend on $x$, is optimal only for constant $\sigma$. The density score's size advantage over S-NCP thus comes partly from the factor $1/\sigma(x)$ and is paid for by lower coverage, and occasionally empty sets, for the noisiest inputs. Users who need comparable coverage across noise levels should prefer S-NCP.

*Shape and scope.* Because thresholds differ across strata, $C^\star(x)$ need not be an interval even for unimodal $f(\cdot\,|\, x)$. Optimality refers to size under the calibration covariate law; under a shifted $Q$, $C^\star$ stays valid in the sense of Corollary 1(i) but is no longer size-optimal. For targets with atoms (ties, zero inflation) Theorem 1 is unaffected, but a smooth density score is then valid without being size-optimal.

## 4.3 The SDLC procedure

Figure 1 summarises the workflow.

![**Fig. 1.** Workflow of stratified density-level conformal prediction (SDLC). Upper row: the location–scale density model $\hat f(y\,|\, x)$ and the target strata $B_1,\dots,B_K$ are fitted on the proper training set. Lower row: calibration scores are grouped by the stratum of the observed target and a conformal quantile $\hat q_k$ is computed in each stratum. The prediction set is the union over strata of the density level sets at the stratum's threshold, which guarantees coverage within every stratum in finite samples (Theorem 1).](/home/user/p_c1_2/Target_Journal_Submission/figures/F0_method_schematic.png){width=100%}


SDLC instantiates (3)–(4) with the plug-in score $s(x,y)=-\hat f(y\,|\, x)$, where $\hat f$ is estimated on $\mathcal{D}_{\mathrm{tr}}$; (5) holds for any $\hat f$. We use the semiparametric location–scale estimator
$$\hat f(y\,|\, x)=\frac{1}{\hat\sigma(x)}\,\hat g\!\left(\frac{y-\hat\mu(x)}{\hat\sigma(x)}\right). \qquad (8)$$
Here $\hat\mu$ is a gradient-boosted regression of $Y$ on $X$, and $\hat\sigma(x)=\max\{\tilde\sigma(x),\varsigma\}$, where $\tilde\sigma$ is a gradient-boosted regression of the absolute *out-of-fold* residuals $|Y-\hat\mu_{-j}(X)|$ (three folds), the spread estimate of locally weighted conformal prediction [@lei2018distribution]. The floor $\varsigma=\max\{10^{-3}\operatorname{sd}(Y_{\mathrm{tr}}),\,0.05\,\mathrm{median}|Y-\hat\mu_{-j}(X)|\}$ is shared by every method that uses $\hat\sigma$. The noise density is a defensive mixture
$$\hat g=(1-\epsilon)\,\hat g_{\mathrm{KDE}}+\epsilon\,t_2(\cdot/\hat s)/\hat s,\qquad \epsilon=0.01, \qquad (9)$$
of a Gaussian kernel density estimate (Silverman bandwidth) and a Student-$t_2$ density with robust scale $\hat s=\mathrm{IQR}/1.349$. The mixture is fitted to *cross-fitted* standardised residuals: the out-of-fold residuals of fold $j$ are divided by a scale model trained on the other two folds, so that neither $\hat\mu$ nor $\hat\sigma$ has seen the residual it standardises (an in-sample scale fit shrinks the residuals, in our data by a median factor of 1.14 in standard deviation). This choice affects efficiency only, not validity, and was not tuned. The defensive component gives $\hat g$ polynomial tails, so that far-out targets still receive a smooth, strictly decreasing density. The nonparametric $\hat g$ captures skewness and heavy tails of the errors, and heteroscedasticity enters through $\hat\sigma$. If $Y=\mu(X)+\sigma(X)\varepsilon$ with $\varepsilon$ independent of $X$, and $\epsilon$ and $\varsigma$ shrink to zero as $N$ grows, (8) can be uniformly consistent and Proposition 3 applies. Our implementation keeps $\epsilon=0.01$ and the floor fixed and truncates to the domain $D$, so Proposition 3 describes the limit of a sequence of such estimators, not the fixed-constant implementation itself. Otherwise SDLC targets the optimal sets of the best location–scale approximation, which affects size but never validity.

Three alternatives serve as ablations. SDLC-N replaces $\hat g$ by the standard normal density (with a unit-scale defensive $t_2$ component), so that its score differs from the normalised residual mainly through the factor $1/\hat\sigma(x)$; because $\hat\sigma$ estimates the mean absolute residual, this isolation is only approximate. An exploratory *two-piece* variant uses side-specific scales below and above $\hat\mu(x)$. A histogram density comes from a multiclass gradient-boosted classifier over 40 equal-mass target bins [cf. @sesia2021conformal; @guha2024conformal].

## 4.4 Implementation

*Strata.* The primary stratification uses the training-target quantiles $0.10, 0.25, 0.75, 0.90$ ($K=5$: lower tail, lower shoulder, bulk, upper shoulder, upper tail). With tied targets, coinciding cut points are merged, so realised strata can differ from the nominal ones; the sensitivity analyses repeat the main comparisons on datasets whose realised tail strata are close to nominal.

*Exact scores and the domain.* Calibration scores are computed exactly at the observed target, $S_i=-\hat f(Y_i\,|\, X_i)$. Sets are restricted to a bounded domain $D=[\min y-0.05r,\max y+0.05r]$ of the training targets ($r$ the training range), intersected with $[0,\infty)$ when all training targets are non-negative. A point with $Y\notin D$ receives the score $+\infty$, stays in its stratum, and counts as not covered. Membership of a test target is decided by the same exact rule, $Y_{n+1}\in\hat C(X_{n+1})$ iff $s(X_{n+1},Y_{n+1})\le\hat q_{k(Y_{n+1})}$, so the lower bound of Theorem 1 applies to the reported coverage, except that a test target outside $D$ always counts as a miss. When $\hat q_k=+\infty$ the reported set is $B_k\cap D$. We report the fraction of test targets outside $D$ and how often $\hat q_k=+\infty$ occurs.

*Set geometry.* Only the size, number of pieces, hull and tail alerts of a set are computed numerically. For a test point, $\hat C(x)\cap B_k=\{\hat\mu(x)+\hat\sigma(x)u:\hat g(u)\ge-\hat q_k\hat\sigma(x)\}\cap B_k$. We tabulate $\hat g$ on a non-uniform standardised grid with analytic $t$ tails, interpolate linearly, and split every cell exactly at the stratum boundaries and the bounds of $D$. A four times finer grid changes mean set sizes by at most 0.2% and individual set sizes by at most 1.5% (Supplementary Section S3, Table S4). The same construction is used for every location–scale baseline (DLS, DCP, HPD-split, S-HPD, SDLC-N).

**Algorithm 1.** Stratified density-level conformal prediction (SDLC).

> *Input:* proper training set $\mathcal{D}_{\mathrm{tr}}$; calibration set $\mathcal{D}_{\mathrm{cal}}$; stratum levels $\alpha_1,\dots,\alpha_K$; stratum probabilities (e.g. $0.10,0.25,0.75,0.90$).
> *Output:* prediction set $\hat C(x)$ for any test input $x$.
>
> 1. Fit the mean model $\hat\mu$ on $\mathcal{D}_{\mathrm{tr}}$ and compute three-fold out-of-fold residuals $Y-\hat\mu_{-j}(X)$.
> 2. Fit the scale model $\tilde\sigma$ on all absolute out-of-fold residuals and three cross-fitted scale models; set $\hat\sigma=\max\{\tilde\sigma,\varsigma\}$.
> 3. Standardise the out-of-fold residuals with the cross-fitted scales and fit the noise density $\hat g$ by Eq. (9); form $\hat f(y\,|\, x)$ by Eq. (8).
> 4. Compute the cut points from the training targets and define the strata $B_1,\dots,B_K$ and the domain $D$.
> 5. **for** each $(X_i,Y_i)\in\mathcal{D}_{\mathrm{cal}}$ **do** $S_i\leftarrow-\hat f(Y_i\,|\, X_i)$ if $Y_i\in D$, else $S_i\leftarrow+\infty$; assign $i$ to stratum $k(Y_i)$.
> 6. **for** $k=1,\dots,K$ **do** $\hat q_k\leftarrow$ the $\lceil (n_k+1)(1-\alpha_k)\rceil$-th smallest score in stratum $k$ (Eq. 3; $+\infty$ if this rank exceeds $n_k$).
> 7. **return** $\hat C(x)=\bigcup_{k}\{y\in B_k\cap D:\hat f(y\,|\, x)\ge-\hat q_k\}$, computed stratum-exactly on the standardised grid.

## 4.5 Computational complexity

Fitting (steps 1–3) requires eight gradient-boosted regressions: one mean model, three out-of-fold mean models, one scale model and three cross-fitted scale models. The kernel density estimate costs $O(N+G_g\log G_g)$ by linear binning and FFT convolution on $G_g$ grid points. Calibration (steps 5–6) costs $O(n\log n)$. Prediction (step 7) inverts the density level on each of the $R$ monotone runs of the piecewise-linear $\hat g$ (typically a handful) within each of the $K$ strata, at $O(KR\log G)$ per test point, so the prediction cost is linear in the number of test points, and one fit serves every $\alpha$. Wall-clock times are reported in Section 6.9.

## 4.6 Two practical variants

*Hull variant (SDLC-hull).* When an interval is required, the convex hull of $\hat C(x)$ is reported. It inherits (5), but not the upper bound of Theorem 1 or the optimality of Proposition 2.

*Floor variant (SDLC-floor).* A user may want the efficiency of a single marginal threshold while protecting rare strata at a lower level $1-\beta$. The set $\hat C_{\mathrm{floor}}(x)=\{y: s(x,y)\le\max(\hat q^{\mathrm{marg}}_\alpha,\hat q_{k(y)}(\beta))\}$, with $\hat q^{\mathrm{marg}}_\alpha$ the ordinary split-conformal quantile at level $\alpha$ and $\hat q_k(\beta)$ the stratified quantile (3) at level $\beta$, contains both the marginal set and the stratified set at level $\beta$, so it has marginal coverage $\ge 1-\alpha$ and stratum-wise coverage $\ge 1-\beta$ in finite samples; we use $\beta=2\alpha$. This simple, conservative rule is not a contribution; level-optimising schemes [@wang2023equal; @kiyani2024length] are principled alternatives.

## 4.7 Relevance-weighted coverage without strata: RW-DLC

Stratified calibration protects each stratum, but its protection ends at the resolution of the strata: outcomes in the top 1% lie inside the upper-tail stratum and are covered only on average with the rest of that stratum, and refining the strata quickly leaves too few calibration points per stratum. The imbalanced-regression literature describes the importance of outcomes not by strata but by a *relevance function* $\phi:\mathbb{R}\to(0,\infty)$, for example the inverse of the target density [@torgo2007utility; @steininger2021denseweight]. We therefore also consider *relevance-weighted coverage*
$$\operatorname{Cov}_\phi(C)=\frac{\mathbb{E}\big[\phi(Y)\,\mathbf{1}\{Y\in C(X)\}\big]}{\mathbb{E}[\phi(Y)]}, \qquad (10)$$
which, for $\phi=1/p_Y$, is coverage averaged uniformly over the range of the target, the continuous analogue of the macro-coverage that @bhattacharyya2026macro study for long-tailed classification. A stratum-wise guarantee for every stratum implies (10) for every $\phi$ that is constant on strata; (10) instead gives one averaged guarantee for a continuous relevance, without choosing strata.

Let $\phi$ be fixed given $\mathcal{D}_{\mathrm{tr}}$, let $S_i=s(X_i,Y_i)$ be the calibration scores with weights $\phi_i=\phi(Y_i)$ and $W=\sum_i\phi_i$, and define for a candidate $y$
$$q(y)=\inf\Big\{s:\ \sum_{i=1}^n\phi_i\,\mathbf{1}\{S_i\le s\}\ \ge\ (1-\alpha)\big(W+\phi(y)\big)\Big\},\qquad \hat C_\phi(x)=\{y:\ s(x,y)\le q(y)\}, \qquad (11)$$
with $q(y)=+\infty$ when no such $s$ exists. The candidate's own weight sits at $+\infty$, as in weighted conformal prediction under covariate shift [@tibshirani2019conformal] and label shift [@podkopaev2021distribution].

**Theorem 2 (relevance-weighted validity).** *If $(X_1,Y_1),\ldots,(X_n,Y_n),(X,Y)$ are i.i.d. given $\mathcal{D}_{\mathrm{tr}}$ and $0<\mathbb{E}\phi(Y)<\infty$, then $\mathbb{E}\big[\operatorname{Cov}_\phi(\hat C_\phi)\big]\ge 1-\alpha$, the expectation being over $\mathcal{D}_{\mathrm{cal}}$. Equivalently, $\hat C_\phi$ has coverage at least $1-\alpha$ for a test point drawn from the target-shifted law $Q$ with $dQ/dP=\phi(y)/\mathbb{E}\phi(Y)$.*

The proof (Appendix A) applies the weighted-exchangeability argument of @tibshirani2019conformal with the likelihood ratio $\phi(y)/\mathbb{E}\phi(Y)$, which depends only on the target. Two consequences matter in practice. First, (11) gives $q(y)=+\infty$ exactly when $\phi(y)>\alpha W/(1-\alpha)$: a candidate whose relevance exceeds the fraction $\alpha/(1-\alpha)$ of the total calibration relevance is always included. Rare targets are protected without strata, but only to the extent that the calibration set contains comparable relevance mass, which the Kish effective sample size $W^2/\sum_i\phi_i^2$ summarises. Second, Theorem 2 is also an exact guarantee under a target shift whose density ratio is proportional to $\phi$.

**Proposition 4 (size-optimal relevance-weighted sets).** *Under the density assumption of Proposition 2, among all set-valued functions with $\operatorname{Cov}_\phi(C)\ge1-\alpha$, the expected Lebesgue size $\mathbb{E}|C(X)|$ is minimised by $C^\star_\phi(x)=\{y:\ \phi(y)f(y\,|\, x)\ge t\}$, with $t$ chosen so that the constraint holds with equality (assuming the distribution of $\phi(Y)f(Y\,|\, X)$ has no atom at $t$).*

The proof is the Neyman–Pearson argument of Proposition 2 with the measure $\phi(y)f(y\,|\, x)\,dy\,dP_X$ in place of the stratum measure; its discrete counterpart for class-weighted coverage is given by @bhattacharyya2026macro. The proposition yields the score of *relevance-weighted density-level conformal prediction* (RW-DLC), $s(x,y)=-\phi(y)\hat f(y\,|\, x)$, calibrated by (11) and using the same density estimate (8) as SDLC. Relevance thus enters twice: it tilts the score towards relevant outcomes, which shapes the sets, and it weights the calibration, which delivers the guarantee. In the experiments $\phi$ is fitted on the training targets only, $\phi_U(y)=1/\max\{\hat p_Y(y),\tau\}$ ("uniform over the target range") or $\phi_H=\phi_U^{1/2}$, with $\hat p_Y$ a Gaussian kernel density estimate and $\tau=0.01\max_i\hat p_Y(Y_i)$ (Section 5).


# 5. Experimental design

The study answers six research questions (RQs), each tied to one experiment; a seventh (RQ7, Section 6.6) evaluates RW-DLC. The datasets, seeds, splits, miscoverage levels, strata, base learners, methods and analyses of the main benchmark were fixed in a version-controlled configuration before it was run (Section 5.7).

* **RQ1 (tail coverage).** Do marginal and covariate-adaptive methods under-cover rare target strata, and does stratified calibration restore stratum-wise coverage? *Experiment 1: main benchmark.*
* **RQ2 (price).** How much larger are the sets under stratum-wise validity, compared with marginal methods at the same and at a stricter level? *Experiment 2.*
* **RQ3 (score).** Does the density score of Proposition 2 give smaller stratified sets than other scores, and which component is responsible? *Experiment 3: ablation on real data, a synthetic study and a confirmatory replication.*
* **RQ4 (shift).** How robust is stratum-wise coverage under target shift? *Experiment 4.*
* **RQ5 (decisions).** Are prediction sets useful for flagging extreme outcomes, compared with dedicated conformal tail classifiers and conformal selection? *Experiment 5.*
* **RQ6 (robustness).** How sensitive are the conclusions to the miscoverage level, strata, calibration-set size, density estimator, base learner, imbalance-aware training and grouped splits? *Experiment 6.*

## 5.1 Datasets

The main benchmark uses the OpenML-CTR23 suite of 35 curated tabular regression datasets [@fischer2023openml]; using a complete external suite avoids selecting datasets that favour the proposed method. By a rule fixed in advance, we excluded the four datasets whose target takes fewer than 20 distinct values, because Lebesgue set size does not measure informativeness for such ordinal targets. Targets with heavy ties or atoms are retained, such as the burned area of forest fires, which is zero for 47.8% of the fires. The remaining 31 datasets (Supplementary Table S1) have 517 to 72,000 observations and 5 to 971 features after one-hot encoding; 15 have a target skewness above 1 in absolute value.

*Confirmatory datasets.* For the replication, we took the regression datasets of the tabular benchmark of @grinsztajn2022tree (OpenML suites 335 and 336), removed every dataset sharing source data with CTR23 and duplicate versions, and applied the same exclusion rule. This left 17 held-out datasets with up to 50,000 observations (Supplementary Table S2).

## 5.2 Splitting, leakage control and repetitions

Each of the 10 predefined seeds defines a random partition into proper training (50%), calibration (25%) and test (25%) sets; the replication uses five seeds. Every model, stratum boundary and density estimate uses the proper training set only. Several datasets contain repeated units, for example exact duplicate rows (9.1% of sarcos), repeated videos (video transcoding) and repeat sales (King County). The guarantees therefore refer to a new row from the same pool, not to a new unit (Supplementary Section S2, Table S3). Ten datasets were used during development or to diagnose the implementation (Section 5.7); the main comparisons are repeated without them.

## 5.3 Base learners

All methods share the same LightGBM models [@ke2017lightgbm] with one fixed configuration (learning rate 0.05, 31 leaves, up to 2000 rounds with early stopping on a 10% internal validation split): a mean model, quantile models (for CQR), the scale models of Algorithm 1, and a multiclass model over 40 target bins (histogram density). No method receives specific tuning. Experiment 6 adds a two-layer perceptron with the same pipeline and LightGBM trained with DenseWeight sample weights, which up-weight rare targets [@steininger2021denseweight].

## 5.4 Compared methods

*Marginal or covariate-adaptive calibration.* Split conformal prediction with absolute residuals (SCP) [@papadopoulos2002inductive]; normalised conformal prediction (NCP) [@lei2018distribution]; CQR [@romano2019conformalized]; Mondrian conformal regression with five bins of the point prediction (Mondrian-ŷ) [cf. @bostrom2020mondrian; @boruah2026distribution]; DCP [@chernozhukov2021distributional]; HPD-split [@izbicki2022cdsplit]; and density level sets with a single threshold (DLS) [cf. @lei2013distribution]. DCP, HPD-split and DLS use the same location–scale density as SDLC, so the comparison isolates the calibration rule.

*Stratified calibration.* BCCP [@randahl2026bin], the absolute-residual score with stratum-wise thresholds, in union and hull form (BCCP-hull); the normalised residual with stratum-wise thresholds (S-NCP), in union and hull form; stratified CQR (S-CQR); the HPD score with stratum-wise thresholds (S-HPD); and SDLC with its hull and floor ($\beta=2\alpha$) variants. S-CQR omits the level optimisation of @wang2023equal and is not an implementation of BFQR. S-NCP is the information-matched comparator of SDLC: both use the same $\hat\mu$ and $\hat\sigma$.

*Ablations.* The chain BCCP → S-NCP → SDLC-N → SDLC adds, in turn, the scale $\hat\sigma(x)$, the density weighting $1/\hat\sigma(x)$ and the estimated noise shape. The histogram and two-piece densities are secondary results.

*Tail-alert rules (Experiment 5).* A set raises an *upper-tail alert* when it intersects the upper stratum; for every method with stratum-wise coverage $1-\alpha$ the alert recall is at least $1-\alpha$. We compare such alerts with a class-conditional conformal tail classifier that thresholds $\hat P(Y\in B_K\,|\, x)$ from the location–scale model (TC-LS) or the histogram model (TC-H) to guarantee recall $1-\alpha$; conformal selection with Benjamini–Hochberg control of the false discovery rate at $q\in\{0.1,0.2\}$ [@jin2023selection]; and the naive rule "alert if $\hat\mu(x)$ is in the tail". All methods are evaluated from the same cached model outputs with the exact rules of Section 4.4.

## 5.5 Evaluation metrics

For each test set we report:

* marginal coverage and stratum-wise coverage (1) in each calibration stratum;
* coverage in strata *not* used for calibration (training-target deciles, the top and bottom 5% and 1%) and in deciles of $\hat\sigma(x)$, a diagnostic of covariate-conditional coverage;
* mean set size divided by the training-target standard deviation (normalised size), the share of empty sets and the number of disjoint pieces;
* tail-alert recall, alert rate, precision, and the expected cost per unit when a missed extreme outcome costs $r$ times a false alert;
* coverage under shift, by importance weighting of the test set: tilts $w(y)=\exp(\gamma z_y)$ ($\gamma\in\{1,2\}$), with $z_y$ the normal score of $y$ under the training distribution, and a *positive control* that multiplies the upper stratum by 5 and the lower by 0.5 without changing the within-stratum laws, so that Corollary 1(i) applies exactly. We report the Kish effective sample size of the weights.

Stratum coverages are averaged over seeds before taking the minimum across strata ("worst-stratum coverage"). Because a minimum over noisy estimates is biased downwards [cf. @boruah2026null], we also report a *null reference*: the worst-stratum coverage expected under exact validity given the realised stratum sizes (Monte Carlo over the Beta–binomial law of split-conformal coverage).

## 5.6 Statistical analysis

Following @demsar2006statistical, the unit of analysis is the dataset: metrics are averaged over seeds and methods are compared across datasets. Set sizes are compared on the log scale by the geometric-mean ratio with a 95% bootstrap confidence interval, the Hodges–Lehmann estimate, wins and losses, and the sign test. Paired comparisons use the Wilcoxon signed-rank test with Holm's correction within each family [@holm1979simple]. One-sided tests are used only for the hypothesis that stratified calibration improves worst-stratum and tail coverage over marginal methods; comparisons among stratified methods are two-sided. Equivalence of worst-stratum coverage is assessed by two one-sided Wilcoxon tests (TOST) with a margin of 0.01. Friedman mean ranks are descriptive only [@benavoli2016should].

## 5.7 Protocol, deviations and confirmatory replication

*What was fixed in advance.* The configuration of the main benchmark, the primary method and directional expectations for RQ1–RQ6 were committed to version control before the benchmark was run, but not registered with a third party.

*What changed afterwards.* (1) A loader bug that parsed string-typed features as missing was corrected and the affected datasets recomputed. (2) After the first run we learned of BCCP and BFQR; BCCP's hull form, decile strata and tail-alert metrics were added. (3) The first implementation evaluated density-based sets on a coarse grid of the *marginal* target distribution, which inflated them; under it the size comparison with BCCP was not significant (Supplementary Section S5). (4) A review of the second run led to corrections applied to every method: cross-fitted standardisation, a defensive $t$ component instead of an ad hoc floor, half-open stratum pieces, a truncated domain and stratum-exact geometry. All reported results use the final implementation.

*Consequences.* Because the implementation changed after results had been seen, every size comparison on CTR23 (RQ3) is exploratory; the coverage results are unaffected in direction. To test the size comparisons, we committed a confirmatory analysis plan (hypotheses, tests, decision rules and script; Supplementary Section S6) to version control (commit `ccba99b`) *before* evaluating any conformal method on the 17 held-out datasets. The time stamp is that of our repository, not of a third-party registry, so we call the plan pre-specified rather than pre-registered; base-model test metrics had already been computed on these datasets. Section 6.5 reports the outcome.

*Relevance-weighted study.* RW-DLC was added after review of an earlier version. Its analysis plan (relevance functions, comparators, metrics, hypotheses RW-1 to RW-4, tests and decision rules; Supplementary Section S7) was committed (commit `a9f31d2`) before RW-DLC was evaluated on any dataset. RW-DLC, its ablations RW-DLS (score $-\hat f$) and RW-NCP (normalised residual), both with relevance-weighted calibration, and the comparators SCP, NCP, CQR, DLS-M, S-NCP and SDLC were evaluated on a grid of 4,000 target values over $D$, with coverage decided by the exact rule. Additional metrics are the relevance-weighted coverage (10), the mean and minimum coverage over training-target deciles, and coverage of the top and bottom 1%.

## 5.8 Use of a large language model

In line with the journal's policy, we document that a large language model (Claude, Anthropic) was used as a research assistant in this study: to search and verify the literature, to write and test code, to orchestrate the computational experiments, to draft and edit the text, and to produce simulated adversarial reviews of the drafts. The model did not generate any data or result. Every number, table and figure in the paper is produced by the released code from public data (Section 5.7), and every reference was checked against its publisher or index record. The authors checked the analyses and the text and take full responsibility for the content.


# 6. Results

All results refer to $\alpha=0.1$ and five strata unless stated otherwise. Each of the 31 datasets contributes the mean over its 10 splits (310 runs). Table 3 summarises the main benchmark, and Fig. 9 shows sets for one dataset.

**Table 3.** Main benchmark ($\alpha=0.1$; means over 31 datasets of the seed-averaged values). *Lower/upper tail*: coverage of the lowest/highest calibration stratum; *worst stratum*: minimum over strata of the seed-averaged stratum coverage; *below null*: number of datasets whose worst-stratum coverage is below the 5% quantile of its exact-validity null reference (5% of datasets expected by chance); *top 5% / top 1%*: coverage of targets above the training 95%/99% quantile (not calibrated); *size*: geometric mean over datasets of the mean normalised set size; *empty %*: share of empty sets; *pieces*: mean number of disjoint intervals.

| Method     | Marginal   | Lower tail   | Upper tail   | Worst stratum   | Below null   | Top 5%   | Top 1%   | Size   | Empty %   | Pieces   |
|:-----------|:-----------|:-------------|:-------------|:----------------|:-------------|:---------|:---------|:-------|:----------|:---------|
| SCP        | 0.903      | 0.865        | 0.690        | 0.630           | 30           | 0.598    | 0.445    | 0.763  | 0.02      | 1.00     |
| NCP        | 0.903      | 0.855        | 0.812        | 0.765           | 27           | 0.756    | 0.650    | 0.769  | 0.08      | 1.00     |
| CQR        | 0.903      | 0.808        | 0.759        | 0.720           | 29           | 0.671    | 0.481    | 0.927  | 0.04      | 1.00     |
| Mondrian-ŷ | 0.905      | 0.827        | 0.811        | 0.770           | 28           | 0.735    | 0.533    | 0.787  | 0.07      | 1.00     |
| DCP        | 0.902      | 0.853        | 0.820        | 0.783           | 26           | 0.770    | 0.655    | 0.781  | 0.08      | 1.00     |
| HPD-split  | 0.903      | 0.857        | 0.809        | 0.759           | 27           | 0.756    | 0.655    | 0.779  | 0.08      | 1.10     |
| DLS        | 0.902      | 0.854        | 0.723        | 0.660           | 31           | 0.631    | 0.465    | 0.703  | 0.74      | 1.10     |
| BCCP       | 0.904      | 0.906        | 0.908        | 0.890           | 2            | 0.863    | 0.687    | 0.969  | 0.01      | 1.47     |
| S-NCP      | 0.904      | 0.905        | 0.907        | 0.891           | 2            | 0.880    | 0.789    | 0.897  | 0.07      | 1.29     |
| S-CQR      | 0.905      | 0.907        | 0.907        | 0.892           | 2            | 0.854    | 0.698    | 1.100  | 0.05      | 1.49     |
| S-HPD      | 0.904      | 0.906        | 0.907        | 0.893           | 1            | 0.879    | 0.790    | 0.923  | 0.06      | 1.49     |
| SDLC-N     | 0.905      | 0.905        | 0.909        | 0.893           | 1            | 0.876    | 0.766    | 0.881  | 0.19      | 1.29     |
| SDLC       | 0.903      | 0.903        | 0.906        | 0.891           | 2            | 0.868    | 0.736    | 0.874  | 0.36      | 1.53     |


## 6.1 Marginal and covariate-adaptive methods under-cover the tails (RQ1)

All methods attained their nominal marginal coverage, but coverage of the target strata differed sharply. The seven marginal or covariate-adaptive methods covered 69.0%–82.0% of the upper-tail targets and 44.5%–65.5% of the top 1%, and their worst-stratum coverage was 63.0%–78.3%. On 26–31 of the 31 datasets, it was below the range expected under exact validity. Marginal methods over-cover the central deciles and pay for it in the outer ones (Fig. 2); covariate adaptivity reduces the shortfall but does not remove it. Every stratified method, in contrast, covered 90.6%–90.9% of the upper tail, with worst-stratum coverage 89.0%–89.3%, and was below the null range on at most 2 datasets, as expected under exact validity. SDLC's worst-stratum coverage exceeded that of each marginal method on at least 29 of 31 datasets (one-sided Holm-adjusted $p\le$ < 0.001; Hodges–Lehmann differences 0.081–0.250). The result is unchanged without the development datasets ($p\le$ < 0.001) and for upper-tail coverage alone ($p\le$ < 0.001). SDLC covered 86.8% of the top 5% and 73.6% of the top 1%, against at most 77.0% and 65.5% for the marginal methods; the top 1% is not calibrated, and its coverage stays below the nominal level for every method.

![**Fig. 2.** Coverage by decile of the training-target distribution (means over 31 datasets with 95% confidence bands, $\alpha=0.1$). Marginal methods (SCP, CQR, HPD-split) over-cover the centre and under-cover the outer deciles; stratified calibration (S-NCP, SDLC) flattens the profile. The residual dip in deciles 2 and 9 lies inside the broad shoulder strata.](/home/user/p_c1_2/Target_Journal_Submission/figures/F3_decile_coverage_profile.png){width=100%}


## 6.2 The price of stratum-wise validity (RQ2)

Stratum-wise validity enlarges the sets (Table 4). Holding the score fixed, stratified calibration increased the geometric-mean size by factors of 1.17 (normalised residual) to 1.27 (absolute residual). For SDLC relative to the single-threshold density level set (DLS) the factor was 1.24 (1.12–1.45), with a median of 1.11, for a gain in worst-stratum coverage of 0.231 (between 0.126 and 0.260 across scores). The price exceeded 1.5 on only 3 datasets for SDLC (Section 6.10).

A fairer comparison is with marginal sets that buy tail coverage by lowering $\alpha$ (Table 5). At $\alpha=0.05$ every marginal method still had a lower worst-stratum coverage (0.772–0.878) than SDLC at $\alpha=0.1$ (0.891), and SDLC's sets were smaller than theirs on 23–28 of the 31 datasets. Calibrating within strata thus gives more tail coverage for less size than raising the overall level.

**Table 4.** Price of stratum-wise validity: size of each score under stratified relative to marginal calibration (geometric mean over datasets with 95% bootstrap CI, median ratio, number of datasets with ratio > 1.5) and the gain in worst-stratum coverage.

| Score             | Size ratio [95% CI]   | Median ratio   | Datasets > 1.5   | Worst-stratum gain   |
|:------------------|:----------------------|:---------------|:-----------------|:---------------------|
| SCP → BCCP        | 1.27 [1.10, 1.52]     | 1.10           | 4                | +0.260               |
| NCP → S-NCP       | 1.17 [1.05, 1.36]     | 1.05           | 1                | +0.126               |
| CQR → S-CQR       | 1.19 [1.08, 1.35]     | 1.08           | 2                | +0.172               |
| HPD-split → S-HPD | 1.18 [1.07, 1.38]     | 1.06           | 1                | +0.134               |
| DLS → SDLC        | 1.24 [1.12, 1.45]     | 1.11           | 3                | +0.231               |
| DLS-N → SDLC-N    | 1.24 [1.12, 1.45]     | 1.15           | 2                | +0.187               |


**Table 5.** Marginal methods at $\alpha=0.05$ against SDLC at $\alpha=0.1$: worst-stratum coverage, geometric-mean size, and the number of datasets on which SDLC's sets are smaller. SDLC at $\alpha=0.1$: worst stratum 0.891, size 0.874.

| Marginal method (α = 0.05)   | Worst stratum   | Size   | SDLC (α = 0.1) smaller on   |
|:-----------------------------|:----------------|:-------|:----------------------------|
| SCP                          | 0.772           | 1.053  | 25/31                       |
| NCP                          | 0.858           | 1.005  | 28/31                       |
| CQR                          | 0.808           | 1.374  | 26/31                       |
| Mondrian-ŷ                   | 0.866           | 1.070  | 26/31                       |
| DCP                          | 0.878           | 1.017  | 27/31                       |
| HPD-split                    | 0.863           | 1.030  | 28/31                       |
| DLS                          | 0.819           | 0.937  | 23/31                       |


## 6.3 The density score gives the smallest stratum-valid sets (RQ3)

Among the stratified methods, which all had equivalent worst-stratum coverage (TOST with margin 0.01: $p\le$ < 0.001 for every comparison with SDLC), SDLC produced the smallest sets (Table 6, Fig. 3). Its sets were smaller than those of BCCP on 24 of 31 datasets (geometric-mean ratio 0.902, 95% CI 0.841–0.956; Holm-adjusted $p$ < 0.001), than those of stratified CQR on 27 (ratio 0.795) and than those of S-HPD on 28 (ratio 0.947). Against the information-matched S-NCP, SDLC was smaller on 27 datasets (Holm $p$ < 0.001; Hodges–Lehmann ratio 0.962), but the gain was small and its geometric-mean ratio, 0.975 (0.941–1.020), was pulled towards one by a few datasets with large losses (Section 6.10). The Hodges–Lehmann ratio, which describes the typical dataset, is our primary size estimand. Post hoc, equivalence within ±5% was not established with S-NCP (TOST $p$ = 0.108) or S-HPD ($p$ = 0.284), and SDLC's sets were reliably smaller than S-NCP's (seed-level 95% interval below zero) on 18 datasets and reliably larger on 0. When an interval is required, SDLC-hull was smaller than BCCP-hull (ratio 0.903, 25/6), whereas against S-NCP-hull the median favoured SDLC-hull (23/8, Hodges–Lehmann ratio 0.979) and the geometric mean did not (1.014). These comparisons are exploratory (Section 5.7); Section 6.5 tests them on held-out data.

SDLC remained smaller than all four stratified comparators without the development datasets, on the 26 datasets with near-nominal tail strata, at other $\alpha$ and with three or ten strata (Holm $p\le$ 0.002; Supplementary Table S5). Two subsets were less clear. On the 9 datasets with fewer than 1,600 observations no stratified score was consistently better (SDLC vs S-NCP: 5/4). On the 15 strongly skewed datasets, the advantage over S-NCP (12/3, Holm $p$ = 0.127) and S-CQR ($p$ = 0.127) was not significant.

**Table 6.** Set-size comparisons among stratified methods ($\alpha=0.1$): geometric-mean ratio of mean set sizes over 31 datasets with 95% bootstrap CI, Hodges–Lehmann ratio, wins/losses of the first method, and Holm-adjusted two-sided Wilcoxon $p$ within each family. All comparisons on CTR23 are exploratory (Section 5.7).

| Family             | Comparison              | Ratio [95% CI]       | HL ratio   | Wins/losses   | Holm p   |
|:-------------------|:------------------------|:---------------------|:-----------|:--------------|:---------|
| Score (stratified) | SDLC vs BCCP            | 0.902 [0.841, 0.956] | 0.933      | 24/7          | < 0.001  |
| Score (stratified) | SDLC vs S-NCP           | 0.975 [0.941, 1.020] | 0.962      | 27/4          | < 0.001  |
| Score (stratified) | SDLC vs S-CQR           | 0.795 [0.702, 0.878] | 0.827      | 27/4          | < 0.001  |
| Score (stratified) | SDLC vs S-HPD           | 0.947 [0.929, 0.963] | 0.953      | 28/3          | < 0.001  |
| Density estimator  | SDLC vs SDLC-2p         | 0.992 [0.976, 1.005] | 0.998      | 17/14         | 0.581    |
| Density estimator  | SDLC vs SDLC-hist       | 0.501 [0.391, 0.622] | 0.543      | 28/3          | < 0.001  |
| Decomposition      | S-NCP vs BCCP           | 0.926 [0.842, 0.995] | 0.973      | 18/13         | 0.111    |
| Decomposition      | SDLC-N vs S-NCP         | 0.982 [0.948, 1.029] | 0.970      | 26/5          | < 0.001  |
| Decomposition      | SDLC vs SDLC-N          | 0.993 [0.985, 0.999] | 0.994      | 23/8          | 0.068    |
| Hull forms         | SDLC-hull vs BCCP-hull  | 0.903 [0.826, 0.980] | 0.925      | 25/6          | 0.002    |
| Hull forms         | SDLC-hull vs S-NCP-hull | 1.014 [0.959, 1.089] | 0.979      | 23/8          | 0.034    |


![**Fig. 3.** Worst-stratum coverage against set size ($\alpha=0.1$; means over datasets; size as geometric mean). Marginal methods (grey) lie to the left of the target line; stratified methods (green) reach it, and SDLC (blue) does so with the smallest sets.](/home/user/p_c1_2/Target_Journal_Submission/figures/F2_coverage_size_tradeoff.png){width=100%}


*Where the gain comes from* (Table 6, Fig. 4). Adding the scale $\hat\sigma(x)$ (BCCP → S-NCP) reduced size on average (ratio 0.926) but not consistently (18/13 datasets, $p$ = 0.111). Adding the factor $1/\hat\sigma(x)$ (S-NCP → SDLC-N) reduced size on 26 of 31 datasets ($p$ < 0.001). Estimating the noise shape (SDLC-N → SDLC) added a smaller, less consistent reduction (ratio 0.993, 23/8, $p$ = 0.068). The two-piece density did not improve on the symmetric one (0.881 vs 0.874), and the histogram density was far less efficient (1.745). The advantage over S-NCP is therefore mostly the coverage reallocation of Section 4: wider sets for low-noise inputs, narrower ones for high-noise inputs.

![**Fig. 4.** Decomposition of the size advantage: per-dataset size ratios of successive score changes (points) and their geometric means (bars). Adding $\hat\sigma$ (left) helps on average but not consistently; the density weighting $1/\hat\sigma$ (centre) gives a small, consistent reduction; the estimated noise shape (right) adds little.](/home/user/p_c1_2/Target_Journal_Submission/figures/F11_decomposition.png){width=100%}


*What the gain costs.* The reallocation has the price the theory predicts. The worst coverage over deciles of $\hat\sigma(x)$ was 0.769 for SDLC against 0.793 for S-NCP (Fig. 5). SDLC returned empty sets for 0.36% of test points (S-NCP 0.07%), concentrated on the noisiest inputs of high-$R^2$ datasets. SDLC also covered fewer of the most extreme outcomes than S-NCP and S-HPD: 0.736 of the top 1% against 0.789 and 0.790 (Holm $p$ = 0.031 and 0.017). It covered more than BCCP and S-CQR (0.687 and 0.698). Within the calibrated strata these differences cancel.

![**Fig. 5.** Coverage by decile of the estimated scale $\hat\sigma(x)$ ($\alpha=0.1$; means over datasets). The density scores (SDLC, and the single-threshold DLS) spend less coverage on the noisiest inputs than the normalised residual (S-NCP); BCCP, without a scale, over-covers low-noise and under-covers high-noise inputs.](/home/user/p_c1_2/Target_Journal_Submission/figures/F12_scale_decile_coverage.png){width=100%}


## 6.4 Synthetic study with known densities

Five synthetic designs with known densities (Table 7; skewed, covariate-dependent skewness, bimodal (C), heavy-tailed, zero-inflated) separate the score from its estimate. With the true density, the oracle SDLC set was smaller than the oracle normalised residual in every design, by 2.9% to 35.2%. The estimated SDLC was smaller than S-NCP in 41 of 50 design-seed combinations, but under the misspecified design C its sets were 53.2% larger than the oracle's. Under a genuine label shift (Supplementary Table S10), all stratified methods degraded similarly.

**Table 7.** Synthetic study ($n_{\mathrm{train}}=n_{\mathrm{cal}}=5000$, 10 seeds, $\alpha=0.1$, 20,000 test points per seed). Each cell: coverage of the upper stratum / mean set size relative to S-NCP. Oracle methods (O-) use the true conditional density or the true $\mu$ and $\sigma$; O-HDR-X is the shortest set with exact covariate-conditional coverage. Design E has no density, hence no oracle.

| Method    | A             | B             | C             | D             | E             |
|:----------|:--------------|:--------------|:--------------|:--------------|:--------------|
| O-HDR-X   | 0.693 / 0.804 | 0.841 / 0.920 | 0.897 / 0.672 | 0.832 / 0.889 |               |
| O-SDLC    | 0.897 / 0.860 | 0.903 / 0.907 | 0.903 / 0.643 | 0.907 / 0.914 |               |
| O-S-NCP   | 0.897 / 0.904 | 0.898 / 0.938 | 0.909 / 0.993 | 0.906 / 0.941 |               |
| O-S-Res   | 0.894 / 1.023 | 0.898 / 1.026 | 0.911 / 1.211 | 0.904 / 1.000 |               |
| SCP       | 0.709 / 0.978 | 0.806 / 1.041 | 0.865 / 1.114 | 0.813 / 0.994 | 0.370 / 0.963 |
| CQR       | 0.694 / 1.020 | 0.752 / 1.071 | 0.795 / 1.080 | 0.758 / 1.087 | 0.556 / 0.751 |
| HPD-split | 0.675 / 0.906 | 0.814 / 0.983 | 0.883 / 0.993 | 0.818 / 0.951 | 0.590 / 0.776 |
| BCCP      | 0.893 / 1.066 | 0.899 / 1.070 | 0.894 / 1.122 | 0.901 / 1.055 | 0.902 / 1.631 |
| S-NCP     | 0.895 / 1.000 | 0.894 / 1.000 | 0.902 / 1.000 | 0.901 / 1.000 | 0.893 / 1.000 |
| S-CQR     | 0.891 / 1.091 | 0.896 / 1.075 | 0.899 / 1.069 | 0.902 / 1.131 | 0.903 / 1.018 |
| S-HPD     | 0.896 / 0.997 | 0.894 / 1.000 | 0.902 / 1.000 | 0.901 / 1.000 | 0.893 / 0.983 |
| SDLC-N    | 0.893 / 0.981 | 0.896 / 0.985 | 0.895 / 0.983 | 0.901 / 0.990 | 0.896 / 0.989 |
| SDLC      | 0.894 / 0.966 | 0.898 / 0.986 | 0.894 / 0.986 | 0.903 / 0.992 | 0.896 / 0.912 |


## 6.5 Confirmatory replication on held-out datasets

On the 17 held-out datasets, analysed exactly as pre-specified (Supplementary Section S6), all four hypotheses were supported (Table 8).

* *C-H1 (tail coverage).* SDLC's worst-stratum coverage exceeded that of each of the seven marginal and covariate-adaptive methods (Holm $p$ < 0.001).
* *C-H2 (validity).* Its worst-stratum coverage fell below the 5% quantile of the exact-validity null reference on 1 of 17 datasets (critical value 3).
* *C-H3 (set size).* SDLC's sets were smaller than those of BCCP (geometric-mean ratio 0.862, 14/3 datasets, Holm $p$ = 0.001), S-CQR (0.841, 15/2, $p$ < 0.001), S-NCP (0.977, 15/2, $p$ = 0.008) and S-HPD (0.984, 15/2, $p$ = 0.008). By the pre-specified rule (signed-rank test plus direction of the geometric-mean ratio), every comparison favours SDLC. The gains over S-NCP and S-HPD are small: the bootstrap intervals of their geometric-mean ratios (0.940–1.028 and 0.963–1.014) include one, although the reduction occurs on most datasets.
* *C-H4 (equivalence).* The worst-stratum coverage of SDLC was equivalent to that of S-NCP and BCCP within 0.02 (TOST $p$ < 0.001 and < 0.001).

C-H1, C-H2 and C-H4 follow from Theorem 1 and check the implementation; only C-H3 could have failed for empirical reasons.

The secondary results repeated the trade-off seen on CTR23. SDLC covered 0.747 of the top 1%, against 0.781 for S-NCP, and its worst coverage over deciles of $\hat\sigma(x)$ was 0.817, against 0.831. The price of stratification relative to DLS was 1.22. The pre-specified secondary analyses (Supplementary Table S17) were less favourable for the interval forms: SDLC-hull was smaller than BCCP-hull (ratio 0.894, Holm $p$ = 0.013) but not than S-NCP-hull (ratio 1.045, 10/7 datasets, $p$ = 0.712). Post hoc, SDLC was equivalent to S-HPD within ±5% (TOST $p$ = 0.004), equivalence with S-NCP narrowly failed ($p$ = 0.054), and SDLC was reliably smaller than S-NCP on 8 of 17 datasets and reliably larger on 1. On the 7 held-out targets with $|$skewness$|>1$, the advantage over S-NCP and S-HPD disappeared (ratios 1.017 and 1.004), while that over BCCP and S-CQR remained (Supplementary Table S18). Among scores that use $\hat\sigma$, the choice matters little for size; the clear gains are over BCCP and stratified CQR.

**Table 8.** Pre-specified confirmatory replication on 17 held-out datasets (5 seeds each, $\alpha=0.1$, five strata). Effects: Hodges–Lehmann difference of worst-stratum coverage (C-H1), geometric-mean size ratio with 95% bootstrap CI (C-H3), median difference (C-H4). Decisions follow the rules fixed before evaluation.

| Hypothesis                                               | Comparison         | Effect                     | Wins/losses   | Holm p         | Decision     |
|:---------------------------------------------------------|:-------------------|:---------------------------|:--------------|:---------------|:-------------|
| C-H1 worst-stratum coverage (one-sided)                  | SDLC vs SCP        | HL difference +0.354       | 17/0          | < 0.001        | supported    |
| C-H1 worst-stratum coverage (one-sided)                  | SDLC vs NCP        | HL difference +0.288       | 16/1          | < 0.001        | supported    |
| C-H1 worst-stratum coverage (one-sided)                  | SDLC vs CQR        | HL difference +0.259       | 17/0          | < 0.001        | supported    |
| C-H1 worst-stratum coverage (one-sided)                  | SDLC vs Mondrian-ŷ | HL difference +0.307       | 17/0          | < 0.001        | supported    |
| C-H1 worst-stratum coverage (one-sided)                  | SDLC vs DCP        | HL difference +0.188       | 16/1          | < 0.001        | supported    |
| C-H1 worst-stratum coverage (one-sided)                  | SDLC vs HPD-split  | HL difference +0.203       | 16/1          | < 0.001        | supported    |
| C-H1 worst-stratum coverage (one-sided)                  | SDLC vs DLS        | HL difference +0.270       | 17/0          | < 0.001        | supported    |
| C-H2 validity (datasets below null 5% quantile)          | SDLC               | 1 of 17 (critical value 3) |               | binomial 0.582 | consistent   |
| C-H3 set size (two-sided)                                | SDLC vs BCCP       | ratio 0.862 [0.785, 0.932] | 14/3          | 0.001          | favours SDLC |
| C-H3 set size (two-sided)                                | SDLC vs S-NCP      | ratio 0.977 [0.940, 1.028] | 15/2          | 0.008          | favours SDLC |
| C-H3 set size (two-sided)                                | SDLC vs S-CQR      | ratio 0.841 [0.730, 0.931] | 15/2          | < 0.001        | favours SDLC |
| C-H3 set size (two-sided)                                | SDLC vs S-HPD      | ratio 0.984 [0.963, 1.014] | 15/2          | 0.008          | favours SDLC |
| C-H4 equivalence of worst-stratum coverage (margin 0.02) | SDLC vs S-NCP      | median difference -0.0000  |               | TOST < 0.001   | equivalent   |
| C-H4 equivalence of worst-stratum coverage (margin 0.02) | SDLC vs BCCP       | median difference -0.0015  |               | TOST < 0.001   | equivalent   |


## 6.6 Relevance-weighted coverage of the most extreme outcomes (RQ7)

Stratified calibration left the most extreme outcomes under-covered (top-1% coverage of SDLC 0.688 on the held-out datasets). RW-DLC was evaluated under its own pre-specified plan (Section 5.7); Table 9 reports the held-out datasets (17 datasets, 85 runs) and Supplementary Table S19 the CTR23 datasets.

* *RW-1 (validity).* The relevance-weighted coverage of RW-DLC was 0.898 on average, equivalent to the nominal 0.90 within the pre-specified margin of 0.02 (TOST $p$ < 0.001), as Theorem 2 predicts.
* *RW-2 (marginal methods miss the weighted target).* RW-DLC exceeded every marginal method in relevance-weighted coverage, by 0.122 (NCP) to 0.180 (DLS-M) on average (largest Holm-adjusted $p$ < 0.001).
* *RW-3 (extreme tail).* RW-DLC covered 0.872 of the top 1% of outcomes, against 0.688 for SDLC (mean difference 0.184, 95% CI 0.063–0.310, higher on 13 of 15 datasets with top-1% test points, one-sided $p$ = 0.011).
* *RW-4 (score).* RW-DLC's sets were smaller than those of the two ablations that use relevance-weighted calibration with an unweighted score, RW-DLS (geometric-mean ratio 0.885) and RW-NCP (0.904), but after Holm correction neither difference reached the pre-specified threshold ($p$ = 0.053 for both), so RW-4 was not supported.

The guarantee has a price elsewhere. Because RW-DLC averages coverage over the target range, it spends less on the bulk: its marginal coverage was 0.884 (minimum over datasets 0.750) and its worst coverage over target deciles was lower than that of SDLC (mean difference -0.080). Its sets were not reliably larger than SDLC's (geometric-mean ratio 1.081, 95% CI 0.916–1.240, descriptive). No test point had an infinite threshold; the smallest effective calibration sample size was 120 (median 1,368). The milder relevance $\phi_H$ gave intermediate results. RW-DLC and SDLC thus answer different requirements: SDLC guarantees every stratum, and RW-DLC guarantees an average over the whole target range that reaches the outcomes beyond the strata (Fig. 6).

**Table 9.** Relevance-weighted study on the 17 held-out datasets ($\alpha=0.1$, 5 seeds; means over datasets). Relevance-weighted coverage uses $\phi_U=1/\max(\hat p_Y,\tau)$; deciles and the top 1% refer to the training-target distribution; size is the arithmetic mean over datasets of the mean set size in units of the training-target standard deviation. RW-DLS and RW-NCP are ablations with relevance-weighted calibration and unweighted scores.

| Method   | Marginal cov.   | Relevance-weighted cov. (φ_U)   | Mean decile cov.   | Worst decile cov.   | Top-1% cov.   | Size / sd(y)   |
|:---------|:----------------|:--------------------------------|:-------------------|:--------------------|:--------------|:---------------|
| SCP      | 0.901           | 0.718                           | 0.894              | 0.510               | 0.406         | 1.741          |
| NCP      | 0.900           | 0.776                           | 0.896              | 0.610               | 0.533         | 1.636          |
| CQR      | 0.901           | 0.746                           | 0.896              | 0.614               | 0.362         | 1.721          |
| DLS-M    | 0.901           | 0.717                           | 0.894              | 0.560               | 0.368         | 1.581          |
| S-NCP    | 0.902           | 0.856                           | 0.900              | 0.825               | 0.730         | 2.103          |
| SDLC     | 0.900           | 0.835                           | 0.900              | 0.808               | 0.688         | 2.114          |
| RW-NCP-U | 0.953           | 0.900                           | 0.950              | 0.815               | 0.784         | 2.549          |
| RW-DLS-U | 0.965           | 0.901                           | 0.960              | 0.845               | 0.805         | 2.537          |
| RW-DLC-U | 0.884           | 0.898                           | 0.885              | 0.728               | 0.872         | 2.410          |
| RW-DLC-H | 0.919           | 0.862                           | 0.914              | 0.737               | 0.748         | 1.958          |


![**Fig. 6.** Coverage of the top 1% of outcomes against set size ($\alpha=0.1$; geometric-mean size over datasets). Marginal methods cover the extremes poorly; stratified methods (S-NCP, SDLC) improve them but stay below the nominal level; RW-DLC with $\phi_U$ approaches the nominal level at a size comparable to the stratified methods.](/home/user/p_c1_2/Target_Journal_Submission/figures/F14_rw_top1_vs_size.png){width=100%}


## 6.7 Target shift (RQ4)

Under the positive control, which re-weights whole strata, the stratum-wise coverage of every stratified method was unchanged, as Corollary 1(i) states (Table 10, Fig. 7). Their marginal coverage stayed at the nominal level (0.904 for SDLC), whereas that of the marginal methods fell to 0.838–0.877. Continuous tilts towards the upper tail also re-weight targets *within* strata, so Corollary 1(i) does not apply. Under a moderate tilt ($\gamma=1$) the stratified methods kept 0.861–0.881 coverage of the upper stratum, against 0.633–0.783 for the marginal methods. Under a strong tilt ($\gamma=2$) every method lost coverage. The stratified methods lost less (0.770–0.833, against 0.550–0.726). Among them, SDLC (0.798) was below S-NCP and S-HPD (0.833), which is the same reallocation away from the most extreme outcomes seen above. The effective sample size of the $\gamma=2$ weights was small (median 49, minimum 5.9), but restricting the analysis to the 15 datasets where it was at least 50 left the ordering unchanged.

**Table 10.** Coverage under target shift ($\alpha=0.1$; means over datasets). *Positive control*: the upper stratum is up-weighted by 5 and the lower stratum down-weighted by 0.5, without changing the within-stratum laws. *Tilts*: importance weights $\exp(\gamma z_y)$ with $z_y$ the normal score of $y$ under the training distribution; the coverage of the upper calibration stratum is shown for all datasets and for the 15 datasets whose effective sample size is at least 50.

| Method     | Positive control: marginal   | Positive control: worst stratum   | Tilt γ=1: upper stratum   | Tilt γ=2: upper stratum   | Tilt γ=2: upper (ESS ≥ 50)   | Tilt γ=2: marginal   |
|:-----------|:-----------------------------|:----------------------------------|:--------------------------|:--------------------------|:-----------------------------|:---------------------|
| SCP        | 0.838                        | 0.630                             | 0.633                     | 0.550                     | 0.532                        | 0.637                |
| NCP        | 0.875                        | 0.765                             | 0.776                     | 0.720                     | 0.751                        | 0.766                |
| CQR        | 0.861                        | 0.720                             | 0.695                     | 0.596                     | 0.624                        | 0.668                |
| Mondrian-ŷ | 0.877                        | 0.770                             | 0.750                     | 0.654                     | 0.649                        | 0.717                |
| DCP        | 0.877                        | 0.783                             | 0.783                     | 0.726                     | 0.765                        | 0.770                |
| HPD-split  | 0.874                        | 0.759                             | 0.773                     | 0.719                     | 0.748                        | 0.765                |
| DLS        | 0.848                        | 0.660                             | 0.664                     | 0.577                     | 0.530                        | 0.658                |
| BCCP       | 0.904                        | 0.890                             | 0.861                     | 0.777                     | 0.754                        | 0.803                |
| S-NCP      | 0.904                        | 0.891                             | 0.881                     | 0.833                     | 0.825                        | 0.847                |
| S-CQR      | 0.905                        | 0.892                             | 0.859                     | 0.770                     | 0.761                        | 0.797                |
| S-HPD      | 0.905                        | 0.893                             | 0.881                     | 0.833                     | 0.825                        | 0.846                |
| SDLC-N     | 0.906                        | 0.893                             | 0.877                     | 0.816                     | 0.795                        | 0.833                |
| SDLC       | 0.904                        | 0.891                             | 0.869                     | 0.798                     | 0.774                        | 0.819                |


![**Fig. 7.** Coverage under shift ($\alpha=0.1$; means over datasets): marginal coverage (left) and coverage of the upper stratum (right) under the positive control and upward tilts.](/home/user/p_c1_2/Target_Journal_Submission/figures/F6_shift.png){width=100%}


## 6.8 Tail alerts and decisions (RQ5)

Every stratified method guarantees an upper-tail alert recall of at least 0.9; their mean recall was 0.978–0.988, and it was at least 0.9 on all 31 datasets (Table 11). The price is a high alert rate. Among the stratified methods SDLC raised fewer alerts than BCCP (25/5 datasets) and S-CQR, but more than S-NCP (12/18). The dedicated tail classifier TC-LS attains the guaranteed recall almost exactly (mean 0.906) and raised fewer alerts than SDLC on every dataset (alert-rate ratio 1.559); for a pure yes/no decision it is the more efficient tool. Conformal selection [@jin2023selection] controls the false discovery rate instead and flagged few units, with high precision (mean 0.766 at $q=0.2$) but a mean recall of only 0.603; the naive point-prediction rule behaved similarly (recall 0.625).

The preferable rule depends on the cost of a miss relative to a false alert. With equal costs, the rules that raise few alerts were cheapest: the point rule and conformal selection (expected cost 0.056 and 0.062 per unit, against 0.277 for SDLC). When a miss costs ten times a false alert, SDLC's expected cost did not differ significantly from that of TC-LS (SDLC lower on 14 of 31 datasets, $p$ = 0.130) and was lower than that of conformal selection on 19 datasets. At a cost ratio of 20, SDLC was cheaper than TC-LS on 22 datasets ($p$ = 0.083), because its recall exceeds the guaranteed 0.9 while TC-LS attains it almost exactly. Among the stratified scores, however, S-NCP gave the cheapest alerts: SDLC's expected cost was higher than S-NCP's on 27 of 31 datasets at $r=10$ and on 29 at $r=20$, because S-NCP raised fewer upper-tail alerts. These $p$-values are unadjusted and descriptive. Alerts read off *marginal* sets (SCP, CQR, HPD-split) were the cheapest on average at high cost ratios (0.279 for HPD-split at $r=20$). They had no recall guarantee, however, and their recall fell below 0.9 on 4–6 datasets. Fig. 8 shows cost curves for three valuation datasets.

**Table 11.** Upper-tail alerts ($\alpha=0.1$; means over datasets): recall, alert rate and precision, the number of datasets with recall at least 0.9, and the expected cost per unit when a missed extreme outcome costs $r$ times a false alert. Set-based alerts (SCP to SDLC-floor) versus dedicated rules built from the same models: conformal tail classifiers (TC-LS, TC-H), conformal selection with FDR level $q$ (CS-BH-$q$) and the point-prediction rule.

| Rule       | Recall   | Alert rate   | Precision   | Datasets recall ≥ 0.9   | Cost r=1   | Cost r=10   | Cost r=20   |
|:-----------|:---------|:-------------|:------------|:------------------------|:-----------|:------------|:------------|
| SCP        | 0.947    | 0.273        | 0.512       | 26                      | 0.175      | 0.229       | 0.289       |
| CQR        | 0.952    | 0.286        | 0.495       | 27                      | 0.187      | 0.234       | 0.285       |
| HPD-split  | 0.952    | 0.278        | 0.493       | 25                      | 0.179      | 0.226       | 0.279       |
| BCCP       | 0.983    | 0.468        | 0.379       | 31                      | 0.362      | 0.381       | 0.402       |
| S-NCP      | 0.983    | 0.358        | 0.449       | 31                      | 0.253      | 0.270       | 0.289       |
| S-CQR      | 0.988    | 0.430        | 0.397       | 31                      | 0.323      | 0.334       | 0.346       |
| SDLC       | 0.978    | 0.382        | 0.428       | 31                      | 0.277      | 0.300       | 0.325       |
| SDLC-floor | 0.966    | 0.330        | 0.467       | 30                      | 0.228      | 0.262       | 0.301       |
| TC-LS      | 0.906    | 0.248        | 0.590       | 19                      | 0.159      | 0.253       | 0.357       |
| TC-H       | 0.909    | 0.272        | 0.523       | 18                      | 0.182      | 0.273       | 0.374       |
| CS-BH-0.1  | 0.479    | 0.054        | 0.861       | 6                       | 0.066      | 0.611       | 1.217       |
| CS-BH-0.2  | 0.603    | 0.076        | 0.766       | 10                      | 0.062      | 0.490       | 0.965       |
| Point      | 0.625    | 0.077        | 0.813       | 5                       | 0.056      | 0.457       | 0.903       |


![**Fig. 8.** Expected cost per unit of upper-tail alert rules as a function of the cost ratio $c(\mathrm{FN})/c(\mathrm{FP})$ for three valuation datasets (means over 10 splits, $\alpha=0.1$).](/home/user/p_c1_2/Target_Journal_Submission/figures/F13_alert_costs.png){width=100%}


## 6.9 Sensitivity analyses (RQ6)

*Miscoverage level and strata.* The conclusions held at $\alpha=0.05$ and $\alpha=0.2$ (SDLC worst stratum 0.947 and 0.789; Supplementary Table S6). With decile strata the worst decile coverage of SDLC rose to 0.888, from 0.863 with five strata, at a size increase from 0.874 to 0.898. The floor variant (SDLC-floor, $\beta=0.2$) reached its weaker guarantee with smaller sets (worst stratum 0.821, size 0.806).

*Calibration-set size.* With a quarter of the calibration split (on average 1,082 points) stratum-wise validity was retained, but SDLC's sets grew from 0.874 to 1.243, mainly because tail strata with fewer than $1/\alpha-1$ points have an infinite threshold (87 runs, against 2 with the full split; Supplementary Table S8).

*Base learner.* With a two-layer perceptron (5 seeds), marginal methods reached a worst-stratum coverage of 0.650–0.830 and stratified methods 0.889–0.891. SDLC again gave the smallest stratified sets: smaller than BCCP on 23 of 31 datasets (ratio 0.946), than S-NCP on 27 (ratio 0.938, Holm $p$ < 0.001) and than S-HPD on 29 (ratio 0.927).

*Imbalance-aware training.* With DenseWeight sample weights [@steininger2021denseweight], SCP's worst-stratum coverage rose from 0.630 to 0.759, but the shortfall remained large and its sets grew by a factor of 1.31. Stratified calibration remained valid (0.885 for SDLC), and SDLC again gave the smallest stratified sets (Holm $p$ < 0.001 or smaller). Imbalance-aware learning and stratified calibration are complementary; the former does not deliver the guarantee.

*Grouped splits.* On three datasets with repeated units (sarcos, superconductivity, video_transcoding) we repeated the main comparison with splits that keep each unit in one part (5 seeds; Supplementary Table S16). On sarcos and superconductivity the results were close to those of random splits (SDLC/S-NCP size ratios 0.965 and 0.914). On video_transcoding, splitting by video increased every method's sets several-fold (SDLC: 0.113 to 0.775), so random splits of this dataset measure interpolation between runs of known videos. Stratified methods still covered their worst stratum at 0.852–0.904, against at most 0.766 for marginal methods, but SDLC's sets were larger than BCCP's (ratio 1.205), and BCCP and S-CQR covered less than nominal marginally (0.875 and 0.873), as expected when exchangeability holds between groups rather than rows. SDLC's size advantage thus depends on the density model transferring to unseen units, and grouped validation is advisable for such data.

*Computational cost.* Computing a prediction set took a median of 13.5 µs per test point for SDLC, against 0.09 µs for S-NCP and 0.07 µs for BCCP (Supplementary Tables S13 and S15). SDLC is roughly two orders of magnitude slower than interval methods at prediction time, but the cost is negligible next to model fitting.

## 6.10 Error analysis

The price of stratum-wise validity (SDLC relative to DLS) rose with the skewness of the target (Spearman $\rho$ = 0.62, $p$ < 0.001) and fell with the calibration-set size ($\rho$ = -0.41). It was largest for forest fires (8.75), whose atom at zero merges the two lower strata. SDLC was larger than S-NCP on 4 datasets (socmob, cars, forest fires and QSAR fish toxicity; ratios up to 1.64), all small or with many ties, so that the scale and noise models rest on few distinct values. The density score helps most when the location model is accurate and the noise is heteroscedastic ($\rho$ = 0.47 with the relative RMSE).

![**Fig. 9.** Prediction sets for 70 test points of the California housing data (seed 0; 14 per calibration stratum, sorted by the true value; dashed lines are stratum boundaries; crosses mark missed targets). CQR misses most of the capped top values; the stratified methods cover them, and SDLC adds disjoint pieces in the upper stratum where its threshold is lower.](/home/user/p_c1_2/Target_Journal_Submission/figures/F9_example_sets_california.png){width=100%}



# 7. Discussion

## 7.1 What the evidence supports

Three findings are robust across datasets, miscoverage levels, stratifications and learners. First, marginal and covariate-adaptive methods systematically under-cover rare targets (worst-stratum coverage 63.0%–78.3% at a nominal 90%), beyond sampling noise, and the oracle analysis shows that this is not an artefact of estimation. Second, calibrating within target strata restores stratum-wise coverage for every score, as Mondrian theory guarantees; the guarantee resisted moderate target shift and cost a 1.17–1.27-fold size increase, less than lowering $\alpha$ for a marginal method. Third, the density score gave smaller stratum-valid sets than the residual score of BCCP, the quantile score and the HPD score on most datasets, as Proposition 2 predicts, and the ordering was confirmed on 17 held-out datasets under a pre-specified plan.

Two qualifications are equally well supported. The gain over the information-matched normalised residual is a few per cent and comes mainly from reallocating coverage from noisy to quiet inputs; its price is lower coverage of the noisiest inputs, occasional empty sets and lower coverage of the uncalibrated top 1%. And the estimated location–scale density is far from the oracle when the noise shape changes with $x$. The ranking of scores is a statement about average efficiency, not a free improvement.

## 7.2 Practical guidance

For practitioners who must report how often extreme outcomes are covered, we suggest the following.

1. *Decide which guarantee is required.* Marginal coverage, however adaptive the score, does not protect rare targets, and lowering $\alpha$ is a less efficient substitute. If every target range must be covered at the nominal level, calibrate within strata (SDLC or S-NCP). If coverage averaged over the target range is required, or the most extreme outcomes beyond any practical stratum matter most, use RW-DLC with an inverse-density relevance; it covered the top 1% at close to the nominal level, at the price of lower coverage in the bulk.
2. *Choose strata from training-target quantiles* so that each stratum receives several times $1/\alpha$ calibration points; otherwise use fewer strata or the floor variant.
3. *Use a score that includes the scale $\hat\sigma(x)$.* SDLC, S-NCP and S-HPD gave stratum-valid sets within a few per cent of each other; SDLC was smallest on most datasets, while S-NCP is simpler, spreads coverage more evenly across noise levels, covers more of the extreme 1% and gives cheaper alerts. The residual score of BCCP and stratified CQR were clearly less efficient. When an interval is required, the hull of S-NCP was as small as the hull of SDLC on held-out data.
4. *Report hulls when an interval is mandatory.* Stratified sets can be discontiguous: SDLC's sets had 1.527 pieces on average (BCCP 1.465), mostly an isolated piece in a tail stratum whose threshold is lower than that of its neighbour (Fig. 9). Such a piece says that an extreme outcome is plausible, but an interval is easier to communicate. SDLC-hull is valid and smaller than BCCP-hull, but loses part of the advantage.
5. *For yes/no decisions about extremes, match the rule to the costs.* A class-conditional conformal tail classifier attains the same recall guarantee with fewer alerts and is the better choice when false alerts are expensive; among set-based alerts, S-NCP's were the cheapest. Set-based alerts have higher recall, are cheaper when misses are very costly, and carry more information about the size of the outcome.

## 7.3 Limitations

*Size cost and data requirements.* Stratum-wise validity is paid for in set size, more so for skewed targets and small tail strata; with fewer than $1/\alpha_k-1$ calibration points the method returns the whole stratum. Pooling sparse strata [@ding2023class], cross-fitted calibration [@barber2021jackknife] and overlapping groups [@bairaktari2025kandinsky] are natural remedies that we did not evaluate.

*Granularity of the guarantee.* The guarantee holds for the calibrated strata, not for arbitrary sub-ranges. Within a stratum, coverage is lower near its outer end, and shifts that move mass within a stratum reduce coverage (Table 10); Corollary 1 explains the direction of this effect, but its bounds are loose for open tail strata. The guarantee is also marginal over $X$ within each stratum, so it says nothing about a particular input, and the density score deliberately trades coverage across inputs.

*Density estimation and baselines.* Proposition 2 is an oracle property, and Proposition 3 requires a uniformly consistent density estimate, which the location–scale model provides only when the noise shape does not depend on $x$; flexible conditional density estimators may close the gap to the oracle. We did not stratify further covariate-adaptive methods such as conditional histograms [@sesia2021conformal] or localised conformal prediction [@hore2025local]; they cannot beat the oracle density score, but their estimated versions may be competitive.

*Evaluation scope.* The benchmark covers tabular targets with at least 20 distinct values; ordinal, count and temporally dependent targets were excluded. With repeated units, the guarantees hold for new rows from the same pool, not for new units or future periods. All results use split calibration and one untuned base-learner configuration. The density-based implementation changed after earlier results had been seen (Section 5.7), which is why the CTR23 size comparisons are exploratory and were replicated on held-out data.

*Applicability of the guarantee.* Stratum-wise coverage requires exchangeability of calibration and test data, holds on average over calibration sets and over the test points of a stratum, and does not protect against covariate shift within strata.


# 8. Conclusion and future work

Prediction intervals that are valid on average can fail exactly where imbalanced regression needs them: on the rare outcomes. Even the oracle interval with exact covariate-conditional coverage under-covers the tails of the target, and on 31 benchmark datasets marginal and covariate-adaptive conformal methods covered only 63.0%–78.3% of the outcomes in their worst-covered stratum at a nominal 90%. We studied two guarantees that protect rare outcomes and the sets that meet them most efficiently.

Calibrating thresholds within strata of the target, an established Mondrian device, guarantees coverage in every stratum for any score. For this guarantee, conditional-density level sets with stratum-specific thresholds are the smallest sets for the oracle, and SDLC, their plug-in version, gave smaller sets than bin-conditional conformal prediction with residual scores and than stratified quantile regression, on most CTR23 datasets and on 17 held-out datasets under a pre-specified analysis. Among scores that use the estimated scale, however, the differences were within a few per cent, and the simpler stratified normalised residual covered noisy inputs and the most extreme outcomes better. Strata also protect only at their own resolution. Relevance-weighted calibration removes that limit: RW-DLC guarantees coverage averaged by an imbalanced-regression relevance function in finite samples, uses the score that is size-optimal for that guarantee, and in a second pre-specified study covered 87.2% of the top 1% of outcomes on held-out data, against 68.8% for SDLC, at a cost in coverage of the bulk. For yes/no decisions about extremes, dedicated conformal tail classifiers attain the same recall guarantee with fewer alerts.

Future work should combine the two guarantees, for example a relevance-weighted guarantee with a floor on every stratum; learn relevance functions or strata that minimise size subject to validity; replace the location–scale density by flexible conditional density estimators, whose gap to the oracle was largest under covariate-dependent multimodality; and extend both guarantees to grouped and dependent data, where our grouped-split analysis showed that efficiency depends on transfer to unseen units.


# Appendix A. Proofs

**Proof of Theorem 1.** Condition on $\mathcal{D}_{\mathrm{tr}}$, which fixes the score $s$ and the strata. Let $E_k=\{Y_{n+1}\in B_k\}$ and $J=\{i\le n+1: Y_i\in B_k\}$, so that $|J|=n_k+1$ on $E_k$. Membership of a point in $B_k$ is a function of that point alone, so any permutation of $\{1,\ldots,n+1\}$ that maps $J$ onto itself leaves the event $\{J=j,\ n+1\in J\}$ unchanged; by exchangeability, conditionally on $J=j\ni n+1$ and on the multiset $\{(X_i,Y_i):i\in j\}$, the index $n+1$ is uniformly distributed over $j$. Let $R$ be the rank of $S_{n+1}=s(X_{n+1},Y_{n+1})$ among $\{S_i\}_{i\in J}$, with ties broken uniformly at random; conditionally as above, $R$ is uniform on $\{1,\ldots,n_k+1\}$. By (3)–(4), $Y_{n+1}\in\hat C(X_{n+1})$ iff $S_{n+1}\le\hat q_k$, which holds whenever $R\le r_k=\lceil(n_k+1)(1-\alpha_k)\rceil$ (if $r_k>n_k$, then $\hat q_k=+\infty$ and coverage is one). Hence the conditional coverage is at least $r_k/(n_k+1)\ge 1-\alpha_k$. Averaging over $J$ and the multiset gives (5); since the argument conditions on $J$, the level $\alpha_k$ may depend on $n_k$. If scores are almost surely distinct, coverage is exactly $\min\{r_k,n_k+1\}/(n_k+1)<1-\alpha_k+1/(n_k+1)$ given $n_k$. The marginal statement follows from the law of total probability, $\sum_kp_k(1-\alpha_k)=1-\sum_kp_k\alpha_k$. Finally, the conditioning on $\mathcal{D}_{\mathrm{tr}}$ allows any score and strata that are measurable functions of $\mathcal{D}_{\mathrm{tr}}$ alone. $\square$

**Proof of Corollary 1.** Given $\mathcal{D}_{\mathrm{tr}}$ and $\mathcal{D}_{\mathrm{cal}}$ the set $A=\{(x,y):y\in\hat C(x)\}$ is fixed. Because the test point is independent of the calibration data, $Q\{Y\in\hat C(X)\,|\, Y\in B_k\}=\mathbb{E}\,Q_k(A)$ and the left-hand side of (5) equals $\mathbb{E}\,P_k(A)$, where $\mathbb{E}$ averages over $\mathcal{D}_{\mathrm{cal}}\sim P^n$ (i.i.d. data are exchangeable, so (5) applies). (i) If $Q_k=P_k$ the two expectations coincide, and the law of total probability gives the marginal statement. (ii) $|Q_k(A)-P_k(A)|\le d_{\operatorname{TV}}(Q_k,P_k)$ for every fixed $A$; average and use (5). (iii) Under label shift the likelihood ratio of $Q_k$ to $P_k$ is $\lambda_k(y)=w(y)/\bar w_k$ with $\bar w_k=\pi_k/p_k=\mathbb{E}_{P_k}w(Y)\ge m_k$. Hence $Q_k(A^c)=\mathbb{E}_{P_k}\{\lambda_k(Y)\mathbf{1}_{A^c}(X,Y)\}\le(M_k/\bar w_k)P_k(A^c)\le(M_k/m_k)P_k(A^c)$; averaging over $\mathcal{D}_{\mathrm{cal}}$ and using (5) gives the multiplicative bound. For the total-variation bound, $\lambda_k\in[a,b]$ with $a=m_k/\bar w_k\le1\le b=M_k/\bar w_k$ and $\mathbb{E}_{P_k}\lambda_k=1$; since $d_{\operatorname{TV}}(Q_k,P_k)=\mathbb{E}_{P_k}(\lambda_k-1)_+$ and, by convexity, $(\lambda-1)_+\le(b-1)(\lambda-a)/(b-a)$ on $[a,b]$, we obtain $d_{\operatorname{TV}}\le(b-1)(1-a)/(b-a)=(M_k-\bar w_k)(\bar w_k-m_k)/\{\bar w_k(M_k-m_k)\}$. The right-hand side is maximised at $\bar w_k=\sqrt{m_kM_k}$, where it equals $(\sqrt{M_k}-\sqrt{m_k})/(\sqrt{M_k}+\sqrt{m_k})=\tanh\{\log(M_k/m_k)/4\}$. $\square$

**Proof of Proposition 2.** Existence: $G_k(t)=P\{f(Y\,|\, X)\ge t\,|\, Y\in B_k\}$ is continuous and non-increasing with $G_k(0^+)=1$ and $G_k(t)\to0$ as $t\to\infty$, so the intermediate value theorem gives $t_k>0$ with $G_k(t_k)=1-\alpha_k$. Optimality: write $A=\{(x,y):y\in C(x)\}$, $A^\star$ likewise, $A_k=A\cap(\mathcal{X}\times B_k)$, $A_k^\star=A^\star\cap(\mathcal{X}\times B_k)$ and $|A|_P=\iint\mathbf{1}_A(x,y)\,dy\,P_X(dx)$, so that $\mathbb{E}|C(X)\cap B_k|=|A_k|_P$ and $p_k\operatorname{Cov}_k(C)=\iint\mathbf{1}_{A_k}f(y\,|\, x)\,dy\,P_X(dx)$. Since $|\{y:f(y\,|\, x)\ge t_k\}|\le 1/t_k$, $|A_k^\star|_P<\infty$; if $|A_k|_P=\infty$ there is nothing to prove. Otherwise the integrand of
$$\Delta_k=\iint\left(\mathbf{1}_{A_k^\star}-\mathbf{1}_{A_k}\right)\left(f(y\,|\, x)-t_k\right)dy\,P_X(dx)$$
is non-negative pointwise: on $A_k^\star\setminus A_k$ we have $f\ge t_k$, and on $A_k\setminus A_k^\star$, where $y\in B_k$, we have $f<t_k$. Hence $\Delta_k\ge 0$, i.e. $t_k(|A_k^\star|_P-|A_k|_P)\le p_k\{\operatorname{Cov}_k(C^\star)-\operatorname{Cov}_k(C)\}\le 0$, and $t_k>0$ gives $|A_k^\star|_P\le|A_k|_P$. Summing over $k$ gives the statement for $\mathbb{E}|C(X)|$. $\square$

**Proof of Proposition 3.** Condition on $\mathcal{D}_{\mathrm{tr}}$ (hence on $\hat f$) and write $V_i=f(Y_i\,|\, X_i)$, $\hat V_i=\hat f(Y_i\,|\, X_i)$, so that $|\hat V_i-V_i|\le\varepsilon_N$. *Thresholds.* By (3), $-\hat q_k$ is the $(n_k+1-r_k)$-th smallest of $\{\hat V_i:i\in I_k\}$, and $(n_k+1-r_k)/n_k\to\alpha_k$ because $n_k\to\infty$ almost surely ($n_k\sim\mathrm{Bin}(n,p_k)$ given $\mathcal{D}_{\mathrm{tr}}$). Order statistics are 1-Lipschitz in the sup-norm, so $-\hat q_k$ differs by at most $\varepsilon_N$ from the same order statistic of $\{V_i:i\in I_k\}$. The $V_i$, $i\in I_k$, are i.i.d. from the law of $f(Y\,|\, X)$ given $Y\in B_k$, independent of $\mathcal{D}_{\mathrm{tr}}$, whose $\alpha_k$-quantile $t_k$ is unique by assumption; hence that order statistic converges to $t_k$ almost surely [@serfling1980approximation, Sec. 2.3], and $\delta_k:=|\hat q_k+t_k|\to0$ in probability. *Sets.* Fix $x$ and $y\in B_k$. If $y$ lies in exactly one of $\hat C(x)$ and $C^\star(x)$, then $\hat f(y\,|\, x)+\hat q_k$ and $f(y\,|\, x)-t_k$ have opposite signs (one is $\ge0$, the other $<0$), while they differ by at most $\varepsilon_N+\delta_k$; hence $|f(y\,|\, x)-t_k|\le\eta:=\varepsilon_N+\max_k\delta_k$. Therefore
$$\mathbb{E}_X|\hat C(X)\triangle C^\star(X)|\le\sum_{k=1}^K h_k(\eta),\qquad h_k(\eta)=\mathbb{E}\,\big|\{y\in B_k:|f(y\,|\, X)-t_k|\le\eta\}\big|.$$
For $\eta<t_k/2$ the set inside $h_k$ lies in $\{y:f(y\,|\, X)\ge t_k/2\}$, whose measure is at most $2/t_k$, and it decreases to $\{y\in B_k:f(y\,|\, X)=t_k\}$ as $\eta\downarrow0$. By dominated convergence $h_k(\eta)\to\mathbb{E}|\{y\in B_k:f(y\,|\, X)=t_k\}|$, which is zero: continuity of the law of $f(Y\,|\, X)$ given $Y\in B_k$ gives $0=p_k^{-1}\iint_{B_k}\mathbf{1}\{f(y\,|\, x)=t_k\}f(y\,|\, x)\,dy\,P_X(dx)=p_k^{-1}t_k\,\mathbb{E}|\{y\in B_k:f(y\,|\, X)=t_k\}|$. Since $\eta\to0$ in probability, (7) follows, and $|\,|\hat C|-|C^\star|\,|\le|\hat C\triangle C^\star|$ gives the statement on expected size. $\square$

**Remark (within-stratum coverage profile).** Under label shift, let $\kappa(y)=P\{y\in\hat C(X_{n+1})\,|\, Y_{n+1}=y\}$, which is the same under $P$ and $Q$. Then the change in stratum-wise coverage equals the within-stratum covariance $\mathbb{E}_{P_k}[\{\kappa(Y)-c\}\{\lambda_k(Y)-1\}]$ for any constant $c$, so coverage is lost only if the shift moves mass within $B_k$ towards values that are covered less often than the stratum average. For the oracle sets $C^\star$ in the Gaussian model of Proposition 1, $C^\star(x)\cap B_k=\{y\in B_k:|y-x|\le r_k\}$ for a stratum-specific radius $r_k$, so the argument of Proposition 1 (with $a=r_k$) shows that $\kappa$ decreases in $|y|$ within every stratum, that is, towards the outer end of a tail stratum; for the estimated sets the same pattern is observed empirically (Section 6). This is why a tilt towards more extreme outcomes can lower tail-stratum coverage even after stratified calibration.

**Proof of Theorem 2.** Write $Z_i=(X_i,Y_i)$ and let $Z_{n+1}=(X,Y)$ be drawn from $Q$ with $dQ/dP(z)=w(z)=\phi(y)/\mathbb{E}\phi(Y)$, independently of $Z_1,\ldots,Z_n\sim P$; conditionally on $\mathcal{D}_{\mathrm{tr}}$ the score $s$ and $\phi$ are fixed. The joint law of $(Z_1,\ldots,Z_{n+1})$ has density $\prod_{i\le n}p(z_i)\cdot p(z_{n+1})w(z_{n+1})$ with respect to the product of the dominating measures, so the vector is weighted exchangeable with weight functions $(1,\ldots,1,w)$ [@tibshirani2019conformal, Lemma 3]. Hence, conditionally on the multiset $E=\{z_1,\ldots,z_{n+1}\}$ of observed values, $P(Z_{n+1}=z_j\,|\, E)=w(z_j)/\sum_kw(z_k)=\phi(y_j)/\sum_k\phi(y_k)$, and the test score $S_{n+1}$ is distributed as $\sum_jp_j\delta_{S_j}$ with $p_j=\phi(y_j)/\sum_k\phi(y_k)$. Therefore $P\{S_{n+1}\le Q_{1-\alpha}(\sum_{j\le n+1}p_j\delta_{S_j})\,|\, E\}\ge1-\alpha$, where $Q_{1-\alpha}$ denotes the $(1-\alpha)$-quantile. Replacing the atom $\delta_{S_{n+1}}$ by $\delta_{+\infty}$ can only raise the quantile, and $S_{n+1}\le Q_{1-\alpha}(\sum_{j\le n+1}p_j\delta_{S_j})$ if and only if $S_{n+1}\le Q_{1-\alpha}(\sum_{i\le n}p_i\delta_{S_i}+p_{n+1}\delta_{+\infty})$ [@tibshirani2019conformal, Lemma 1]. The right-hand quantile equals $q(Y_{n+1})$ in (11), because the normalisation $\sum_k\phi(y_k)=W+\phi(Y_{n+1})$ is the same. Taking expectations over $E$ gives $Q\{Y\in\hat C_\phi(X)\}\ge1-\alpha$. Finally, for a fixed set $C$, $Q\{Y\in C(X)\}=\mathbb{E}_P[w(Z)\mathbf{1}\{Y\in C(X)\}]=\operatorname{Cov}_\phi(C)$, so averaging over $\mathcal{D}_{\mathrm{cal}}$ yields $\mathbb{E}[\operatorname{Cov}_\phi(\hat C_\phi)]\ge1-\alpha$. $\square$

**Proof of Proposition 4.** Let $C$ satisfy $\operatorname{Cov}_\phi(C)\ge1-\alpha=\operatorname{Cov}_\phi(C^\star_\phi)$ and write $h(x,y)=\phi(y)f(y\,|\, x)$. Pointwise, $(\mathbf{1}\{y\in C^\star_\phi(x)\}-\mathbf{1}\{y\in C(x)\})(h(x,y)-t)\ge0$, because the first factor is positive only where $h\ge t$ and negative only where $h<t$. Integrating over $dy\,dP_X(x)$ gives $\mathbb{E}[\phi(Y)](\operatorname{Cov}_\phi(C^\star_\phi)-\operatorname{Cov}_\phi(C))\ge t\,(\mathbb{E}|C^\star_\phi(X)|-\mathbb{E}|C(X)|)$. The left-hand side is at most zero and $t>0$, so $\mathbb{E}|C^\star_\phi(X)|\le\mathbb{E}|C(X)|$. $\square$


# References

::: {#refs}
:::


<!-- End matter in the form required by the journal ("Statements and Declarations"). Headings carry {-} so that they stay unnumbered. Bracketed text marks placeholders for the authors; identifying information is kept on the separate title page for double-blind review. -->

# Statements and Declarations

**Competing interests.** The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper. [To be confirmed by every author before submission.]

**Funding.** [Placeholder: funding sources and grant numbers; otherwise: "The authors did not receive support from any organization for the submitted work."]

**Author contributions.** [Placeholder, given on the title page to preserve anonymity; for example: Author 1: conceptualization, methodology, software, formal analysis, investigation, visualization, writing – original draft. Author 2: conceptualization, validation, supervision, writing – review & editing.]

**Data availability.** All datasets analysed in this study are publicly available on OpenML: study 353, the OpenML-CTR23 benchmark suite [@fischer2023openml], and, for the confirmatory replication, suites 335 and 336 [@grinsztajn2022tree]. They are downloaded programmatically through the OpenML API by the released scripts; the OpenML identifier and licence of each dataset are listed in Supplementary Tables S1 and S2.

**Code availability.** All code, configuration files, raw per-run results, the pre-specified confirmatory analysis plan and the analysis scripts are provided as supplementary material for review (anonymised) and will be deposited in a public repository [repository URL] upon acceptance. A single command (`python run_all.py --mode full`) regenerates every table, figure and number of the manuscript from the raw data.

**Ethics approval and consent.** Not applicable. The study used only publicly available, de-identified benchmark data and involved no human participants, animals or personal data.

**Use of large language models.** The use of a large language model in this work is documented in Section 5.8, as required by the journal's policy.

# Problem formulation {#sec:problem}

## Target-conditional coverage

Let $(X,Y)\in\mathcal{X}\times\mathbb{R}$ have joint law $P$ with conditional density $f(y\mid x)$ with respect to Lebesgue measure. A *prediction set* is a measurable map $C:\mathcal{X}\to\mathcal{B}(\mathbb{R})$. Split conformal prediction [@papadopoulos2002inductive; @lei2018distribution] guarantees *marginal* coverage $P\{Y\in C(X)\}\ge 1-\alpha$, and much recent work targets approximate *covariate-conditional* coverage $P\{Y\in C(X)\mid X=x\}\approx 1-\alpha$ [@romano2019conformalized; @izbicki2022cdsplit; @gibbs2025conformal], which cannot be guaranteed in finite samples without further assumptions [@barber2021limits].

In imbalanced regression the outcomes of interest are rare target values. Let $\mathcal{B}=\{B_1,\ldots,B_K\}$ be a partition of $\mathbb{R}$ into intervals (*target strata*), for instance the lower tail, the bulk and the upper tail of the target distribution, with $p_k=P(Y\in B_k)>0$. We call
$$\mathrm{Cov}_k(C)=P\{Y\in C(X)\mid Y\in B_k\},\qquad k=1,\ldots,K, \tag{1}$$
the *target-conditional* (or stratum-wise) coverage of $C$. Stratum-wise coverage answers the question that matters when extremes are costly: *when the outcome is extreme, how often does the prediction set contain it?* It is the regression analogue of class-conditional coverage in classification [@vovk2005algorithmic; @vovk2012conditional; @sadinle2019least].

Because $\sum_k p_k\,\mathrm{Cov}_k(C)=P\{Y\in C(X)\}$, marginal coverage only constrains a $p$-weighted average of the $\mathrm{Cov}_k$; rare strata (small $p_k$) can be under-covered while the bulk is over-covered. The next proposition shows that this is not a defect of estimation that better covariate-conditional methods would remove: even the *oracle* covariate-conditional set fails.

## Covariate-conditional validity does not imply target-conditional validity

**Proposition 1.** *Let $X\sim N(0,\tau^2)$ and $Y\mid X\sim N(X,\sigma^2)$ with $\tau^2+\sigma^2=1$, so that $R^2=\tau^2$ is the fraction of variance explained by the optimal predictor. Let $C^*(x)=[x-z\sigma,\,x+z\sigma]$ with $z=\Phi^{-1}(1-\alpha/2)$; $C^*$ is the shortest set with exact covariate-conditional coverage $1-\alpha$ at every $x$. Then*
$$P\{Y\in C^*(X)\mid Y=y\}=\Phi\!\left(\frac{z\sigma-(1-R^2)y}{s}\right)-\Phi\!\left(\frac{-z\sigma-(1-R^2)y}{s}\right),\qquad s=\sigma\sqrt{R^2}, \tag{2}$$
*which is strictly decreasing in $|y|$ and tends to $0$ as $|y|\to\infty$ whenever $R^2<1$.*

*Proof.* $(X,Y)$ is bivariate normal with $\mathrm{Var}(Y)=1$ and $\mathrm{Cov}(X,Y)=\tau^2$, hence $X\mid Y=y\sim N(\tau^2 y,\,\tau^2\sigma^2)$ and $Y-X\mid Y=y\sim N((1-\tau^2)y,\,\tau^2\sigma^2)$. Since $Y\in C^*(X)$ iff $|Y-X|\le z\sigma$, (2) follows. The expression is the probability that a normal variable with standard deviation $s$ and mean $(1-R^2)y$ falls in the fixed symmetric interval $[-z\sigma,z\sigma]$; it is maximised at mean zero, decreases as $|(1-R^2)y|$ grows and vanishes as $|y|\to\infty$. $\square$

Table [-@tbl:prop1] reports (2) integrated over the top decile of $Y$. For a predictor explaining half of the variance the oracle covariate-conditional interval covers only {{prop1.upper10_r05}} of the top-10% outcomes and {{prop1.upper1_r05}} of the top-1% outcomes, while covering {{prop1.central_r05}} of the central 80%. The mechanism is general: an extreme outcome is, on average, the sum of an extreme signal and an extreme noise realisation, and any $X$-measurable set is blind to the latter. Target-conditional coverage therefore requires calibration that conditions on $Y$, which is what the proposed method does.

# Target-stratified conformal prediction {#sec:method}

## Stratified calibration and its finite-sample guarantee

Data are split into a proper training set $\mathcal{D}_{\mathrm{tr}}$ and a calibration set $\mathcal{D}_{\mathrm{cal}}=\{(X_i,Y_i)\}_{i=1}^n$. Using $\mathcal{D}_{\mathrm{tr}}$ only we fit a nonconformity score $s:\mathcal{X}\times\mathbb{R}\to\mathbb{R}$ (small values = conforming) and choose the strata $\mathcal{B}$, e.g. from quantiles of the training targets. Let $k(y)$ denote the stratum containing $y$, $I_k=\{i:Y_i\in B_k\}$, $n_k=|I_k|$, and for levels $\alpha_k\in(0,1)$ let
$$\hat q_k=\text{the }\lceil (n_k+1)(1-\alpha_k)\rceil\text{-th smallest value of }\{s(X_i,Y_i):i\in I_k\}\quad(\hat q_k=+\infty\text{ if this rank exceeds }n_k). \tag{3}$$
The target-stratified conformal (TSC) prediction set is
$$\hat C(x)=\{y\in\mathbb{R}: s(x,y)\le \hat q_{k(y)}\}=\bigcup_{k=1}^K\{y\in B_k: s(x,y)\le\hat q_k\}. \tag{4}$$
Note that the stratum used for a candidate value $y$ is the stratum *of that candidate*, not of a prediction; this is what makes the guarantee target-conditional. Equation (4) is a Mondrian conformal predictor whose taxonomy depends on the label [@vovk2005algorithmic; @vovk2012conditional]; for regression it yields sets that may be unions of up to $K$ intervals.

**Theorem 1 (finite-sample stratum-wise validity).** *If $(X_1,Y_1),\ldots,(X_n,Y_n),(X_{n+1},Y_{n+1})$ are exchangeable conditionally on $\mathcal{D}_{\mathrm{tr}}$, then for every $k$ with $P(Y\in B_k)>0$,*
$$P\{Y_{n+1}\in\hat C(X_{n+1})\mid Y_{n+1}\in B_k\}\ \ge\ 1-\alpha_k. \tag{5}$$
*If, in addition, the scores within each stratum are almost surely distinct, then conditionally on $n_k$, $P\{Y_{n+1}\in\hat C(X_{n+1})\mid Y_{n+1}\in B_k, n_k\}\le 1-\alpha_k+1/(n_k+1)$. Consequently $\hat C$ also has marginal coverage $\ge 1-\max_k\alpha_k$.*

*Proof.* Condition on $\mathcal{D}_{\mathrm{tr}}$ (which fixes $s$ and $\mathcal{B}$), on the event $E_k=\{Y_{n+1}\in B_k\}$ and on the set $J=\{i\le n+1: Y_i\in B_k\}$, $|J|=n_k+1$. Membership in $B_k$ is a function of each point separately, so the conditional law of $(Z_i)_{i\in J}$ given $J$ and $\{n+1\in J\}$ is still exchangeable, and $n+1$ is a uniformly random element of $J$ given the multiset $\{Z_i: i\in J\}$. By (4), $Y_{n+1}\in\hat C(X_{n+1})$ iff $S_{n+1}=s(X_{n+1},Y_{n+1})\le\hat q_k$, i.e. iff $S_{n+1}$ is among the $\lceil (n_k+1)(1-\alpha_k)\rceil$ smallest of the $n_k+1$ scores $\{S_i\}_{i\in J}$ (ties broken in favour of coverage). By exchangeability this has probability at least $\lceil (n_k+1)(1-\alpha_k)\rceil/(n_k+1)\ge 1-\alpha_k$, and at most $\lceil (n_k+1)(1-\alpha_k)\rceil/(n_k+1)<1-\alpha_k+1/(n_k+1)$ without ties. When the rank exceeds $n_k$, $\hat q_k=\infty$ and coverage is one. Averaging over $J$ gives (5); averaging (5) over $k$ with weights $p_k$ gives the marginal statement. $\square$

**Corollary 1 (robustness to target shift).** *Suppose the test point is drawn from $Q$ with $Q(\,\cdot\mid Y\in B_k)=P(\,\cdot\mid Y\in B_k)$ for all $k$ but arbitrary stratum probabilities $Q(Y\in B_k)$. Then $Q\{Y\in\hat C(X)\}\ge 1-\max_k\alpha_k$, whereas a marginally calibrated set only satisfies $Q\{Y\in C(X)\}=\sum_k Q(B_k)\mathrm{Cov}_k(C)\ge\min_k\mathrm{Cov}_k(C)$, which may be far below $1-\alpha$.*

The corollary follows directly from (5) and the law of total probability. It covers deployment periods in which extremes are more frequent than in the calibration data (e.g. a market boom or an extreme-weather season), as long as the covariate distribution *within* each target stratum is stable. This is the stratified analogue of conformal prediction under label shift for classification [@podkopaev2021distribution], but it requires no estimate of the shifted stratum probabilities.

Theorem 1 holds for *any* score, so validity is never the issue; the choice of score determines how large the sets are. The next result identifies the best possible score.

## The smallest sets with stratum-wise coverage

For a prediction set $C$ let $|C(x)|$ denote its Lebesgue measure and $\mathbb{E}|C(X)|$ the expected size.

**Theorem 2 (oracle optimality of stratum-wise density level sets).** *Fix $\alpha_1,\ldots,\alpha_K\in(0,1)$ and suppose that, for each $k$, the random variable $f(Y\mid X)$ has a continuous distribution conditional on $Y\in B_k$. Let $t_k>0$ satisfy $P\{f(Y\mid X)\ge t_k\mid Y\in B_k\}=1-\alpha_k$ and define*
$$C^\star(x)=\bigcup_{k=1}^K\{y\in B_k: f(y\mid x)\ge t_k\}. \tag{6}$$
*Then $C^\star$ satisfies $\mathrm{Cov}_k(C^\star)=1-\alpha_k$ for all $k$, and every prediction set $C$ with $\mathrm{Cov}_k(C)\ge 1-\alpha_k$ for all $k$ satisfies $\mathbb{E}|C(X)|\ge\mathbb{E}|C^\star(X)|$.*

*Proof.* Let $p_X$ be the marginal density (or law) of $X$ and write $A=\{(x,y): y\in C(x)\}$, $A^\star=\{(x,y):y\in C^\star(x)\}$ and $A_k=A\cap(\mathcal{X}\times B_k)$, $A_k^\star=A^\star\cap(\mathcal{X}\times B_k)$. Then $\mathbb{E}|C(X)|=\sum_k\iint_{A_k}p_X(x)\,dy\,dx$ and $p_k\mathrm{Cov}_k(C)=\iint_{A_k}f(y\mid x)\,p_X(x)\,dy\,dx$. For each $k$, the integrand of
$$\Delta_k=\iint\left(\mathbf{1}_{A_k^\star}-\mathbf{1}_{A_k}\right)\left(f(y\mid x)-t_k\right)p_X(x)\,dy\,dx$$
is non-negative: on $A_k^\star\setminus A_k$ we have $f\ge t_k$, and on $A_k\setminus A_k^\star$ (where $y\in B_k$) we have $f<t_k$. Hence $\Delta_k\ge 0$, i.e.
$$t_k\left(|A_k^\star|_{p}-|A_k|_{p}\right)\le p_k\left(\mathrm{Cov}_k(C^\star)-\mathrm{Cov}_k(C)\right)\le 0,$$
where $|A|_p=\iint_A p_X\,dy\,dx$. Since $t_k>0$, $|A_k^\star|_p\le|A_k|_p$ for every $k$; summing over $k$ gives the claim. $\square$

Theorem 2 is the regression counterpart of the Neyman–Pearson argument behind least-ambiguous set-valued classifiers with class-specific error levels [@sadinle2019least]; with $K=1$ it reduces to the familiar optimality of conditional-density level sets for marginal coverage [@lei2013distribution; @izbicki2022cdsplit]. Two consequences guide the method. First, the optimal score is the conditional density, $s(x,y)=-f(y\mid x)$, *combined with stratum-specific thresholds*; a single threshold is optimal only for marginal coverage. Second, the optimal sets need not be intervals: for an $x$ whose conditional density places non-negligible mass in a rare stratum, $C^\star(x)$ may include a separate piece of that stratum. Because any set satisfying the stratum constraints also satisfies the marginal constraint at level $1-\sum_k p_k\alpha_k$, the *price of stratum-wise validity*, $\mathbb{E}|C^\star(X)|$ minus the size of the optimal marginal set, is non-negative and equals zero exactly when the marginal level set already has equal coverage in every stratum.

## The proposed method: stratified density-level conformal prediction (SDLC)

SDLC instantiates (3)–(4) with the plug-in score $s(x,y)=-\hat f(y\mid x)$, where $\hat f$ is estimated on $\mathcal{D}_{\mathrm{tr}}$. By Theorem 1 the guarantee (5) holds for any $\hat f$; by Theorem 2 the sets approach the optimal ones as $\hat f$ approaches $f$. We use a semiparametric location–scale estimator,
$$\hat f(y\mid x)=\frac{1}{\hat\sigma(x)}\,\hat g\!\left(\frac{y-\hat\mu(x)}{\hat\sigma(x)}\right), \tag{7}$$
where $\hat\mu$ is a gradient-boosted regression of $Y$ on $X$, $\hat\sigma$ is a gradient-boosted regression of the absolute *out-of-fold* residuals $|Y-\hat\mu_{-j}(X)|$ (three folds, as in locally weighted conformal prediction [@lei2018distribution]), and $\hat g$ is a Gaussian kernel density estimate (Silverman bandwidth) of the standardised out-of-fold residuals. The noise density $\hat g$ is nonparametric, so (7) captures skewness and heavy tails of the error distribution, while heteroscedasticity enters through $\hat\sigma$. As a fully nonparametric alternative we also evaluate a histogram estimator obtained from a multiclass gradient-boosted classifier over $40$ equal-mass target bins (a "regression-as-classification" density, cf. @sesia2021conformal and @guha2024conformal).

**Implementation.** All densities are represented on a common grid of approximately $200$ equal-mass cells of the training targets spanning the domain $D=[\min y-0.05r,\max y+0.05r]$ ($r$ = training range); stratum edges are always grid edges, so every cell lies in a single stratum. The score of a calibration point is the density of the cell containing its target, which is exactly how membership of a candidate $y$ in a test set is decided, so Theorem 1 applies to the implemented procedure without approximation (for targets inside $D$; the fraction of test targets outside $D$ is reported). The primary stratification uses the training-target quantiles $0.10, 0.25, 0.75, 0.90$ ($K=5$: lower tail, lower shoulder, bulk, upper shoulder, upper tail). Algorithm 1 summarises the procedure.

> **Algorithm 1 (SDLC).** *Input:* $\mathcal{D}_{\mathrm{tr}}$, $\mathcal{D}_{\mathrm{cal}}$, levels $\alpha_k$, strata probabilities. (i) Fit $\hat\mu$, out-of-fold residuals, $\hat\sigma$ and $\hat g$ on $\mathcal{D}_{\mathrm{tr}}$; build strata and grid from training targets. (ii) For each calibration point compute $S_i=-\hat f(Y_i\mid X_i)$ and its stratum $k(Y_i)$. (iii) Compute $\hat q_k$ by (3) within each stratum. (iv) For a test $x$, evaluate $\hat f(\cdot\mid x)$ on the grid and return all cells $c$ with $\hat f(c\mid x)\ge-\hat q_{k(c)}$. *Cost:* fitting is that of three regressions; calibration is $O(n\log n)$; prediction is $O(G)$ per test point for a grid of $G$ cells.

## Two practical variants

*Floor variant (SDLC-floor).* Practitioners may want the marginal efficiency of a single threshold while protecting rare strata at a lower level $1-\beta$ ($\beta\ge\alpha$). Define $\hat C_{\mathrm{floor}}(x)=\{y: s(x,y)\le\max(\hat q^{\mathrm{marg}}_\alpha,\hat q_{k(y)}(\beta))\}$, where $\hat q^{\mathrm{marg}}_\alpha$ is the ordinary split-conformal quantile. Since $\hat C_{\mathrm{floor}}$ contains both the marginal set and the stratified set at level $\beta$, it has marginal coverage $\ge 1-\alpha$ and stratum-wise coverage $\ge 1-\beta$ simultaneously (finite sample). We use $\beta=2\alpha$.

*Hull variant (SDLC-hull).* When an interval is required, the convex hull of $\hat C(x)$ is reported. It contains $\hat C(x)$ and therefore inherits (5), at the price of larger size.

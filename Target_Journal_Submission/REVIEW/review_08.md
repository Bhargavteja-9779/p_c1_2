# Review 08: Hostile competing researcher (bin-conditional / relevance-weighted conformal prediction)

Manuscript: "Covering rare outcomes in imbalanced regression: stratified and relevance-weighted conformal prediction with density scores" (JKSU-CIS)

Reviewer stance: an author of competing work on bin-conditional and long-tail conformal methods. I tried to show that the work is incremental, unnecessary or overclaimed. I checked every number below against the result files with read-only Python. The scripts are in my scratchpad and modified no project file. I do not repeat issues closed in reviews 01–07; I re-raise two only where the earlier fix is incomplete, and I say why.

**Literature access caveat.** In this sandbox, arxiv.org, export.arxiv.org, proceedings.mlr.press and api.datacite.org were blocked: DNS failed or the proxy returned 403. I could not open any external paper. For the two papers I rely on (Yi, Tang & Wang 2025, arXiv:2510.10985, DOI 10.48550/arXiv.2510.10985; Bairaktari, Wu & Wu 2025, Kandinsky CP), I used the authors' own description in `supplementary/literature_matrix.md`, which says they read these papers, plus web-search snippets. The editor should have the descriptions of Yi et al. in issue 2 checked against the paper before relying on them. I cite no other external paper.

---

## Summary

The paper makes two claims.

**(A) SDLC.** Mondrian/BCCP calibration within strata of the target, which the paper credits as known, is combined with a conditional-density score. The paper shows that this score is oracle size-optimal per stratum (Prop. 2, a per-stratum Neyman–Pearson / Sadinle et al. argument) and asymptotically attainable (Prop. 3).

**(B) RW-DLC.** This is weighted split conformal prediction with label-only weights φ(y) (Theorem 2, via Tibshirani et al. 2019), plus the score φ(y)·f̂(y|x) (Prop. 4, again Neyman–Pearson). It is evaluated under a pre-specified plan on 17 held-out datasets.

The empirical work is large, carefully disclosed and mostly reproducible from the raw files. The headline numbers in the abstract match the result files. My concerns are about significance and novelty, not honesty:

1. Against the information-matched S-NCP, SDLC's size advantage is a consistent but practically small 2–3.5% at the median. SDLC also loses to S-NCP on exactly the quantities the paper is motivated by: top-5% and top-1% coverage, coverage under upward tilt, empty sets and alert cost. For a reader who cares about rare outcomes, the simpler competitor is the better choice, and the paper's own Discussion concedes this.
2. RW-DLC is, mathematically, weighted conformal prediction under a known target shift dQ/dP ∝ φ(y) with the weight-adjusted conditional-density (HPD-type) score. According to the authors' own literature matrix, this construction already exists for regression in Yi, Tang & Wang (2025). The manuscript cites that paper only in the distribution-shift paragraph and claims that "a regression counterpart has been missing".
3. The main empirical claim for RW-DLC (RW-3: top-1% coverage 0.872 vs 0.688) compares it with a stratified method that was not calibrated on the top 1%. A stratified method with a 1% tail stratum is feasible on all 17 held-out datasets, and was requested in review 01 (C1-03, item 6) but never run. This is the comparison that would show whether RW-DLC is needed at all.
4. The exploratory CTR23 arm of the RW plan was neither reported nor declared as a deviation, although reviews 05 and 06 raised it.

## Recommendation

**Major revision.** The paper is publishable as a careful empirical study of target-stratified conformal regression only if the RW-DLC novelty claim is re-scoped against Yi et al. (2025) and Kandinsky CP. It also needs the missing comparator (a stratified method with a 1% tail stratum) for RW-3, and the CTR23 RW arm reported or the deviation declared. None of this requires new model fits: the stratified comparator and the CTR23 RW arm run from cached contexts.

---

## Numbered issues

### 1. MAJOR: SDLC's advantage over the simple stratified normalised residual (S-NCP) is a 2–3.5% size reduction bought with worse coverage of the very outcomes the paper is about

**Location.** Abstract; Introduction contribution 1; §6.3.1; Table 6; Table 3; §7.2 item 3; Conclusion.

**Evidence.** I recomputed from `results/raw_eval_v3/*.jsonl` (CTR23) and `results/confirmatory/raw_eval_v3/*.jsonl` (held-out). Normalised size = size / y_train_sd, averaged over seeds per dataset, then compared across datasets with a two-sided Wilcoxon test on log ratios.

SDLC-LS vs S-NCP size, across every alternative summary I tried:

| Setting | n | GM ratio | Median ratio | Wins/losses | Datasets >2% smaller / >2% larger | p |
|---|---|---|---|---|---|---|
| CTR23, α=0.1, S5 | 31 | 0.975 | 0.966 | 27/4 | 21/3 | 0.0003 |
| CTR23, α=0.1, S5, excluding dev 44957/44959/44970 | 28 | 0.977 | 0.966 | 25/3 | 19/3 | 0.0009 |
| CTR23, α=0.05, S5 | 31 | 0.990 | 0.970 | 25/6 | 20/4 | 0.002 |
| CTR23, α=0.2, S5 | 31 | 0.938 | 0.954 | 28/3 | 23/2 | <0.001 |
| CTR23, S3 / S10 | 31 | 0.962 / 0.980 | 0.961 / 0.966 | 28/3 ; 26/5 | | <0.001 |
| Held-out, S5 / S3 / S10 | 17 | 0.977 / 0.975 / 0.987 | 0.977 / 0.973 / 0.978 | 15/2 ; 13/4 ; 14/3 | 11/1 (S5) | 0.004 / 0.031 / 0.013 |
| Hull forms, held-out | 17 | 1.040 | 0.994 | 10/7 | 5/4 | 0.71 |

The direction is robust, and I concede that. The magnitude is 2–4% at the median in every setting, and it vanishes once an interval is required.

Same datasets (`results/per_dataset_main_v3.csv`, CTR23, α=0.1), SDLC minus S-NCP:

- **Top-1% coverage:** −0.053 on average (median −0.016). SDLC is lower on 20 datasets and higher on 7 (Wilcoxon p = 0.003, unadjusted).
- **Top-5% coverage:** SDLC is lower on 23 of 31.
- **Upper-stratum coverage under tilt γ=2:** −0.036. SDLC is lower on 24 of 31.
- **Empty sets:** 0.36% vs 0.07% (higher on 15, lower on 3).
- **Upper-tail alert rate:** higher on 18 of 31. §6.6 already reports a higher expected cost on 27/31 datasets at c=10.
- **Worst σ̂-decile coverage:** 0.769 vs 0.793 on average.

Proposition 2 explains why. Within a tail stratum, the size-optimal set puts its misses at the lowest-density, outermost points, which are the most extreme outcomes. The "optimal score" is therefore, by construction, anti-aligned with the paper's own motivation.

The Discussion (§7.1, §7.2 item 3) and the Conclusion concede this. The abstract and the contribution list still lead with "the smallest valid sets" / "the size-optimal score". The abstract says only that SDLC's sets "were within a few percent" of S-NCP's. It omits that S-NCP covered more of the top 1% on CTR23 (0.789 vs 0.736) and on held-out data (0.781 vs 0.747; 0.793 vs 0.760 under the unified definition, Table S17b).

**Fix.** Text only, no new computation:

1. In the abstract, add one clause: S-NCP's sets were within a few percent of SDLC's and covered more of the most extreme outcomes.
2. Re-title contribution 1 as an efficiency characterisation, not a recommended method, or state its trade-off in the same sentence.
3. Report the per-dataset "datasets >2% smaller / larger" counts so readers can judge practical relevance. The median is 2–4%, and only 11 of 17 held-out datasets gain more than 2%.

### 2. MAJOR: RW-DLC is weighted conformal prediction under a known target shift with a weight-adjusted density score; the regression version of this construction appears to exist (Yi, Tang & Wang 2025), and the paper does not credit it as such

**Location.** Introduction, paragraph 4 ("a regression counterpart has been missing") and contribution 2; §2.2 last sentences; §2.4; §4.7 (Theorem 2, Proposition 4); Table 1, RW-DLC row; cover letter ("We introduce relevance-weighted coverage for continuous outcomes").

**Evidence.**

- The manuscript itself states (§4.7, after Theorem 2) that relevance-weighted coverage is "Equivalently ... coverage ... for a test point drawn from the target-shifted law Q with dQ/dP = φ(y)/Eφ(Y)". The proof is Tibshirani et al. (2019), Lemmas 1 and 3, with a label-only likelihood ratio, exactly as in Podkopaev & Ramdas (2021) for classification.
- Prop. 4's optimal set {y: φ(y) f(y|x) ≥ t} is the level set of the weight-adjusted conditional density. Up to the x-dependent normaliser it is the target-domain conditional density under that shift, q(y|x) ∝ w(y) f(y|x).
- The authors' own `supplementary/literature_matrix.md` (row `yi2025distribution`, and row 35) describes Yi, Tang & Wang (2025), arXiv:2510.10985 (DOI 10.48550/arXiv.2510.10985), as "Regression target shift: likelihood-ratio identification plus HPD sets from a weight-adjusted conditional density". A web search returned the same description: an estimated ratio, then prediction sets from a weight-adjusted conditional density using highest predictive density sets.
- RW-DLC therefore differs from that construction mainly in that (i) the weight is a user-chosen relevance φ rather than an estimated density ratio, and (ii) Prop. 4 uses one global threshold under P_X. Point (i) is a reinterpretation, not a new mechanism. I could not open the paper (see the caveat at the top), so the precise overlap of the score, the calibration and any optimality statement must be checked by the authors, who say in the matrix that they read it.
- The manuscript cites yi2025distribution only in §2.4 as a method that "estimate[s] the shift" and contrasts it with stratified calibration. It never relates it to RW-DLC in §4.7 or Table 1.
- Kandinsky CP (Bairaktari et al. 2025), as described in the authors' own matrix row 32, covers weight classes {Φ(x,y)ᵀβ} with label-dependent, fractional groups. A single basis function Φ(x,y) = φ(y) gives a (high-probability, approximate) relevance-weighted coverage guarantee. Table 1 lists Kandinsky, but §4.7 does not say that relevance-weighted coverage is a one-function special case of its target.

**Fix.** Text only:

1. In §4.7, state that RW-DLC calibration is weighted conformal prediction under a known label-only shift. State that its score is the weight-adjusted density used for regression target shift by Yi et al. (2025), and that the novelty is the interpretation (imbalanced-regression relevance as the "shift") and the empirical study.
2. Delete "a regression counterpart has been missing" (Introduction) and "We introduce relevance-weighted coverage" (cover letter), or qualify them.
3. Add Yi et al. and Kandinsky (single weight function) to the RW-DLC discussion and to Table 1.
4. Verify the Yi et al. description against the full text before re-wording.

### 3. MAJOR: RW-3, the main empirical result for RW-DLC, is a comparison with a stratified method that was not calibrated on the top 1%; the obvious competitor, a stratum at the top 1%, is feasible on every held-out dataset and was never run

**Location.** Abstract ("covered 87.2% of the top 1% of outcomes, against 68.8% for SDLC"); §4.7 first paragraph ("refining the strata quickly leaves too few calibration points"); §6.4 RW-3; §7.2 item 1; Conclusion; cover letter.

**Evidence.**

- SDLC in the RW study uses the S5 strata, with an upper stratum at the training 90% quantile. Its top-1% coverage is therefore not calibrated. RW-DLC wins RW-3 by construction of the comparison, not because strata cannot reach the top 1%.
- Feasibility: the calibration-set sizes in `results/confirmatory/raw_eval_v3` are 1,052–12,500 rows. A top-1% stratum would hold about 11, 22, 22, 22, 25, 34, 42, 43, 57 and 125 (×8) calibration points. Every dataset exceeds the 1/α − 1 = 9 points needed for a finite threshold at α = 0.1. For comparison, RW-DLC's own smallest Kish ESS was 120 (§6.4).
- Review 01, C1-03 item 6, asked for an "extreme-strata stress test" with cut points at training quantiles {0.01, 0.05, 0.10, 0.25, 0.75, 0.90, 0.95, 0.99}. Response 01 addressed C1-03 with text and the top-1% metric only. The scheme was never added: the raw files contain schemes S3, S5 and S10 only. This review re-raises the request because it has become decisive. The RW study now rests its main claim on the unresolved-strata comparator.
- The relevance-weighted ablations already show that much of RW-3 comes from weighting alone. From `results/rw/confirmatory/*.json`, seed-averaged:
  - RW-NCP-U covers 0.784 of the top 1%; RW-DLS-U covers 0.805.
  - Under the unified definition, RW-DLC-U is higher than RW-NCP-U on 13/17 datasets, by +0.060 on average.
- RW-DLC also pays in marginal coverage, which the abstract summarises only as "lower coverage of typical outcomes":
  - Its marginal coverage per dataset is below 0.85 on 5 of 17 held-out datasets: elevators 0.750, sulfur 0.783, Ailerons 0.847, medical_charges 0.847, SGEMM 0.849.
  - Its worst-decile coverage is lower than SDLC's on 13/17 datasets and lower than S-NCP's on 14/17.

**Fix (new computation, cheap, from cached contexts; no refitting).** Add a stratification scheme with cut points at {0.01, 0.10, 0.25, 0.75, 0.90, 0.99} (or the C1-03 scheme) to `evaluate_from_cache3.py` / `run_rw.py`. Evaluate S-NCP, SDLC and BCCP on the 17 held-out datasets with the same grid, and report the following against RW-DLC-U, labelled post hoc:

- top-1% coverage;
- marginal coverage;
- worst-decile coverage;
- size;
- the number of infinite thresholds.

Then report:

- in the abstract, the number of held-out datasets with RW-DLC marginal coverage below 0.85 (5 of 17);
- if the 1%-stratum methods match RW-DLC on top-1% coverage at similar size, that strata suffice. Otherwise RW-DLC's advantage becomes a real finding.

### 4. MAJOR: the pre-specified exploratory CTR23 arm of the RW study is missing and not declared as a deviation (re-raised from reviews 05 and 06; the fix is inadequate)

**Location.** `PREREGISTRATION_relevance_weighted.md` §2 ("Exploratory: all 31 OpenML-CTR23 datasets ... The same analysis is run on both") and §5 ("Any change after this commit will be listed in the manuscript as a deviation"); manuscript §5.7 and §6.4; Supplement Table S18.

**Evidence.**

- `results/rw/` contains only `confirmatory/`.
- `results/rw_statistics.json` has the single key `confirmatory`.
- Table S18's "suite" column holds only `confirmatory`.
- `PROJECT_STATE.md` (lines 35, 62–71, 94–96) lists `run_rw.py ctr23` as pending.
- Response 05 (item 10) promised the arm, and review 06 asked that it be run or that the citation of a CTR23 RW table be removed. The citation was removed, but the manuscript now says nothing about the arm and lists no deviation.

The omission matters. CTR23 contains the regime where RW-DLC is most likely to fail: calibration sets of 129–1,044 points on 12 datasets, extreme skewness up to 59, and atoms. The held-out collection, by the paper's own admission (§5.1 iii), contains none of these.

**Fix.** Either run the CTR23 arm (310 tasks from refitted contexts, already scripted) and report RW-1 to RW-4 in Table S18 with one sentence in §6.4, or state in §5.7 that the pre-specified CTR23 arm was not run and why. The first option is strongly preferred.

### 5. MODERATE: the RW study is labelled "pre-specified" but reuses held-out data whose tail behaviour was already known, and RW-1 to RW-3 were nearly certain by construction

**Location.** §5.7 "Relevance-weighted study"; §6.4; Abstract ("a second pre-specified study").

**Evidence.**

- The RW plan (commit a9f31d2, 2026-11-20) was written after the confirmatory evaluation of SDLC, S-NCP and the marginal methods on the same 17 held-out datasets (commit adeec38, 2026-11-18). Before writing RW-3, the authors therefore knew SDLC's top-1% coverage on these data: §6.3.3 reports 0.747.
- RW-1 is Theorem 2.
- RW-2 compares a φ-weighted-calibrated method with unweighted methods on the φ-weighted metric.
- RW-3 compares an inverse-density-weighted method with a method that is not calibrated at the top 1% (issue 3).
- The only hypothesis that could fail on empirical grounds, RW-4 (score optimality), failed (Holm p = 0.053 for both comparisons).
- The git order is consistent with the claims: a9f31d2 at 23:02:56, the evaluator fd68e0d at 23:06:14, partial results 1c9ee4b at 23:06:24. These are commit times only, so they cannot show when the files were produced, and three commits in under four minutes suggest batch commits.

**Fix.** Text only:

1. In §5.7, state that the RW plan was written after the held-out results for the comparators were known, and that RW-1 to RW-3 follow largely from the construction.
2. Call RW-4, the only empirical test of Prop. 4, "not supported" in the abstract or the contribution list, not only in §6.4.

### 6. MODERATE: the theoretical results are short corollaries of known arguments; the contribution list should say so as plainly as §4 does

**Location.** Introduction, contributions 1–2 ("we prove finite-sample validity ... (Theorem 2), show that level sets ... are the smallest valid sets (Proposition 4)"); Table 1 (columns "Size optimality").

**Evidence.**

- Prop. 2's proof is a stratum-wise copy of the Neyman–Pearson / Sadinle et al. (2019) argument. The constraints separate by stratum, so the result is immediate once this is noticed.
- Prop. 4 is the same argument with the measure φ(y) f(y|x) dy dP_X.
- Theorem 2 is Tibshirani et al. (2019), Lemmas 1 and 3, verbatim with w = φ / Eφ.
- Prop. 3 follows the plug-in arguments of Lei et al. (2013) and Izbicki et al. (2022). It does not cover the implementation (fixed λ, floor and truncation), as §4.3 admits.
- Prop. 1 is a bivariate-normal calculation.

Section 4 credits all of this fairly ("the per-stratum form of known level-set results", "applies the weighted-exchangeability argument"). The Introduction's verbs ("we prove", "show") and the cover letter present them as contributions on a par with the empirical study.

**Fix.** Text only: in the Introduction, rephrase as "we note/derive (by the standard argument) that ...". Present the empirical characterisation of the efficiency/extreme-tail trade-off as the main contribution.

### 7. MODERATE: implementation changes made after seeing results all favoured the density-based methods; the replication mitigates this for C-H3, but the CTR23 evidence is still presented as if pre-specified in the cover letter

**Location.** §5.7 "What changed afterwards"; Supplement Table S19; cover letter ("Evidence under pre-specified analysis plans. 31 OpenML-CTR23 datasets ...").

**Evidence.**

- Table S19: SDLC vs BCCP went from Holm p = 0.809 (v1) to 0.017 (v2) to < 0.001 (final). SDLC vs S-NCP went from a median log ratio of +0.023 (v1, SDLC larger) to a GM of 1.004 (v2) to 0.975 (final).
- The changes listed in §5.7(3)–(4) were cross-fitted standardisation of ĝ, a defensive t component, stratum-exact geometry and a truncated domain. They act almost entirely on the density-based scores. S-NCP and BCCP are closed-form intervals and gain little from exact geometry.
- The manuscript discloses this and correctly labels the CTR23 size comparisons exploratory.
- The confirmatory plan (ccba99b) froze the implementation. Between ccba99b and the held-out results (adeec38), the only code changes I found were NaN handling in `statistics/tests.py` and task enumeration in `refit_scales.py`, neither of which affects any method.
- Point (4) is therefore handled adequately in the paper, except for one problem: the cover letter's sentence groups CTR23 under "pre-specified analysis plans".

**Fix.** Text only: in the cover letter, say that the CTR23 size comparisons are exploratory and only the held-out replication is pre-specified.

### 8. MINOR: three different "SDLC top-1% coverage on held-out data" numbers, and the abstract uses the definition with the largest gap

**Location.** Abstract and §6.4 (0.688, strict y > q₀.₉₉, n = 15 datasets); §6.3.3 (0.747, y ≥ q₀.₉₉, all seeds); Table S17b (0.760, y ≥ q₀.₉₉, seeds with at least 10 test points).

**Evidence.** Table S17b: RW-DLC minus SDLC is 0.184 under the strict definition and 0.125 under the unified definition, with RW-DLC at 0.872 vs 0.884. The pre-specified definition is legitimate to report, but leaves 2 datasets empty, and the abstract gives no hint that the gap is about one-third smaller under the paper's own main-pipeline definition.

**Fix.** Text only: in the abstract, add "(0.884 vs 0.760 with the main-pipeline definition)", or use the range "0.13–0.18".

### 9. MINOR: RW-DLC's size relative to SDLC is described only by the geometric mean, although the paper's stated primary size estimand is Hodges–Lehmann

**Location.** §6.4 ("Its sets were not reliably larger than SDLC's (geometric-mean ratio 1.081 ...)"); Fig. 6 caption.

**Evidence.** From `results/rw/confirmatory/*.json`, RW-DLC-U / SDLC:

- HL ratio 1.115;
- median ratio 1.174;
- larger on 9 of 17 datasets (two-sided Wilcoxon p = 0.145).

Against S-NCP: HL ratio 1.060, median ratio 1.148. §6.3.1 says "The Hodges–Lehmann ratio ... is our primary size estimand".

**Fix.** Text only: report the HL ratio (1.12) and the median (1.17) next to the GM in §6.4.

---

## Points checked and found adequate

- **Abstract numbers.** Worst-stratum coverage of the seven marginal/covariate-adaptive methods is 0.630–0.783 (`per_dataset_main_v3.csv`). Stratified methods fall below the null 5% quantile on 1–2 of 31 datasets. RW-DLC's φ_U coverage is 0.898 and its top-1% coverage 0.872 vs 0.688 (pre-specified definition). The 70.5% oracle figure matches Table 2. All verified.
- **"SDLC's worst-stratum coverage exceeded that of each marginal method on at least 29 of 31 datasets."** Verified: 29–31 of 31.
- **Table 6 / Table 8 size ratios.** My recomputation from raw jsonl reproduces SDLC vs S-NCP / S-HPD / BCCP / S-CQR to three decimals: CTR23 0.975 / 0.947 / 0.902 / 0.795 with wins 27 / 28 / 24 / 27; held-out 0.977 / 0.984 / 0.862 / 0.841 with wins 15 / 15 / 14 / 15. Hull-form results (CTR23 1.014; held-out 1.040, 10/7) are as reported.
- **Robustness of the SDLC-vs-BCCP/S-CQR advantage.** It survives medians, win counts, exclusion of the 3 development datasets, α ∈ {0.05, 0.2}, S3/S10 strata, reduced calibration fractions and the held-out data. Against BCCP, the median ratio is 0.92–0.97 and the GM 0.86–0.94. This is the paper's solid empirical result. It is fairly stated, though I note the BCCP comparator is BCCP with the absolute residual, as the BCCP paper uses, and that S-NCP (BCCP with a normalised score, which BCCP admits) captures most of the gain.
- **Development datasets.** The exclusion analyses in Table S5 use the 3 configured development datasets (`code/config/benchmark.json: dev_datasets`) and, separately, the 10 development+diagnostic datasets. §5.2's "ten datasets" is consistent with the latter.
- **Confirmatory plan integrity.** No method code changed between ccba99b and the held-out results (adeec38). The C-H3 decision rule was applied as written. The weak points (bootstrap CIs for S-NCP and S-HPD include 1) are stated in the text.
- **Theorem 2 proof.** It is correct for a candidate-dependent q(y): the label-only weight enters both the multiset conditioning and the normaliser W + φ(y). Theorem 1 and Corollary 1 are correctly stated and credited as known.
- **Crediting of BCCP.** Table 1 and §2.2 credit stratified calibration, its validity and its shift robustness to BCCP and Mondrian conformal prediction, and do not claim them. As a BCCP-side reader, I find this fair.
- **RW-4 negative result.** It is reported honestly as not supported.

# Review 10 (final adversarial check before submission)

## Summary

The manuscript is in good shape. Theory, the main benchmark tables, Table 7 (confirmatory), Table 8 and the RW hypothesis tests, the timing paragraph and most supplement cross-references agree with the result files; I recomputed a sample with read-only Python (details below). The remaining problems come from the review-8/9 restructuring and the post hoc tail-strata analysis:

- The manuscript title differs from the title on the title page and in the cover letter.
- The headline RW-DLC number in the abstract, conclusion and cover letter (88.4% vs 76.0%) uses a post hoc definition. The conclusion attributes it to the pre-specified study, while the body reports 87.2% vs 68.8%.
- "About a third smaller" is wrong arithmetic (the ratio is 0.749, so the sets are 25% smaller). "Where sparse ... a third larger" is not what the data show.
- A few sentences contradict their own supplement tables: the shift results, the temporal splits and the skewness limitation.
- There are several mechanical cross-reference errors (a wrong section, a wrong equation number, leftover "review round" labels).

All of these can be fixed in the text. None needs new experiments.

## Recommendation

Minor revision before submission. Fix Issues 1–4 without fail; they are the ones a referee or editor would notice. The rest are quick mechanical fixes.

## Numbered issues

### 1. MAJOR: Title of the manuscript differs from the title page and the cover letter
- **Location:** `manuscript/src/00_front.md` (rendered title) vs `manuscript/src/title_page.md`, `manuscript/src/cover_letter.md`. Also in `manuscript/title_page.docx`, `manuscript/cover_letter.docx`.
- **Evidence:** The manuscript and Final_Manuscript.docx read "Covering rare outcomes in imbalanced regression with conformal prediction: guarantees, size-optimal scores and what tail coverage costs". The title page and cover letter (md and docx, checked by text extraction) read "Covering rare outcomes in imbalanced regression: stratified and relevance-weighted conformal prediction with density scores". Commit 857758b ("Review 9: reframed title/abstract...") changed only the manuscript.
- **Fix:** Copy the manuscript title into `title_page.md` and `cover_letter.md`, then rebuild both docx files.

### 2. MAJOR: Headline RW-DLC result uses a post hoc definition that the body does not report, and the conclusion calls it pre-specified
- **Location:**
  - Abstract: "RW-DLC covered 88.4% of the top 1% of held-out outcomes against 76.0% for SDLC with five strata".
  - Conclusion (Section 8): "in a second pre-specified study covered 88.4% of the top 1% of outcomes on held-out data, against 76.0% for SDLC".
  - Cover letter, *Evidence*: same numbers.
  - Section 6.4, *Dedicated tail strata*: "against 0.884 for RW-DLC".
- **Evidence:**
  - The pre-specified RW-3 result, reported in Section 6.4, Table 8 and Fig. 6, is 0.872 vs 0.688 (`rw_statistics.json` confirmatory/RW-3: rw 0.8719, sdlc 0.6882, n = 15).
  - 0.884 / 0.760 is the post hoc "unified" variant ($y\ge q_{0.99}$, at least 10 test points per seed): `statistics_review05.json` rw3_sensitivity, Table S17b. It appears only in Supplementary Section S8.3b, labelled "post hoc".
  - 76.0% appears nowhere in the main text. A reader who checks the abstract against Table 8 finds 0.872/0.688.
  - In Section 6.4 the definition switches silently: Table 8 says RW-DLC covered 0.872, and two paragraphs later "0.884 for RW-DLC". That 0.884 also equals RW-DLC's marginal coverage, 0.884 in the same sentence, which reads like a copy error.
- **Fix:** Choose one of the following.
  - (a) Use the pre-specified numbers in the abstract, conclusion and cover letter: "87.2% ... against 68.8%".
  - (b) Keep 88.4/76.0, but in the conclusion delete "in a second pre-specified study" before these numbers or add "(post hoc unified definition of the top 1%; 87.2% vs 68.8% under the pre-specified definition)". In Section 6.4, *Dedicated tail strata*, write: "against 0.884 for RW-DLC (top 1% defined as $y\ge q_{0.99}$ with at least 10 test points per seed, as in Supplementary Section S8.3b; 0.872 under the pre-specified definition of Table 8)".
  - Either way, add one main-text sentence under RW-3 that states the 0.884 vs 0.760 values if they stay in the abstract.

### 3. MAJOR: "About a third smaller" is arithmetically wrong, and "where sparse ... about a third larger" misstates the data
- **Location:**
  - Section 7.1 item 1: "it reached the same coverage of the top 1% with sets about a third smaller than dedicated strata".
  - Cover letter: "whereas on smaller datasets RW-DLC needs sets about a third smaller" (this sentence is also ungrammatical).
  - Abstract: "dedicated 1% strata matched this coverage but, where sparse, gave sets about a third larger".
  - Conclusion: "about a third larger on the smaller CTR23 datasets, where such strata are sparse".
- **Evidence:** `statistics_review08.json` ctr23."vs SDLC-S7".size_geo = 0.749 (HL 0.779). RW-DLC sets are therefore 25% smaller (22% by HL); dedicated-strata sets are 1/0.749 = 1.34 times larger. The commit message of 9c1356a itself says "~25% smaller". The 0.749 is the geometric mean over all 31 CTR23 datasets. I recomputed it by sparsity using `raw_tail1_ctr23` and `rw/ctr23`:
  - On the 12 datasets with an infinite 1% threshold, the ratio is 0.55 (dedicated sets about 1.8 times larger; RW-DLC smaller on 11 of 12).
  - On the 19 others it is 0.911.
  - The top-1% coverage match (0.913 vs 0.917) is computed on 24 datasets with at least 10 top-1% test points. Only 5 of the 12 sparse datasets are among them.

  So on sparse datasets the size penalty is about 1.8, not "a third". The "matched coverage" claim rests mostly on the non-sparse datasets.
- **Fix:**
  - Section 7.1 and cover letter: replace "about a third smaller" with "about a quarter smaller".
  - Abstract: "dedicated 1% strata matched this coverage on the large held-out datasets, but on the smaller CTR23 datasets, where these strata were often too sparse, their sets were about a third larger on average".
  - Section 6.4: add "(top-1% coverage over the 24 datasets with at least 10 such test points per seed; on the 12 datasets with sparse 1% strata RW-DLC's sets were about 45% smaller, geometric-mean ratio 0.55)". Export these two subgroup numbers from `analyze_review08.py`.
  - Cover letter: "whereas on smaller datasets RW-DLC reaches it with sets about a quarter smaller".

### 4. MODERATE: Section 6.5 states the opposite of Supplementary Table S22 for SDLC vs S-NCP
- **Location:** Section 6.5: "under a strong tilt every method lost coverage of the upper stratum, the stratified ones less (0.770–0.833, against 0.550–0.726), and SDLC less than S-NCP".
- **Evidence:** In the parallel construction this reads as "SDLC lost less than S-NCP". Table S22 shows SDLC 0.798 against S-NCP 0.833 under γ = 2, so SDLC lost more. S8.4 says it correctly: "SDLC (0.798) was below S-NCP and S-HPD (0.833)".
- **Fix:** Replace with "and SDLC more than S-NCP (0.798 against 0.833; Supplementary Section S8.4)".

### 5. MODERATE: The temporal and grouped split results are overstated or reported selectively
- **Location:**
  - Section 6.7: "splitting video transcoding by video and Moneyball forward in time enlarged all sets several-fold and removed SDLC's size advantage".
  - S8.6: "With Moneyball split forward in time ..., stratified methods kept close to nominal coverage (0.881 for SDLC)".
  - Section 6.7: "Splits that ... hold out whole months changed little".
- **Evidence (Table S15):**
  - Moneyball forward: marginal sets grew only 1.4–1.6 times (SCP 0.906→1.422, CQR 1.110→1.757, HPD-split 0.947→1.368). Video by video: CQR grew 1.8 times (0.253→0.466). "All sets several-fold" is false.
  - 0.881 is SDLC's *marginal* coverage. Its worst-stratum coverage was 0.802 (stratified range 0.802–0.877). The marginal methods had *higher* worst-stratum coverage (CQR 0.927, SCP 0.862) with sets about half the size. This is the one setting where stratified calibration lost its tail advantage, and the text does not mention it.
  - Bike sharing by month: S8.6 itself says "sets grew by about a quarter", which conflicts with "changed little".
- **Fix:**
  - Section 6.7: "enlarged the sets of the stratified methods three- to six-fold (marginal methods 1.4–4 fold) and removed SDLC's size advantage".
  - S8.6: "stratified methods kept close to nominal marginal coverage (0.881 for SDLC), but their worst-stratum coverage fell to 0.80–0.88, below that of the over-covering marginal methods (CQR 0.927), whose sets were about half as large".
  - Change "hold out whole months changed little" to "hold out whole months enlarged sets by about a quarter but left the conclusions unchanged".

### 6. MODERATE: The limitation on skewness contradicts the held-out subgroup results
- **Location:**
  - Section 7.2, *Evaluation scope*: "none with the extreme skewness of some CTR23 targets, so it does not test the regimes in which the CTR23 size advantage disappeared (small or strongly skewed targets)".
  - Section 5.1: "no extremely skewed target ($|$skewness$|\le$ 6.7 ...)".
- **Evidence:**
  - Section 6.3 defines "strongly skewed" as |skewness| > 1 (15 CTR23 datasets).
  - The held-out collection has 7 such datasets (Table S17, training-target skewness). Section 6.3.1 and S8.3 report that on them "the advantage over S-NCP ... disappeared". So the held-out data did test, and replicated, the strongly-skewed regime.
  - Table S17 gives a training-target skewness of 7.362 for sulfur (44145), above the "≤ 6.7" bound. That bound is the full-data value from Table S2 (6.72).
- **Fix:**
  - Section 7.2: "... and none with the extreme skewness (above about 7) of some CTR23 targets. It contained no small datasets, the regime in which the CTR23 size advantage disappeared; on its 7 strongly skewed datasets the advantage over S-NCP disappeared as on CTR23".
  - Section 5.1: "$|$skewness$|\le$ 6.7 on the full data".

### 7. MODERATE: Three different held-out top-1% coverages for SDLC with no reconciliation in the text
- **Location:**
  - Section 6.4: "top-1% coverage of SDLC 0.688 on the held-out datasets".
  - Abstract and conclusion: 76.0%.
  - S8.3: "SDLC covered 0.747 of the top 1%, against 0.781 for S-NCP (... top 1% defined as $y\ge q_{0.99}$ ..., as everywhere in the main pipeline)".
- **Evidence:**
  - Table S17b (continued) and `statistics_review08.json` held-out.top1_sdlc_vs_sncp give, under the same $y\ge q_{0.99}$ definition with at least 10 test points, SDLC 0.760 vs S-NCP 0.793.
  - S8.3's 0.747/0.781 is a third variant (no minimum-count rule), although S8.3b says the ≥10 rule is the main-pipeline definition.
  - S8.3's own claim "as everywhere in the main pipeline" is therefore inconsistent with S8.3b and S17b.
- **Fix:** In S8.3 replace "0.747 ... 0.781" with "0.760 ... 0.793 (17 datasets; Table S17b)", or state "(all seeds, no minimum count)". Fix together with Issue 2.

### 8. MODERATE: Leftover internal-process labels in the supplement
- **Location:** Table S17b caption: "(review round 5; scripts/analyze_review05.py; ...)". Table S17b (continued, third block): "(... review round 8; experiments/eval_tail1.py ...)". Both also appear in Supplementary_Material.docx (2 occurrences).
- **Evidence:** In a first submission, "review round 5/8" suggests an earlier rejected submission or exposes the simulated-review workflow. Referees will ask about it.
- **Fix:** Replace with "(post hoc check; scripts/analyze_review05.py)" and "(post hoc; experiments/eval_tail1.py, scripts/analyze_review08.py)". Rename the script mentions too if desired.

### 9. MINOR: Wrong section cross-reference for RW-4
- **Location:** Section 5.7, *Relevance-weighted study*: "only RW-4 could fail for empirical reasons, and it did (Section 6.3.1)". Source: `03_setup.md` line 61, `[-@sec:confirmatory]`.
- **Evidence:** RW-4 is reported in Section 6.4 (`sec:rw-results`). Section 6.3.1 is the SDLC confirmatory replication.
- **Fix:** Change `[-@sec:confirmatory]` to `[-@sec:rw-results]`.

### 10. MINOR: Wrong equation number in Table B1
- **Location:** Appendix B, Table B1: "stratum-wise and relevance-weighted coverage (Eqs. 1 and 10)".
- **Evidence:** $\operatorname{Cov}_\phi$ is Eq. (9). Eq. (10) is $q(y)$, which the next row correctly cites.
- **Fix:** "(Eqs. 1 and 9)".

### 11. MINOR: Main text points to S8.3 for the RW-3 definition check, but it is in S8.3b
- **Location:** Section 6.4, RW-3: "The definition-sensitivity of RW-3 is reported in Supplementary Section S8.3".
- **Fix:** "Supplementary Section S8.3b and Table S17b".

### 12. MINOR: Broken sentences from replacing figure and section references in the supplement
- **Location:**
  - S8.5: "... below 0.9 on 4–6 datasets. the cost figure of the main text shows cost curves ..." (sentence starts in lower case).
  - S8.1: "(the protocol section of the main text); the confirmatory section of the main text tests them".
  - S8.4: "(Supplementary Table S22, the shift figure of the main text)".
- **Fix:**
  - S8.5: "Fig. 8 of the main text shows cost curves ...".
  - S8.1: "(main text, Section 5.7); Section 6.3.1 of the main text tests them".
  - S8.4: "(Table S22; Fig. 7 of the main text)". Inside the supplement, write "Table S22", not "Supplementary Table S22".

### 13. MINOR: Robustness claim on effective sample size (ESS) is only partly true
- **Location:** S8.4: "restricting the analysis to the 15 datasets where it was at least 50 left the ordering unchanged".
- **Evidence (Table S22, γ = 2, ESS ≥ 50 column):**
  - BCCP (0.754) falls below the marginal method DCP (0.765), so stratified and marginal methods no longer separate.
  - BCCP/S-CQR and SCP/DLS swap order.
  - Only the SDLC < S-NCP = S-HPD ordering is preserved.
- **Fix:** "left SDLC below S-NCP and S-HPD (0.774 vs 0.825), but BCCP and S-CQR (0.754, 0.761) then no longer exceeded the best marginal method (DCP, 0.765)".

### 14. MINOR: Fig. 6 caption does not describe the left panel
- **Location:** Fig. 6 caption.
- **Evidence:** The figure has two panels, "OpenML-CTR23 (exploratory)" and "Held-out datasets". The caption speaks only of the held-out values (Table 8, ratio 1.081). The plotted top-1% values use the pre-specified definition (0.872/0.688), not the abstract's 0.884/0.760 (see Issue 2).
- **Fix:** Add "Left: the 31 CTR23 datasets (exploratory arm, Supplementary Table S19); right: the 17 held-out datasets (Table 8). Top 1% as pre-specified ($y>q_{0.99}$)."

### 15. MINOR: Remark A.1 cites the wrong place for its empirical support
- **Location:** Appendix A, Remark A.1: "for the estimated sets the same pattern is observed empirically (Section 6.5)".
- **Evidence:** Section 6.5 reports only stratum-level coverage under tilts, not coverage within strata. The within-stratum dip is visible in Fig. 2 (deciles 2 and 9).
- **Fix:** "(Fig. 2, deciles 2 and 9; Section 6.5)".

### 16. MINOR: Cover letter wording
- **Location:** Cover letter, *Reproducibility*: "the pre-specified confirmatory analysis plan".
- **Evidence:** There are two plans (Section 5.7, Code availability).
- **Fix:** "both pre-specified analysis plans".

## Points checked and found adequate

- **Abstract, introduction and conclusion vs Table 3, Table 4 and Table 5:**
  - Worst-stratum coverage of 63.0%–78.3% matches Table 3 (0.630–0.783).
  - The price of 1.24 [1.12–1.45] matches Table 4. The gains of 0.231 (range 0.126–0.260) and "23–28 of 31" match Table 5.
  - Proposition 1 values (70.5%, 37.5%, 94.9%, 86.2%) match Table 2.
- **Section 6.1:** every range (0.690–0.820, 0.445–0.655, 26–31 datasets, 0.906–0.909, 0.890–0.893) agrees with Table 3.
- **Section 6.3:**
  - Ratios, HL, wins/losses and Holm p match Table 6 and Table S5.
  - "Holm $p\le$ 0.002" is the maximum in Table S5.
  - The subset statements (9 small datasets 5/4; 15 skewed 12/3, p = 0.127) match Table S5.
  - Top-5% 22/31 and held-out top-1% 13/17 match `statistics_review08.json`.
- **Table 7 vs `confirmatory/statistics_confirmatory.json`:** all HL differences, geometric-mean ratios with CIs, wins/losses, Holm p, C-H2 (1 of 17, critical value 3, binomial 0.582) and C-H4 (margin 0.02 as in the plan) match.
- **Section 6.4 and Table S18 vs `rw_statistics.json`:**
  - RW-1: 0.898, TOST.
  - RW-2: 0.122–0.180, Holm < 0.001.
  - RW-3: 0.184 [0.063, 0.310], 13/15, p = 0.011.
  - RW-4: 0.885/0.904, Holm 0.053.
  - CTR23 arm: 0.901, 0.907 vs 0.715, 28/28, 0.828/0.874.
  - Descriptive size ratio 1.081 [0.916, 1.240], worst-decile difference −0.080.
- **Dedicated-strata numbers vs `statistics_review08.json`:** held-out 0.906, min 0.87, marginal 0.901/0.884, 0.952, HL 0.987, 9/17, 1 dataset with infinite threshold. CTR23 0.913/0.917, 12 datasets with infinite threshold, 24/31, 0.749, marginal 0.862/0.904. I recomputed 0.952 and 0.749 from the raw files.
- **Timing paragraph vs `timing_summary.json`:** 13.3 µs, 0.07 µs, factor 207, 1.32, max 77, about 6 ms, 1.5 ms, 143 µs, ratio 1.01, 4.9 s, 202 MB, grid change < 0.1%.
- **Grouped splits (S8.6) vs Table S15:** video 0.113→0.775, ratio 1.205, 0.852–0.904, 0.875/0.873; sarcos and superconductivity ratios. The Limitations range of 0.75–0.89 matches `statistics_review05.json` grouped.video.
- **Equation numbering:** (1)–(10) and (A.1) are tagged consistently. All other "Eq./(n)" references point correctly, apart from Issue 10.
- **Supplementary references:** every cited Supplementary Table S1–S23, Section S2–S8.7 and Fig. S4 exists and holds the claimed content, apart from Issues 11 and 12. Development and diagnostic datasets total 10, as stated in Section 5.2.
- **Bibliography:** every citation key in the manuscript resolves in `references_verified.bib`. The journal self-citations in the cover letter (zhang2025conformal, zhu2026swarm) are JKSU-CIS papers.
- **Plan commits:** `ccba99b` (2026-11-18) and `a9f31d2` (2026-11-20) exist, with messages consistent with Section 5.7. The RW evaluator was committed afterwards (fd68e0d), and the RW results came later still (af33ef5). PLAN_TIMESTAMPS.md is generated by `build_anonymous_package.py`.
- **`eval_tail1.py` and `analyze_review08.py`:** they reuse the cached contexts with no refit, and n_strata_inf uses the same $n_k<1/\alpha-1$ rule as Eq. (3). Holm is applied over the six tests as stated. The only weakness is the undisclosed restriction to 24 datasets for top-1% coverage (Issue 3).

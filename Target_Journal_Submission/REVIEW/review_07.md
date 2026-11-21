# Review 07: Reviewer #7 (scientific writing, presentation and journal compliance)

**Journal:** Journal of King Saud University – Computer and Information Sciences (JKSU-CIS, Springer Nature)
**Manuscript:** "Covering rare outcomes in imbalanced regression: stratified and relevance-weighted conformal prediction with density scores"
**Material inspected:** `manuscript/build/manuscript_filled.md`; `manuscript/Final_Manuscript.pdf` (38 pp.; pages 1–6, 10, 16–30 read visually); `manuscript/Final_Manuscript.docx` (headings, captions, references, core properties, line numbering, OMML math, all checked with python-docx); `title_page.docx`; `cover_letter.docx`; `Supplementary_Material.docx/.pdf` and `build/supplementary_filled.md`; `build/highlights_filled.md`; the figure PNGs in `figures/` used by the manuscript (F0, F2, F3, F6_shift, F9, F11, F12, F13, F14).
**Scope:** writing, logical structure, claims as worded, terminology, notation, figures, tables, references and compliance with the JKSU-CIS author guidelines. This review does not repeat the substantive issues already raised in `review_01`–`review_04`, for example C1-01/02/03 on framing and size claims, C1-36 on length and unused figures, C1-38 on placeholders, C1-39 on general reference rendering, R2-04 on the desk test of the old title, and R3-03 on verifiability. Where an earlier issue is still unresolved in this version, it is mentioned in one line only.

Page numbers (p.) refer to `Final_Manuscript.pdf`.

---

## 1. Desk-editor first impression

An editor who reads only the title, the abstract, the contribution list (p. 2) and Fig. 1 (p. 10) would probably **send the paper out for review, but with hesitation**. In its favour, the problem is clear and practically motivated, the 70.5% oracle figure is a good hook, the evaluation is large, and the authors are unusually candid about small effects. Five things would make the editor hesitate.

1. **The abstract reads as a statistics paper.** "An established Mondrian device", "OpenML-CTR23", "stratified normalised residual" and "oracle interval" go unexplained in the first 120 words, and the efficiency result is stated as a near-null ("stayed within a few per cent of a stratified normalised residual"). The editor will look for the computer-science contribution and will find mainly a score choice plus a new weighted guarantee.
2. **The contributions are overloaded and hedged.** Contribution 1 alone packs in four results: two Propositions, a Theorem and another Proposition. It concedes in passing that Proposition 2 is "the per-stratum form of known level-set results". Contributions 3 and 4 describe an evaluation and guidance, not contributions. Two clear claims would land better than four diffuse ones.
3. **Fig. 1 does not sell the idea.** It is a generic six-box flowchart for SDLC only. RW-DLC, the method the title gives equal weight, is absent. The figure does not show the key visual insight: per-stratum thresholds on a density can produce a set that is not an interval and that reaches into the tail. It also has a typesetting defect (issue 7).
4. **There are signs of a recycled submission.** "RW-DLC was added after review of an earlier version" (p. 16). The Supplementary Material still carries the previous title and the heading "Pre-registered analysis plan". Placeholders remain in the declarations, the cover letter and the title page. Any one of these suggests a manuscript moved from another journal without a final pass.
5. **The volume is very high for JKSU-CIS:** 38 pages, 11 tables, 9 figures and roughly 16,000 words, with proofs in the main text. This was raised earlier (C1-36, R2-06) and is not repeated here, but together with points 1–4 it is what would tip a borderline desk decision.

The following changes would most improve the desk outcome:
- rewrite the abstract as in issue 3;
- cut the contribution list to two items: (a) the size-optimal score for stratum-wise coverage; (b) relevance-weighted coverage with RW-DLC; with the evidence stated in one sentence;
- redraw Fig. 1 as a two-panel figure: (a) the stratified density level set for one input, with the thresholds shown; (b) the SDLC/RW-DLC pipeline;
- synchronise the supplement and remove the review-history sentence.

---

## 2. Summary of issues

| No. | Severity | Topic |
|---|---|---|
| R7-01 | MAJOR | Supplementary Material is out of sync with the manuscript: old title, missing Section S7 and six cited tables, "pre-registered" heading |
| R7-02 | MAJOR | Anonymity: review-history sentence, commit hashes and repository file names that can be searched |
| R7-03 | MAJOR | Abstract: undefined jargon and abbreviations, and an availability claim that conflicts with the Code availability statement |
| R7-04 | MAJOR | Logical structure: RQ7 out of order, duplicate "Experiment k"/"RQk" labelling, Section 4 title does not cover RW-DLC |
| R7-05 | MAJOR | Overstated or inaccurate wording in the Discussion, the Introduction and one caption (Fig. 9 caption contradicts its figure) |
| R7-06 | MODERATE | Notation: at least twelve symbol collisions and symbols used before they are defined |
| R7-07 | MODERATE | Fig. 1 quality: overlap, undefined "OOF", missing test set and RW-DLC |
| R7-08 | MODERATE | Figure quality: Figs. 3, 4, 6, 7 and 8 (overlaps, missing axis titles, colour semantics, clipped labels, scale mismatch with Table 9) |
| R7-09 | MODERATE | Method-name and terminology inconsistency (S-Res, DLS-M, DLS-N, SDLC-2p, -U/-H suffixes, "positive control", "stratum-wise"/"target-conditional") |
| R7-10 | MODERATE | Rendering defects in the reviewer PDF ("p ≤ < 0.001", "−0.0000", misplaced subscripts, equation numbers, no line numbers) |
| R7-11 | MODERATE | Reference list: incomplete entries, a/b ordering, editions, missing DOIs, a heavy share of very recent arXiv preprints |
| R7-12 | MODERATE | Table quality: Tables 3, 7, 8 and 9 |
| R7-13 | MINOR | Garbled sentence in Section 2.2 (Sadinle et al.) |
| R7-14 | MINOR | Statements and Declarations: Elsevier wording, placeholders still present |
| R7-15 | MINOR | Figure citation order, "Figure" vs "Fig.", forward reference to "Experiment 4" |
| R7-16 | MINOR | Theorem and Proposition numbering, Remark and Algorithm presentation |
| R7-17 | MINOR | Highlights and cover letter out of date or inconsistent |
| R7-18 | MINOR | Small wording and style points |

---

## 3. Issues

### R7-01 (MAJOR) The Supplementary Material does not match the manuscript

**Location:** `Supplementary_Material.docx/.pdf` (built 20 Nov, one day before the manuscript); the manuscript's citations of supplementary items.

**What is wrong:**
- **Wrong title.** The supplement's title is the previous one: "Covering the rare outcomes: stratified conformal prediction with size-optimal density scores for imbalanced regression". The DOCX core property "title" carries the same old title. In the PDF, the hyphen is lost ("sizeoptimal").
- **Missing items.** The manuscript cites *Supplementary Section S7* (p. 16, the RW-DLC analysis plan) and *Tables S13, S15, S16, S17, S18 and S19* (Sections 6.5, 6.6, 6.9). The supplement has Sections S1–S6 only, and Tables S1–S12 and S14 only. Six cited tables and one cited section do not exist, including the CTR23 results for RW-DLC (S19) and the grouped-split results (S16).
- **Terminology contradiction.** The supplement's Section S6 is headed "Pre-registered analysis plan of the confirmatory replication" and says it was "committed to the public repository". It refers to `PREREGISTRATION_confirmatory.md` and to `supplementary/v1_preregistered_analysis/`. The manuscript (Section 5.7) says explicitly that the plan is "pre-specified rather than pre-registered", and the Code availability statement says that the repository will be made public only upon acceptance.

**Proposed fix:**
- Rebuild the supplement from the current sources.
- Rename the S6 heading to "S6. Pre-specified analysis plan of the confirmatory replication (verbatim)".
- Replace "committed to the public repository" with "committed to the authors' version-controlled repository (commit ccba99b) before any confirmatory evaluation".
- Rename the archived folders and files (`v1_preregistered_analysis` → `v1_analysis`; `PREREGISTRATION_confirmatory.md` → `ANALYSIS_PLAN_confirmatory.md`), or cite them without names.
- Add Section S7 and Tables S13 and S15–S19.
- Finally, run a script that checks that every "Table S*n*" and "Section S*n*" cited in the manuscript exists in the supplement.

### R7-02 (MAJOR) Double-blind anonymity

**Locations:** Section 5.7 (p. 16); the supplement, S5 and S6; Code availability.

1. "*RW-DLC was added after review of an earlier version.*" This reveals the manuscript's review history. Reviewers who saw the earlier version elsewhere can identify it, and the sentence invites the "rejected elsewhere" reading. **Rewrite:** "RW-DLC was developed after the main benchmark had been run. Its analysis plan (…) was committed before RW-DLC was evaluated on any dataset."
2. Commit hashes (`ccba99b`, `a9f31d2`) and verbatim file names (`PREREGISTRATION_confirmatory.md`, `supplementary/v2_exact_insample_analysis/`) can be searched on GitHub or Software Heritage once any copy of the repository is public. Together with the supplement's claim that the plan is in "the public repository", they invite reviewers to look for the authors. **Fix:** keep the hashes, but provide the code through an anonymising mirror, for example anonymous.4open.science, and say so: "An anonymised copy of the repository, including the commit history with these hashes, is available to reviewers at [anonymous link]". Otherwise, move the hashes to the title page.
3. DOCX metadata were checked and are clean: the author field holds the anonymisation note, and no `lastModifiedBy` is set. No acknowledgements, self-citations or funding identifiers appear in the manuscript. These need no change.

### R7-03 (MAJOR) The abstract does not meet the JKSU-CIS requirement of no undefined abbreviations, and it contradicts the availability statement

**Location:** Abstract (p. 1). Length: 239 words, which is within 150–250. It contains no citations, which is correct.

- **Undefined or jargon terms:**
  - "an established Mondrian device": a term known only to specialists;
  - "OpenML-CTR23": an abbreviation that is never expanded;
  - "stratified normalised residual": a method family named without saying what it is;
  - "oracle interval": not explained.
- **Inaccurate availability claim.** "Code and raw results are released" conflicts with the Code availability statement ("will be deposited in a public repository upon acceptance"), and also with Section 5.8 ("produced by the released code").
- **Imprecise phrase.** "consistent with exact validity" is jargon; the plain meaning is "attained the nominal level".

**Proposed abstract (238 words):**

> Conformal prediction intervals for regression are usually calibrated to hold on average over all outcomes, so they can systematically miss the rare, extreme outcomes that matter most in imbalanced regression. Even the ideal interval with exact coverage at every input covers only 70.5% of the top decile of the target in a Gaussian model with half of the variance explained. We therefore study two guarantees for rare outcomes. For coverage within every stratum (range) of the target, calibrating separately within each stratum is an established technique; we show that conditional-density level sets with stratum-specific thresholds are the smallest valid sets and evaluate the resulting method, stratified density-level conformal prediction (SDLC). For coverage weighted by a relevance function, as used in imbalanced regression, we propose relevance-weighted density-level conformal prediction (RW-DLC), which needs no strata and has a finite-sample guarantee. On 31 datasets of the OpenML-CTR23 benchmark suite, standard methods covered only 63.0%–78.3% of their worst-covered stratum at a nominal 90%, whereas stratified methods attained the nominal level. SDLC gave smaller sets than stratified methods based on absolute residuals or quantiles, which an analysis plan fixed in advance confirmed on 17 held-out datasets, but its sets were within a few per cent of those of a stratified normalised residual. On the held-out datasets, RW-DLC met its relevance-weighted target and covered 87.2% of the top 1% of outcomes, against 68.8% for SDLC, at the cost of lower coverage of typical outcomes.

### R7-04 (MAJOR) Logical structure of Sections 4–6

**Problems:**
1. **RQ7 is out of order.** Section 5 announces "six research questions … a seventh (RQ7, Section 6.6)". Section 6 then runs RQ1, RQ2, RQ3, an unnumbered synthetic study (6.4), an unnumbered confirmatory replication (6.5), RQ7 (6.6), RQ4 (6.7), RQ5 (6.8) and RQ6 (6.9). Readers lose track of where each question is answered. RW-DLC, the second method in the title, appears only as an afterthought RQ.
2. **Experiments and RQs are labelled twice.** "Experiment 1–6" (Section 5, and also Sections 4.1, 5.3 and 5.4) duplicates "RQ1–RQ6". The Results section uses only RQ labels, so "Experiment 4" (Section 4.1, p. 8) and "Experiment 5/6" (Sections 5.3–5.4) are never resolved.
3. **The Section 4 title is too narrow.** Section 4 is titled "Proposed method: stratified density-level conformal prediction". It contains (a) Theorem 1 and Corollary 1, which the authors say are not new; (b) SDLC; and (c) a second, independent method, RW-DLC (4.7), with its own theorem and proposition.

**Proposed restructuring (the content is unchanged):**
- Section 4 "Stratum-wise coverage: calibration and the size-optimal score": 4.1–4.6 as now.
- Section 5 "Relevance-weighted coverage: RW-DLC": the current 4.7.
- Renumber the RQs in the order of the Results: RQ1 tail coverage; RQ2 price; RQ3 score, with the synthetic study and the confirmatory replication as 6.3.1–6.3.3 so that headings stay within 3 levels; RQ4 relevance-weighted coverage; RQ5 shift; RQ6 decisions; RQ7 sensitivity.
- Delete every "Experiment k" label. Replace "Experiment 4" in Section 4.1 with "the target-shift experiment (Section 6.7)".
- In Section 5, replace "The study answers six research questions (RQs), each tied to one experiment; a seventh (RQ7, Section 6.6) evaluates RW-DLC." with "The study answers seven research questions (RQ1–RQ7), reported in this order in Section 6."

### R7-05 (MAJOR) Overstated or inaccurate wording (claims as written, not the underlying statistics)

| Location | Current text | Problem | Proposed rewrite |
|---|---|---|---|
| Section 1, contribution 2 (p. 2) | "both have exact implementations whose cost is linear in the number of test points" | Section 4.4 tabulates ĝ on a grid with linear interpolation, and Section 5.7 evaluates RW-DLC "on a grid of 4,000 target values". Only membership of the test target is decided exactly. | "both decide coverage exactly at the observed target and compute set geometry on a fine grid, at a cost linear in the number of test points" |
| Section 7.1 (p. 30) | "Three findings are robust across datasets, miscoverage levels, stratifications and learners." | Section 6.3 reports that the third finding is not significant on the 15 skewed or 9 small datasets. Section 6.9 reports that it reverses against BCCP under grouped splits (video_transcoding). | "The first two findings held in every analysis; the third held on most datasets but not on small or strongly skewed targets or under grouped splits." |
| Section 7.1 | "the guarantee resisted moderate target shift" | Table 10: under γ = 1 every stratified method fell below 0.90 (0.861–0.881). Only the positive control preserved the guarantee. | "the guarantee was preserved exactly when the shift re-weighted whole strata, and stratified methods lost less coverage than marginal ones under continuous tilts" |
| Section 7.1 | "as Proposition 2 predicts" | Proposition 2 is an oracle statement and predicts nothing about estimated scores or about BCCP. | "consistent with Proposition 2" |
| Section 4.2, last paragraph of "Coverage is reallocated" (p. 9) | "Users who need comparable coverage across noise levels should prefer S-NCP." | Fig. 5 shows S-NCP also uneven: 0.835 in the lowest σ̂ decile against 0.900 for SDLC. | "S-NCP spreads coverage more evenly over the noisiest inputs, and is preferable when coverage of high-noise inputs matters." |
| Heading 6.3 (p. 19) | "The density score gives the smallest stratum-valid sets (RQ3)" | The text reports that equivalence with S-NCP and S-HPD could not be rejected and that the gain is a few per cent. | "6.3 Density, residual and quantile scores under stratified calibration (RQ3)" |
| Fig. 9 caption (p. 30) | "CQR misses most of the capped top values; the stratified methods cover them" | In the figure, CQR misses only one of the roughly eight values at the 500k cap, and CQR and SDLC both miss 8 of 70 points. | "CQR's sets around the capped top values are wide and miss one of them; SDLC adds disjoint pieces in the upper stratum, where its threshold is lower. CQR and SDLC both miss 8 of the 70 targets, BCCP and S-NCP 6." |
| Fig. 6 caption (p. 26) | "RW-DLC … approaches the nominal level at a size comparable to the stratified methods" | The geometric-mean size is 8% larger than SDLC's (Section 6.6), and the arithmetic mean in Table 9 is 14% larger. | "… at sets about 8% larger than SDLC's (geometric mean)" |
| Section 5.8 (p. 16) | "Every number … is produced by the released code"; "every reference was checked against its publisher or index record" | The code is not released (R7-03). One reference is incomplete (Zhu et al. 2026, "38:" with no article number; R7-11). | "… is produced by the code provided as supplementary material …"; then fix the reference |
| Section 6.9 (p. 29) | "(Holm p < 0.001 or smaller)" | The phrase is tautological. | "(Holm p < 0.001)" |

### R7-06 (MODERATE) Notation: symbol collisions and symbols used before they are defined

The paper uses about 60 symbols, and several carry two or three meanings, sometimes inside a single section.

| Symbol | Meanings (location) | Proposed fix |
|---|---|---|
| φ | standard normal density (proof of Prop. 1, p. 6); relevance function (Section 4.7 onward) | Write the normal density as φ_N or as Φ′; keep φ for relevance |
| τ | signal variance τ² (Prop. 1); density floor τ = 0.01 max p̂_Y (Section 4.7, Table 9) | Rename the floor to p_min |
| s | score function s(x, y); standard deviation s = σ√R² in Eq. (2); robust scale ŝ in Eq. (9) | Use ω in Eq. (2) and ŝ_IQR in Eq. (9) |
| r, r_k | rank r_k (Eq. 3); training range r (Section 4.4); cost ratio r (Sections 5.5, 6.8); radius r_k (Remark, Appendix A) | Use ρ_k for the radius, Δ_y for the range and c for the cost ratio (already written c(FN)/c(FP) in Fig. 8) |
| R | number of monotone runs (Section 4.5); rank (proof of Thm 1); R² | Use M for the runs and ρ for the rank |
| ε, ϵ, ε_N | model noise; mixture weight ϵ = 0.01 (Eq. 9); sup-norm error ε_N (Prop. 3) | Use η or λ for the mixture weight |
| q | conformal quantile q̂_k and q(y); FDR level q (Section 5.4, Table 11) | Write the FDR level as q_FDR |
| Q | shifted test law (Cor. 1, Thm 2); quantile operator Q_{1−α} (proof of Thm 2) | Use Quant_{1−α}(·) |
| p_k, p_j | stratum probability; conformal weights p_j (proof of Thm 2) | Write π̃_j for the weights |
| w | label-shift density ratio (Cor. 1); weight function w(z) (proof of Thm 2); tilt weights w(y) = exp(γ z_y) (Section 5.5) | Acceptable as "a density ratio" throughout, but define it once and use a different letter (ω_γ) for the tilts |
| z | normal quantile Φ⁻¹(1−α/2) (Prop. 1); normal score z_y (Section 5.5); data points z_i (proof of Thm 2) | Use z_{α} for the normal quantile and ζ_y for the normal score |
| E, E_k | event E_k (proof of Thm 1); multiset E (proof of Thm 2) | Write 𝓔 for the multiset |
| t_k, t_2, t_ν | density thresholds; Student-t distributions | Write the Student densities as St_2 or t_{(2)} |
| D, 𝒟 | domain D; data sets 𝒟_tr, 𝒟_cal | Rename the domain to 𝒴_D or [y_lo, y_hi] |
| k | stratum index; summation index in Σ_k φ(y_k) (proof of Thm 2) | Use l for the summation |

**Symbols used before or without a definition:**
- G in O(KR log G) (Section 4.5; only G_g is defined);
- d_TV (Cor. 1; never defined);
- N (used in Section 4.3 before Prop. 3 defines it as the training-set size);
- Φ (Prop. 1);
- ŷ in "Mondrian-ŷ" and in Table 1;
- the notation "|C(x)|" for Lebesgue measure appears in Section 4.2 but is used for counts elsewhere ("pieces").

**Proposed fix:** add a notation table (Table A1 in the appendix, or one paragraph at the start of Section 3) and apply the renamings above.

### R7-07 (MODERATE) Fig. 1 (F0_method_schematic.png)

1. **Overlap.** In the green box, the subscript *k* under the big ∪ collides with the "| Y" of the line below. The ∪ itself is set at text size, so the formula reads "C(x) = ∪{…}" with the index touching the next line. The defect is clearly visible at the printed size (p. 10).
2. **Undefined abbreviation.** "(OOF)" is never defined. Note also that μ̂ is not an out-of-fold model; only σ̂ is fitted to OOF residuals.
3. **Notation mismatch.** "C(x)" lacks the hat; the text writes Ĉ(x). "≥ − q̂_k" is spaced as a binary minus.
4. **Missing test set.** The test set (25%) is missing, so the 50/25 percentages do not sum to anything meaningful.
5. **Incomplete scope.** There is no RW-DLC, although the title, the abstract and the contributions present two methods. The figure is the only overview figure.
6. **Wasted space and no visual of the result.** About 15% of the canvas is white margin, and the figure carries no visual of an actual prediction set.

**Proposed fix:** a two-panel figure:
- (a) for one test input x, the curve f̂(y | x), the stratum boundaries, the per-stratum horizontal thresholds −q̂_k and the resulting union of pieces;
- (b) the pipeline, with a third branch "relevance weights φ(y_i) → weighted quantile q(y) → RW-DLC".

**Caption rewrite:** "**Fig. 1.** (a) Prediction set of SDLC for one input: the estimated density f̂(y | x) is cut at a different height in each target stratum, which can give a set of several pieces. (b) Workflow: the density model and the strata are fitted on the proper training set; calibration scores are grouped by the stratum of the observed target (SDLC) or weighted by relevance (RW-DLC)."

### R7-08 (MODERATE) Quality of the other figures

- **Fig. 3 (F2_coverage_size_tradeoff.png):**
  - Labels overlap. "S-HPD" is overprinted by the "S-NCP-hull" leader line and reads "S-·PD". "SDLC-N" sits on its marker. "S-CQR" is cut by the vertical target line.
  - The caption explains grey, green and blue, but not the **orange** markers (SDLC-hull, S-NCP-hull, SDLC-floor).
  - The caption reads "coverage against set size", but the figure plots size (y) against coverage (x).
  - **Fix:** use adjustText or manual offsets, add the orange class to the caption, and write "Set size against worst-stratum coverage".
- **Colour semantics across figures.** Orange means CQR in Figs. 2 and 8 but hull and floor variants in Fig. 3, and the second ablation step in Fig. 4. Green means S-NCP in Figs. 2, 5, 7 and 8 but "all stratified methods" in Fig. 3 and "adds σ̂" in Fig. 4. Grey means marginal methods in Fig. 3 but SCP and DLS in Figs. 5 and 7, and BCCP in Fig. 9. **Fix:** assign one fixed colour per method across all figures, and use shape rather than colour for the method family.
- **Fig. 4 (F11):**
  - There is no x-axis title.
  - The caption says "bars", but the means are drawn as horizontal lines.
  - Two outliers (0.33, 0.49) are not identified.
  - **Fix:** write "geometric means (horizontal lines)" and label the outlying datasets.
- **Fig. 6 (F14_rw_top1_vs_size.png):**
  - The "RW-DLC-U" label is clipped by the right frame.
  - NCP and the ablations RW-NCP and RW-DLS, all of which appear in Table 9, are missing.
  - The x-axis (geometric mean, 0.99–1.31) cannot be reconciled with Table 9's "Size / sd(y)" column (arithmetic mean, 1.58–2.54), because the two use different summaries without saying so prominently.
  - DLS-M and CQR are almost the same dark grey.
  - **Fix:** extend the x-limits, add the missing methods, use the same size summary as Table 9 (or add a geometric-mean column to Table 9), and use distinct colours.
- **Fig. 7 (F6_shift.png):**
  - Neither panel has a y-axis title.
  - The x categories say "Whole-strata re-weighting", while the text and Table 10 say "positive control".
  - Lines join categorical conditions, which suggests a continuum.
  - The left panel shows γ = 1 marginal coverage, which is not reported in Table 10.
  - **Fix:** add a "Coverage" y-axis title, rename the category to "Positive control (whole strata)", use markers without lines or a dot plot, and add the γ = 1 marginal column to Table 10.
- **Fig. 8 (F13_alert_costs.png):**
  - The panels use different log-scale tick formats (10⁰ vs 6×10⁻¹).
  - Dataset names are in lower case ("kings county") while the text writes "King County".
  - The x-range runs to 50, although the text discusses only r ∈ {1, 10, 20}.
  - The legend covers the upper-left of the third panel.
  - **Fix:** use a shared tick formatter, title-case the dataset names, place the legend below the panels, and mark r = 10 and r = 20.
- **Fig. 9 (F9):** the y-axis label is a raw variable name ("medianHouseValue (thousands)"). Change it to "Median house value (thousand USD)". On the caption, see R7-05.
- **Figs. 2 and 5 (F3, F12):** these are legible and acceptable. Add "(test points)" consistently, and in Fig. 2 state that the shaded bands are 95% confidence intervals over datasets.

### R7-09 (MODERATE) Method names and terminology

**Method names that appear without a definition, or under two names:**
- "**O-S-Res**" (Table 7) is never defined. "S-Res" appears nowhere else; it presumably means the oracle BCCP (stratified absolute residual). Rename it to "O-BCCP".
- "**DLS-M**" (Section 5.7, Table 9, Fig. 6) vs "DLS" elsewhere: define it or merge the two names.
- "**DLS-N**" (Table 4) is never defined.
- "**SDLC-2p**" and "**SDLC-hist**" (Table 6) vs "two-piece" and "histogram density" in the text: define them in Section 4.3 ("SDLC-2p", "SDLC-hist").
- "**RW-DLC-U / -H**", "**RW-NCP-U**" and "**RW-DLS-U**" (Table 9, Fig. 6) vs "RW-DLC with φ_U / φ_H" in the text: define the suffixes in Section 4.7.
- "**Point**" (Table 11, Fig. 8) vs "naive rule"/"point-prediction rule" in the text.

**Terms used for the same concept:**
- "**stratum-wise**" (29 uses), "**target-conditional**" (4, including the headings of Sections 3.1 and 3.2), and "**label-conditional**"/"**bin-conditional**" (for the same property in prior work). Define it once ("stratum-wise (target-conditional) coverage") and then use "stratum-wise" only. Rename 3.1 to "Stratum-wise coverage" and 3.2 to "Covariate-conditional validity does not imply stratum-wise validity".
- "**pre-specified**" (15 uses) vs "fixed before evaluation" (3), "fixed in advance" (2), "committed" and, in the supplement, "pre-registered". Use "pre-specified" throughout and define it once in Section 5.7, which already does so well.
- "**upper tail**" (Table 3 column header), "upper stratum", "upper calibration stratum" and "top decile": all denote B_K. Use "upper stratum (B_K)" and rename the Table 3 columns "Lowest stratum" and "Highest stratum".
- "**positive control**" (text, Table 10) vs "Whole-strata re-weighting" (Fig. 7).
- "**size**", "normalised size" and "Size / sd(y)": choose "normalised size".
- "**per cent**" (5 uses) vs "%": use "%" with numbers and write "a few percent" (Springer uses US spelling of "percent" in house style; British spelling elsewhere is acceptable but should be consistent).

### R7-10 (MODERATE) Rendering defects in the reviewer PDF

The PDF is printed from HTML by Chromium. Reviewers will read this file.

- **"p ≤ < 0.001".** A template placeholder renders as "𝑝 ≤ < 0.001" four times on p. 17 and p. 19 (Sections 6.1 and 6.3). Replace it with "p < 0.001".
- **"median difference −0.0000"** (Table 8, p. 24): write "0.000".
- **ASCII hyphens used as minus signs** ("-0.41", "-0.080", "-0.0015"): use "−".
- **Inline math.** Subscripts are mis-set (the subscript of "Cov_k" is detached from Cov, and "p_k" drops below the line on p. 6). A comma is orphaned at the start of a line in Proposition 1. Line spacing is very wide around "locally weighted conformal prediction" on p. 10. Math is set in a sans-serif font next to serif text.
- **Equation numbers** sit right after the equation rather than right-aligned (Eqs. 1, 2, 8 and 9).
- **Line numbers.** The PDF has none; the DOCX has them (`w:lnNumType`). Reviewers need line numbers to cite locations.
- **Fix:** produce the reviewer PDF from the Springer Nature LaTeX template (`sn-jnl`, `sn-basic` author–year option) or export it from the DOCX, with line numbering switched on.

### R7-11 (MODERATE) Reference list (78 entries, Springer basic author–year)

The in-text author–year format ("Randahl et al. (2026)", "(Vovk et al. 2005; Lei et al. 2018)") follows the guideline. The defects below are specific and do not repeat C1-39.

1. **Incomplete entry.** Zhu et al. (2026), JKSU-CIS "38:" has no article number. Complete it as "38:<article no.>".
2. **a/b suffixes in the wrong order.** Barber et al. "2021b" (*Limits*) is listed before "2021a" (*Jackknife+*). Springer assigns the suffixes in list order, so swap the labels.
3. **Two editions of the same book.** Vovk, Gammerman, Shafer 2005 and 2022 have identical titles. Add "2nd edn" to the 2022 entry, plus the DOIs (10.1007/b106715; 10.1007/978-3-031-06649-8). Cite the edition actually used for each claim.
4. **Year and locator mismatch.** Branco et al. "2017a" (*ACM Comput Surv* 49) is cited with the source key `branco2016survey`, and its page field "1–50" should be the article number: "49(2):31".
5. **Missing DOIs** for Springer and IEEE proceedings and books:
   - Papadopoulos et al. 2002;
   - Torgo & Ribeiro 2007 and 2009;
   - Torgo et al. 2013;
   - Ren et al. 2022 (CVPR);
   - Serfling 1980;
   - Boström & Johansson 2020 and other PMLR entries (add the URL);
   - Fischer et al. 2023, which has no URL or venue locator: add the OpenReview or arXiv identifier, since this is the benchmark itself;
   - Santos et al. 2026 (TMLR, no URL);
   - Guha et al. 2024 (ICLR, no URL).
6. **Missing pages:**
   - Ke et al. 2017: 3146–3154;
   - Romano et al. 2019: 3543–3553;
   - Tibshirani et al. 2019: 2530–2540.
7. **Inconsistent publishers.** NeurIPS entries are published by "Curran Associates, Inc." in 2017–2021 but by "Neural Information Processing Systems Foundation, Inc. (NeurIPS)" in 2023–2024. Use one form.
8. **Formatting:**
   - delete the "®" in "Foundations and Trends® in Machine Learning";
   - "Ribeiro R" (2007, 2009) vs "Ribeiro RP" (2013, 2017, 2020) is the same author: unify the initials.
9. **arXiv preprints.** Ten entries (13%) are preprints, five of them from 2026. Three carry core arguments:
   - Bhattacharyya et al. 2026 (2606.28598), the discrete counterpart of Prop. 4 and of RW-DLC;
   - Boruah 2026a and 2026b, used in Table 1 and to justify the null-reference correction. Boruah 2026b (2611.14521) was posted in November 2026, weeks before submission.

   Springer style is "arXiv:2606.28598"; the DOI form is acceptable but should be used consistently. For each preprint, check whether a peer-reviewed version exists (for example Chzhen et al. 2021; Angelopoulos et al. 2024, now a book), and avoid resting a methodological choice (the null reference) on a single-author preprint. Cite Demšar or a published worst-group bias result instead or as well.
10. **Nested parentheses** in the citation of contribution 1 (p. 2): "(Proposition 2, the per-stratum form of known level-set results (Lei et al. 2013; Sadinle et al. 2019))". **Rewrite:** "(Proposition 2; the per-stratum form of known level-set results, see Lei et al. 2013; Sadinle et al. 2019)".
11. **Peripheral journal citations.** Zhang et al. (2025, JKSU-CIS, conformal deep forests for classification) is cited for a sentence that plays no role in the argument ("Conformal uncertainty measures have also been built into classifiers such as deep forests"). Reviewers may read it as a citation to please the journal. Either connect it to the argument or drop it.

### R7-12 (MODERATE) Table quality

- **Table 3:**
  - "Empty %" values (0.02–0.74) look like proportions. State "(% of test points)" in the header.
  - "Upper tail" and "Lower tail" mean the extreme calibration strata (R7-09).
  - The table has 11 columns; consider moving "Pieces" and "Empty %" to Table 6 or to the supplement.
- **Table 7:**
  - Cells combine "coverage / size", which is hard to scan. Split the table into two blocks (coverage; relative size).
  - Designs A–E are never mapped to their names in the caption. Add "A: skewed; B: covariate-dependent skewness; C: bimodal; D: heavy-tailed; E: zero-inflated".
  - Define O-S-Res (R7-09).
  - Explain why design E has empty oracle rows; the caption says so only briefly.
- **Table 8:**
  - Method names break at hyphens across lines ("SDLC vs S-" / "NCP"; "Mondrian-" / "ŷ"). Use non-breaking hyphens (U+2011) or widen the column.
  - The "Holm p" column also holds a binomial p and TOST p-values. Rename it "p (test)" and give the test in a separate column.
  - "−0.0000": see R7-10.
- **Table 9:** the size column is an arithmetic mean while every other size in the paper (Tables 3–6, Fig. 6) is a geometric mean. Report geometric means, or say in the header "Size / sd(y) (arithmetic mean)".
- **Table 2:** write "t₃", "t₅" and "t₃₀" with subscripts, as in the text.
- **DOCX:** table captions use the style "Body Text" rather than a Caption style, so Word cannot build a list of tables. This is minor, but the Springer production system benefits from Caption styles.

### R7-13 (MINOR) Garbled sentence in Section 2.2 (p. 3)

**Current:** "Closest to our optimality result is Sadinle et al. (2019), who showed that the least ambiguous classifier under class-specific coverage thresholds p(y | x) with class-specific cut-offs (see also …)". The verb of the subordinate clause is missing.

**Rewrite:** "Closest to our optimality result is Sadinle et al. (2019), who showed that the least ambiguous set-valued classifier under class-specific coverage constraints thresholds p(y | x) at class-specific cut-offs (see also Lei 2014; Chzhen et al. 2021)."

### R7-14 (MINOR) Statements and Declarations

- The competing-interests sentence is the Elsevier template ("no known competing financial interests or personal relationships that could have appeared to influence…"). Springer's standard wording is: "The authors have no relevant financial or non-financial interests to disclose."
- The bracketed placeholders are still present in the manuscript, the title page and the cover letter, as already flagged in C1-38: "[To be confirmed…]", "[Placeholder: funding…]" and "[repository URL]". They must be resolved before upload.
- The title page duplicates the declarations with different wording ("Data and code availability" vs separate "Data availability" and "Code availability" in the manuscript). Keep one version.
- The placement after the References and the presence of all required items (competing interests, funding, author contributions, data availability, ethics, LLM use) are compliant.

### R7-15 (MINOR) Figure citation order and cross-references

- Fig. 9 is cited in the first paragraph of Section 6 (p. 16), before Figs. 2–8. Springer requires figures to be cited in consecutive order. Either drop "and Fig. 9 shows sets for one dataset" there, or move the California example to Fig. 2 and place it at the start of Section 6. This would also help the desk impression, since it is the most intuitive figure.
- Fig. 9 is not cited in Section 6.10, where it is placed.
- "Figure 1 summarises the workflow" (p. 10): in-text references should read "Fig. 1".
- "Experiment 4" is used in Section 4.1 before it is defined (R7-04).
- Section 6.3 says "SDLC-hist … far less efficient (1.745)" next to Table 6's ratio 0.501. One is an absolute size and the other a ratio. Write "(normalised size 1.745; ratio 0.501)".

### R7-16 (MINOR) Numbering of results and presentation

- Theorems, propositions and the corollary are numbered independently: Proposition 1 (Section 3.2) comes before Theorem 1 (Section 4.1), and Theorem 2 comes between Propositions 3 and 4. This is acceptable, but a single counter (Theorem 1, Proposition 2, …) or section-based numbering (Proposition 4.1) would make cross-references easier.
- Contribution 1 lists results out of numerical order: Prop. 1, 2, 3, Thm 2, Prop. 4.
- The unnumbered **Remark** in Appendix A ("within-stratum coverage profile") is never referred to from the main text, although it explains a result in Section 6.7. Number it ("Remark A.1") and cite it in Section 6.7 and Section 7.3.
- **Algorithm 1** is typeset as a block quote without a frame. Use an algorithm float (algorithm2e or algorithmic) with numbered lines.
- Proofs: Proposition 1's proof is in the main text, while all other proofs are in Appendix A. Move it to the appendix for consistency.

### R7-17 (MINOR) Highlights and cover letter

- `highlights_filled.md` predates RW-DLC: it does not mention it. It says "Calibrating within target strata guarantees coverage of rare, extreme outcomes", which is overstated, since the top 1% is covered at 0.69–0.74. It also says "SDLC gave the smallest stratum-valid sets … confirmed on 17", which ignores the near-equivalence with S-NCP. JKSU-CIS does not require highlights; if they are uploaded, rewrite them. Suggested replacements: "Stratified calibration restores coverage within each target stratum, not of the most extreme outcomes"; "Relevance-weighted conformal prediction (RW-DLC) guarantees coverage averaged over the target range".
- **Cover letter:**
  - It uses "(Randahl et al., 2026)", with a comma, unlike the manuscript.
  - "the journal regularly publishes … a review of class overlap" gives no citation.
  - "To our knowledge the journal has not yet published work on conformal prediction intervals for regression" is a risky claim that an editor can check in seconds. Rephrase it as "The paper extends the journal's recent work on conformal classification (Zhang et al. 2025) to regression."

### R7-18 (MINOR) Small wording and style points

- Section 1, last paragraph of the Introduction: "Section 2 reviews related work (Table 1)" can be shortened by cutting the roadmap to one sentence. The paper is long.
- Section 3.1: "We call (1) the stratum-wise (target-conditional) coverage" is the correct place to define the term (R7-09).
- Section 4.4: "(Supplementary Section S3, Table S4)" is fine, but other cross-references alternate between "Supplementary Table" and "Table S" without "Supplementary". Use "Supplementary Table Sn" everywhere.
- Section 6.6: "(largest Holm-adjusted p < 0.001)" → "(all Holm-adjusted p < 0.001)".
- Section 7.2, item 4: "1.527 pieces (BCCP 1.465)" vs Table 3 "1.53/1.47". Use the same precision.
- Section 4.6 title "Two practical variants": SDLC-hull and SDLC-floor are also used in the Results. Name them in the heading: "4.6 Interval (hull) and floor variants".
- Keywords: there are six, which is compliant. "Extreme values" suggests extreme-value theory; consider "Rare outcomes" instead.
- Heading depth is at most 2 levels, decimal numbering is used, and figure captions begin with "Fig.". All compliant.

---

## 4. Compliance checklist (JKSU-CIS / Springer Nature)

| Item | Status |
|---|---|
| Abstract 150–250 words, no citations | 239 words, no citations — **compliant**; undefined abbreviations and jargon (R7-03) |
| 4–6 keywords | 6 — compliant |
| Decimal headings ≤ 3 levels | 2 levels — compliant |
| Author–year citations | compliant (nested parentheses, R7-11.10) |
| Statements and Declarations after the References | present and complete in structure; Elsevier wording and placeholders remain (R7-14) |
| LLM use documented in Methods | Section 5.8 — compliant; the claim of "released code" needs correcting (R7-05) |
| Double-blind anonymity | metadata clean; review-history sentence and repository traces (R7-02) |
| Figure captions start with "Fig." | compliant; in-text "Figure 1" (R7-15) |
| Figures cited in order | **not compliant** (Fig. 9 cited first, R7-15) |
| Tables numbered with captions above | compliant; Caption style not used in the DOCX (R7-12) |
| Supplementary material consistent | **not compliant** (R7-01) |
| Line numbers in the reviewer PDF | missing (R7-10) |
| Reference completeness and DOIs | incomplete entries and missing DOIs (R7-11) |

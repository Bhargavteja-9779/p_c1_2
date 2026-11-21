# Review 9: Associate Editor desk screening (JKSU-CIS, Springer Nature, double-blind)

**Reviewer role:** Associate Editor, desk-reject screening.
**Material inspected:** `manuscript/build/manuscript_filled.md` (rendered), `manuscript/Final_Manuscript.docx` (python-docx text, `docProps/core.xml`, `docProps/custom.xml`, `word/document.xml`), `manuscript/Final_Manuscript.pdf`, `manuscript/build/{title_page,cover_letter,supplementary}_filled.md`, `manuscript/Supplementary_Material.{docx,pdf}`, Figs. 1 and 3 (`figures/F0_method_schematic.png`, `figures/F2_coverage_size_tradeoff.png`), `journal_selection/selected_journal.md` and `journal_comparison.md`, `code/scripts/build_supplement.py`, git metadata of the project repository, and reviews/responses 01–08.
**Already fixed and not repeated:** Kandinsky/Yi et al. credit (R8-2), RW plan timing disclosure (R8-5), "we prove" wording (R8-6), anonymised hashes in the text (R7-02), figure order (R7), keyword choice (R7). Two earlier points come back below because their fixes are incomplete: length (C1-36/R2-06) and the top-1% numbers (R8-8). The open item R8-4 also comes back.

---

## Summary

The paper studies conformal prediction sets that cover *rare* regression outcomes. It makes three points. (i) Marginal and covariate-adaptive conformal methods under-cover the target tails. This holds even for the oracle, and on 31 OpenML-CTR23 datasets their worst-stratum coverage was 63.0–78.3% at a nominal 90%. (ii) Calibrating within target strata (Mondrian/BCCP, credited as prior art) restores stratum-wise coverage, and conditional-density level sets with per-stratum thresholds (SDLC) are the size-optimal score for that guarantee. (iii) A relevance-weighted guarantee (RW-DLC) needs no strata. The evidence is large and honest: 31 + 17 datasets, two pre-specified plans, ablations, shift, decision and sensitivity studies.

The work is rigorous, and its self-criticism is unusually candid. As a desk editor, my difficulty is not with the science. It is that the paper does not *sell a clear computer-science contribution in its first page*, and it is far longer than a JKSU-CIS article. By its own account, the headline method (SDLC) beats the information-matched baseline (S-NCP) by about 2–4% in size and covers the extreme 1% *worse*. The second method (RW-DLC) loses its top-1% advantage to SDLC with dedicated 1% strata. The abstract ends on that last point. An editor skimming it will read "two methods, neither clearly better than a simple stratified baseline" and may reject for insufficient novelty or significance. The publishable contribution is real, but it is a different one from the paper's framing: a diagnosis, a cost analysis and a decision guide for tail-valid uncertainty quantification, with optimal scores as the theoretical backbone. Some compliance defects must also be fixed before submission: a missing supplementary table, a stale PDF, an unreported pre-specified analysis arm, and a code package that is promised but does not yet exist and would leak identity.

## Desk decision and probability

**Decision if submitted as is: send out for review, but marginal.**
**Estimated desk-reject probability: 35%** (range 30–40%).

Reasons that push towards desk rejection, in order of weight:
1. **Significance as framed.** The two named methods show, respectively, a small gain over a simple stratified baseline and no advantage over a dedicated-strata variant. The abstract states both, and it ends on the second (Issue 1).
2. **Length and density.** The main text (Sections 1–8) runs to about 13,400 words without table cells and display maths, about 16,200 with table cells, plus a 1,500-word proofs appendix. It has 11 tables, 9 figures, 8 formal results and about 36 method acronyms. The last built PDF has 39 pages, and the current version is longer (Issue 2).
3. **"Statistics paper" impression.** Seven formal results sit in Sections 3–4, and the results lean on Wilcoxon/Holm/TOST machinery (19 mentions of "Holm"). The abstract has no application or system hook (Issue 3).
4. **Visible readiness defects.** A cited supplementary table is missing, the submission PDF is stale, a pre-specified analysis arm is unreported, and title-page and cover-letter placeholders remain (Issues 4–7). Any one of these can trigger a technical return without review.

Reasons against desk rejection: the scope fits well (imbalanced learning and uncertainty quantification, with JKSU-CIS precedents cited), the empirical design is unusually strong, the reproducibility is good, and the prior-art credit is honest.

**The changes that would most reduce the probability** (estimated 15–20% after all five):
1. Reframe the title, abstract and contribution list around the diagnosis, the price of tail coverage and the decision guide, with the optimal scores as the theoretical support. Do not end the abstract on a negative comparison (Issue 1).
2. Cut the main text to about 9–10k words. Move Proposition 3, Corollary 1(ii)–(iii), the synthetic study, the shift table, the tail-alert table and most of Section 6.7 to the supplement (Issue 2).
3. Fix the readiness defects: Table S13, rebuild the PDF, report or declare the CTR23 RW arm, and fill the placeholders (Issues 4–7).
4. Build and check the anonymised code package before submission (Issue 5).
5. Make every summary number agree across the abstract, conclusion and cover letter (Issue 8).

---

## Numbered issues

### Issue 1 (MAJOR): The framing undersells the real contribution and ends on a negative

**Location:** Title; abstract (last two sentences); Introduction, contributions 1–2 (`01_intro.md`); Conclusion, second paragraph.

**Evidence:**
- The abstract's final sentence is: "On held-out data, RW-DLC met its relevance-weighted target and covered 88.4% of the top 1% of outcomes, against 76.0% for SDLC with five strata; SDLC with dedicated 1% tail strata covered 90.6% with similar set sizes." The reader's last impression is that the second proposed method is matched by a variant of the first.
- The previous sentence says SDLC's sets "were within a few percent of those of a stratified normalised residual, which covered the most extreme outcomes better."
- The contribution list names two *methods* (SDLC, RW-DLC). Their empirical edge is small (C-H3: SDLC/S-NCP ratio 0.977, 95% CI 0.940–1.028) or absent (RW-DLC vs dedicated strata: ratio 0.952, smaller on 9/17).
- The clearly positive, large, robust findings are not presented as contributions:
  - worst-stratum shortfall of 11–27 points for every standard method, which persists for the oracle (Prop. 1, Table 2);
  - stratified calibration costs 1.17–1.27× in size, yet beats lowering α to 0.05 on 23–28/31 datasets (Table 5);
  - exactness under stratum re-weighting (Table 10);
  - a cost-based comparison of alert rules (Table 11).
- The title ("…stratified and relevance-weighted conformal prediction with density scores") names techniques, not the problem solved or the finding.

**Fix (honest, no overclaiming):**
- *Title*, for example: "Prediction intervals that cover rare outcomes in imbalanced regression: guarantees, optimal scores and a 48-dataset evaluation". Or: "Covering rare outcomes in imbalanced regression with conformal prediction: what it costs and which guarantee to choose".
- *Contributions*, reordered as four:
  - (C1) diagnosis: standard and even oracle covariate-adaptive intervals under-cover rare outcomes, quantified on 48 datasets;
  - (C2) the price of tail validity: about 1.2× size, cheaper than lowering α, exact under stratum re-weighting;
  - (C3) size-optimal scores for two tail guarantees (stratum-wise: SDLC; relevance-weighted: RW-DLC), with the honest finding that among scale-aware scores the choice changes size by only a few percent;
  - (C4) a decision guide covering which guarantee, which strata, intervals versus sets, and alerts versus tail classifiers, under explicit costs.
- *Abstract*: lead with the practical finding, keep one sentence on the small SDLC/S-NCP gap, and end on the guidance, for example: "For a known extreme range, a dedicated stratum suffices; RW-DLC is preferable when coverage must hold across the whole target range without choosing strata." Remove the fragment "calibrating within each stratum is established;" which is ungrammatical as written.

### Issue 2 (MAJOR): Length and density are far above a typical JKSU-CIS article (re-raised: earlier fix inadequate and since reversed)

**Location:** Whole manuscript.

**Evidence:**
- Word counts from `manuscript_filled.md`, Sections 1–8 (lines 12–605): 16,180 words including table cells; 13,608 without table rows; about 13,360 with display maths removed. The appendix (proofs and notation) adds 1,488 words. The docx body text is 19,204 words in total.
- Response 07 reported "about 12,600 words". Text has since been added (dedicated tail strata in §6.4, temporal splits in §6.7, extra held-out checks in §6.3.3).
- The main text has 11 tables, 9 figures, Table B1, Theorem 1–2, Corollary 1, Propositions 1–4 and Remark A.1.
- Section 6 has 8 subsections plus 3 sub-subsections.
- The supplement is a further 13,350 words with 20 tables.
- The stale PDF has 39 pages.
- I could not measure JKSU-CIS article lengths from the material provided. In my experience as an editor, applied-ML research articles in the journal run to about 15–25 typeset pages and roughly 7–11k words. The manuscript is about 1.5–2× that.

**Fix:** Target about 9–10k words in the main text.
- Move to the supplement, each with a one-line summary in the text:
  - Proposition 3 and its proof;
  - Corollary 1(ii)–(iii) (keep (i));
  - Table 7 and §6.3.2 (synthetic);
  - Table 10 (keep Fig. 7);
  - Table 11 (keep Fig. 8 and two sentences);
  - most of §6.7 (grouped and temporal splits, MLP, DenseWeight) as one summary paragraph;
  - §6.8 except one paragraph;
  - Fig. 4 or Fig. 5 (keep one).
- Merge §7.1 into §8, so the findings are not stated three times (abstract, §7.1, §8).
- Introduce no more than 10 method acronyms in the main text. Rename ablation-only variants (SDLC-2p, SDLC-hist, DLS-N, DLS-2p, DLS-hist, O-*, RW-DLS-U, RW-NCP-U) only in the supplement.

### Issue 3 (MODERATE): Reads as a statistics paper; the computer-science angle is under-signposted

**Location:** Abstract; §1; §§3–4; §6.

**Evidence:**
- The abstract contains no application, system or deployment element. Its vocabulary is "stratum", "normalised residual", "relevance-weighted target".
- Eight formal results appear before any experiment.
- The CS assets exist but are buried: Algorithm 1 (§4.4), complexity (§4.5), timing (§6.7, 13.5 µs per test point), the cost-based alert study (§6.6) and the practical guidance (§7.2).
- The selection note (`selected_journal.md`, "Key rejection risks") already lists desk rejection as "too statistical/theoretical" as the top risk.

**Fix:**
- Add one sentence to the abstract on deployment: per-point cost, that it works with any regressor (LightGBM, MLP), and recalibration without refitting.
- Give one concrete use case (valuation or energy load) in the first paragraph, carried into Fig. 8.
- Move §7.2 "Practical guidance" up, or summarise it as a decision table early in §6 or §7.
- State Propositions 2 and 4 in the main text, and put Proposition 3 and Corollary 1(ii)–(iii) in the appendix or supplement (see Issue 2).

### Issue 4 (MODERATE): Cited Supplementary Table S13 does not exist

**Location:** §6.7 "Computational cost" ("Supplementary Tables S13 and S14").

**Evidence:**
- `supplementary_filled.md` and `Supplementary_Material.docx` contain Tables S1–S12, S14–S19 and S17b. There is no S13.
- `build_supplement.py` (lines 171–190) emits S13 only if `tables/D15c_timing_like.csv` exists, and that file is absent.
- The headline timing (13.5 µs SDLC, 0.09 µs S-NCP) is therefore not documented in the supplement.
- Tables S7, S9, S11, S12 and S19 are never cited from the main text. That is allowed for a supplement, but the numbering then looks arbitrary, as does "S17b".

**Fix:** Generate `D15c_timing_like.csv` (run `timing_like.py`) and rebuild, or cite the timing source that exists. Renumber the supplementary tables in order of citation, and replace S17b with an integer number.

### Issue 5 (MAJOR): The anonymised code package is promised but not built, and the repository as it stands would break double-blind review

**Location:** §5.7 (commit identifiers "in the version history of the anonymised code package provided as supplementary material"); Code availability; Supplement S5–S7.

**Evidence:**
- There is no package (zip/tar/bundle) in the project, and no script that builds one.
- The git repository from which it would be made has:
  - an `origin` remote that is a personal GitHub account URL containing a user name;
  - branch names `claude/...`;
  - commit messages such as "Response to review 8", "Review 5: …", "Review cycle 1: …" and "Pre-registered confirmatory analysis plan…";
  - the folder `Target_Journal_Submission/archive_eswa/` and the file `journal_selection/*`, which reveal that the paper was first targeted at another journal.
- Commit messages mentioning numbered "reviews" may be read by referees as earlier journal rejections.
- "Pre-registered" in commit messages and file names (`PREREGISTRATION_*.md`) contradicts the manuscript's careful "pre-specified rather than pre-registered" (§5.7).
- `results/` is about 1.0 GB. Check the Editorial Manager supplementary file-size limit, or use an anonymous repository link.
- The docx metadata are otherwise clean (creator = anonymisation note, no lastModifiedBy). But `docProps/custom.xml` stores the local paths `/home/user/p_c1_2/…/references_verified.bib` and the CSL path, and each figure's alt text (`descr`) in `document.xml` holds an absolute local path.

**Fix:**
- Build the package from a fresh `git init` with only `code/`, the configs and the plan files. Use neutral commit messages, no remote and no `archive_eswa`/`journal_selection`/`REVIEW` folders.
- If the cited identifiers `ccba99b`/`a9f31d2` must remain verifiable, provide a scrubbed `git bundle` or rewritten history with a mapping note. Alternatively, cite plan time stamps through an anonymous OSF/anonymous.4open.science link instead of hashes.
- Rename the `PREREGISTRATION_*` files to `ANALYSIS_PLAN_*`.
- Strip `custom.xml` (bibliography/csl properties) and the image `descr` paths from the docx.

### Issue 6 (MAJOR): The pre-specified CTR23 arm of the relevance-weighted study is neither reported nor declared as a deviation (re-raised: R8-4 still open)

**Location:** §5.7 "Relevance-weighted study"; §6.4; Supplement S7 (verbatim plan, §2 "Data" and §5 "Deviations").

**Evidence:**
- The verbatim plan specifies "Exploratory: all 31 OpenML-CTR23 datasets … The same analysis is run on both". It also says "Any change after this commit will be listed in the manuscript as a deviation with its reason."
- The manuscript reports only the 17 held-out datasets (Table 9, S18).
- Table S19 is now the earlier-implementations table, not the RW CTR23 results that Response 08 promised.
- No mention of the CTR23 arm, and no deviation statement, appears in §5.7 or §6.4.
- `results/raw_refit/` holds 93 files, so the refit appears to be incomplete.

A reviewer who reads S7 will spot this at once. It looks like selective reporting, which in this paper would be especially damaging, given how much credibility it draws from pre-specification.

**Fix:** Report the CTR23 arm, for example as one row block in a supplementary table plus one sentence in §6.4. If it cannot be completed before submission, add an explicit deviation: "The pre-specified exploratory CTR23 arm was not run because …; all RW claims rest on the held-out arm, as the plan specified for disagreements."

### Issue 7 (MODERATE): Submission files are stale or incomplete

**Location:** `manuscript/Final_Manuscript.pdf`; `title_page_filled.md`; `cover_letter_filled.md`.

**Evidence:**
- The PDF (created 15:39, built from an earlier render) has an abstract that differs from the docx (16:02). It gives "87.2% … against 68.8%", has no dedicated-tail-strata sentence, and contains no "Moneyball" (temporal split) or "Dedicated tail strata" text.
- The title page still contains "[Author 1]", "[Department, institution …]", "Funding: [Placeholder.]", "Acknowledgements: [Placeholder …]" and "[To be confirmed by the authors.]".
- The cover letter has "[Corresponding author name]", "[Affiliation …]", "[E-mail address]" and "[Date]".

**Fix:** Rebuild the PDF from the current sources, or upload only the docx. Have the authors complete the title page and cover letter. Add a pre-upload check (grep for `[` placeholders and compare PDF and docx abstracts).

### Issue 8 (MODERATE): Headline top-1% numbers differ between abstract, conclusion and cover letter (re-raised: R8-8 fix incomplete)

**Location:** Abstract; §6.3.3; §6.4; §8; cover letter.

**Evidence:**

| Source | RW-DLC top-1% coverage | SDLC (five strata) top-1% coverage |
|---|---|---|
| Abstract | 88.4% | 76.0% (post hoc unified definition) |
| §8 Conclusion | 87.2% | 68.8% (pre-specified definition) |
| Cover letter | 87.2% | 68.8% |
| §6.4 first sentence | — | 0.688 |
| §6.3.3 | — | 0.747 |

So one quantity appears as three numbers (0.688, 0.747, 0.760) across sections, and the abstract and conclusion use different definitions.

**Fix:** Pick one definition for all summary statements (abstract, §7, §8, cover letter), preferably the pre-specified one, since the paper's credibility rests on pre-specification. Report the other once, in §6.4, labelled as a sensitivity check.

### Issue 9 (MODERATE): Too much hedging and post hoc material in the main results

**Location:** §§6.3.1, 6.3.3, 6.4, 6.7.

**Evidence:**
- The main text uses "post hoc" 8 times, "pre-specified" 22, "Holm" 19 and "small" 64 times.
- §6.3.3 alone mixes:
  - pre-specified decisions;
  - post hoc merged-duplicate checks;
  - continuous-target subsets;
  - tail-mass subsets;
  - TOST at ±5%;
  - "reliably smaller" counts;
  - skewness subsets.
- §6.3.1 reports three size estimands (geometric mean, Hodges–Lehmann, wins) plus post hoc TOST.

Each caveat is justified, but together they bury the message. The reader cannot tell which result the authors stand behind.

**Fix:**
- In the main text, report the pre-specified decision and one effect size per comparison. Move every post hoc robustness check to one supplementary table, referenced by a single sentence ("post hoc checks (Table Sx) left every decision unchanged; the advantage over S-NCP was confined to continuous targets").
- Choose one size estimand for the main text and state it once.

### Issue 10 (MINOR): Abstract at the word limit and dense with qualifiers

**Location:** Abstract.

**Evidence:** 248 words by whitespace count (docx paragraph and md agree; limit 150–250). It contains parenthetical scope qualifiers ("4,209–50,000 rows, no extremely skewed targets") and six method names (SDLC, RW-DLC, OpenML-CTR23, plus the descriptions "stratified normalised residual", "absolute residuals", "quantiles"). Different counting tools (for example, splitting "63.0%–78.3%" or "4,209–50,000" at the dash) could take it over 250.

**Fix:** Aim for about 220 words. Move the scope qualifiers to §5.1 and §7.3.

### Issue 11 (MINOR): Reference list consistency

**Location:** References (docx).

**Evidence:**
- Several entries with known DOIs carry none, for example:
  - Papadopoulos et al. 2002 (LNCS);
  - Torgo and Ribeiro 2007 and 2009, Torgo et al. 2013 (Springer LNCS/LNAI);
  - Vovk et al. 2005 and 2022 (books);
  - Ren et al. 2022 (CVPR/IEEE).
- NeurIPS and ICML entries vary: some give page ranges, others (Ke et al. 2017; Romano et al. 2019; Tibshirani et al. 2019) do not.
- Six arXiv preprints from 2025–2026 support claims in related work, including Boruah 2026a/b, Choi 2026 and Lee et al. 2026. A reviewer may question leaning on recent unrefereed work, so keep each to a supporting role.
- The two JKSU-CIS citations (Zhang et al. 2025; Zhu et al. 2026) are relevant and appropriately placed.

**Fix:** Add the missing DOIs and make the conference entries uniform (pages for all, or for none).

### Issue 12 (MINOR): Figure 1 rendering details

**Location:** Fig. 1(b).

**Evidence:**
- In the "Scores at the observed targets" box, the hat of f̂ in "SDLC: S_i = −f̂(Y_i | X_i)" renders as a stray mark below the line, between the two formula lines.
- The arrow from "Relevance φ(y)" to the RW-DLC box crosses the SDLC→output arrow.

**Fix:** Re-typeset the box label and route the relevance arrow around the SDLC row.

---

## Points checked and found adequate

- **Scope:** imbalanced learning, uncertainty quantification and conformal methods fit JKSU-CIS. Two recent JKSU-CIS papers are cited and positioned correctly. The application examples (valuation, loads, toxicity) and the decision/cost study suit a CS readership.
- **Honesty of claims:** prior art (Mondrian, BCCP, BFQR, Sadinle et al., Kandinsky, Yi et al., weighted CP) is credited explicitly in §1, §2.2 and Table 1. Small and negative results (RW-4 not supported; SDLC worse than S-NCP on top-1%, noisy inputs, alerts and hulls) are reported.
- **Keywords:** 6 (within 4–6), consistent across manuscript and title page.
- **Structure:** decimal headings with at most 3 levels (deepest is 6.3.1). Algorithm box, complexity section, notation table.
- **Anonymisation of the manuscript text:** no author names, institutions, e-mails, URLs, GitHub/Zenodo links, branch names or acknowledgements in `manuscript_filled.md` or `supplementary_filled.md`. The supplement's branch name and motivation paragraph are redacted. The docx creator field holds the anonymisation note, and lastModifiedBy is empty. Exceptions are in Issue 5.
- **Statements and Declarations:** competing interests, funding (on the title page), author contributions (on the title page), data availability (OpenML IDs, licences, licence-restricted files), code availability, ethics and the LLM statement are all present, after the references.
- **LLM-use statement:** in the Methods (§5.8), specific about tasks, states that no data or results were generated, and that the authors take responsibility. This matches the journal policy recorded in `selected_journal.md`.
- **Cross-references:** no `??` and no unfilled `{{…}}` placeholders in the rendered manuscript or supplement. Tables 1–11 and Figs. 1–9 are each defined once and cited in numerical order. Every cited supplementary item except Table S13 exists (S1–S8, S10, S14–S18, Sections S2, S3, S5–S7). Captions start with bold "Fig."/"Table".
- **Citation style:** author–year, alphabetical, with DOIs for most journal articles (Springer basic author-date CSL). In-text form "(Branco et al. 2017a; Ribeiro and Moniz 2020)" is correct.
- **Figures:** Fig. 3 (coverage–size trade-off) is clear, colour-consistent and readable in greyscale through marker shapes. Fig. 1(a) conveys the method intuitively.
- **Main message in the first two pages:** the problem statement (§1, paragraphs 2–3) and the oracle shortfall (70.5% of the top decile) are clear and compelling. The weakness is the contribution framing (Issue 1), not the problem statement.

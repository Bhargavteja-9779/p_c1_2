# Response to review rounds 2–4

Status legend: FIXED (changed, with computation where needed) · PARTIAL · DECLINED (with reason).

## Review 2 (novelty / prior art)
| ID | Issue | Status | What changed |
|---|---|---|---|
| R2-01 FATAL | Contribution reduces to known pieces + benchmark | FIXED (research change) | New method **RW-DLC**: relevance-weighted coverage for continuous outcomes with a finite-sample guarantee (Theorem 2, proof in App. A), size-optimal score φ(y)f(y\|x) (Proposition 4), evaluated under a second analysis plan committed before its first evaluation (PREREGISTRATION_relevance_weighted.md, commit a9f31d2). Held-out results: RW-1–RW-3 supported, RW-4 not supported (reported). Contribution statements rewritten around two guarantees; stratified calibration credited as prior art throughout. |
| R2-02 | Missed long-tailed classification prior art | FIXED | Ding et al. (2025), Liu et al. (2025), Bhattacharyya et al. (2026), Chzhen et al. (2021) verified on arXiv and cited in §2.2 and the introduction; RW-DLC positioned as the regression counterpart of macro-coverage. |
| R2-03 | Table 1 unfair | FIXED | Table rebuilt: label-shift robustness credited to Mondrian/BCCP calibration; Sadinle/Podkopaev row "exact under label shift"; Gibbs and Kiyani split; Kandinsky, Lei 2013, long-tailed classification and macro-coverage rows added; SDLC optimality cell states conditions. |
| R2-04 | Fails one-minute desk test; "size-optimal" in title | FIXED | New title without "size-optimal"; abstract states both guarantees, what is new (RW-DLC) and that gains over S-NCP are a few per cent. Highlights not required by the journal (archived). |
| R2-05 | Real open problems left open (sparse tail strata, top 1%, joint constraints, choosing strata) | PARTIAL | RW-DLC addresses the top 1% and the need for strata (top-1% coverage 0.872 vs 0.688 held-out); joint marginal + per-stratum constraints and learned strata are stated as future work. |
| R2-06 | Fit / length for JKSU-CIS | PARTIAL | Main text shortened (target ≈12.5k words); algorithm box, complexity, runtime, decision study and practical guidance retained for a CS readership. |
| R2-07 | Continuous label-shift literature; Cor. 1 credited to SDLC | FIXED | Choi (2026) cited; Cor. 1 and Table 1 state the property belongs to stratified calibration. |
| R2-08 | "Imbalanced regression" notion of rarity (relevance) not used | FIXED | Relevance functions (Torgo & Ribeiro; DenseWeight) now define RW-DLC's guarantee. |
| R2-09 | Neighbouring 2026 "tail" conformal papers | PARTIAL | The verified ones are cited; papers we could not verify are not cited. |
| R2-10 | BCCP "any score" attribution | FIXED | Attribution removed; we state the argument does not depend on the score. |
| R2-11 | Asymptotic optimality stated without conditions | FIXED | Abstract no longer claims it; §4.3 states the conditions and that the fixed-constant implementation is outside them. |
| R2-12 | Duplicated BFQR description | FIXED | |
| R2-13 | "13 procedures" inflates comparison | FIXED | Abstract no longer counts procedures. |
| R2-14 | "We are aware of two…" undated | FIXED | "As of November 2026". |
| R2-15 | Table placement | FIXED | Positioning table at end of §2. |

## Review 3 (statistics)
| ID | Status | What changed |
|---|---|---|
| R3-01 estimand/decision rule | FIXED | Primary size estimand declared (Hodges–Lehmann / signed-rank, typical dataset); geometric mean secondary; post hoc TOST ±5% (`scripts/analyze_secondary.py`): not equivalent on CTR23; on held-out SDLC ≡ S-HPD (p = 0.004), S-NCP borderline (p = 0.054); text reports both. |
| R3-02 missing secondary analyses | FIXED | Hull comparisons on held-out data reported in §6.5 and Supplementary Table S17, including the unfavourable SDLC-hull vs S-NCP-hull (ratio 1.045, p = 0.71). |
| R3-03 "made public" unverifiable | FIXED | "Pre-registered" → "pre-specified"; "committed to version control (commit ccba99b)"; disclosure that base-model test metrics existed before the plan. |
| R3-04 skewness of held-out data | FIXED | Skewness table (S18) and subgroup comparisons: advantage over S-NCP/S-HPD vanishes on the 7 skewed held-out datasets, as on CTR23; reported. |
| R3-05 C-H1/2/4 follow from Theorem 1 | FIXED | Stated in §6.5. |
| R3-06 alert costs vs S-NCP; unadjusted p | FIXED | §6.8 reports S-NCP cheaper (27/31 at r=10, 29/31 at r=20); p-values labelled unadjusted/descriptive; guidance updated. |
| R3-07 dataset-level reliability | FIXED | Per-dataset seed-level 95% intervals: CTR23 SDLC reliably smaller than S-NCP on 18/31, larger on 0; held-out 8/17 and 1/17. |
| Minor items | PARTIAL | Holm families as defined in the tables; second-order cross-fitting leak acknowledged in review response (efficiency only). |

## Review 4 (method / code)
| ID | Status | What changed |
|---|---|---|
| R4-1 Prop. 3 vs implemented estimator | FIXED (text) | §4.3: Prop. 3 applies when ε and the floor vanish with N; the fixed-constant implementation is outside it. |
| R4-2 ĝ mis-calibration | PARTIAL | Text no longer claims the in-sample version is "too narrow" without qualification; states cross-fitted residuals make ĝ mildly too wide and that this affects efficiency only. Re-fitting ĝ on full-model residuals would require a v4 re-evaluation of every method; not done (declared). |
| R4-3 SDLC-N mis-scaled | FIXED (text) | Described exactly as implemented, with its limitation for the decomposition. |
| R4-4 closed stratum pieces | FIXED (text) | Effect stated: measure zero for size, coverage decided by exact rule. |
| R4-5 domain truncation and the Theorem 1 bound | FIXED | Sentence corrected. |
| R4-6 complexity / number of regressions | FIXED | O(K·R·log G) per test point; 8 regressions in a single-pass implementation, 12 in the benchmark code. |
| README names ESWA | FIXED | (code/README.md updated in this revision). |

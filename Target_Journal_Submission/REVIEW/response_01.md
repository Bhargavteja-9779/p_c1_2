# Response to review cycle 1 (REVIEW/review_01.md, 46 consolidated issues)

All changes were implemented in code first and then propagated to the manuscript. Every number in the manuscript is
regenerated from result files (`scripts/analyze3.py`, `scripts/render_manuscript.py`). Main code changes are listed in
EXPERIMENT_LOG.md items 11–13. Status codes: **F** = fixed with new computation; **T** = fixed in text;
**P** = partially addressed (reason given); **D** = declined (reason given).

## Critical

| ID | Status | Action |
|---|---|---|
| C1-01 pre-registration overstated, post-hoc H3 | F+T | "Pre-registered" removed for the main benchmark (Section 5.7 states what was fixed in advance and what changed). All CTR23 size comparisons labelled exploratory. **New confirmatory replication** on 17 held-out datasets (OpenML suites 335/336, no source overlap with CTR23): analysis plan + script committed and pushed (commit ccba99b) before any confirmatory evaluation. Script unchanged at analysis time. All four hypotheses supported (Section 6.5, Table "confirmatory"). Earlier implementations summarised in Supplementary S5 / Table S14. |
| C1-02 no advantage over S-NCP, weakened competitors | F+T | v3 estimator (cross-fitted standardisation, robust KDE, no floor) re-evaluated for *all* LS methods; harmonised scale floor for every method using σ̂; half-open stratum pieces for interval baselines; S-NCP-hull, S-NCP-floor and BCCP-floor added. S-NCP is now named the information-matched comparator. Result: SDLC smaller than S-NCP on 27/31 CTR23 datasets (Holm p < 0.001) and 15/17 held-out datasets (p = 0.008), but by a small amount (geometric-mean ratio ≈ 0.98). This is stated in the abstract, results, discussion and conclusion. Ablation chain BCCP → S-NCP → SDLC-N → SDLC attributes the gain mostly to the 1/σ̂ factor. |
| C1-03 worse coverage of the most extreme outcomes | F+T | Top-1% and top-5% coverage are now reported for all methods with Holm-corrected tests against stratified comparators. SDLC's lower top-1% coverage vs S-NCP and S-HPD is stated in results, discussion, conclusion and abstract ("lower coverage of the noisiest inputs"). Title and highlights no longer claim extreme-outcome superiority. |

## Major

| ID | Status | Action |
|---|---|---|
| C1-04 empty sets / high-σ coverage / reallocation | F+T | Empty-set rate, σ̂-decile coverage and worst σ̂-decile coverage reported (Table "main", Fig. "sigma"). New theory remark ("Coverage is reallocated across inputs", Section 4.3) derives the reallocation and the empty sets for the oracle in a location–scale model. Practical guidance recommends S-NCP when even coverage across noise levels is required. |
| C1-05 in-sample standardisation | F | `experiments/refit_scales.py`: cross-fitted scale models; ĝ fitted to cross-fitted standardised residuals. In-sample shrinkage quantified (median sd ratio reported in Section 4.4). |
| C1-06 ad hoc KDE floor / grid | F | ĝ = 0.99·FFT-KDE + 0.01·Student-t₂ (no floor, polynomial tails); bandwidth-adapted grid (spacing ≤ h/4); stratum-exact set geometry; grid-convergence study (Supplementary Table S4: mean-size change ≤ 0.17%, per-point ≤ 1.5%). |
| C1-07 closed stratum pieces | F | Interval methods use half-open stratum pieces (`conformal.interval_method(half_open=True)`); unit tests. |
| C1-08 realised strata | F+T | Realised K and tail masses per dataset (Supplementary Table S1); modal-K filter for seed averaging; all H3 comparisons repeated on the 26 datasets with nominal tail strata (Table S5). |
| C1-09 dependence on α, n, hull, summary | F+T | Sensitivity table S5 (α, strata, development/diagnostic exclusions, skewness, size); geometric mean and Hodges–Lehmann ratio, wins/losses and sign test reported for every comparison; hull forms reported separately, including the mixed result against S-NCP-hull. |
| C1-10 error-analysis prose | T | Error analysis rewritten from the statistics: price rises with skewness (ρ = 0.62) and falls with calibration size; the four datasets where SDLC loses to S-NCP are named and explained. |
| C1-11 claims rest on non-skewed datasets | F+T | Subgroup analysis by skewness (Table S5); on the 15 strongly skewed datasets SDLC beats BCCP and S-HPD, but not significantly S-NCP or S-CQR, which is stated in the results. |
| C1-12 exclusion rationale | T | Rationale restated (ordinal targets with a handful of values); atom-heavy targets retained and discussed explicitly (forest fires, health insurance). |
| C1-13 Theorem 2 novelty | T+F | Recast as Proposition 2 with credit to Lei et al. 2013, Sadinle et al. 2019 and Kiyani et al. 2024 (whose groups are covariate-defined; verified). **New Proposition 3**: asymptotic size-optimality of the plug-in procedure, with proof (Appendix A). "Main methodological contribution" removed. |
| C1-14 Proposition 1 scope | F+T | Claims restricted to the Gaussian model; elementary general fact added; Monte Carlo extension to t₃/t₅/t₃₀ signals and Gamma noise (Table "prop1") shows the shape is model-dependent, including over-coverage of the lower tail under skewed noise. Earlier empirical reports credited. |
| C1-15 Corollary 1 credit, loose bounds | T | Credits to Podkopaev & Ramdas, Angelopoulos–Barber–Bates (label shift) and Barber et al. 2023 (Sec. 4.5; verified). Text states that the bounds are loose for the studied tilts and explain only the direction. |
| C1-16 BFQR-style comparator | T | "BFQR-style" label dropped; S-CQR described as stratified CQR without BFQR's level optimisation. BFQR's level optimisation and Theorem 4.1 described accurately (verified by the bibliography agent). Decile strata (S10) analysis reported (Table S5/S7). A faithful BFQR implementation was **not** added (P): BFQR deliberately trades coverage across bins (Σβ_m/M = 1−α), so it does not target per-stratum 1−α and is not a like-for-like comparator; this is stated. |
| C1-17 Kandinsky mischaracterised | T | Rewritten in related work and theory (label-dependent, overlapping and fractional groups; approximate high-probability guarantee; regression experiment). Overlapping/weighted groups named as a remedy in the limitations. Kandinsky experiment not run (P): time budget; listed as future work. |
| C1-18 shift: ESS, metric, positive control | F | Stratum-wise tilted coverage (not marginal) is the reported metric; Kish ESS reported, analysis repeated on datasets with ESS ≥ 50; positive control (whole-strata re-weighting) added, which shows exact preservation; genuine label shift with known X∣Y in the synthetic study. |
| C1-19 synthetic study only correctly specified | F | Five designs: skewed, covariate-dependent skewness, covariate-dependent bimodality, heavy tails, zero inflation; n = 500 and 5000; genuine label shift (Table "synthetic", Table S10). |
| C1-20 MLP floor/imputation | F | `run_learner_generality3.py`: training-only median imputation with missingness indicators, cross-fitted scales and the harmonised floor, identical to the main pipeline. |
| C1-21 tail-alert claim | F+T | Decision study with dedicated conformal tail classifiers and conformal selection (Jin & Candès 2023). Result stated honestly: dedicated classifiers need fewer alerts for the same recall guarantee; set-based alerts are competitive when misses are costly. |
| C1-22 no decision-oriented case study | F | Expected-cost curves for three valuation datasets (Fig. "costs") and cost-ratio analysis across all datasets (Table "alerts"). |
| C1-23 no imbalanced-regression learners | F | DenseWeight-weighted LightGBM (Steininger et al. 2021) experiment (`run_denseweight.py`), reported in Section 6.8. |

## Moderate and minor

| ID | Status | Action |
|---|---|---|
| C1-24 no shift-aware competitor | D (T) | The paper studies robustness without shift estimation; re-weighting competitors require target-domain information. Stated in Section 4.2 and the limitations. |
| C1-25 strong covariate-conditional baselines | P (T) | Not run (CHR, conditional calibration, RLCP); discussed as a limitation with the observation that Proposition 2 bounds their oracle versions. |
| C1-26 floor variant as contribution | T | Floor now a "practical variant, not a contribution"; level-optimising alternatives credited; floor and hull compared with all stratified comparators. |
| C1-27 geometry vs scored set; untested code | F | Stratum-exact geometry for the same set whose coverage is scored; new monotone-run algorithm verified against a cell-wise reference (unit test). |
| C1-28 dev/diagnostic datasets | F+T | All seven diagnostic datasets named; H1 and H3 repeated without development and without development + diagnostic datasets. |
| C1-29 Table 5 signs | F | All tables regenerated from `analyze3.py` with explicit conventions. |
| C1-30 statistical refinements | F | Hodges–Lehmann with Wilcoxon-inversion CI, sign test, wins/losses, TOST, geometric-mean ratio with bootstrap CI; Friedman ranks descriptive only. |
| C1-31 independence claim false | F+T | Sentence deleted; repeated units described; grouped-split robustness experiment (`run_grouped.py`: sarcos de-duplicated, video transcoding grouped by video, superconductivity grouped by feature vector). |
| C1-32 domain includes negatives | F | D ∩ [0, ∞) for non-negative targets. |
| C1-33 outliers and SD normalisation | T | All size comparisons are within-dataset ratios, unaffected by the normalisation; skewness reported as is (brazilian houses noted). |
| C1-34 calibration-size confound | F+T | Runs with infinite thresholds reported (Table S8) and the size growth attributed to them in the text. |
| C1-35 fit-time accounting | F | `timing_fit.py`: per-component single-thread fit times; `timing.py`: per-dataset medians after warm-up (Table S13). |
| C1-36 length / tables / names | T | Method names unified (BCCP, S-NCP, S-CQR, S-HPD, SDLC, SDLC-N); dataset table, sensitivity, α, strata, calibration-size and error tables moved to the supplement; three figures moved to the supplement. |
| C1-37 supplementary material missing | F | `scripts/build_supplement.py` builds Supplementary_Material.docx/.pdf with Sections S1–S6, Tables S1–S14 (incl. licences) and Figures S1–S3. |
| C1-38 submission readiness | P | Author/affiliation placeholders must be completed by the authors; code package included for review; AI-use declaration made specific. |
| C1-39 references | F | Bibliography verified and corrected by a dedicated agent (arXiv identifiers, TMLR, article numbers, capitals, names, Kandinsky co-author); CSL patched to print a URL when no DOI exists and PMLR volumes. |
| C1-40 Algorithm 1 cost, timing environment | F+T | Algorithm 1 states eight GBDT fits and the FFT-KDE and prediction costs; timing single-threaded with warm-up discarded. |
| C1-41 theory statement fixes | T | Appendix remark restated for C* in the Gaussian model; vacuous convexity claim deleted; HPD for LS2 dropped; +∞ exception completed. |
| C1-42 missing related work | T | pintervals/clustered conformal, CTI (Luo & Zhou 2025), Wang et al. Thm 4.1, Romano et al. 2020, DenseWeight, Balanced MSE, Jin & Candès, Barber et al. 2023, Kiyani et al. 2024 added (all verified). |
| C1-43 ESWA works characterised without reading | T | Characterisations limited to what titles/abstracts support (Oucheikh: Mondrian; SMOGAN: generic oversampler; Johansson: interpretable regression trees); literature matrix now has a row for every bib key with read status. |
| C1-44 matched-coverage comparison | F | Marginal methods at α = 0.05 vs SDLC at α = 0.1 (Table "matched"). |
| C1-45 package hygiene, stale audit | F | Leakage audit re-run on final data; stray file removed; README/REPRODUCIBILITY_STATUS updated; review workflow excluded from the release package. |
| C1-46 discontiguous sets | T | Mean pieces reported for every method; interpretability discussed; hull variant recommended when an interval is required. |

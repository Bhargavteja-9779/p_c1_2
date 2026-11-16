# PROJECT_STATE (checkpoint file — updated after every major stage)

## Fixed decisions
* Target journal: Expert Systems with Applications (Elsevier) — see journal_selection/. ≤100-day acceptance NOT verifiable for any suitable journal (disclosed).
* Topic: Target-stratified conformal prediction (TSCP) for imbalanced regression — per-target-stratum coverage guarantees; size-optimal score = conditional-density level sets per stratum.
* Data: OpenML-CTR23 (suite 353), 31 of 35 datasets (pre-registered exclusion: <20 distinct target values).
* Development datasets (used for design decisions before the full run): airfoil (44957), concrete (44959), QSAR fish (44970). Confirmatory statistics are also reported on the remaining 28.
* Pre-registered primary method: SDLC-LS (stratified density-level conformal with location-scale density). Config: code/config/benchmark.json.

## Pre-registered hypotheses
H1 stratified methods attain per-stratum coverage ≥ 1-α; marginal/X-conditional methods do not on tail strata.
H2 price of stratum validity (size increase vs marginal counterpart with the same score) is quantified.
H3 (theory-driven) density-level score yields smaller stratified sets than residual/CQR scores — may fail with estimated densities.
H4 stratified methods remain valid under target (label) shift; marginal ones degrade.
H5 floor variant interpolates (marginal ≥1-α and stratum ≥1-2α) at intermediate size.

## Status (checkpoint 2026-11-16 07:10 UTC)
- [x] Journal selection (ESWA; ≤100-day acceptance not verifiable — disclosed)
- [x] Literature matrix (65 verified refs) + ESWA benchmark (32 papers) — supplementary/
- [x] PRIOR ART: BCCP (Randahl et al. 2026) and BFQR (Wang et al. 2023) already calibrate within Y-bins → novelty repositioned
- [x] v1 pre-registered benchmark complete (310/310), archived: results/raw_v1_preregistered; analysis: supplementary/v1_preregistered_analysis
- [x] v1 finding: H1 supported; H3 not supported (grid artifact diagnosed) → exact grid-free LS implementation (src/methods/ls_exact.py)
- [~] v2 fit-only run caching model outputs: results/raw_contexts (124/310 at checkpoint; restarted: results/experiment_logs/fitonly_v2_part2.log)
- [ ] evaluate_from_cache.py over all 310 contexts → results/raw_eval
- [ ] MLP learner study (experiments/run_learner_generality.py) and synthetic oracle study (experiments/synthetic.py)
- [ ] analyze.py (default RAW = results/raw_eval), analyze_extra.py, figures_extra.py, render_manuscript.py
- [x] Drafts: 01_intro, 015_related (agent), 02_theory, 03_setup, drafts/positioning.md (agent)
- [ ] Failed agents to re-run (usage limit): declarations, proof-check A/B, citation audit
- [ ] Results/discussion/conclusion/abstract; 10-agent review cycles; DOCX; cover letter; final audits

## Next step
Resume workflow wf_fb169d56-2b7 (failed agents) while fits run; then evaluation stage.

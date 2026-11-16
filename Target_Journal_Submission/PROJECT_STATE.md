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

## Status (checkpoint 2026-11-16 18:40 UTC)
- [x] Journal selection (ESWA; ≤100-day acceptance not verifiable — disclosed)
- [x] Literature matrix (65+ verified refs) + ESWA benchmark (32 papers); BCCP/BFQR prior art → novelty repositioned
- [x] v1 pre-registered benchmark (archived results/raw_v1_preregistered; analysis supplementary/v1_preregistered_analysis)
- [x] v2 fits cached (results/raw_contexts, 310/310); exact LS evaluation (results/raw_eval, 310/310)
- [x] MLP learner study (results/raw_mlp, 155/155); synthetic oracle study; timing experiment (results/timing_methods.csv)
- [x] analyze.py / analyze_extra.py / figures_extra.py → results/*.json, tables/, figures/
- [x] Manuscript sources manuscript/src/*.md; rendered DOCX manuscript/Final_Manuscript.docx (+ highlights.docx)
- [ ] 10-agent review cycles (code/scripts/review_cycle_workflow.js) — next
- [ ] Cover letter, final PDF (pandoc→MathML HTML→Chromium), final audits, rejection-risk report, manifest

## Key results (all machine-generated)
H1 supported (SDLC > every marginal method on worst-stratum coverage, Holm p<0.001, ≥30/31 datasets).
Null reference: stratified methods consistent with exact validity (0–3/31 datasets below null 5%).
H3 (exact implementation): SDLC smaller than BCCP (geo 0.932, 22/31, p=0.018), S-CQR (0.833), S-HPD (0.949);
vs S-NCP typical but not uniform (24/31 smaller, geo 1.004). MLP study: SDLC smaller than BCCP, S-NCP, S-HPD.

## Next step
Run review cycle 1 workflow; fix; iterate.

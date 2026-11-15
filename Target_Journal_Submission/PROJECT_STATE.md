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

## Status
- [x] Journal selection
- [x] Topic selection + prior-art checks (ongoing deeper literature agent)
- [x] Implementation (code/src, experiments/run_benchmark.py)
- [~] Full benchmark running (results/raw/, log results/experiment_logs/full_run.log)
- [x] Prop.1 verification (results/prop1_gaussian.json)
- [~] Synthetic oracle study (results/synthetic.jsonl)
- [ ] Analysis/statistics/figures/tables
- [ ] Manuscript, reviews, DOCX, cover letter

## Next step
After the full run: rerun failed tasks (bug fix in fit_classifier for tiny datasets), then scripts/analyze.py.

# PROJECT_STATE (checkpoint file — updated after every major stage)

## Fixed decisions
* Target journal: Expert Systems with Applications (Elsevier) — see journal_selection/. ≤100-day acceptance NOT verifiable for any suitable journal (disclosed).
* Topic: stratified (target-conditional) conformal prediction for imbalanced regression; size-optimal score = conditional-density level sets per stratum (SDLC).
* Data: OpenML-CTR23 (suite 353), 31 of 35 datasets (exclusion: <20 distinct target values). Confirmatory: 17 held-out datasets (OpenML suites 335/336, config/confirmatory.json).
* Development datasets: airfoil (44957), concrete (44959), QSAR fish (44970); diagnostic datasets: 44978, 44969, 44994, 44960, 44962, 45012, 44983.
* Primary method: SDLC-LS. Final implementation = v3 (cross-fitted standardisation, KDE+t2 noise density, harmonised floor, stratum-exact monotone-run geometry, half-open strata, D∩[0,∞)).
* Framing: main benchmark NOT called pre-registered; CTR23 size comparisons exploratory; confirmatory replication pre-registered (PREREGISTRATION_confirmatory.md, commit ccba99b, pushed before evaluation).

## Status (checkpoint 2026-11-21 ~12:00 UTC)
- [x] Review cycle 1 (REVIEW/review_01.md, 46 issues) → response REVIEW/response_01.md
- [x] v3 refit (raw_contexts_v3) + v3 evaluation 310/310 (results/raw_eval_v3), analysis scripts/analyze3.py → results/metrics_v3.json, statistics_v3.json, tables/T*, D*, figures/
- [x] Synthetic v3 (results/synthetic_v3.jsonl), Prop1 extension, tail-alert decision study (results/tail_alerts.jsonl), grid convergence
- [x] Confirmatory replication: fit 85/85, refit 85/85, eval 85/85; analyze_confirmatory.py (unchanged since pre-registration) → results/confirmatory/statistics_confirmatory.json. ALL hypotheses supported.
- [x] Manuscript revised (all src/*.md), renderer v3 context, supplementary builder (scripts/build_supplement.py), bibliography verified (agent), CSL URL fallback
- [x] Queue scripts/queue_cycle1b.sh complete: MLP v3 155/155, DenseWeight 93/93, grid, grouped splits 15/15 (resumed after container restart 2026-11-21), timing_fit, timing v3
- [x] analyze3 rerun; 04_results.md: MLP, DenseWeight, repeated units (grouped splits), computational cost; discussion limitation updated; supplement Tables S14 (grouped), S15 (fit times), earlier implementations now S16; DOCX/PDF/supplement rendered
- [x] ESWA comparison refreshed (REVIEW/final_comparison_eswa.md, 2026-11-21)
- [ ] Review cycle 2 = FINAL pre-submission cycle (user decision 2026-11-21: one full cycle, then submit). Running as workflow
      (code/scripts/review_cycle_workflow.js, args {cycle: 2, notes: final pre-submission focus}). Progress auto-synced every
      4 min to REVIEW/cycle02_progress/ (STATUS.md, <reviewer>.json = finished review, .partial.md = interrupted).
- [ ] Then: consolidate → REVIEW/review_02.md; implement fixes; REVIEW/response_02.md; REVIEW_HISTORY.md; re-render
      (code/scripts/render_manuscript.py, build_supplement.py, build_pdf.py); submit/not-submit verdict to the user.

### RESUME IN A NEW SESSION/ACCOUNT (review cycle 2)
1. Setup: `pip install --no-build-isolation -r code/requirements.txt` (data re-download needed only for build_supplement.py).
2. Read REVIEW/cycle02_progress/STATUS.md. Reviewers with a `.json` file are done — do NOT rerun them.
3. If REVIEW/review_02.md does not exist: run the workflow script with REVIEWERS reduced to the missing ones, then a
   consolidation agent over ALL JSON reviews in REVIEW/cycle02_progress/ (same prompt as in the script) → REVIEW/review_02.md.
4. If review_02.md exists: check REVIEW/response_02.md for the issues already handled and continue with the rest.

## Key results (machine-generated; see results/statistics_v3.json)
RQ1: marginal worst-stratum 0.63–0.78 (26–31/31 below null); stratified ≈0.89 (≤2/31 below null).
RQ2: price SDLC/DLS geo 1.24; SDLC at α=0.1 smaller than every marginal method at α=0.05 on 23–28/31 while covering tails better.
RQ3 (exploratory on CTR23): SDLC smaller than BCCP 0.902 (24/31), S-NCP 0.975 (27/31), S-CQR 0.795, S-HPD 0.947; gain mostly from 1/σ factor; costs: lower top-1% and σ-decile coverage, 0.4% empty sets.
Confirmatory (17 held-out): C-H1–C-H4 supported; size ratios BCCP 0.862, S-NCP 0.977, S-CQR 0.841, S-HPD 0.984 (Holm p ≤ 0.008).
Grouped splits: no change for sarcos/superconductivity; video_transcoding (by video) sets ~6x larger, per-split coverage variable (SDLC 0.79–0.94, mean 0.900), SDLC < S-NCP (0.88) but > BCCP (1.20).
RQ5: dedicated tail classifier (TC-LS) needs fewer alerts at the same recall guarantee; at cost ratio 10 no significant difference to SDLC.

## Resume instructions
If the container restarted: `pip install --no-build-isolation -r code/requirements.txt` (liac-arff fails to build otherwise); datasets re-download from OpenML into data/ (ARFF fallback, slow). Previously: check `ls results/raw_mlp_v3 | wc -l` (155), `results/raw_denseweight` (93), `results/raw_grouped` (15), `results/timing_*.csv`; re-launch `bash code/scripts/queue_cycle1b.sh` (all steps skip finished outputs except timing/grid, which are cheap).

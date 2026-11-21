# PROJECT_STATE (checkpoint file — updated after every major stage)

## Fixed decisions
* Target journal: Expert Systems with Applications (Elsevier) — see journal_selection/. ≤100-day acceptance NOT verifiable for any suitable journal (disclosed).
* Topic: stratified (target-conditional) conformal prediction for imbalanced regression; size-optimal score = conditional-density level sets per stratum (SDLC).
* Data: OpenML-CTR23 (suite 353), 31 of 35 datasets (exclusion: <20 distinct target values). Confirmatory: 17 held-out datasets (OpenML suites 335/336, config/confirmatory.json).
* Development datasets: airfoil (44957), concrete (44959), QSAR fish (44970); diagnostic datasets: 44978, 44969, 44994, 44960, 44962, 45012, 44983.
* Primary method: SDLC-LS. Final implementation = v3 (cross-fitted standardisation, KDE+t2 noise density, harmonised floor, stratum-exact monotone-run geometry, half-open strata, D∩[0,∞)).
* Framing: main benchmark NOT called pre-registered; CTR23 size comparisons exploratory; confirmatory replication pre-registered (PREREGISTRATION_confirmatory.md, commit ccba99b, pushed before evaluation).

## Status (checkpoint 2026-11-21)
- [x] Review cycle 1 (REVIEW/review_01.md, 46 issues) → response REVIEW/response_01.md
- [x] v3 refit (raw_contexts_v3) + v3 evaluation 310/310 (results/raw_eval_v3), analysis scripts/analyze3.py → results/metrics_v3.json, statistics_v3.json, tables/T*, D*, figures/
- [x] Synthetic v3 (results/synthetic_v3.jsonl), Prop1 extension, tail-alert decision study (results/tail_alerts.jsonl), grid convergence
- [x] Confirmatory replication: fit 85/85, refit 85/85, eval 85/85; analyze_confirmatory.py (unchanged since pre-registration) → results/confirmatory/statistics_confirmatory.json. ALL hypotheses supported.
- [x] Manuscript revised (all src/*.md), renderer v3 context, supplementary builder (scripts/build_supplement.py), bibliography verified (agent), CSL URL fallback
- [x] Queue complete (queue_cycle1b → resumed by queue_cycle1c/1d after two container restarts): MLP v3 155/155, DenseWeight 93/93, grid convergence, grouped splits 15/15, timing_fit 31/31, timing_methods_v3
- [x] analyze3 rerun; 04_results.md: MLP, DenseWeight, repeated units (grouped splits), computational cost; supplement Tables S13 (method timing), S14 (fit timing), S15 (grouped), S16 (earlier implementations); DOCX/PDF rendered
- [ ] Review cycles 2–10 (workflow), final comparison with strongest ESWA papers, final audit, rejection-risk report, READY/NOT READY decision, manifest

## Key results (machine-generated; see results/statistics_v3.json)
RQ1: marginal worst-stratum 0.63–0.78 (26–31/31 below null); stratified ≈0.89 (≤2/31 below null).
RQ2: price SDLC/DLS geo 1.24; SDLC at α=0.1 smaller than every marginal method at α=0.05 on 23–28/31 while covering tails better.
RQ3 (exploratory on CTR23): SDLC smaller than BCCP 0.902 (24/31), S-NCP 0.975 (27/31), S-CQR 0.795, S-HPD 0.947; gain mostly from 1/σ factor; costs: lower top-1% and σ-decile coverage, 0.4% empty sets.
Confirmatory (17 held-out): C-H1–C-H4 supported; size ratios BCCP 0.862, S-NCP 0.977, S-CQR 0.841, S-HPD 0.984 (Holm p ≤ 0.008).
Grouped splits: sarcos/superconductivity unchanged; video_transcoding by video: sets ×6.9 (SDLC), single-split coverage 0.79–0.96 → guarantees are row-level (reported).
Cost: SDLC 10.5 µs/test point (S-NCP 0.07); extra fits median 34% of S-NCP fit time, ≤3.6 s.
RQ5: dedicated tail classifier (TC-LS) needs fewer alerts at the same recall guarantee; at cost ratio 10 no significant difference to SDLC.

## Resume instructions
If the container restarted: check `ls results/raw_mlp_v3 | wc -l` (155), `results/raw_denseweight` (93), `results/raw_grouped` (15), `results/timing_*.csv`; all compute is finished. Environment: pip install -r code/requirements.txt fails on liac-arff (Debian setuptools); install the rest, copy arff.py from the liac-arff sdist into site-packages, then `pip install --no-deps openml==0.15.1` + its deps. Data download falls back to ARFF (slow for large confirmatory sets).

# PROJECT_STATE (checkpoint file — updated after every major stage)

## Fixed decisions
* Target journal (re-selected 2026-11-20): J. King Saud Univ. – Comput. Inf. Sci. (Springer Nature), JIF 6.4 (2025), measured median received→accepted 69 d (2026, n=988). ESWA archived (147–187 d too slow for ≤72-d ceiling).
* Topic: stratified (target-conditional) conformal prediction for imbalanced regression; size-optimal score = conditional-density level sets per stratum (SDLC).
* Data: OpenML-CTR23 (suite 353), 31 of 35 datasets (exclusion: <20 distinct target values). Confirmatory: 17 held-out datasets (OpenML suites 335/336, config/confirmatory.json).
* Development datasets: airfoil (44957), concrete (44959), QSAR fish (44970); diagnostic datasets: 44978, 44969, 44994, 44960, 44962, 45012, 44983.
* Primary method: SDLC-LS. Final implementation = v3 (cross-fitted standardisation, KDE+t2 noise density, harmonised floor, stratum-exact monotone-run geometry, half-open strata, D∩[0,∞)).
* Framing: main benchmark NOT called pre-registered; CTR23 size comparisons exploratory; confirmatory replication pre-registered (PREREGISTRATION_confirmatory.md, commit ccba99b, pushed before evaluation).

## Status (checkpoint 2026-11-20, session 3)
- [x] Review cycle 1 + v3 implementation + confirmatory replication (all pre-registered hypotheses supported)
- [x] MLP v3 (155/155), DenseWeight (93/93), grid convergence — done and integrated
- [x] JOURNAL RE-SELECTED (user ceiling: final acceptance ≤ 72 days, high IF, not MDPI): JKSU-CIS, Springer Nature.
      Evidence: journal_selection/selected_journal.md, journal_comparison.md, journal_verification.md, measure/*.py
      (Crossref census 2026: median 69 d, n=988). OUP JCDE measured 117.5 d (rejected). ESWA archived in journal_selection/archive_eswa/.
- [x] Manuscript adapted to JKSU-CIS house style (profile of 6 accepted papers): anonymised (double-blind) + manuscript/src/title_page.md;
      Springer author-year CSL (manuscript/build/springer-basic-author-date.csl); 6 keywords; abstract ≤250 words;
      "Statements and Declarations" AFTER References; Appendix before References; LLM use documented in §5.8 (required by journal);
      positioning table (tables/L1_positioning.csv, Table 1) at end of Related work; Algorithm 1 pseudocode; §4.5 Computational complexity;
      workflow figure F0 = Fig. 1; Conclusion and future work; cover letter re-addressed to JKSU-CIS; highlights archived (not required).
- [x] Grouped splits (15/15) + timing integrated (04_results.md "Grouped splits", "Computational cost"; Supp. Tables S13, S15, S16).
- [x] Review rounds 2-4 done: REVIEW/review_02.md (novelty: R2-01 FATAL "incremental"), review_03.md (statistics), review_04.md (method/code).
- [~] Fixes for review 3+4 delegated to a helper (it writes REVIEW/response_03_04.md and commits). CHECK `git log` — if response_03_04.md
      is missing, redo: fix every issue in review_03.md/review_04.md (scope: 02_theory, 03_setup, 04_results, 05_discussion, 09_appendix,
      analysis scripts; new confirmatory post-hoc analyses in a NEW script, never edit analyze_confirmatory.py).
- [~] NOVELTY FIX for R2-01 (user priority: no desk rejection): NEW METHOD RW-DLC (relevance-weighted density-level conformal prediction).
      Pre-registered in PREREGISTRATION_relevance_weighted.md (commit a9f31d2, BEFORE evaluation). Code: code/experiments/run_rw.py,
      test code/tests/test_rw_validity.py. Theory to add to 02_theory.md as a new subsection after "Two practical variants":
        Prop. 4 (validity): weighted split conformal with known relevance phi gives E[Cov_phi] >= 1-alpha (weighted exchangeability,
        Tibshirani et al. 2019; Podkopaev & Ramdas 2021); Cov_phi = E[phi(Y)1{covered}]/E[phi(Y)].
        Prop. 5 (oracle optimality): smallest sets with Cov_phi >= 1-alpha are {y: phi(y) f(y|x) >= t} (Neyman-Pearson; discrete analogue
        Bhattacharyya, Ding & Barber 2026). Score s = -phi(y) f_hat(y|x). q(y)=+inf iff phi(y) > alpha W/(1-alpha), W = sum of cal weights.
      Runs: `cd code && python experiments/run_rw.py confirmatory 4` (85 tasks -> results/rw/confirmatory) and, after contexts exist,
      `python experiments/run_rw.py ctr23 4` (310 tasks; needs results/raw_refit_contexts from
      `OMP_NUM_THREADS=1 python experiments/run_benchmark.py --mode fitonly --out ../results/raw_refit` — bit-identical to stored seed-0
      contexts; gitignored, ~2-3 h on 4 cores; skips nothing, so delete partial outputs only if corrupted). Both scripts skip finished outputs? run_rw yes.
      Early held-out result (19/85 runs, descriptive): RW-DLC-U Cov_phiU 0.898, top-1% coverage 0.898 (SDLC 0.70), size +24% vs SDLC;
      RW-DLC smaller than RW-DLS/RW-NCP. Then: write analysis script (tests exactly as pre-registered: RW-1 TOST margin 0.02, RW-2 Holm
      one-sided vs SCP/NCP/CQR/DLS-M, RW-3 top-1% vs SDLC one-sided, RW-4 size vs RW-DLS & RW-NCP two-sided Holm + geo CI), tables, figure.
- [ ] Manuscript restructure (my part, NOT done yet): new title (drop "size-optimal"), abstract/intro/contributions around TWO guarantees
      (per-stratum SDLC + relevance-weighted RW-DLC), Table 1 already rewritten (tables/L1_positioning.csv, includes RW-DLC row),
      cite new refs already in bib: ding2025longtailed, bhattacharyya2026macro, choi2026continuous, liu2025longtail, chzhen2021setvalued;
      address R2-02..R2-15; cut main text to ~11-12k words (move synthetic/sensitivity/error details to supplement); conclusion; cover letter.
- [ ] Review rounds 5-10 (R5 dataset validity/generalisation, R6 computation, R7 writing+JKSU-CIS guidelines, R8 competing researcher,
      R9 JKSU-CIS associate editor desk-reject test, R10 final adversarial), fix after each; response files REVIEW/response_XX.md.
- [ ] Final: render (python code/scripts/render_manuscript.py; build_supplement.py; build_pdf.py), REVIEW/final_audit.md,
      rejection-risk report, READY/NOT READY decision, file manifest, push.

## Environment note (fresh container)
pip install -r code/requirements.txt fails on liac-arff (setuptools bug). Workaround: install the other requirements, then
`pip install --no-deps openml==0.15.1 && pip install tqdm xmltodict minio requests python-dateutil`, and copy arff.py from the
liac-arff sdist (`pip download --no-deps --no-binary :all: liac-arff`) into site-packages. OpenML data download via ARFF fallback works.


## CHECKPOINT 2026-11-21 (session practical-sagan; branch claude/practical-sagan-qny271 = dreamy-albattani line + review-6 work)
Done this session: complexity/deployment text for RW-DLC (02_theory §Computational complexity); experiments/timing_like.py
(like-for-like SDLC/S-NCP/BCCP timing); scripts/analyze_timing.py (-> tables/D15c, D15d, results/timing_summary.json);
Supplementary Table S13 = (a) like-for-like timing, (b) RW timing/grid accuracy (build_supplement.py); g_at computes the
t tail only outside the table (bit-identical, tests/test_density_gat.py); timing_rw.py records peak memory.
Running when the session stopped (may have died with the container):
  queue scripts/queue_cycle3.sh (timing_rw -> CTR23 refit fitonly -> run_rw.py ctr23 4), then queue_cycle3b.sh
  (timing_like.py), then queue_cycle3c.sh (timing_rw.py rerun). Markers in results/experiment_logs/queue_cycle3.log.
  Review-5 reviewer agent (dataset validity) writing REVIEW/review_05.md — re-run it if the file is missing.
RESUME: check queue_cycle3.log; relaunch missing steps (all skip finished outputs except timings):
  cd code && OMP_NUM_THREADS=1 python3 experiments/run_benchmark.py --mode fitonly --out ../results/raw_refit
  && python3 experiments/run_rw.py ctr23 4 ; then (idle machine) python3 experiments/timing_like.py ; python3 experiments/timing_rw.py
Then: python3 scripts/analyze_timing.py; analyze_rw (CTR23 table D17_rw_ctr23) ; rewrite 04_results.md "*Computational cost.*"
paragraph with {{J:timing_summary.json|...}} placeholders (like.SDLC.pred_us_median, like.ratio_pred_sdlc_sncp, like.ratio_e2e_sdlc_sncp,
like.SDLC.single_p50_us_median, rw.RW-DLC.us_median, rw.ratio_rwdlc_sdlc_grid_median, rw.point_change_max, rw.mean_size_change_max),
cite Supplementary Table S13 only; add CTR23 RW sentence in RQ4; write REVIEW/response_06.md (issues 1-10; binned KDE for p_Y
declined for reported results = pre-specified implementation, noted as deployment option), response_05.md; reviews 8-10; final audit.
Env: deps install needs `pip install --ignore-installed setuptools; pip install --no-build-isolation liac-arff; pip install -r code/requirements.txt`;
cloud environment "p_c1_2" allows OpenML hosts.

## Key results (machine-generated; see results/statistics_v3.json)
RQ1: marginal worst-stratum 0.63–0.78 (26–31/31 below null); stratified ≈0.89 (≤2/31 below null).
RQ2: price SDLC/DLS geo 1.24; SDLC at α=0.1 smaller than every marginal method at α=0.05 on 23–28/31 while covering tails better.
RQ3 (exploratory on CTR23): SDLC smaller than BCCP 0.902 (24/31), S-NCP 0.975 (27/31), S-CQR 0.795, S-HPD 0.947; gain mostly from 1/σ factor; costs: lower top-1% and σ-decile coverage, 0.4% empty sets.
Confirmatory (17 held-out): C-H1–C-H4 supported; size ratios BCCP 0.862, S-NCP 0.977, S-CQR 0.841, S-HPD 0.984 (Holm p ≤ 0.008).
RQ5: dedicated tail classifier (TC-LS) needs fewer alerts at the same recall guarantee; at cost ratio 10 no significant difference to SDLC.

## Resume instructions
A new session should: read this file, `git log --oneline | head`, then check `ls results/raw_grouped | wc -l` (15 needed) and `ls results/timing_fit.csv results/timing_methods_v3.csv`; if incomplete, install deps (note above) and run `bash code/scripts/queue_cycle2.sh` in the background; then continue the unchecked items above in order.

## CHECKPOINT 2026-11-21 ~15:45 UTC (session zen-pasteur took over; branch claude/zen-pasteur-413mhs = practical-sagan + merge)
User asked THIS branch/session to lead; other sessions should be stopped. Compute: `bash code/scripts/resume_queue3.sh`
(from Target_Journal_Submission/; idempotent; markers REFIT_DONE, QUEUE3_DONE, QUEUE3B_DONE, QUEUE3C_DONE in
results/experiment_logs/queue_cycle3.log; refit skips finished tasks). Python: /root/venv/bin/python (cloud env "p_c1_2").
While it runs: analysis/writing items from the practical-sagan checkpoint above (response_05, response_06, reviews 8-10).

### Progress (zen-pasteur, 2026-11-21 evening)
- [x] Review 5 addressed: REVIEW/response_05.md (post hoc scripts/analyze_review05.py; leakage audit extended; supplement S1/S2/S3/S15/S17b).
      Open from review 5: temporal splits Moneyball/Bike (C1-31(d)) not run; CTR23 RW arm pending (queue 3).
- [ ] Queue 3 running (resume_queue3.sh): refit -> run_rw ctr23 -> timing_like -> timing_rw. Supplement S13 needs timing_like (D15c).
- [ ] Then: analyze_timing.py, analyze_rw.py (CTR23), response_06.md, RW CTR23 sentence in §6.4; reviews 8-10 (ask user re: agent cost); final audit.

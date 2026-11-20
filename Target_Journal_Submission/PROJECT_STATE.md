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
- [ ] RUNNING/NEXT: `bash code/scripts/queue_cycle2.sh` (grouped splits → results/raw_grouped, need 15 files; then timing_fit.py → results/timing_fit.csv;
      timing.py → results/timing_methods_v3.csv). Scripts skip finished grouped runs. Needs pip deps (see note below).
- [ ] Then: `cd code && python scripts/analyze3.py` and write the paragraph at the `<!-- GROUPED_TIMING -->` marker in manuscript/src/04_results.md
      (grouped-split robustness + measured runtimes; §4.5 already points to it). Every number via {{T:...}}/{{J:...}} placeholders only.
- [ ] Review rounds 2–10 (REVIEW/review_02.md … review_10.md), each a DIFFERENT focus as in the original brief (R2 novelty/prior art,
      R3 statistics/leakage, R4 ML method + code-vs-paper, R5 dataset validity/generalisation, R6 computation, R7 writing + JKSU-CIS guideline
      compliance, R8 competing researcher, R9 JKSU-CIS associate editor (desk-reject test), R10 final adversarial). Fix + rerun after each.
      USER PRIORITY: avoid desk/editor rejection for novelty or journal fit (reviewers there reject rather than ask for major revision).
- [ ] Final: render (python code/scripts/render_manuscript.py; code/scripts/build_pdf.py; code/scripts/build_supplement.py), REVIEW/final_audit.md,
      rejection-risk report, READY/NOT READY decision, file manifest, push.

## Environment note (fresh container)
pip install -r code/requirements.txt fails on liac-arff (setuptools bug). Workaround: install the other requirements, then
`pip install --no-deps openml==0.15.1 && pip install tqdm xmltodict minio requests python-dateutil`, and copy arff.py from the
liac-arff sdist (`pip download --no-deps --no-binary :all: liac-arff`) into site-packages. OpenML data download via ARFF fallback works.

## Key results (machine-generated; see results/statistics_v3.json)
RQ1: marginal worst-stratum 0.63–0.78 (26–31/31 below null); stratified ≈0.89 (≤2/31 below null).
RQ2: price SDLC/DLS geo 1.24; SDLC at α=0.1 smaller than every marginal method at α=0.05 on 23–28/31 while covering tails better.
RQ3 (exploratory on CTR23): SDLC smaller than BCCP 0.902 (24/31), S-NCP 0.975 (27/31), S-CQR 0.795, S-HPD 0.947; gain mostly from 1/σ factor; costs: lower top-1% and σ-decile coverage, 0.4% empty sets.
Confirmatory (17 held-out): C-H1–C-H4 supported; size ratios BCCP 0.862, S-NCP 0.977, S-CQR 0.841, S-HPD 0.984 (Holm p ≤ 0.008).
RQ5: dedicated tail classifier (TC-LS) needs fewer alerts at the same recall guarantee; at cost ratio 10 no significant difference to SDLC.

## Resume instructions
A new session should: read this file, `git log --oneline | head`, then check `ls results/raw_grouped | wc -l` (15 needed) and `ls results/timing_fit.csv results/timing_methods_v3.csv`; if incomplete, install deps (note above) and run `bash code/scripts/queue_cycle2.sh` in the background; then continue the unchecked items above in order.

# Review cycle 2 (token-light): one independent ESWA associate-editor/referee agent, 2026-11-21

Read: manuscript_filled.md (after the valuation case study was added), eswa_paper_benchmark.md §1/§3, review_01 action plan.

## Forecast (agent's estimate)
Desk reject ~20% · reject after review ~25% · major revision ~45% · minor/accept ~10%.
Desk-reject risks: read as a stats/ML-theory paper; length (~15k words); self-declared non-novelty of the
calibration device; visible author/URL placeholders.

## Main points and status
| # | Issue | Action | Status |
|---|---|---|---|
| 1 | Contribution hierarchy should lead with the problem evidence and the benchmark; qualify "smallest sets" (CIs vs S-NCP/S-HPD include 1) | abstract qualified ("on average", "intervals including one"); intro reframed around an auditable outcome-conditional requirement | done (abstract/intro); title unchanged |
| 2 | "Pre-registered ... public repository" vs "[repository URL] upon acceptance" | §5.7 now cites commit ccba99b and its timestamp; authors must give a public link (GitHub/Zenodo/OSF) before submission | partly (needs authors' URL) |
| 3 | Case study: one split, widths unreported, "two of the datasets are housing" wrong | 10-split top-stratum coverage with ranges, width relative to price, wording fixed | done |
| 4 | Shift claim "ordering unchanged" for ESS >= 50 false (DCP > BCCP, S-CQR) | corrected | done |
| 5 | Alert/cost claims too strong (SDLC alerts costlier than S-NCP at r=20; vs TC-LS n.s.) | discussion item 5 and Fig. 6 sentence tempered | done |
| 6 | Pre-empt "incremental": present S-NCP as the default when even coverage across noise levels matters | already in guidance item 3 | existing |
| 7 | Shorten to ~11–12k words (move Cor. 1(ii)-(iii), Remark, parts of §6.9 to supplement; merge §7.1 with conclusion) | not done | open |
| 8 | Slips: "p<= < 0.001", "compared with 13 procedures", BFQR defined twice, DLS-N undefined, TOST margin 0.01 vs 0.02 | all fixed (renderer post-processing; "evaluated among"; definition; margin justified) | done |
| opt | Faithful BFQR (level-optimised) or Kandinsky baseline on a subset | not done (new experiment) | open |

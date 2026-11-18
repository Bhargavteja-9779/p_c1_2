# REVIEW_HISTORY

Each cycle: 10 independent reviewer agents (novelty, methodology/theory, experimental design, statistics,
dataset/leakage, robustness, efficiency/reproducibility, literature, associate editor, hostile competitor) review the
rendered manuscript, code and results; a consolidation agent merges their reports into REVIEW/review_XX.md; fixes are
implemented with real computation where needed; the response is recorded in REVIEW/response_XX.md.

## Cycle 1 (2026-11-16/17)
* Reviewed: manuscript v2 (exact in-sample implementation), 38 pages.
* Consolidated issues: 46 (3 critical, 20 major, 16 moderate, 7 minor) — REVIEW/review_01.md.
* Main consequences: v3 estimator and geometry (all LS methods re-evaluated); confirmatory replication on 17 held-out
  datasets with a pushed pre-registration; decision study; misspecified synthetic designs; DenseWeight and MLP v3
  studies; grouped-split robustness; theory recast (Propositions 2–3, coverage-reallocation remark, credits);
  "pre-registered" framing removed for the main benchmark; supplementary material built; bibliography verified.
* Response: REVIEW/response_01.md (status per issue: fixed / partially / declined with reasons).
* Outcome of the confirmatory replication (pre-registered decision rules): all four hypotheses supported.

# Selected target journal (re-selection of 2026-11-20 under the ≤ 72-day acceptance constraint)

The earlier choice (Expert Systems with Applications, archived in `archive_eswa/`) was abandoned because its reported
submission-to-acceptance time (147–187 days, journal-page snapshots) violates the user's ceiling of 72 days.

| Field | Value (verification status) |
|---|---|
| TARGET JOURNAL | **Journal of King Saud University – Computer and Information Sciences (JKSU-CIS)** |
| PUBLISHER | Springer Nature (on behalf of King Saud University; moved from Elsevier in 2025). Journal page: https://link.springer.com/journal/44443 |
| ISSN | eISSN 2213-1248; print ISSN 1319-1578 ("listed for regulatory purposes") |
| JCR STATUS | Indexed in Science Citation Index Expanded (stated on the official Springer journal page). Clarivate JCR / Master Journal List could not be opened from this environment. |
| JCR QUARTILE | **Q1 in the 2024 JCR** according to King Saud University (news.ksu.edu.sa/en/node/145338, 29 June 2025) — owner-institution source, not Clarivate. 2025-JCR quartile: **UNVERIFIED**. |
| JOURNAL IMPACT FACTOR | **6.4 (2025)**, 5-year JIF 6.0 (official Springer journal page, read 2026-11-20) |
| JCR SUBJECT CATEGORY | **UNVERIFIED** (no primary source names it; Computer Science, Information Systems is plausible) |
| VERIFIED REVIEW/DECISION TIMELINE | No official decision-time statistics are published on the Springer page. |
| VERIFIED ACCEPTANCE TIMELINE | **Own measurement**: received→accepted dates deposited in Crossref for all 2026 articles: n = 988 dated, **median 69 days**, IQR 53–96 days, mean 77.3 days; 53.8 % accepted ≤ 72 days, 36.6 % ≤ 60 days (`measure/jksu_full.py`, `measure/jksu_cis_2026.csv`). Subset of 41 ML papers on regression/imbalance/uncertainty/calibration: median 63 days. This is the interval for *accepted* papers only; it says nothing about the time to a rejection and is **not a guarantee**: about half of accepted papers took longer than 72 days. |
| APC | Fully open access: GBP 1,590 / USD 2,090 / EUR 1,790 (+VAT where applicable); waivers for lowest-income countries |
| SCOPE FIT | Computer and information sciences broadly; 2026 issues contain ML methodology papers on imbalanced learning (SMOTE variants, class-overlap review, imbalanced SVMs), regression (monotonic gradient boosting, multi-target regression), and uncertainty quantification (conformal deep forest for classification, 10.1007/s44443-025-00175-3; quantile-regression ensembles for long-tailed small-sample prediction, 10.1007/s44443-026-01353-7). |
| RESEARCH FIT | Conformal prediction intervals for imbalanced regression extends two lines the journal already publishes (conformal UQ for classification; imbalanced/long-tailed learning). No 2024–2026 JKSU-CIS paper on conformal regression or prediction-interval benchmarks was found, so the paper is new to the journal without being outside its scope. |
| KEY AUTHOR GUIDELINES | Double-blind review (title page separate, anonymised manuscript); abstract 150–250 words; 4–6 keywords; decimal headings ≤ 3 levels; author–year references "(Thompson 1990)", alphabetical, with DOIs; "Statements and Declarations" after references: competing interests (mandatory), funding, data availability (mandatory for original research), author contributions (encouraged), ethics where applicable; use of LLMs must be documented in the Methods section; figure captions start with bold "Fig."; colour free; no length limit stated. |
| KEY REJECTION RISKS | (i) desk rejection as "too statistical/theoretical" for a computer-science journal → mitigated by a short, application-led introduction, an explicit algorithm box, complexity analysis, a decision study, and theory proofs moved to the appendix; (ii) novelty challenge (Mondrian/bin-conditional calibration is prior art) → contribution stated as score theory + method + 48-dataset evidence with a pre-registered replication, prior art credited up front; (iii) small gain over the strongest stratified baseline → reported openly; (iv) length (no limit, but reviewers' patience). |

## Constraint status
* ≤ 72-day acceptance: satisfied **as a median** for 2026 articles (69 days), measured independently from Crossref
  deposits; not guaranteed for any individual manuscript.
* Q1: supported by the owner institution for JCR 2024; the 2025 quartile could not be verified in Clarivate.
* "Oxford-like" publishers: the Oxford University Press candidate with matching scope (J. Computational Design and
  Engineering, JIF 6.8) was measured at a median of 117.5 days (n = 24, 0 % ≤ 72 days) and its own page states
  15 weeks submission→acceptance, so it fails the ceiling. No OUP, Elsevier-measurable, Wiley, T&F, IOP or IET title
  with suitable scope came close to 72 days (see `journal_comparison.md`).

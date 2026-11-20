# Journal comparison under the ≤ 72-day acceptance ceiling (2026-11-20)

Primary filter: **measured** median received→accepted interval (Crossref-deposited dates, 2026 articles, up to 400
per journal; script `measure/crossref_times.py`) or, for OUP, dates read from the article pages (n = 24). Elsevier
non-medical titles deposit no such dates and were judged from the journal-page snapshots documented in
`archive_eswa/`. JIF values: official publisher page where stated, otherwise from the earlier verification
(`archive_eswa/journal_comparison_eswa.md`); quartiles unverified unless stated.

| Journal (publisher) | JIF | Median rec→acc (days) | % ≤ 72 d | n | Scope fit | Decision |
|---|---|---|---|---|---|---|
| **J. King Saud Univ. – Comput. Inf. Sci. (Springer Nature)** | **6.4 (2025, official)** | **69** | **53.8** | 988 | Good (imbalanced learning, regression, UQ) | **SELECTED** |
| J. Computational Design and Engineering (OUP) | 6.8 (official) | 117.5 (page dates) | 0 | 24 | Medium (engineering design + ML) | Rejected: too slow; official 15 weeks |
| Expert Systems with Applications (Elsevier) | 9.4 | 147–187 (page snapshots) | n/a | — | Good | Rejected: too slow (previous choice) |
| Knowledge-Based Systems (Elsevier) | 8.0 | 155–158 (snapshots) | n/a | — | Good | Rejected: too slow |
| Pattern Recognition (Elsevier) | 9.1 | 206–250 (snapshots) | n/a | — | Good | Rejected |
| Scientific Reports (Springer Nature) | — | 121 | 15.9 | 391 | Medium | Rejected: slow; not Q1 in a CS category |
| Discover Artificial Intelligence (Springer) | — | 125 | 12.3 | 397 | Good | Rejected: slow; JCR status unclear |
| Int. J. Computational Intelligence Systems (Springer) | — | 137.5 | 14.2 | 394 | Good | Rejected: slow |
| Journal of Cheminformatics (Springer) | — | 131.5 | 7.5 | 186 | Partial (QSAR data only) | Rejected |
| Journal of Intelligent Information Systems (Springer) | — | 131 | 6.7 | 75 | Good | Rejected |
| Complex & Intelligent Systems (Springer) | — | 149 | 7.2 | 348 | Good | Rejected |
| Engineering with Computers (Springer) | — | 151 | 10.4 | 211 | Medium | Rejected |
| Expert Systems (Wiley) | — | 164.5 | 9.8 | 286 | Good | Rejected |
| Int. J. Intelligent Systems (Wiley/Hindawi) | — | 160.5 | 5.6 | 144 | Good | Rejected |
| CAAI Trans. Intelligence Technology (IET/Wiley) | — | 161 | 9.6 | 104 | Good | Rejected |
| Journal of Cloud Computing (Springer) | — | 165 | 25.1 | 191 | Weak | Rejected |
| Int. J. Data Science and Analytics (Springer) | — | 170.5 | 9.0 | 378 | Good | Rejected |
| Artificial Intelligence Review (Springer) | 13.9 (prior) | 188 | 4.8 | 294 | Weak (mainly surveys) | Rejected |
| Data Science and Engineering (Springer) | — | 188 | 10.2 | 49 | Good | Rejected |
| EPJ Data Science (Springer) | — | 188 | 2.8 | 106 | Weak | Rejected |
| Machine Learning (Springer) | 4.9 | 206 | 2.5 | 242 | Excellent | Rejected: slow |
| Connection Science (T&F) | — | 211 | 10.0 | 40 | Good | Rejected |
| Statistical Analysis and Data Mining (Wiley) | — | 219 | 0 | 62 | Excellent | Rejected |
| Applied Intelligence (Springer) | — | 238 | 1.8 | 389 | Good | Rejected |
| Data Mining and Knowledge Discovery (Springer) | 5.5 | 243 | 1.8 | 109 | Very good | Rejected |
| Neural Computing and Applications (Springer) | — | 246 | 1.5 | 389 | Good | Rejected |
| Journal of Big Data (Springer) | — | 257 | 1.3 | 236 | Good | Rejected |
| Int. J. Machine Learning and Cybernetics (Springer) | — | 288 | 0.8 | 399 | Good | Rejected |
| Cognitive Computation (Springer) | — | 290 | 7.1 | 127 | Weak | Rejected |
| Knowledge and Information Systems (Springer) | — | 292 | 2.1 | 287 | Good | Rejected |
| Journal of Applied Statistics (T&F) | — | 369 | 0 | 132 | Good | Rejected |
| Soft Computing (Springer) | — | 421.5 | 1.3 | 230 | Good | Rejected |
| Bioinformatics / Briefings in Bioinformatics / JAMIA (OUP) | 5.5 / 7.3 / 7.1 | 154 / 125 / 123 (PubMed, earlier) | ≤ 35 % ≤ 100 d | — | Out of scope | Rejected |

Not measurable and not chosen: Egyptian Informatics Journal, Big Data Research (Elsevier; no deposited dates; no
official timeline found), IEEE Transactions (no deposited dates; typically slow), Artificial Intelligence / JAIR
(no deposited dates). MDPI and IEEE Access were excluded by instruction.

**Result.** Among ≈ 35 reputable candidates, JKSU-CIS is the only journal with suitable scope whose measured median
acceptance time is within 72 days; it also has the highest verified JIF of the fast group. Its Q1 status rests on
the owner institution's report for JCR 2024.

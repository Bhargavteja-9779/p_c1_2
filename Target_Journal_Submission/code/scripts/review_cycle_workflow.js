export const meta = {
  name: 'tscp-review-cycle',
  description: 'One review cycle: 10 independent reviewer agents + consolidation for the SDLC manuscript',
  whenToUse: 'Run once per review-and-improvement cycle; args = {cycle: number, notes: string}',
  phases: [
    { title: 'Review', detail: '10 independent reviewer perspectives' },
    { title: 'Consolidate', detail: 'deduplicate vs history, prioritise, write REVIEW/review_XX.md' },
  ],
}

const BASE = '/home/user/p_c1_2/Target_Journal_Submission'
const cycle = (args && args.cycle) || 1
const notes = (args && args.notes) || ''
const pad = String(cycle).padStart(2, '0')

const COMMON = `You are an expert reviewer for the journal Expert Systems with Applications (Elsevier, JIF 9.4). Review cycle ${cycle}.
MATERIALS (read what you need; do NOT edit any file):
- Rendered manuscript with all numbers filled in: ${BASE}/manuscript/build/manuscript_filled.md (sources in ${BASE}/manuscript/src/*.md; every number comes from ${BASE}/manuscript/build/placeholder_values.json or a {{T:...}}/{{J:...}} lookup into tables/ and results/). Supplementary material: ${BASE}/manuscript/build/supplementary_filled.md. Highlights/cover letter: ${BASE}/manuscript/build/highlights_filled.md, cover_letter_filled.md.
- Code (final = v3): ${BASE}/code/ — src/methods/ls_exact3.py (exact location-scale sets, monotone-run geometry; _build_sets_ref = reference), src/methods/conformal.py, src/methods/strata.py, src/models/density.py (RobustLSDensity), src/models/learners.py, experiments/run_benchmark.py (fits), experiments/refit_scales.py (cross-fitted scales), experiments/evaluate_from_cache3.py (evaluation), experiments/synthetic3.py, experiments/tail_alerts.py, experiments/run_learner_generality3.py, experiments/run_denseweight.py, experiments/run_grouped.py, scripts/analyze3.py (all statistics/tables/figures), scripts/analyze_confirmatory.py, scripts/render_manuscript.py, tests/.
- Results: ${BASE}/results/metrics_v3.json, statistics_v3.json, per_dataset_main_v3.csv, raw_eval_v3/*.jsonl (one file per dataset x seed), synthetic_v3.jsonl, tail_alerts.jsonl, raw_mlp_v3/, confirmatory/ (statistics_confirmatory.json, raw_eval_v3/); tables in ${BASE}/tables/*.csv (D* are the printed tables); figures in ${BASE}/figures/*.png.
- Pre-registration of the confirmatory replication: ${BASE}/PREREGISTRATION_confirmatory.md (committed in git commit ccba99b before any confirmatory evaluation; check with git log if you wish).
- History: ${BASE}/EXPERIMENT_LOG.md, ${BASE}/REVIEW_HISTORY.md, previous consolidated reviews ${BASE}/REVIEW/review_*.md and responses ${BASE}/REVIEW/response_*.md (what was fixed and how), ${BASE}/supplementary/literature_matrix.md, ${BASE}/supplementary/references_verified.bib, ${BASE}/journal_selection/selected_journal.md.
RULES: Be hostile but scientifically fair. Find NEW problems or inadequate fixes (check the previous responses: re-raise an issue only if the fix is inadequate, saying why). Every issue must cite concrete evidence (file and line, table, number, or code location) and propose a precise, feasible corrective action; say if a new experiment is required and describe it exactly. Do not invent problems to reach a count; report only real ones; if the manuscript is ready, say so. Never fabricate numbers: if you compute something, say how (you may run read-only Python on the result files; do not start long computations, never modify files). ${notes}`

const ISSUE_SCHEMA = {
  type: 'object',
  properties: {
    reviewer: { type: 'string' },
    recommendation: { type: 'string', enum: ['accept', 'minor revision', 'major revision', 'reject'] },
    summary: { type: 'string' },
    issues: {
      type: 'array',
      items: {
        type: 'object',
        properties: {
          severity: { type: 'string', enum: ['fatal', 'critical', 'major', 'moderate', 'minor'] },
          title: { type: 'string' },
          evidence: { type: 'string' },
          corrective_action: { type: 'string' },
          new_experiment: { type: 'string' },
        },
        required: ['severity', 'title', 'evidence', 'corrective_action'],
      },
    },
  },
  required: ['reviewer', 'recommendation', 'summary', 'issues'],
}

const REVIEWERS = [
  { key: 'R1-novelty', lens: 'AGENT 1 - NOVELTY AND PRIOR-ART REVIEWER. Search the web (WebSearch/WebFetch, arXiv API, Crossref) for papers, preprints or packages that already propose: stratified/bin-conditional/label-conditional conformal regression, density-level-set scores with stratum-specific thresholds, optimality results for set size under class/stratum-specific coverage, floor-type dual guarantees, target-shift robustness of Mondrian CP. Try to invalidate every novelty claim in the abstract, introduction contributions and conclusion. Check that the paper credits BCCP, BFQR, Mondrian theory, Sadinle et al., Kandinsky CP accurately.' },
  { key: 'R2-methodology', lens: 'AGENT 2 - METHODOLOGY REVIEWER. Check mathematical correctness of Proposition 1, Theorem 1, Corollary 1, Propositions 2-3 (new asymptotic optimality result) and the coverage-reallocation remark, and every proof in Appendix A; consistency between the equations and the implementation in code/src/methods/ls_exact3.py, conformal.py, strata.py and density.py (score definition, out-of-domain handling, infinite thresholds, tie handling, monotone-run geometry vs the reference implementation, cross-fitted standardisation, defensive t component, scale floor).' },
  { key: 'R3-experimental-design', lens: 'AGENT 3 - EXPERIMENTAL DESIGN REVIEWER. Check fairness of the comparison (identical base models, no method-specific tuning, same cached outputs), choice and faithfulness of baselines (BCCP, S-NCP, S-CQR, S-HPD, CQR, HPD-split, DCP, Mondrian-yhat, dedicated tail classifiers and conformal selection in the decision study), whether any strong baseline is missing, the split protocol, the strata design, metrics, the protocol section (what was fixed in advance), and whether the confirmatory replication was run and analysed exactly as pre-registered (compare PREREGISTRATION_confirmatory.md, scripts/analyze_confirmatory.py and the reported results).' },
  { key: 'R4-statistics', lens: 'AGENT 4 - STATISTICAL REVIEWER. Check the unit of analysis, Wilcoxon signed-rank tests, one-sided vs two-sided choices, Holm families, effect sizes, bootstrap confidence intervals, geometric-mean ratios vs Hodges-Lehmann vs sign tests (do they agree?), TOST equivalence, multiple comparisons across metrics, the null reference for worst-stratum coverage, the pre-registered confirmatory analysis, and whether every claim of significance in the text matches statistics_v3.json / statistics_confirmatory.json exactly.' },
  { key: 'R5-data-leakage', lens: 'AGENT 5 - DATASET AND LEAKAGE REVIEWER. Check dataset validity and licensing (data/*.json, tables/S2_leakage_audit.csv), duplicates across splits, target discreteness/ties (strata merging, realised K), zero-inflation (forest fires), out-of-domain targets, whether strata/grids/models use training data only (inspect code), whether calibration labels leak into any modelling choice, and whether the exclusion rule is applied as stated.' },
  { key: 'R6-robustness', lens: 'AGENT 6 - ROBUSTNESS AND GENERALIZATION REVIEWER. Try to show the method fails: small calibration sets (infinite thresholds), very skewed or zero-inflated targets, alpha levels, number of strata, calibration fraction, target shift (positive control, tilts, synthetic genuine label shift), a second learner family (MLP), misspecified synthetic designs, held-out datasets. Identify the conditions where SDLC is worse than BCCP or S-NCP and check that the manuscript reports them honestly; propose additional stress tests if essential.' },
  { key: 'R7-efficiency', lens: 'AGENT 7 - COMPUTATIONAL EFFICIENCY REVIEWER. Check the cost claims of Algorithm 1 (number of model fits, FFT-KDE, O(K R log G) monotone-run geometry), the equivalence test of the fast geometry against the reference (tests/test_ls_exact3.py), grid convergence (results/grid_convergence.json), timing results if present (results/timing_*.csv), scalability to large n and to deployment; whether the extra cost of density estimation is justified by the gains; whether timing measurements are fair (single thread, same hardware).' },
  { key: 'R8-literature', lens: 'AGENT 8 - LITERATURE AND CITATION REVIEWER. Verify that every [@key] used in manuscript/src/*.md exists in references_verified.bib and that the attributed claims match the literature matrix descriptions; check DOI/venue/year formatting in the bib entries actually cited; identify important missing competing studies (search the web if needed) and misrepresentations of prior work; check that no reference is cited that was flagged as unverified.' },
  { key: 'R9-associate-editor', lens: 'AGENT 9 - ASSOCIATE EDITOR OF EXPERT SYSTEMS WITH APPLICATIONS. Evaluate scope fit (intelligent/expert systems and their applications), novelty relative to the journal standard (see supplementary/eswa_paper_benchmark.md), clarity, length, structure, abstract (<=250 words), highlights (3-5 bullets, <=85 characters each), keywords (1-7), declarations, data/code availability, figure and table quality, reproducibility package, and likely desk-rejection risks. Give an explicit desk-reject probability judgement with reasons.' },
  { key: 'R10-hostile-competitor', lens: 'AGENT 10 - HOSTILE COMPETING RESEARCHER (e.g. an author of BCCP). Try to show the work is incremental or unnecessary: that simple BCCP or S-NCP achieves the same results; that gains are caused by the location-scale model rather than the theory; that the implementation changes after earlier results favour the proposed method (check the confirmatory replication and Supplementary Table S16); that the benchmark favours the method; that the size metric or strata choice is cherry-picked. Use the raw results to check whether the claimed advantages survive alternative summaries (medians, per-dataset win counts, excluding development datasets, alpha=0.05/0.2).' },
]

phase('Review')
const reviews = await parallel(REVIEWERS.map(r => () =>
  agent(`${COMMON}\n\nYOUR ROLE: ${r.lens}\nReturn your full review via the structured output.`,
    { label: `cycle${cycle}:${r.key}`, phase: 'Review', schema: ISSUE_SCHEMA, effort: 'high' })))
const got = reviews.filter(Boolean)
log(`cycle ${cycle}: ${got.length}/10 reviews returned`)

phase('Consolidate')
const consolidated = await agent(`You consolidate review cycle ${cycle} of the SDLC manuscript (Expert Systems with Applications). Below are ${got.length} independent reviews as JSON. Also read ${BASE}/REVIEW_HISTORY.md (issues raised and fixed in earlier cycles).
TASKS: (1) Merge duplicate issues across reviewers (keep the independent supporting arguments and list which reviewers raised each). (2) Mark issues that repeat an already-fixed issue as 'repeat' unless the reviewer argues the fix is inadequate. (3) Assign final priority: fatal, critical, major, moderate, minor. (4) For each issue give a precise corrective action and whether it needs a new experiment, a re-analysis, a code fix or only text changes. (5) Write the consolidated review to ${BASE}/REVIEW/review_${pad}.md with sections: Summary of recommendations (reviewer -> recommendation), Fatal/Critical, Major, Moderate, Minor, Repeats, and an 'Action plan' table (id, priority, action type, files). Use issue ids C${cycle}-01, C${cycle}-02, ... Do not edit any other file. Return the action plan as plain text.

REVIEWS JSON:
${JSON.stringify(got)}`, { label: `cycle${cycle}:consolidate`, phase: 'Consolidate', effort: 'high' })

return { cycle, n_reviews: got.length, recommendations: got.map(r => `${r.reviewer}: ${r.recommendation}`), consolidated }

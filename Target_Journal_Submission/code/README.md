# Target-stratified conformal prediction for imbalanced regression

Code, configuration and raw results for the manuscript
*"Target-stratified conformal prediction for imbalanced regression: finite-sample coverage for rare and extreme outcomes"*
(submitted to *Expert Systems with Applications*).

The method (SDLC, stratified density-level conformal prediction) calibrates a separate conformal
threshold within each stratum of the **target** (e.g. lower tail / bulk / upper tail). Every candidate
value `y` is tested against the threshold of *its own* stratum, which yields finite-sample coverage
*conditional on the target stratum* — i.e. guaranteed coverage of rare/extreme outcomes — and
robustness to shifts of the target distribution. The conformity score is a conditional density
estimate, which is the size-optimal choice (Theorem 2 of the paper).

## 1. Installation

```bash
python -m venv .venv && source .venv/bin/activate   # Python 3.13 was used
pip install -r requirements.txt                      # exact versions used for the paper
# or: conda env create -f environment.yml
```
Everything runs on CPU (LightGBM, scikit-learn). No GPU, CUDA or Apple MPS is required.

## 2. Data

All data are public and downloaded automatically from OpenML (suite 353, *OpenML-CTR23*,
Fischer, Feurer & Bischl 2023):
```bash
python src/data/openml_ctr23.py      # caches ../data/<id>.parquet (+ metadata json)
```
The 31 datasets used and the exclusion rule (targets with < 20 distinct values) are listed in
`config/benchmark.json`. Licences are recorded in each `data/<id>.json` (CC BY 4.0, CC0, public,
GPL ≥ 2, or non-commercial scholarly use for `socmob`).

## 3. Reproducing the study

```bash
python run_all.py --mode quick   # ~1 min: unit tests + 3 development datasets, 1 seed
python run_all.py --mode full    # complete study (~3–4 h on 4 CPU cores)
```
`--mode full` runs, in order:

| Step | Script | Output |
|---|---|---|
| unit tests (validity by Monte Carlo, partition nesting, supersets) | `tests/` | — |
| data download | `src/data/openml_ctr23.py` | `../data/` |
| main benchmark (31 datasets × 10 seeds × α∈{0.05,0.1,0.2}, sensitivity analyses) | `experiments/run_benchmark.py` | `../results/raw/*.jsonl` |
| learner generality (MLP base models, 5 seeds) | `experiments/run_learner_generality.py` | `../results/raw_mlp/` |
| Proposition 1 (analytic + Monte Carlo) | `experiments/prop1_gaussian.py` | `../results/prop1_gaussian.json` |
| synthetic study with known density (Theorem 2) | `experiments/synthetic.py` | `../results/synthetic.jsonl` |
| leakage/duplicate audit | `scripts/leakage_audit.py` | `../tables/S2_leakage_audit.*` |
| statistics, tables, figures | `scripts/analyze.py`, `scripts/analyze_extra.py`, `scripts/figures_extra.py` | `../results/*.json`, `../tables/`, `../figures/` |
| manuscript numbers + DOCX | `scripts/render_manuscript.py` | `../manuscript/` |

Runs are checkpointed: each `(dataset, seed)` is one JSON-lines file and existing files are skipped,
so an interrupted run resumes where it stopped. Individual pieces can be run alone, e.g.
`python experiments/run_benchmark.py --datasets 44977 --seeds 0 1`.

**Every number in the manuscript** is inserted by `scripts/render_manuscript.py` from
`results/metrics.json`, `results/statistics.json`, `results/statistics_extra.json` and `tables/*.csv`;
the build aborts if any placeholder cannot be resolved. `manuscript/build/placeholder_values.json`
lists each inserted value.

## 4. Repository layout

```
config/benchmark.json        pre-registered configuration (datasets, seeds, splits, alphas, grids)
src/data/                    OpenML loader
src/methods/strata.py        target strata and the evaluation grid (from training targets only)
src/methods/conformal.py     all conformal procedures (marginal and stratified)
src/models/learners.py       LightGBM base learners (identical for all methods)
src/models/density.py        histogram and location-scale conditional densities, HPD, CDF
src/evaluation/metrics.py    coverage, stratum coverage, size, components, worst-slab coverage
src/statistics/tests.py      Wilcoxon/Holm/rank-biserial/bootstrap/Friedman/Nemenyi
experiments/                 benchmark, learner generality, Proposition 1, synthetic study
scripts/                     analysis, figures, leakage audit, manuscript rendering
tests/                       unit and Monte-Carlo validity tests
```

## 5. Using the method on your own data

```python
from src.methods.strata import make_partition
from src.models import density as D
from src.methods import conformal as C
part = make_partition(y_train)                     # strata at training quantiles .1,.25,.75,.9
lsd = D.LocationScaleDensity(part, z_oof)          # z_oof: OOF standardised residuals
Fc, Ft = lsd.cells(mu_cal, sd_cal), lsd.cells(mu_test, sd_test)
S = C.mask_method(-D.at(Fc, y_cal, part), Ft, alpha=0.1, part=part,
                  strata_cal=part.stratum(y_cal))  # boolean mask over grid cells
```
See `experiments/run_benchmark.py::fit_context` for the complete fitting pipeline.

## 6. Determinism

Seeds 0–9 are fixed in the configuration; splits, model seeds and sub-sampling seeds are derived from
them. LightGBM is run single-threaded per task (`n_jobs_per_task = 1`), which makes results
bit-reproducible on the same platform; different CPU architectures or library versions may produce
tiny numerical differences in the gradient-boosting models.

## 7. Licence
Code: MIT. Data: see the licence of each OpenML dataset.

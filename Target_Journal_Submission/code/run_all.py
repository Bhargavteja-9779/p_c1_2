"""One-command reproduction of every number, table and figure in the manuscript and supplement.

    python run_all.py --mode quick   # a few minutes: unit tests + full v3 pipeline on 3 development datasets, seed 0
    python run_all.py --mode full    # complete study (about 6-8 h on 4 CPU cores)

Full mode, in order (completed units are cached and skipped, so an interrupted run resumes):
  1. unit tests (validity Monte Carlo, exact geometry vs reference, interval rules)
  2. download/cache OpenML-CTR23 (suite 353) and the confirmatory datasets (suites 335/336)
  3. fit all base models once per dataset x seed                 -> results/raw, results/raw_contexts
  4. cross-fitted scale models for the noise density (v3)        -> results/raw_contexts_v3
  5. evaluate every conformal method from the cached outputs     -> results/raw_eval_v3
  6. Proposition 1 (analytic + Monte Carlo extensions), synthetic study, tail-alert decision study,
     MLP and DenseWeight learner studies, grid convergence, grouped splits, timing, leakage audit
  7. confirmatory replication (fit, refit, evaluate, pre-registered analysis)  -> results/confirmatory
  8. statistics, tables and figures (scripts/analyze3.py, scripts/figures_extra.py)
  9. manuscript DOCX/PDF, highlights, cover letter and supplementary material, every number filled from files
No GPU is required; hardware is detected only to report it.
"""
from __future__ import annotations

import argparse
import os
import platform
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TOP = ROOT.parent


def hw():
    info = {"python": sys.version.split()[0], "platform": platform.platform(), "cpus": os.cpu_count()}
    try:
        import torch
        info["cuda"] = torch.cuda.is_available()
        info["mps"] = bool(getattr(torch.backends, "mps", None) and torch.backends.mps.is_available())
    except ImportError:
        info["cuda"] = info["mps"] = "torch not installed (not required)"
    return info


def sh(*args, env=None):
    print("+", " ".join(args), flush=True)
    subprocess.run([sys.executable, *args], cwd=ROOT, check=True, env={**os.environ, **(env or {})})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["quick", "full"], default="quick")
    ap.add_argument("--workers", type=int, default=min(4, os.cpu_count() or 1))
    a = ap.parse_args()
    print("hardware:", hw())
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    sh("-m", "pytest", "-q", "tests")
    w = str(a.workers)
    if a.mode == "quick":
        q = TOP / "results_quick"
        env = {"TSCP_CACHE_DIR": str(q / "raw_contexts"), "TSCP_CACHE3_DIR": str(q / "raw_contexts_v3"),
               "TSCP_EVAL_DIR": str(q / "raw_eval_v3"), "TSCP_OUT_ROOT": str(q / "analysis")}
        sh("experiments/run_benchmark.py", "--mode", "fitonly", "--datasets", "44957", "44959", "44970",
           "--seeds", "0", "--workers", w, "--out", str(q / "raw"))
        sh("experiments/refit_scales.py", w, env=env)
        sh("experiments/evaluate_from_cache3.py", w, env=env)
        sh("scripts/analyze3.py", str(q / "raw_eval_v3"), env=env)
        print("quick mode finished: see", q / "analysis")
        return
    conf = {"TSCP_CONFIG": "confirmatory.json", "TSCP_NMAX": "50000",
            "TSCP_CACHE_DIR": str(TOP / "results" / "confirmatory" / "raw_contexts"),
            "TSCP_CACHE3_DIR": str(TOP / "results" / "confirmatory" / "raw_contexts_v3"),
            "TSCP_EVAL_DIR": str(TOP / "results" / "confirmatory" / "raw_eval_v3")}
    sh("src/data/openml_ctr23.py")
    sh("experiments/run_benchmark.py", "--mode", "fitonly", "--workers", w)
    sh("experiments/refit_scales.py", w)
    sh("experiments/evaluate_from_cache3.py", w)
    sh("experiments/prop1_gaussian.py")
    sh("experiments/prop1_extension.py")
    sh("experiments/synthetic3.py", w)
    sh("experiments/tail_alerts.py", w)
    sh("experiments/run_learner_generality3.py")
    sh("experiments/run_denseweight.py")
    sh("experiments/grid_convergence.py")
    sh("experiments/run_grouped.py", w)
    sh("experiments/timing_fit.py")
    sh("experiments/timing.py")
    sh("scripts/leakage_audit.py")
    sh("experiments/run_benchmark.py", "--mode", "fitonly", "--workers", w,
       "--out", str(TOP / "results" / "confirmatory" / "raw"), env=conf)
    sh("experiments/refit_scales.py", w, env=conf)
    sh("experiments/evaluate_from_cache3.py", w, env=conf)
    sh("scripts/analyze_confirmatory.py")
    sh("scripts/analyze3.py")
    sh("scripts/figures_extra.py", "f0", "f1", "f9")
    sh("scripts/render_manuscript.py")
    sh("scripts/build_pdf.py")
    sh("scripts/build_supplement.py")


if __name__ == "__main__":
    main()

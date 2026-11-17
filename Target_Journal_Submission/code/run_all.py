"""One-command reproduction of every number, table and figure in the manuscript.

    python run_all.py --mode quick   # ~2 min: unit tests + pipeline on 3 development datasets, seed 0
    python run_all.py --mode full    # complete study (~4-5 h on 4 CPU cores)

Full mode, in order:
 1. unit tests (incl. Monte-Carlo validity checks)
 2. download/cache OpenML-CTR23 (suite 353)
 3. fit all base models once per dataset x seed and cache their outputs   (results/raw, results/raw_contexts)
 4. evaluate every conformal method from the cached outputs                (results/raw_eval)
 5. learner-generality study with an MLP                                   (results/raw_mlp)
 6. Proposition 1 verification, synthetic oracle study, timing experiment, leakage audit
 7. statistics, tables, figures (scripts/analyze*.py, scripts/figures_extra.py)
 8. manuscript DOCX/PDF, highlights and cover letter with every number filled from the result files
Completed units are cached and skipped, so an interrupted run resumes where it stopped.
Optional: --with-v1 also re-runs the archived pre-registered (fixed-grid) implementation.
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
    ap.add_argument("--with-v1", action="store_true", help="also re-run the pre-registered fixed-grid run")
    a = ap.parse_args()
    print("hardware:", hw())
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    sh("-m", "pytest", "-q", "tests")
    w = str(a.workers)
    if a.mode == "quick":
        q = TOP / "results_quick"
        env = {"TSCP_CACHE_DIR": str(q / "raw_contexts"), "TSCP_EVAL_DIR": str(q / "raw_eval"),
               "TSCP_FIT_DIR": str(q / "raw"), "TSCP_OUT_ROOT": str(q / "analysis")}
        sh("experiments/run_benchmark.py", "--mode", "fitonly", "--datasets", "44957", "44959", "44970",
           "--seeds", "0", "--workers", w, "--out", str(q / "raw"))
        sh("experiments/evaluate_from_cache.py", w, env=env)
        sh("scripts/analyze.py", str(q / "raw_eval"), env=env)
        print("quick mode finished: see", q / "analysis")
        return
    sh("src/data/openml_ctr23.py")
    sh("experiments/run_benchmark.py", "--mode", "fitonly", "--workers", w)
    sh("experiments/evaluate_from_cache.py", w)
    sh("experiments/run_learner_generality.py", "0", "1", "2", "3", "4")
    sh("experiments/prop1_gaussian.py")
    sh("experiments/synthetic.py", "10")
    sh("experiments/timing.py")
    sh("scripts/leakage_audit.py")
    if a.with_v1:
        sh("experiments/run_benchmark.py", "--mode", "full", "--workers", w,
           "--out", str(TOP / "results" / "raw_v1_rerun"))
    sh("scripts/analyze.py")
    sh("scripts/analyze_extra.py")
    sh("scripts/figures_extra.py")
    sh("scripts/render_manuscript.py")
    sh("scripts/build_pdf.py")


if __name__ == "__main__":
    main()

"""One-command reproduction.

    python run_all.py --mode quick   # ~1 min: 3 development datasets, 1 seed, pipeline check
    python run_all.py --mode full    # full study (~3-4 h on 4 CPU cores)

Full mode: downloads the OpenML-CTR23 datasets, runs the main benchmark (31 datasets x 10
seeds x 3 alpha levels), the MLP learner-generality study, Proposition 1 verification, the
synthetic oracle study, the leakage audit, then regenerates every table and figure and the
numbers inserted into the manuscript. Completed runs are cached in results/raw*/ and skipped.
No CUDA/MPS is needed; all models run on CPU (LightGBM/scikit-learn). Hardware is detected
only to report it in the log.
"""
from __future__ import annotations

import argparse
import os
import platform
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def hw():
    info = {"python": sys.version.split()[0], "platform": platform.platform(), "cpus": os.cpu_count()}
    try:
        import torch
        info["cuda"] = torch.cuda.is_available()
        info["mps"] = bool(getattr(torch.backends, "mps", None) and torch.backends.mps.is_available())
    except ImportError:
        info["cuda"] = info["mps"] = "torch not installed (not required)"
    return info


def sh(*args):
    print("+", " ".join(args), flush=True)
    subprocess.run([sys.executable, *args], cwd=ROOT, check=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--mode", choices=["quick", "full"], default="quick")
    ap.add_argument("--workers", type=int, default=min(4, os.cpu_count() or 1))
    a = ap.parse_args()
    print("hardware:", hw())
    os.environ.setdefault("OMP_NUM_THREADS", "1")
    sh("-m", "pytest", "-q", "tests")
    if a.mode == "quick":
        sh("experiments/run_benchmark.py", "--mode", "quick", "--workers", str(a.workers))
        sh("scripts/analyze.py", str(ROOT.parent / "results" / "raw_quick"))
        return
    sh("src/data/openml_ctr23.py")
    sh("experiments/run_benchmark.py", "--mode", "full", "--workers", str(a.workers))
    sh("experiments/run_learner_generality.py")
    sh("experiments/prop1_gaussian.py")
    sh("experiments/synthetic.py", "10")
    sh("scripts/leakage_audit.py")
    sh("scripts/analyze.py")
    sh("scripts/analyze_extra.py")
    sh("scripts/figures_extra.py")
    sh("scripts/render_manuscript.py")


if __name__ == "__main__":
    main()

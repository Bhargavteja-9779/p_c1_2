#!/bin/bash
# Sequential compute queue for review-cycle-1 experiments (keeps 4 cores busy).
cd "$(dirname "$0")/.."
LOG=../results/experiment_logs
export OMP_NUM_THREADS=1
while pgrep -f evaluate_from_cache3 >/dev/null; do sleep 30; done
python3 experiments/synthetic3.py 4 > $LOG/synthetic_v3.log 2>&1
TSCP_CONFIG=confirmatory.json TSCP_NMAX=50000 python3 experiments/run_benchmark.py --mode fitonly --workers 4 --out ../results/confirmatory/raw > $LOG/confirmatory_fit.log 2>&1
TSCP_CONFIG=confirmatory.json TSCP_NMAX=50000 TSCP_CACHE_DIR=../results/confirmatory/raw_contexts TSCP_CACHE3_DIR=../results/confirmatory/raw_contexts_v3 python3 experiments/refit_scales.py 4 > $LOG/confirmatory_refit.log 2>&1
python3 experiments/run_learner_generality3.py > $LOG/mlp_v3.log 2>&1
python3 experiments/run_denseweight.py > $LOG/denseweight.log 2>&1
python3 experiments/grid_convergence.py > $LOG/grid_convergence.log 2>&1
python3 experiments/timing_fit.py > $LOG/timing_fit.log 2>&1
python3 experiments/timing.py > $LOG/timing_v3.log 2>&1
echo QUEUE_DONE >> $LOG/queue_cycle1.log

#!/bin/bash
# Sequential compute queue (replaces the tail of queue_cycle1.sh so that the confirmatory evaluation runs
# directly after the confirmatory fits).
cd "$(dirname "$0")/.."
LOG=../results/experiment_logs
export OMP_NUM_THREADS=1
while pgrep -f "run_benchmark.py --mode fitonly" >/dev/null; do sleep 30; done
TSCP_CONFIG=confirmatory.json TSCP_NMAX=50000 TSCP_CACHE_DIR=../results/confirmatory/raw_contexts TSCP_CACHE3_DIR=../results/confirmatory/raw_contexts_v3 python3 experiments/refit_scales.py 4 > $LOG/confirmatory_refit.log 2>&1
TSCP_CONFIG=confirmatory.json TSCP_NMAX=50000 TSCP_CACHE_DIR=../results/confirmatory/raw_contexts TSCP_CACHE3_DIR=../results/confirmatory/raw_contexts_v3 TSCP_EVAL_DIR=../results/confirmatory/raw_eval_v3 python3 experiments/evaluate_from_cache3.py 4 > $LOG/confirmatory_eval.log 2>&1
echo CONFIRMATORY_EVAL_DONE >> $LOG/queue_cycle1b.log
python3 experiments/run_learner_generality3.py > $LOG/mlp_v3.log 2>&1
python3 experiments/run_denseweight.py > $LOG/denseweight.log 2>&1
python3 experiments/grid_convergence.py > $LOG/grid_convergence.log 2>&1
python3 experiments/run_grouped.py 4 > $LOG/grouped.log 2>&1
python3 experiments/timing_fit.py > $LOG/timing_fit.log 2>&1
python3 experiments/timing.py > $LOG/timing_v3.log 2>&1
echo QUEUE_DONE >> $LOG/queue_cycle1b.log

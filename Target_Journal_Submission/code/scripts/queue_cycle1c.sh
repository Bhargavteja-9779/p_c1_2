#!/bin/bash
# Resume of queue_cycle1b.sh after a container restart (2026-11-21): the remaining steps only.
# run_grouped.py skips finished outputs; timing steps run alone (no concurrent jobs).
cd "$(dirname "$0")/.."
LOG=../results/experiment_logs
export OMP_NUM_THREADS=1
python3 experiments/run_grouped.py 4 >> $LOG/grouped.log 2>&1
echo GROUPED_DONE >> $LOG/queue_cycle1b.log
python3 experiments/timing_fit.py > $LOG/timing_fit.log 2>&1
echo TIMING_FIT_DONE >> $LOG/queue_cycle1b.log
python3 experiments/timing.py > $LOG/timing_v3.log 2>&1
echo QUEUE_DONE >> $LOG/queue_cycle1b.log

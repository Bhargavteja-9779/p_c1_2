#!/bin/bash
# Second resume after a container restart (2026-11-21): fit timing (resumes per dataset), then method timing.
cd "$(dirname "$0")/.."
LOG=../results/experiment_logs
export OMP_NUM_THREADS=1
python3 experiments/timing_fit.py >> $LOG/timing_fit.log 2>&1
echo TIMING_FIT_DONE >> $LOG/queue_cycle1b.log
python3 experiments/timing.py > $LOG/timing_v3.log 2>&1
echo QUEUE_DONE >> $LOG/queue_cycle1b.log

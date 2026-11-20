#!/bin/bash
# Remaining compute of cycle 1b (container was recycled): grouped splits, timing.
cd "$(dirname "$0")/.."
LOG=../results/experiment_logs
export OMP_NUM_THREADS=1
python3 experiments/run_grouped.py 4 >> $LOG/grouped.log 2>&1
python3 experiments/timing_fit.py > $LOG/timing_fit.log 2>&1
python3 experiments/timing.py > $LOG/timing_v3.log 2>&1
echo QUEUE2_DONE >> $LOG/queue_cycle2.log

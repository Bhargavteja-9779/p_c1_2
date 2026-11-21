#!/bin/bash
# Remaining compute after review round 7 (container recycled): RW timing (review 6), CTR23 context refit,
# RW-DLC on CTR23 (pre-registered secondary suite).
cd "$(dirname "$0")/.."
LOG=../results/experiment_logs
export OMP_NUM_THREADS=1
python3 experiments/timing_rw.py > $LOG/timing_rw.log 2>&1
echo TIMING_RW_DONE >> $LOG/queue_cycle3.log
python3 experiments/run_benchmark.py --mode fitonly --out ../results/raw_refit >> $LOG/refit_contexts.log 2>&1
echo REFIT_DONE >> $LOG/queue_cycle3.log
python3 experiments/run_rw.py ctr23 4 > $LOG/rw_ctr23.log 2>&1
echo QUEUE3_DONE >> $LOG/queue_cycle3.log

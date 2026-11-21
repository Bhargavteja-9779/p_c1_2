#!/bin/bash
# After queue_cycle3b.sh: re-run the RW timing with the final g_at (tail density only outside the table)
# and peak-memory measurement, on an idle machine.
cd "$(dirname "$0")/.."
LOG=../results/experiment_logs
until grep -q QUEUE3B_DONE $LOG/queue_cycle3.log 2>/dev/null; do sleep 60; done
python3 experiments/timing_rw.py > $LOG/timing_rw.log 2>&1
echo QUEUE3C_DONE >> $LOG/queue_cycle3.log

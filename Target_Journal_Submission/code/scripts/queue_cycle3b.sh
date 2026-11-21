#!/bin/bash
# Runs after queue_cycle3.sh on an otherwise idle machine: like-for-like timing (review 6, issue 6).
cd "$(dirname "$0")/.."
LOG=../results/experiment_logs
until grep -q QUEUE3_DONE $LOG/queue_cycle3.log 2>/dev/null; do sleep 60; done
python3 experiments/timing_like.py > $LOG/timing_like.log 2>&1
echo QUEUE3B_DONE >> $LOG/queue_cycle3.log

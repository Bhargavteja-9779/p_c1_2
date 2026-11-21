#!/bin/bash
# Resume the remaining compute queue in a fresh container (idempotent; finished outputs are skipped).
# Usage: bash code/scripts/resume_queue.sh   (from Target_Journal_Submission/)
# Needs network access to openml.org, www.openml.org, api.openml.org, data.openml.org (cloud env "p_c1_2").
set -u
cd "$(dirname "$0")/.."
PY=/root/venv/bin/python
if ! $PY -c "import sklearn,scipy,lightgbm,openml" 2>/dev/null; then
  python3 -m venv /root/venv && /root/venv/bin/pip install -q -r requirements.txt
fi
LOG=../results/experiment_logs
export OMP_NUM_THREADS=1
n() { ls "$1" 2>/dev/null | wc -l; }
[ "$(n ../results/raw_grouped)" -ge 15 ] || $PY experiments/run_grouped.py 4 >> $LOG/grouped.log 2>&1
[ -f ../results/timing_fit.csv ] || $PY experiments/timing_fit.py > $LOG/timing_fit.log 2>&1
$PY experiments/timing.py > $LOG/timing_v3.log 2>&1
echo QUEUE_DONE >> $LOG/queue_cycle1b.log

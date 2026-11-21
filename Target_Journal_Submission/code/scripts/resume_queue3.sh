#!/bin/bash
# Resume compute queue 3 in a fresh container (steps with a marker in queue_cycle3.log are skipped).
cd "$(dirname "$0")/.."
PY=/root/venv/bin/python
$PY -c "import sklearn,scipy,lightgbm,openml" 2>/dev/null || { python3 -m venv /root/venv && /root/venv/bin/pip install -q -r requirements.txt; }
LOG=../results/experiment_logs; Q=$LOG/queue_cycle3.log
export OMP_NUM_THREADS=1
done_() { grep -q "^$1$" $Q 2>/dev/null; }
done_ REFIT_DONE  || { $PY experiments/run_benchmark.py --mode fitonly --out ../results/raw_refit >> $LOG/refit_contexts.log 2>&1 && echo REFIT_DONE >> $Q; }
done_ QUEUE3_DONE || { $PY experiments/run_rw.py ctr23 4 > $LOG/rw_ctr23.log 2>&1 && echo QUEUE3_DONE >> $Q; }
done_ QUEUE3B_DONE || { $PY experiments/timing_like.py > $LOG/timing_like.log 2>&1 && echo QUEUE3B_DONE >> $Q; }
done_ QUEUE3C_DONE || { $PY experiments/timing_rw.py > $LOG/timing_rw.log 2>&1 && echo QUEUE3C_DONE >> $Q; }

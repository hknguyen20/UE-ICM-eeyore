#!/bin/bash
pkill -f "python ICM.py" || true
cd src/experiments


# Other than testbed and model, other params are to be adjusted and experimented. Currently letting many defaults.
nohup python ICM.py \
  --testbed eeyore-preference \
  --model hugging-quants/Meta-Llama-3.1-8B-Instruct-AWQ-INT4 \
  --K 100 \
  --consistency_fix_K 5 \
  --batch_size 32 \
  > "progress.log" 2>&1 &

echo "Process started with PID: $!"

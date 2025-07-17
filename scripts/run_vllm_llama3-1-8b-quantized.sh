#!/bin/bash

# Kill any existing vLLM processes
pkill -f "vllm.entrypoints.openai.api_server"

# ---------------------------
# Explanation of parameters:
# --quantization awq            : Activation-aware Weight Quantization
# --gpu-memory-utilization      : How many % of each GPU's available memory
# --max-num-seqs                : Max number of concurrent sequences served
# --max-model-len               : Max tokens per request (input + output)
# --tensor-parallel-size 2      : Number of GPUs used to shard model weights, should divide attention head
# --enable-prefix-caching       : Cache shared prompt prefixes to speed up inference
# --port 8000                   : Server will run on port 8000
# ---------------------------

nohup python3 -m vllm.entrypoints.openai.api_server \
  --model hugging-quants/Meta-Llama-3.1-8B-Instruct-AWQ-INT4 \
  --quantization awq \
  --gpu-memory-utilization 0.8 \
  --max-num-seqs 64 \
  --max-model-len 38448 \
  --tensor-parallel-size 2 \
  --enable-prefix-caching \
  > vllm_server.log 2>&1 &

echo "Process started with PID: $!"

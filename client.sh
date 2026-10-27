#!/bin/bash
# CS5470 A1 client -- netid zz986, cfg 122863a3
# usage: ./client.sh <tag>   e.g. ./client.sh tp1  or  ./client.sh probe
TAG=${1:?usage: ./client.sh <tag>}
python3 benchmark.py --backend vllm \
    --model meta-llama/Llama-3.1-8B \
    --seed 28162 \
    --request-rate 12 \
    --num-prompts 150 \
    --dataset-name dummy \
    --long-prompts 5 \
    --long-prompt-len 16000 \
    --save-result --result-dir results \
    --metadata netid=zz986 cfg=122863a3 run=$TAG

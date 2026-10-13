#!/usr/bin/env bash
# Run ScienceAgentBench inference for every model in models.txt (one background
# job per model, each resumable: run_infer.py skips tasks already in its log).
# Usage: ./run_all.sh [extra run_infer.py args, e.g. --use_knowledge]
set -euo pipefail
cd "$(dirname "$0")"
: "${RIVAULT_API_KEY:?set RIVAULT_API_KEY}"
export PYTHONPATH=.

RESULTS=results
mkdir -p "$RESULTS"

run_model() {
    local model=$1; shift
    local tag=${model//\//__}
    local dir=$RESULTS/$tag
    mkdir -p "$dir"
    .venv/bin/python -u run_infer.py \
        --llm_engine_name "rivault/$model" \
        --log_fname "$dir/science_agent.jsonl" \
        --out_fpath "$dir/pred_programs" \
        "$@" > "$dir/run.log" 2>&1
}

while read -r model; do
    [[ -z $model || $model == \#* ]] && continue
    run_model "$model" "$@" &
done < models.txt
wait
echo "all models done"

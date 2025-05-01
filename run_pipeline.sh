#!/usr/bin/env bash

# 処理したいファイルのリスト
input=(
"./data/2012/097.jsonl"
"./data/2013/098.jsonl"
"./data/2014/099.jsonl"
"./data/2015/100.jsonl"
"./data/2016/101.jsonl"
"./data/2017/102.jsonl"
"./data/2018/103.jsonl"
"./data/2019/104.jsonl"
"./data/2020/105.jsonl"
"./data/2021/106.jsonl"
"./data/2022/107.jsonl"
"./data/2023/108.jsonl"
"./data/2024/109.jsonl"
)

meta=(
"./data/2012/metadata_097.jsonl"
"./data/2013/metadata_098.jsonl"
"./data/2014/metadata_099.jsonl"
"./data/2015/metadata_100.jsonl"
"./data/2016/metadata_101.jsonl"
"./data/2017/metadata_102.jsonl"
"./data/2018/metadata_103.jsonl"
"./data/2019/metadata_104.jsonl"
"./data/2020/metadata_105.jsonl"
"./data/2021/metadata_106.jsonl"
"./data/2022/metadata_107.jsonl"
"./data/2023/metadata_108.jsonl"
"./data/2024/metadata_109.jsonl"
)

years=(
"2012"
"2013"
"2014"
"2015"
"2016"
"2017"
"2018"
"2019"
"2020"
"2021"
"2022"
"2023"
"2024"
)

CONFIG="Qwen/Qwen2.5-7B-Instruct"
PROMPT_FILE="scripts/prompts/prompt_yakugaku.jsonl"
OUT_DIR="./baseline_results"

huggingface-cli login --token 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 --add-to-git-credential

# 結果を格納する配列（必要であれば）
output=()
result=()

for i in "${!input[@]}"; do
    in_file="${input[$i]}"
    meta_file="${meta[$i]}"
    year="${years[$i]}"
    echo "Processing ${in_file} with ${meta_file} for year ${year}"

    # pipeline.pyを呼び出して処理
    MKL_SERVICE_FORCE_INTEL=1 CUDA_VISIBLE_DEVICES="0" python scripts/pipeline.py \
        --in-file "${in_file}" \
        --meta-file "${meta_file}" \
        --config "${CONFIG}" \
        --prompt-file "${PROMPT_FILE}" \
        --out-dir "${OUT_DIR}" \
        --text-only # 必要なら付ける
done

# python scripts/pipeline.py --config "${CONFIG}" --evaluate-only

# 必要であれば、ループ後にexcel_outputなどを別途呼び出すスクリプトや処理をここで行う

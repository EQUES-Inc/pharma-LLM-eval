# Yakugaku QA Scripts
All API keys are removed. You need to get your key for ChatGPT/GPT-4/GPT-4o if you want to run them.

## Prediction
We provide five baselines provided in our paper. Run:
```bash
python baseline_main.py --in-file ../data/2012/097-A.jsonl --config chatgpt
python baseline_main.py --in-file ../data/2012/097-A.jsonl --config gpt4
python baseline_main.py --in-file ../data/2012/097-A.jsonl --config gpt4o
python baseline_main.py --in-file ../data/2012/097-A_translate.jsonl --config chatgpt-en --prompt-file prompts/prompt_translate.jsonl 
python baseline_main.py --in-file ../data/2012/097-A.jsonl --student-majority
python baseline_main.py --in-file ../data/2012/097.jsonl --config gpt4o --prompt-file prompts/prompt_yakugaku.jsonl
```
This will output prediction jsonl files in `../baseline_results/`. Replace the `--in-file` argument with your questions.

## Evaluation
```bash
python evaluate_main.py --gold-file ../data/2012/097-A.jsonl --pred-file ../baseline_results/097-A_gpt4o.jsonl  --text-only
python evaluate_main02.py --gold-file ../data/2012/097.jsonl --pred-file ../baseline_results/097_gpt4o.jsonl --meta-file ../data/2012/metadata_097.jsonl --text-only
python evaluate_meta.py --gold-file ../data/2012/097.jsonl --pred-file ../baseline_results/097_gpt4o.jsonl --meta-file ../data/2012/metadata_097.jsonl --text-only
```

## Pipeline

### yakugaku.def
```bash
BootStrap: docker
From: pytorch/pytorch:latest

%post
    apt-get update
    apt-get -y upgrade
    apt-get -y install build-essential git
    pip install wandb
    # 作業ディレクトリを作成
    mkdir -p /opt/YakugakuQA
```

### run_pipeline.sh
```bash
#!/usr/bin/env bash

pip install -r requirements.txt
cd ./scripts

# 処理したいファイルのリスト
input=(
"../data/2012/097.jsonl"
"../data/2013/098.jsonl"
"../data/2014/099.jsonl"
"../data/2015/100.jsonl"
"../data/2016/101.jsonl"
"../data/2017/102.jsonl"
"../data/2018/103.jsonl"
"../data/2019/104.jsonl"
"../data/2020/105.jsonl"
"../data/2021/106.jsonl"
"../data/2022/107.jsonl"
"../data/2023/108.jsonl"
"../data/2024/109.jsonl"
)

meta=(
"../data/2012/metadata_097.jsonl"
"../data/2013/metadata_098.jsonl"
"../data/2014/metadata_099.jsonl"
"../data/2015/metadata_100.jsonl"
"../data/2016/metadata_101.jsonl"
"../data/2017/metadata_102.jsonl"
"../data/2018/metadata_103.jsonl"
"../data/2019/metadata_104.jsonl"
"../data/2020/metadata_105.jsonl"
"../data/2021/metadata_106.jsonl"
"../data/2022/metadata_107.jsonl"
"../data/2023/metadata_108.jsonl"
"../data/2024/metadata_109.jsonl"
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

CONFIG="elyza/Llama-3-ELYZA-JP-8B"
PROMPT_FILE="prompts/prompt_yakugaku.jsonl"
OUT_DIR="../baseline_results"

for i in "${!input[@]}"; do
    in_file="${input[$i]}"
    meta_file="${meta[$i]}"
    year="${years[$i]}"
    echo "Processing ${in_file} with ${meta_file} for year ${year}"

    # pipeline.pyを呼び出して処理
    python pipeline.py \
        --in-file "${in_file}" \
        --meta-file "${meta_file}" \
        --config "${CONFIG}" \
        --prompt-file "${PROMPT_FILE}" \
        --out-dir "${OUT_DIR}" \
        --text-only 

done

    python pipeline.py --config "${CONFIG}" --evaluate-only
```

### run0.sh
```bash
#!/bin/bash
#SBATCH --job-name hf
#SBATCH --output %x-%j.log
#SBATCH --error %x-%j.err
#SBATCH --nodes 1
#SBATCH --cpus-per-task 8
#SBATCH --gpus=1
#SBATCH --time 06:00:00

date
export CUDA_VISIBLE_DEVICES="0"
export OPENAI_API_KEY="sk-proj-6XMunTG86wqGm5K75gtCT3BlbkFJeovvP8y0EG1uigs6r56U"
export HUGGINGFACE_HUB_TOKEN="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"
export WANDB_API_KEY="6a097cdb4ace71ed59b3d7afb8345f7ca00a1507"
export HF_HOME="/scratch/"
singularity exec --pwd /opt/YakugakuQA --bind /scratch:/scratch --bind /home/ishihara/YakugakuQA:/opt/YakugakuQA --nv yakugaku.sif  bash run_pipeline.sh
date
```

### slurm
```bash
sbatch run0.sh
```


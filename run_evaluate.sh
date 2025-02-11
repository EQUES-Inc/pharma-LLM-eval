#!/bin/bash
#SBATCH --job-name yakugakuqa-pipeline
#SBATCH --output %x-%j.log
#SBATCH --error %x-%j.err
#SBATCH --nodes 1
#SBATCH --cpus-per-task 8
#SBATCH --gpus=4
#SBATCH --time=10-00

webhook_url="https://hooks.slack.com/services/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"
job_id=${SLURM_JOB_ID:-"UNKNOWN_JOB_ID"}
job_name=${SLURM_JOB_NAME:-"UNKNOWN_JOB_NAME"}

error_handler() {
  local exit_code=$?
  gpu_status=$(nvidia-smi)
  message="ジョブ（ID: $job_id, 名称: $job_name）がエラー終了しました。エラーコード: $exit_code\nGPUステータス:\n$gpu_status"
  
  curl -X POST -H 'Content-type: application/json' --data "{\"text\":\"$message\"}" $webhook_url
}

success_handler() {
  gpu_status=$(nvidia-smi)
  message="ジョブ（ID: $job_id, 名称: $job_name）が正常に終了しました。\nGPUステータス:\n$gpu_status"
  
  curl -X POST -H 'Content-type: application/json' --data "{\"text\":\"$message\"}" $webhook_url
}

date
singularity exec --nv --bind /scratch:/mnt ../.image/basic.sif python scripts/evaluate_main02.py \
  --pred-file /home/sukeda/work/YakugakuQA/baseline_results/109_EQUES_TinySwallow-Stratos-1.5B.jsonl \
  --gold-file /home/sukeda/work/YakugakuQA/data/2024/109.jsonl \
  --meta-file /home/sukeda/work/YakugakuQA/data/2024/metadata_109.jsonl \
  --text-only
date

if [ $? -eq 0 ]; then
  success_handler
fi

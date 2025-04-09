# Evaluating LLMs on Japanese National Pharmacist Licensing Examinations and others

本リポジトリは、経済産業省及びNEDOによる生成AI開発力強化プロジェクト「GENIAC」により支援を受けた成果の一部である。

## 環境
Singularity + Slurm

## YakugakuQA
We evaluate LLMs on Japanese medical lincensing examinations from the past 13 years (2012-2024) and release the data as the YakugakuQA (薬学QA) benchmark.

**Benchmark Collection**

Notice that we do not rely on any translation of sources from other languages (e.g., English) or countries, and the benchmark comes solely from resources that are originally written in Japanese.
See our paper for more detail.

**Usage**
1. `run_pipeline.sh`中のl52前後にあるCONFIGを変更する.
2. `run_pipeline.sh`中のl67にあるCUDA_VISIBLE_DEVICESを変更する. (複数指定するとエラーが生じやすい.)
3. 評価の実行.
    - (slurm利用の場合)`sbatch run.sh` を実行する.
    - (それ以外) `singularity shell --nv eval.sif` の後, `bash run_pipeline.sh`

**Output**
- モデルの応答：`/baseline_results` 以下に`<年>_<モデル>.jsonl` というファイルが作成されます.
- モデルの正答数：`/baseline_results` 以下に`<年>_<モデル>_count.jsonl` というファイルが作成されます.


## Acknowledgement
This repository is partly forked from [IgakuQA]().


## Citations
```
```


# EQUES's Pharma LLM Project

本リポジトリは、経済産業省及びNEDOによる生成AI開発力強化プロジェクト「GENIAC」により支援を受けた成果の一部である。

This work is based on results obtained from GENIAC (Generative AI Accelerator Challenge, a project to strengthen Japan’s generative AI development capabilities), a project implemented by the Ministry of Economy, Trade and Industry (METI) and the New Energy and Industrial Technology Development Organization (NEDO).



# Models
See [JPharmatron](https://huggingface.co/collections/EQUES/pharmatron-680a330b4dfce3ac43009984).


# Benchmarks

See also [JPharmaBench](https://huggingface.co/collections/EQUES/jpharmabench-680a34acfe96870e41d050d8).

Requirements are
- jsonlines
- mojimoji
- openai
- vllm
- pandas
- openpyxl
- transformers 
- accelerate
- httpx

## YakugakuQA

**Summary**

We evaluate LLMs on Japanese medical lincensing examinations from the past 13 years (2012-2024) and release the data as the YakugakuQA (薬学QA) benchmark.

**Benchmark Collection**

Notice that we do not rely on any translation of sources from other languages (e.g., English) or countries, and the benchmark comes solely from resources that are originally written in Japanese.
See our paper for more detail.

**Usage**
1. Change CONFIG in line 52 of `run_pipeline.sh`.
2. Change CUDA_VISIBLE_DEVICES in line 69 of `run_pipeline.sh`.
3. Run `bash run_pipeline.sh`.

You may add `--evaluate-only` to line 69 of `run_pipeline.sh` if only evaluation is needed.

**Output**
- `/baseline_results/<year_ID>_<model_name>.jsonl` 
- `/baseline_results<year_ID>_<model_name>_count.jsonl` 

**Acknowledgement**  
This repository is partly forked from [IgakuQA](https://github.com/jungokasai/IgakuQA).


## NayoseBench（NayoseQA）

Switch to the branch **NayoseBench**.


## SogoBench（SogoCheck）

Switch to the branch **SogoBench**.


## Citations
```
Coming soon...
```


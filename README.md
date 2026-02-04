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

Move to **NayoseBench/**.


## SogoBench（SogoCheck）

Move to **SogoBench/**.


## Citations
```
@inproceedings{ono-etal-2025-japanese,
    title = "A {J}apanese Language Model and Three New Evaluation Benchmarks for Pharmaceutical {NLP}",
    author = "Ono, Shinnosuke  and
      Sukeda, Issey  and
      Fujii, Takuro  and
      Buma, Kosei  and
      Sasaki, Shunsuke",
    editor = "Inui, Kentaro  and
      Sakti, Sakriani  and
      Wang, Haofen  and
      Wong, Derek F.  and
      Bhattacharyya, Pushpak  and
      Banerjee, Biplab  and
      Ekbal, Asif  and
      Chakraborty, Tanmoy  and
      Singh, Dhirendra Pratap",
    booktitle = "Proceedings of the 14th International Joint Conference on Natural Language Processing and the 4th Conference of the Asia-Pacific Chapter of the Association for Computational Linguistics",
    month = dec,
    year = "2025",
    address = "Mumbai, India",
    publisher = "The Asian Federation of Natural Language Processing and The Association for Computational Linguistics",
    url = "https://aclanthology.org/2025.ijcnlp-long.72/",
    pages = "1316--1332",
    ISBN = "979-8-89176-298-5",
    abstract = "We present **JPharmatron**, a Japanese domain-specific large language model (LLM) for the pharmaceutical field, developed through continual pre-training on two billion Japanese pharmaceutical tokens and eight billion English biomedical tokens. For rigorous evaluation, we introduce **JPharmaBench**, a benchmark suite consisting of three new benchmarks: YakugakuQA, based on national pharmacist licensing exams; NayoseQA, which tests cross-lingual synonym and terminology normalization; and SogoCheck, a novel task involving cross-document consistency checking.We evaluate our model against open-source medical LLMs and commercial models, including GPT-4o. Experimental results show that **JPharmatron** outperforms existing open models and achieves competitive performance with commercial ones.Interestingly, even GPT-4o performs poorly on SogoCheck, suggesting that cross-sentence consistency reasoning remains an open challenge.**JPharmatron** enables secure and local model deployment for pharmaceutical tasks, where privacy and legal constraints limit the use of closed models. Besides, **JPharmaBench** offers a reproducible framework for evaluating Japanese pharmaceutical natural language processing. Together, they demonstrate the feasibility of practical and cost-efficient language models for Japanese healthcare and pharmaceutical sectors.Our model, codes, and datasets are available on HuggingFace: https://huggingface.co/collections/EQUES/jpharmatron and https://huggingface.co/collections/EQUES/jpharmabench."
}
```


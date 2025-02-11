import os
from generation.evaluate import evaluate, excel_output
from utils.tools import answer2jsonl, read_jsonl
import pandas as pd

def main(in_file, config="chatgpt", prompt_file="prompts/prompt_yakugaku.jsonl", out_dir="../baseline_results/"):
    questions = read_jsonl(in_file)
    prompt = read_jsonl(prompt_file)
    scores = None
    if config == "chatgpt":
        from generation.chatgpt import run_chatgpt
        answers, outputs = run_chatgpt(questions, prompt=prompt)
    elif config == "chatgpt-en":
        from generation.chatgpt_en import run_chatgpt_en
        answers, outputs = run_chatgpt_en(questions, prompt=prompt)
    elif config == "gpt3":
        from generation.gpt3 import run_gpt3
        answers, outputs = run_gpt3(questions, prompt=prompt)
    elif config == "gpt4":
        from generation.chatgpt import run_chatgpt
        answers, outputs = run_chatgpt(questions, prompt=prompt, model="gpt-4")
    elif config == "gpt4o":
        from generation.chatgpt import run_chatgpt
        answers, outputs = run_chatgpt(questions, prompt=prompt, model="gpt-4o")
    elif config == "o1-preview":
        from generation.chatgpt import run_chatgpt
        answers, outputs = run_chatgpt(questions, prompt=prompt, model="o1-preview")
    elif config == "o1-mini":
        from generation.chatgpt import run_chatgpt
        answers, outputs = run_chatgpt(questions, prompt=prompt, model="o1-mini")
    elif config == "student-majority":
        from generation.student import run_student
        meta_data = read_jsonl(in_file.replace('.jsonl', '_metadata.jsonl'))
        answers, outputs = run_student(questions, meta_data)
    else:
        from generation.chatgpt import run_openmodel
        print(config)
        answers, outputs = run_openmodel(questions, prompt=prompt, model=config)
    new_config = config.replace("/", "_")
    out_file = os.path.basename(in_file).replace('.jsonl', '')
    out_file = out_file + "_" + new_config + ".jsonl"
    out_file = os.path.join(out_dir, out_file)
    print(out_file)
    answer2jsonl(answers, outputs, questions, out_file)

    return out_file

if __name__ == '__main__':
    import argparse
    import time
    import wandb

    input = ['../data/2012/097.jsonl','../data/2013/098.jsonl', '../data/2014/099.jsonl', '../data/2015/100.jsonl', '../data/2016/101.jsonl', '../data/2017/102.jsonl', '../data/2018/103.jsonl', '../data/2019/104.jsonl', '../data/2020/105.jsonl', '../data/2021/106.jsonl', '../data/2022/107.jsonl', '../data/2023/108.jsonl', '../data/2024/109.jsonl']
    years = ["2012", "2013", "2014", "2015", "2016", "2017", "2018", "2019", "2020", "2021", "2022", "2023", "2024"]
   
    parser = argparse.ArgumentParser(allow_abbrev=False)

    parser.add_argument('--in-file', type=str, default='../data/2012/097.jsonl', help='input jsonl file')
    parser.add_argument('--meta-file', type=str, default='../data/2012/metadata_097.jsonl', help='metadata file')
    parser.add_argument('--config', type=str, default='elyza/Llama-3-ELYZA-JP-8B', help='baseline configuration')
    parser.add_argument('--prompt-file', type=str, default='prompts/prompt_yakugaku.jsonl', help='prompt file')
    parser.add_argument('--out-dir', type=str, default='../baseline_results/', help='baseline results output')
    parser.add_argument('--text-only', action='store_true', help='text only')
    parser.add_argument('--evaluate-only', action='store_true', help='evaluate only')

    args = parser.parse_args()
    print(f"モデル名：{args.config}")

    wandb.login()
    wandb.init(project="YakugakuQA", config={
        "model_name": f"{args.config}",
        "task": "baseline"
    })
    start_time = time.time()

    if not args.evaluate_only:
        # main, evaluate, excel_output関数は元のままとして仮定
        # 以下の行で実行する処理を1ペア(in_file, meta_file)のみ実施する
        out_file = main(args.in_file, args.config, args.prompt_file, args.out_dir)
        count_file = evaluate(out_file, args.in_file, args.meta_file, args.text_only)
    else:
        result = []
        for in_file in input:
            new_config = args.config.replace("/", "_")
            out_file = os.path.basename(in_file).replace('.jsonl', '')
            out_file = out_file + "_" + new_config + "_count.jsonl"
            out_file = os.path.join(args.out_dir, out_file)
            result.append(out_file)
        
        excel_output(result, years, args.config, args.out_dir)

    # 結果をwandbにログしたい場合や、何らかの出力をここで行う
    # yearsやoutput/resultをまとめて処理する部分は外部スクリプトで行うか、ここでは省略。

    end_time = time.time()
    elapsed_time = end_time - start_time
    print("経過時間：", elapsed_time)
    wandb.log({"elapsed_time": elapsed_time})
    wandb.finish()

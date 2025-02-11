import os

from utils.tools import answer2jsonl, check_jsonls, read_jsonl


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

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(allow_abbrev=False)

    parser.add_argument('--in-file', type=str, metavar='N',
                        default='../data/2022/116-A.jsonl', help='input jsonl file')
    parser.add_argument('--config', type=str, metavar='N',
                        #choices=["chatgpt", "chatgpt-en", "gpt3", "gpt4", "gpt4o", "student-majority", "*"],
                        default='chatgpt', help='baseline configuration')
    parser.add_argument('--out-dir', type=str, metavar='N',
                        default='../baseline_results/', help='baseline results output')
    parser.add_argument('--prompt-file', type=str, metavar='N',
                        default='prompts/prompt.jsonl', help='prompt file')
    # 引数を解析
    args = parser.parse_args()

    import wandb
    import time
    wandb.login(key="6a097cdb4ace71ed59b3d7afb8345f7ca00a1507")
    wandb.init(project="YakugakuQA", config={
        "model_name": f"{args.config}",
        "task": "baseline"
    })
    start_time = time.time()

    main(args.in_file, args.config, args.prompt_file, args.out_dir)
    
    end_time = time.time()
    elapsed_time = end_time - start_time
    wandb.log({
        "elapsed_time": elapsed_time
    })
    wandb.finish()

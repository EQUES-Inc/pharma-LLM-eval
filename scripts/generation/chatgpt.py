import os
import string
import threading
import time
import torch
import mojimoji
from openai import OpenAI

from utils.tools import check_jsonls

def run_chatgpt(questions, model="gpt-4o", prompt=None):
    #print(model)
    preds = []
    outputs = []
    for q_idx in range(len(questions)):
        question = questions[q_idx]
        print(question['problem_id'])
        if model in ["o1-preview", "o1-mini"]:
            chatgpt_input = create_input1(prompt, question)
        else:
            chatgpt_input = create_input1(prompt, question)
        done = False
        nb_trials = 0
        while not done:
            try:
                answer = chatgpt_problem(chatgpt_input, model)
                # 出力結果を表示
                #print(answer)
                if answer is None:
                    done = False
                    print(' failed')
                else:
                    done = True
            except:
                print(' failed')
                time.sleep(5.0)
                nb_trials += 1
            if nb_trials == 3:
                explanation = 'NA'
                answer = 'NA'
                break
        preds.append(answer)
        outputs.append(answer)
    return preds, outputs

def run_openmodel(questions, model, prompt=None):
    from huggingface_hub import HfApi, HfFolder
    from transformers import AutoModelForCausalLM, AutoTokenizer
    from vllm import LLM, SamplingParams
    global output

    model_name = model

    # vllm を使用してモデルをロード
    # 利用可能なGPUの数を取得
    gpu_count = torch.cuda.device_count()
    print(f"利用可能なGPUの数: {gpu_count}")

    # tensor_parallel_size を設定（最大4、利用可能なGPU数まで）
    desired_parallel_size = 4
    print(f"要求するGPUの数: {desired_parallel_size}")
    tensor_parallel_size = min(desired_parallel_size, gpu_count) if gpu_count > 0 else 0
    print(f"設定したGPUの数: {tensor_parallel_size}")

    if tensor_parallel_size == 0:
        raise RuntimeError("GPUが利用可能ではありません。'device' を 'cpu' に設定してください。")

    # LLMの初期化
    llm = LLM(model=model_name, device="cuda", tensor_parallel_size=tensor_parallel_size,trust_remote_code=True,max_model_len=4096)

    # サンプリングパラメータを設定
    sampling_params = SamplingParams(
        temperature=0.4,
        top_p=0.9,
        max_tokens=1024,
        stop="<|im_end|>" #check: base modelだと"<|endoftext|> chat modelだと"<|im_end|>"という理解であっているか.
    )

    preds = []
    outputs = []
    for q_idx in range(len(questions)):
        question = questions[q_idx]
        print(question['problem_id'])
        chatgpt_input = create_input(prompt, question)
        done = False
        nb_trials = 0
        while not done:
            try:
                first_part = model_name.split("/")[0]
                if first_part in ["elyza", "tokyotech-llm", "meta-llama", "turing-motors", "google", "Qwen", "EQUES"]:
                    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
                    prompt_applied = tokenizer.apply_chat_template(
                        chatgpt_input,
                        tokenize=False,
                        add_generation_prompt=True
                    )
                else: #check: 本fileの最下部に定義された関数. 原則使わずに, tokenizerに付与のchat templateを利用する.
                    prompt_applied = apply_chat_template(
                        message=chatgpt_input,
                        tokenize=False,
                        add_generation_prompt=True
                    )
                # import pdb; pdb.set_trace() #chekc: prompt_appliedやtokenizerが問題ないか要チェック

                # モデルの実行
                outputs_from_llm = llm.generate(prompt_applied, sampling_params)
                answer = outputs_from_llm[0].outputs[0].text.strip()
                print("="*30)
                print("Raw Output from LLM, Before Postprocessing")
                print(answer)


                ### Adhocな後処理. #check: Instruction-followingしないモデルが問題となる.
                if len(answer) >= 3:
                    if answer[1] == ",":
                        answer = answer[:3]
                    else:
                        answer = answer[0]
                else:
                    answer = answer[0]

                print("Output from LLM, After Postprocessing")
                print(answer)

                if answer is None:
                    done = False
                    print('\nfailed(1)')
                else:
                    done = True
            except:
                print('\nfailed(2)')
                time.sleep(5.0)
                nb_trials += 1
            if nb_trials == 3:
                explanation = 'NA'
                answer = 'NA'
                break
            
        preds.append(answer)
        outputs.append(answer)

    return preds, outputs

def create_input(prompt, question):
    messages = [{"role": "system", "content": "薬剤師国家試験を解きます。"}]
    for example in prompt:
        messages.extend(dict2problem(example))
    messages.extend(dict2problem(question, False))
    return messages

def create_input1(prompt, question):
    messages = []
    for example in prompt:
        messages.extend(dict2problem(example))
    messages.extend(dict2problem(question, False))
    return messages

def dict2problem(dict_input, demo=True):
    problem = "問題: " + dict_input['problem_text']
    choices = dict_input['choices']
    answer = dict_input['answer']
    if len(choices) > 0:
        for choice, label in zip(choices, ["1","2","3","4","5","6","7","8","9"]):
            problem = problem + '\n' + label + ': ' + choice
        problem = problem + "\n必ず1,2,3,4,5,6の中からちょうど{}個選んでください。".format(len(answer))
        problem = problem + "\n答え:"
    output = [{"role": "user", "content": problem}]
    if not demo:
        return output
    output.append({"role": "assistant", "content": ",".join(answer)})
    return output

def chatgpt_problem(messages, model):
    t = threading.Thread(target=run_api, args=(model, messages,))
    t.start()
    max_time = 30
    while t.is_alive() and max_time > 0:
        time.sleep(0.1)  # check every 0.1 seconds
        max_time -= 0.1
    if t.is_alive():
        # Thread is still running after maximum time limit
        # We need to stop it and exit the program
        print("Maximum time limit exceeded. Exiting program...")
        t._stop()
        return None, None
    answer = output.choices[0].message.content
    pred = mojimoji.zen_to_han(answer).lower()
    t._stop()
    return pred

def run_api(model, messages):
    global output
    client = OpenAI()
    output = client.chat.completions.create(
      model=model,
      messages=messages,
    )

# チャットテンプレート関数
def apply_chat_template(message, tokenize=False, add_generation_prompt=True):
    template = ""
    for msg in message:
        if msg["role"] == "system":
            template += f"<|system|>{msg['content']}\n"
        elif msg["role"] == "user":
            template += f"<|user|>{msg['content']}\n"
        elif msg["role"] == "assistant":
            template += f"<|assistant|>{msg['content']}\n"
    if add_generation_prompt:
        template += "<|assistant|>"
    return template
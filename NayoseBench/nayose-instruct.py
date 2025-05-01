from datasets import load_dataset
from tqdm import tqdm
data_instruct = load_dataset("EQUES/Nayose-Bench-Instruction")

import os
os.environ["CUDA_VISIBLE_DEVICES"]="0"
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "SakanaAI/TinySwallow-1.5B-Instruct"
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto"
)
tokenizer = AutoTokenizer.from_pretrained(model_name)

total_num = 0
correct_num = 0
for data1 in tqdm(data_instruct["test"]):
    instruction = data1["instruction"]
    answer1 = data1["response"]

    prompt = f"以下の質問に答えてください。最終的な回答のみを出力としてください。{instruction}"
    messages = [
        {"role": "system", "content": "You are a pharmaceutical expert and a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
    text = tokenizer.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )
    model_inputs = tokenizer([text], return_tensors="pt").to(model.device)

    generated_ids = model.generate(
        **model_inputs,
        max_new_tokens=512,
    )
    generated_ids = [
        output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
    ]

    response1 = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]


    print("【問題1】")
    print(instruction.strip())
    print("【LLMの回答】")
    print(response1.strip())
    print("【正解】")
    print(answer1.strip())
    print("【判定】")
    judge = response1.strip().replace(f"{instruction.replace("?","")}","") == answer1
    print(judge)

    if judge:
        correct_num += 1
    total_num += 1

    # import pdb; pdb.set_trace()

print("="*30)
print("【集計結果】")
print(f"{correct_num}/{total_num} = {correct_num/total_num}")

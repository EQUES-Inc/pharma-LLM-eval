import os
from datasets import load_dataset
from tqdm import tqdm
data_qa = load_dataset("EQUES/Nayose-Bench-QA")

is_openai = False
if not is_openai:
    from transformers import AutoModelForCausalLM, AutoTokenizer
    os.environ["CUDA_VISIBLE_DEVICES"]="0"
    model_name = "<MODEL_NAME>"
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        device_map="auto"
    )
    tokenizer = AutoTokenizer.from_pretrained(model_name)

else:
    from openai import OpenAI
    import os
    client = OpenAI()
    client.api_key = os.environ['OPENAI_API_KEY']  # 環境変数から取得


total_num = 0
correct_num = 0
for data2 in tqdm(data_qa["test"]):
    question = data2["question"]
    label = data2["label"]
    choices = [data2["choice0"],data2["choice1"],data2["choice2"],data2["choice3"],data2["choice4"]]
    answer2 = choices[label]
    prompt = f"{question}以下の中から１つ選択してください。思考の過程は出力せず、答えのみを出力してください。{choices}"

    if is_openai:
        completion = client.chat.completions.create(
            model="gpt-4o",  # モデルの指定
            messages=[
                {"role": "system", "content": "You are an excellent secretary who responds in Japanese."},
                {"role": "user", "content": prompt}
            ]
        )
        response2 = completion.choices[0].message.content

    else:       
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
            max_new_tokens=32,
        )
        generated_ids = [
            output_ids[len(input_ids):] for input_ids, output_ids in zip(model_inputs.input_ids, generated_ids)
        ]

        response2 = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]

    ### 

    print("【問題】")
    print(prompt.strip())
    print("【LLMの回答】")
    response2 = response2.replace("'","")
    print(response2.strip())
    print("【正解】")
    print(answer2.strip())
    print("【判定】")
    judge = (answer2.strip() == response2.strip())
    print(judge)

    if judge:
        correct_num += 1
    total_num += 1

    

print("="*30)
print("【集計結果】")
print(f"{correct_num}/{total_num} = {correct_num/total_num}")

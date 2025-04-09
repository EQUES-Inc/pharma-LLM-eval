import pandas as pd
import glob


# model_name = "SakanaAI_TinySwallow"
# model_name = "EQUES_TinySwallow"
# model_name = "Qwen_Qwen2.5"
# model_name = "bespokelabs_Bespoke"
# model_name = "tokyotech-llm_Llama-3.1-Swallow-8B-Instruct-v0.3"
# model_name = "EQUES_Qwen2.5-7B_ja-cleaned"
model_name = "EQUES_dare_ties"

files = sorted(glob.glob(f"./baseline_results/*_{model_name}*_count.jsonl"))
print(len(files))
correct = 0
total = 0
csv = []
csv_total = []
for i,file in enumerate(files):
    print(f"{2012+i}")
    df = pd.read_json(file, orient='records', lines=True)
    categories = df["category"].to_list()
    correct += df["count"].sum()
    total += df["total_count"].sum()
    
    for k in range(9):
        tmp = 0
        tmp_total = 0
        tmp += df.iloc[k,1]
        tmp_total += df.iloc[k,2]
        print(k,":", categories[k], tmp,"/",tmp_total,"=",tmp/tmp_total)

    csv.append(df["count"].tolist())
    csv_total.append(df["total_count"].tolist())


print(correct,"/",total,"=",correct/total)
print("Total")
print(csv_total)
print("Correct")
print(csv)
pd.DataFrame(csv).to_csv("calc.csv",index=False,header=None)
import pandas as pd
import glob


model_name = "SakanaAI_TinySwallow"
# model_name = "EQUES_TinySwallow"
# model_name = "Qwen_Qwen2.5"
# model_name = "bespokelabs_Bespoke"

files = sorted(glob.glob(f"/home/sukeda/work/YakugakuQA/baseline_results/*_{model_name}*_count.jsonl"))
print(len(files))
correct = 0
total = 0
chemistry = 0
chemistry_total = 0
physics = 0
physics_total = 0
for file in files:
    df = pd.read_json(file, orient='records', lines=True)
    correct += df["count"].sum()
    total += df["total_count"].sum()
    physics += df.iloc[7,1]
    physics_total += df.iloc[7,2]
    chemistry += df.iloc[1,1]
    chemistry_total += df.iloc[1,2]
    # chemistry += df["count"]


print(correct,total)
print(correct/total)
print("Chem", chemistry,"/",chemistry_total,"=",chemistry/chemistry_total)
print("Physics", physics, "/", physics_total,"=",physics/physics_total)

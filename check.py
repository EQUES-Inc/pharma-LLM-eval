import pandas as pd

year = "097"
answer_file = f"./data/2012/{year}.jsonl"
answer_df = pd.read_json(answer_file, orient='records', lines=True)

meta_file = f"./data/2012/metadata_{year}.jsonl"
meta_df = pd.read_json(meta_file, orient='records', lines=True).iloc[:345,:]

response_file = f"./baseline_results/{year}_EQUES_dare_ties.jsonl"
response_df = pd.read_json(response_file, orient='records', lines=True)

own_category_file = f"./data/data_evalated.jsonl"
own_category_df = pd.read_json(own_category_file, orient='records', lines=True)


compare = pd.DataFrame(columns=["problem_id","correct","response"])
compare["problem_id"] = answer_df["problem_id"]
compare["correct"] = answer_df["answer"].apply(lambda x : ",".join(x))
compare["response"] = response_df["prediction"]


judge = []
for i,v in compare.iterrows():
    if v["correct"] == v["response"]:
        judge.append(1)
    else:
        judge.append(0)
compare["judge"] = judge
compare["text_only"] = answer_df["text_only"]
compare["category"] = meta_df["category"]

compare = pd.merge(compare, own_category_df, left_on="problem_id", right_on="id", how="left")
compare.drop(["id"],inplace=True,axis=1)



print("="*10)
print(compare)
print("="*10)
print("fullの総数:",len(compare))
print("fullの正答数:",compare["judge"].sum())

print("="*10)
print("text_onlyの総数:", len(compare[compare["text_only"]==True]))
print("text_onlyの正答数:", compare[compare["text_only"]==True]["judge"].sum())

print("="*10)


compare.to_csv("check.csv",index=False)

df  = compare[compare["text_only"]==True]


candidates = {0:"category", 1:"専門性", 2: "難易度", 3:"複雑な推論・計算", 4:"選択肢類似性"}
interest = candidates[0]
print(df[["judge",interest]].groupby(interest).mean())
interest = candidates[2]
print(df[["judge",interest]].groupby(interest).mean())
interest = candidates[3]
print(df[["judge",interest]].groupby(interest).mean())
interest = candidates[4]
print(df[["judge",interest]].groupby(interest).mean())
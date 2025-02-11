import argparse, os
from utils.tools import read_jsonl, check_jsonls
import jsonlines
import pandas as pd

def get_category_data(categories, category_name):
    for category in categories:
        if category["category"] == category_name:
            return category
    return None

def evaluate(pred_file, gold_file, meta_file, text_only):
    # カテゴリごとの情報を持つリスト形式に変更
    categories = [
        {"category": "Biology", "count": 0, "total_count": 0, "accuracy": 0},
        {"category": "Chemistry", "count": 0, "total_count": 0, "accuracy": 0},
        {"category": "Hygiene", "count": 0, "total_count": 0, "accuracy": 0},
        {"category": "Law", "count": 0, "total_count": 0, "accuracy": 0},
        {"category": "Pathology", "count": 0, "total_count": 0, "accuracy": 0},
        {"category": "Pharmacology", "count": 0, "total_count": 0, "accuracy": 0},
        {"category": "Pharmacy", "count": 0, "total_count": 0, "accuracy": 0},
        {"category": "Physics", "count": 0, "total_count": 0, "accuracy": 0},
        {"category": "Practice", "count": 0, "total_count": 0, "accuracy": 0}
    ]
    preds = read_jsonl(pred_file)
    golds = read_jsonl(gold_file)
    metas = read_jsonl(meta_file)
    check_jsonls(preds, golds)
    results= accuracy(categories, preds, golds, metas, text_only)
    
    # 各カテゴリごとのaccuracyを計算
    for category in categories:
        if category["total_count"] > 0:
            category["accuracy"] = category["count"] / category["total_count"]
        else:
            category["accuracy"] = 0  # total_countが0の場合はaccuracyを0とする

    print(results)
    print(categories)
    count_file = pred_file.replace('.jsonl', '_count.jsonl')

    with jsonlines.open(count_file, mode='w') as fout:
        print("count_file")
        fout.write_all(categories)

    return count_file

def counting(categories, pred, ans, categ):
    prediction = pred["prediction"]
    prediction = sorted(x.strip() for x in prediction.split(','))
    gold = ans["answer"]
    gold = sorted(gold)
    category_name = categ["category"]
    points = int(ans["points"])
    print(ans['problem_id'])
    bool = False
    
    if prediction == gold:
        category_data = get_category_data(categories, category_name)
        bool = True
        if category_data:
            category_data["count"] += points
            
    category_data = get_category_data(categories, category_name)
    if category_data:
        category_data["total_count"] += points

    print(f"推論：{prediction}, 正解：{gold}, 判定：" + ("○" if bool else "×"))

    return

def accuracy(categories, preds, golds, metas, text_only):
    
    for pred, ans, categ in zip(preds, golds, metas):
        textonly = ans["text_only"]
        if text_only:
            if textonly:
                counting(categories, pred, ans, categ)
        else:
            counting(categories, pred, ans, categ)
    return

def excel_output(result, years, config, out_dir):

    counted = []

    for year, out_file_count in zip(years,result):
        print(year)
        out_count = read_jsonl(out_file_count)
        df = pd.DataFrame(out_count)
        # 行を "count", "total_count", "accuracy" に変換
        df = df.set_index('category').T
        year_list = [year, year, year]
        # "year" 列を先頭に挿入
        df.insert(0, 'year', year_list)  # 0 は挿入位置
        counted.append(df)

    # 複数のデータフレームを結合
    df_combined = pd.concat(counted)
    print(df_combined)

    # インデックスの名前を確認
    print(df_combined.index.names)
    print("df_combined columns:", df_combined.columns)

    # 列インデックス名が 'category' であることを確認
    if df_combined.columns.name == 'category':

        # 現在の行インデックスをリセットしてデータ列に戻す
        df_reset = df_combined.reset_index()
        print(df_reset.head())

        # マルチインデックスを設定する
        df_multi = df_reset.set_index(['index', 'year'], append=True)
        print(df_multi)

        # インデックスでソートする
        df_sorted = df_multi.sort_index(level=['index', 'year'], ascending=[False, True])
        print(df_sorted)

        # Excelに出力
        new_config = config.replace("/", "_")
        out_file = new_config + ".xlsx"
        out_file = os.path.join(out_dir, out_file)
        print(out_file)
        df_sorted.to_excel(out_file, index=True)  # index=Falseでインデックスを出力しない
        print(f"Excelファイル {out_file} が作成されました。")
    else:
        print("エラー: 'category' が列インデックスの名前として設定されていません。")
    


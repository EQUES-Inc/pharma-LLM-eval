import argparse, os
from utils.tools import read_jsonl, answer2jsonl, check_jsonls

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

def get_category_data(category_name):
    for category in categories:
        if category["category"] == category_name:
            return category
    return None

def main(pred_file, gold_file, meta_file, text_only):
    preds = read_jsonl(pred_file)
    golds = read_jsonl(gold_file)
    metas = read_jsonl(meta_file)
    check_jsonls(preds, golds)
    results, cat = accuracy(preds, golds, metas, text_only)
    
    # 各カテゴリごとのaccuracyを計算
    for category in categories:
        if category["total_count"] > 0:
            category["accuracy"] = category["count"] / category["total_count"]
        else:
            category["accuracy"] = 0  # total_countが0の場合はaccuracyを0とする

    print(results)
    print(categories)

def evaluate(pred, ans, categ, correct, count, score, total):
    prediction = pred["prediction"]
    prediction = sorted(prediction.split(','))
    gold = sorted(ans["answer"])
    category_name = categ["category"]
    points = int(ans["points"])
    
    if prediction == gold:
        correct += 1
        score += points
        category_data = get_category_data(category_name)
        if category_data:
            category_data["count"] += 1
            
    count += 1
    total += points
    category_data = get_category_data(category_name)
    if category_data:
        category_data["total_count"] += 1

    return correct, count, score, total

def accuracy(preds, golds, metas, text_only):
    count = 0
    correct = 0
    total = 0
    score = 0
    
    for pred, ans, categ in zip(preds, golds, metas):
        textonly = ans["text_only"]
        if text_only:
            if textonly:
                correct, count, score, total = evaluate(pred, ans, categ, correct, count, score, total)
        else:
            correct, count, score, total = evaluate(pred, ans, categ, correct, count, score, total)
    
    return {'accuracy': correct / count if count > 0 else 0, 'score': score, 'total': total}, categories

if __name__ == '__main__':
    parser = argparse.ArgumentParser(allow_abbrev=False)

    parser.add_argument('--pred-file', type=str, metavar='N',
                        default='', help='prediction file')
    parser.add_argument('--gold-file', type=str, metavar='N',
                        default='', help='gold file')
    parser.add_argument('--meta-file', type=str, metavar='N',
                        default='', help='meta file')
    parser.add_argument('--text-only', action='store_true', help='text only')
    args = parser.parse_args()
    main(args.pred_file, args.gold_file, args.meta_file, args.text_only)


import argparse
import os

from utils.tools import answer2jsonl, check_jsonls, read_jsonl

nested_dict ={'Biology': {"count": 0, "total_count": 0},
 'Chemistry': {"count": 0, "total_count": 0},
 'Hygiene': {"count": 0, "total_count": 0},
 'Law': {"count": 0, "total_count": 0},
 'Pathology': {"count": 0, "total_count": 0},
 'Pharmacology': {"count": 0, "total_count": 0},
 'Pharmacy': {"count": 0, "total_count": 0},
 'Physics': {"count": 0, "total_count": 0},
 'Practice': {"count": 0, "total_count": 0}}

def main(pred_file, gold_file, meta_file, text_only):
    preds = read_jsonl(pred_file)
    golds = read_jsonl(gold_file)
    metas = read_jsonl(meta_file)
    check_jsonls(preds, golds)
    results, cat = accuracy(preds, golds, metas, text_only)
    print(results)
    print(cat)

def evaluate(pred, ans, categ, correct, count, score, total):
    prediction = pred["prediction"]
    prediction = sorted(prediction.split(','))
    gold = sorted(ans["answer"])
    category = categ["category"]
    points = int(ans["points"])
    if prediction == gold:
        correct += 1
        score += points
        nested_dict[category]["count"] += 1
    count += 1
    total += points
    nested_dict[category]["total_count"] += 1

    return correct, count, score, total

def accuracy(preds, golds, metas, text_only):
    count = 0
    correct = 0
    total = 0
    score = 0
    for pred, ans, categ in zip(preds, golds, metas):
        textonly= ans["text_only"]

        if text_only:
            if textonly:
                correct, count, score, total =evaluate(pred, ans, categ, correct, count, score, total)
        else:
            correct, count, score, total = evaluate(pred, ans, categ, correct, count, score, total)

    return {'accuracy': correct/count, 'score': score, 'total': total}, nested_dict


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

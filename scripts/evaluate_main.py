import argparse
import os

from utils.tools import answer2jsonl, check_jsonls, read_jsonl


def main(pred_file, gold_file, text_only):
    preds = read_jsonl(pred_file)
    golds = read_jsonl(gold_file)
    check_jsonls(preds, golds)
    results = accuracy(preds, golds, text_only)
    print(results)

def evaluate(pred, ans, correct, count, score, total):
    prediction = pred["prediction"]
    prediction = sorted(prediction.split(','))
    gold = sorted(ans["answer"])
    points = int(ans["points"])
    print(ans["problem_id"], prediction, gold)
    if ans["problem_id"] == "116A71":
        correct += 1
        score += points
    elif ans["problem_id"] == "112B30" and (prediction == ["a"] or prediction == ["d"]):
        correct += 1
        score += points
    elif prediction == gold:
        correct += 1
        score += points
    count += 1
    total += points

    return correct, count, score, total

def accuracy(preds, golds, text_only):
    #print("1" + str(text_only))
    count = 0
    correct = 0
    total = 0
    score = 0
    for pred, ans in zip(preds, golds):
        textonly= ans["text_only"]
        #print("2" + str(textonly))

        if text_only:
            if textonly:
                correct, count, score, total =evaluate(pred, ans, correct, count, score, total)
        else:
            correct, count, score, total = evaluate(pred, ans, correct, count, score, total)

    return {'accuracy': correct/count, 'score': score, 'total': total}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(allow_abbrev=False)

    parser.add_argument('--pred-file', type=str, metavar='N',
                        default='', help='prediction file')
    parser.add_argument('--gold-file', type=str, metavar='N',
                        default='', help='gold file')
    parser.add_argument('--text-only', action='store_true', help='text only')
    args = parser.parse_args()
    main(args.pred_file, args.gold_file, args.text_only)

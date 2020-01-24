import sys
import argparse
import logging

from gensim.models import word2vec


def parse_arg():
    parser = argparse.ArgumentParser(description="Calc word operation.")
    parser.add_argument("-m", "--model", type=str, nargs=1,
                        help="Word2Vec model.")
    parser.add_argument("equation", type=str,
                        help="equation like 猫-犬+男性")
    return parser.parse_args()


def neighbor_word(posi, nega=[], n=10):
    count = 1
    result = model.most_similar(positive=posi, negative=nega, topn=n)
    for r in result:
        print(str(count)+" "+str(r[0])+" "+str(r[1]))
        count += 1


def calc(equation):
    if "+" not in equation or "-" not in equation:
        neighbor_word([equation])
    else:
        posi, nega = [], []
        positives = equation.split("+")
        for positive in positives:
            negatives = positive.split("-")
            posi.append(negatives[0])
            nega = nega + negatives[1:]
        neighbor_word(posi=posi, nega=nega)


def main():
    args = parse_arg()
    model = word2vec.Word2Vec.load(args.model[0])
    calc(args.equation)


if __name__ == "__main__":
    main()

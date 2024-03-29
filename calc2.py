import sys
import argparse
import logging

from gensim.models import word2vec


def parse_arg():
    parser = argparse.ArgumentParser(description="Calc word operation.")
    parser.add_argument("-m", "--model", type=str, nargs=1, help="Word2Vec model.")
    parser.add_argument("equation", type=str, help="equation like 猫-犬+男性")
    return parser.parse_args()


def neighbor_word(model, posi, nega=[], n=20):
    count = 1
    result = model.wv.most_similar(positive=posi, negative=nega, topn=n)
    for r in result:
        print(str(count) + " " + str(r[0]) + " " + str(r[1]))
        count += 1


def calc(model, equation):
    posi, nega = [], []
    pos_terms = equation.split("+")
    for term in pos_terms:
        tokens = term.split("-")
        posi.extend(tokens[:1])
        nega.extend(tokens[1:])
    neighbor_word(model, posi=posi, nega=nega)


def main():
    args = parse_arg()
    model = word2vec.Word2Vec.load(args.model[0])
    calc(model, args.equation)


if __name__ == "__main__":
    main()

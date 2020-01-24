# -*- coding: utf-8 -*-

import sys
import argparse

from gensim.models import word2vec


def parse_arg():
    parser = argparse.ArgumentParser(description="Similarity calculation.")
    parser.add_argument("-m", "--model", type=str, nargs=1,
                        help="Word2Vec model.")
    parser.add_argument("-n", "--num", type=int, default=10,
                        help="the number of similar words to be shown as a result.")
    parser.add_argument("WORDS", type=str, nargs='+',
                        help="words for searching similar words.")
    return parser.parse_args()


def main():
    args = parse_arg()
    model = word2vec.Word2Vec.load(args.model[0])
    for w in args.WORDS:
        results = model.most_similar(positive=w, topn=args.num)
        for result in results:
            print(result[0], '\t', result[1])


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-

import sys
import argparse
import logging

from gensim.models import word2vec


def parse_arg():
    parser = argparse.ArgumentParser(description="Calculate Word2Vec.")
    parser.add_argument("-i", "--input", type=str, nargs=1, help="wakati-gaki text.")
    parser.add_argument("-o", "--output", type=str, nargs=1, help="file to which resulting model will be saved.")
    parser.add_argument("-d", "--dimension", type=int, default=100, help="dimension of vector.")
    parser.add_argument("-w", "--window_size", type=int, default=10, help="skip-gram window.")
    return parser.parse_args()


def main():
    args = parse_arg()
    logging.basicConfig(format="%(asctime)s : %(levelname)s : %(message)s", level=logging.INFO)
    sentences = word2vec.LineSentence(args.input[0])
    model = word2vec.Word2Vec(
        sentences, sg=1, vector_size=args.dimension, min_count=1, window=args.window_size, hs=1, negative=0
    )
    model.save(args.output[0])


if __name__ == "__main__":
    main()

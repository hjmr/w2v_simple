import sys
import argparse

import numpy as np
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
from gensim.models import word2vec


def parse_arg():
    parser = argparse.ArgumentParser(description="Draw word2vec model.")
    parser.add_argument("-m", "--model", type=str, nargs=1, help="Word2Vec model.")
    parser.add_argument("-s", "--skip", type=int, default=0, help="the number of words to skip.")
    parser.add_argument("-n", "--num", type=int, default=200, help="the number of words to plot.")
    parser.add_argument("--font_size", type=int, default=24, help="font size.")
    parser.add_argument("--width", type=int, default=40, help="plot width.")
    parser.add_argument("--height", type=int, default=40, help="plot height.")
    parser.add_argument("equation", type=str, help="equation like 猫-犬+男性")
    return parser.parse_args()


def get_converter(x):
    converter = TSNE(n_components=2, random_state=0)
    np.set_printoptions(suppress=True)
    converter.fit_transform(x)
    return converter


def plot(vocab, skip, num, converter, width, height, font_size):
    plt.rcParams["font.size"] = font_size
    plt.figure(figsize=(width, height))  # 図のサイズ
    plt.scatter(converter.embedding_[skip:skip+num-1, 0],
                converter.embedding_[skip:skip+num-1, 1])

    count = 0
    for label, x, y in zip(vocab, converter.embedding_[:, 0], conveter.embedding_[:, 1]):
        count += 1
        if(count <= skip):
            continue
        plt.annotate(label, xy=(x, y), xytext=(0, 0), textcoords='offset points')
        if(count == skip + num):
            break
    plt.show()


def main():
    args = parse_arg()
    word2vec_model = word2vec.Word2Vec.load(args.model[0])

    vocab = word2vec_model.wv.vocab
    emb_tuple = tuple([word2vec_model[v] for v in vocab])
    converter = get_converter(np.vstack(emb_tuple))

    plot(vocab, args.skip, args.num, converter, args.width, args.height, args.font_size)


if __name__ == "__main__":
    main()

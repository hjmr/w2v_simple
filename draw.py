import sys
import argparse
import collections

import numpy as np
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
import japanize_matplotlib
from gensim.models import word2vec


def parse_arg():
    parser = argparse.ArgumentParser(description="Draw word2vec model.")
    parser.add_argument("-m", "--model", type=str, nargs=1, help="Word2Vec model.")
    parser.add_argument("-s", "--skip", type=int, default=0, help="the number of words to skip.")
    parser.add_argument("-n", "--num", type=int, default=200, help="the number of words to plot.")
    parser.add_argument("-o", "--output", type=str, help="Save figure to the file.")
    parser.add_argument("--plot_original", action="store_true", help="plot original vocabs in gray dots.")
    parser.add_argument("--font_size", type=int, default=24, help="font size.")
    parser.add_argument("--width", type=int, default=40, help="plot width.")
    parser.add_argument("--height", type=int, default=40, help="plot height.")
    parser.add_argument("wakati_files", type=str, nargs="*", help="wakati files to be plotted.")
    return parser.parse_args()


def get_converter(x):
    converter = PCA(random_state=0)
    converter.fit(x)
    return converter


def make_plot(model, conv, vocab_list, plot_orig, orig_vocab, skip, num, width, height, font_size):
    plt.rcParams["font.size"] = font_size
    fig = plt.figure(figsize=(width, height))  # 図のサイズ
    cmap = ["red", "blue", "green", "magenta", "cyan", "yellow", "black"]

    if plot_orig:
        orig_pos = [model.wv[v] for v in orig_vocab]
        emb_pos = conv.transform(orig_pos)
        plt.scatter(emb_pos[:, 0], emb_pos[:, 1], c="gray")

    for i, vocab in enumerate(vocab_list):
        available_vocab = []
        orig_pos = []
        for j in range(skip, len(vocab)):
            try:
                p = model.wv[vocab[j]]
                available_vocab.append(vocab[j])
                orig_pos.append(p)
            except:
                continue

        emb_pos = conv.transform(orig_pos)
        plt.scatter(emb_pos[:, 0], emb_pos[:, 1], c=cmap[i % len(cmap)])
        for label, x, y in zip(available_vocab, emb_pos[:, 0], emb_pos[:, 1]):
            plt.annotate(label, xy=(x, y), xytext=(0, 0), textcoords='offset points')
    return fig


def vocab_from_file(wakati_file):
    v = []
    with open(wakati_file, "r") as f:
        for line in f:
            v.extend(line.strip().split(" "))
    c = collections.Counter(v)
    v, _ = zip(*c.most_common())
    return v


def main():
    args = parse_arg()
    w2v_model = word2vec.Word2Vec.load(args.model[0])

    vocab = w2v_model.wv.index2word
    emb_tuple = tuple([w2v_model.wv[v] for v in vocab])
    converter = get_converter(np.vstack(emb_tuple))

    orig_vocab = vocab if args.plot_original else None

    if 0 < len(args.wakati_files):
        vocab_list = [vocab_from_file(f) for f in args.wakati_files]
    else:
        vocab_list = [vocab]

    fig = make_plot(w2v_model, converter, vocab_list,
                    args.plot_original, orig_vocab,
                    args.skip, args.num,
                    args.width, args.height, args.font_size)

    if args.output is not None:
        fig.savefig(args.output)
    else:
        fig.show()
        input('press enter')


if __name__ == "__main__":
    main()

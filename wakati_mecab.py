# -*- coding: utf-8 -*-

import sys
import argparse

import MeCab


def parse_arg():
    parser = argparse.ArgumentParser(description="Convert japanese text into Wakati-gaki text.")
    parser.add_argument("-i", "--input", type=str, nargs=1,
                        help="japanese text.")
    parser.add_argument("-o", "--output", type=str,
                        help="file to which resulting wakati-gaki text will be saved.")
    parser.add_argument("-d", "--dictionary", type=str,
                        help="specify dictionary for MeCab.")
    parser.add_argument("-p", "--pos", type=str, default="名詞,動詞",
                        help="comma seperated part-of-speech like 名詞,動詞")
    return parser.parse_args()


def main():
    args = parse_arg()
    pos = args.pos.split(",")

    if args.dictionary is not None:
        t = MeCab.Tagger("-d {}".format(args.dictionary))
    else:
        t = MeCab.Tagger("")
    t.parse("")  # to avoid bug

    with open(args.input[0], "r") as fi:
        for line in fi:
            word_list = []
            token = t.parseToNode(line.strip())
            while token:
                features = token.feature.split(",")
                p = features[0]
                if p in pos:
                    w = features[6] if 0 < len(features[6]) else token.surface
                    word_list.append(w)
                token = token.next
    wakati = " ".join(word_list)
    if args.output is not None:
        with open(args.output, "w") as fo:
            fo.write(wakati)
    else:
        print(wakati)


if __name__ == "__main__":
    main()

# -*- coding: utf-8 -*-

import sys
import argparse

from janome.tokenizer import Tokenizer


def parse_arg():
    parser = argparse.ArgumentParser(description="Convert japanese text into Wakati-gaki text.")
    parser.add_argument("-i", "--input", type=str, nargs=1,
                        help="japanese text.")
    parser.add_argument("-o", "--output", type=str,
                        help="file to which resulting wakati-gaki text will be saved.")
    parser.add_argument("-p", "--pos", type=str, default="名詞,動詞",
                        help="comma seperated part-of-speech like 名詞,動詞")
    return parser.parse_args()


def main():
    args = parse_arg()
    pos = args.pos.split(',')

    t = Tokenizer()
    with open(args.input[0], "r") as fi:
        for line in fi:
            token_list = t.tokenize(line.strip())
            word_list = []
            for token in token_list:
                p = token.part_of_speech.split(',')[0]
                if p in pos:
                    word_list.append(token.base_form)
    wakati = ' '.join(word_list)
    if args.output is not None:
        with open(args.output, "w") as fo:
            fo.write(wakati)
    else:
        print(wakati)


if __name__ == "__main__":
    main()

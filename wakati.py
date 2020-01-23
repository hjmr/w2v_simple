# -*- coding: utf-8 -*-

from janome.tokenizer import Tokenizer
import sys

t = Tokenizer()

fi = open(sys.argv[1], 'r')
fo = open(sys.argv[2], 'w')

line = fi.readline()
while line:
    token_list = t.tokenize(line.strip())
    word_list = []
    for token in token_list:
        pos = token.part_of_speech.split(',')[0]
        if pos == '名詞' or pos == '動詞' or pos == '形容詞' or pos == '形容動詞':
            word_list.append(token.base_form)
    fo.write(' '.join(word_list))
    line = fi.readline()

fi.close()
fo.close()

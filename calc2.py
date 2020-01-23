from gensim.models import word2vec
import logging
import sys

model = word2vec.Word2Vec.load(sys.argv[1])

def neighbor_word(posi, nega=[], n=20):
    count = 1
    result = model.most_similar(positive = posi, negative = nega, topn = n)
    for r in result:
        print(str(count)+" "+str(r[0])+" "+str(r[1]))
        count += 1


def calc(equation):
    posi,nega = [],[]
    pos_terms = equation.split('+')
    for term in pos_terms:
        tokens = term.split('-')
        posi.extend(tokens[:1])
        nega.extend(tokens[1:])
    neighbor_word(posi = posi, nega = nega)

if __name__=="__main__":
    equation = sys.argv[2]
    calc(equation)

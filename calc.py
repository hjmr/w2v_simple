from gensim.models import word2vec
import logging
import sys

model = word2vec.Word2Vec.load(sys.argv[1])


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


if __name__ == "__main__":
    equation = sys.argv[2]
    calc(equation)

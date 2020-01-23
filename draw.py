import sys
import matplotlib.pyplot as plt 
from sklearn.manifold import TSNE
import numpy as np
from gensim.models import word2vec

word2vec_model = word2vec.Word2Vec.load(sys.argv[1])

#取り出す単語の範囲を指定
skip=0
limit=200 #よく出る241単語のみをプロットする

#word2vecの結果をt-SNEで次元圧縮
vocab = word2vec_model.wv.vocab
emb_tuple = tuple([word2vec_model[v] for v in vocab])
X = np.vstack(emb_tuple)

print('fitting.')

model = TSNE(n_components=2, random_state=0)
np.set_printoptions(suppress=True)
model.fit_transform(X) 

print('plotting.')

#matplotlibでt-SNEの図を描く
plt.rcParams["font.size"] =24
plt.figure(figsize=(40,40))#図のサイズ
plt.scatter(model.embedding_[skip:limit, 0], model.embedding_[skip:limit, 1])

count = 0
for label, x, y in zip(vocab, model.embedding_[:, 0], model.embedding_[:, 1]):

    count +=1
    if(count<skip):continue
    plt.annotate(label, xy=(x, y), xytext=(0, 0), textcoords='offset points')
    if(count==limit):break
plt.show()


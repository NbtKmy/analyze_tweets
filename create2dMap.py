from gensim.models import Word2Vec
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import japanize_matplotlib

def createPlot(w):
    model = Word2Vec.load('./models/tweetsOlympic_202103.model')
    words = model.wv.most_similar(positive=[w], topn=20)

    wordlist = []
    wordvecs = []
    for word in words:
        wrd = word[0]
        wordlist.append(wrd)
        wordvecs.append(model.wv[wrd])
    
    pca = PCA(n_components=2)
    pca.fit(wordvecs)
    X_2d = pca.transform(wordvecs)


    fig = plt.figure(figsize = (10, 10))
    ax = fig.add_subplot(111)
    ax.grid()

    wordlen = len(wordlist)
    for i in range(wordlen):
        plt.plot(X_2d[i][0], X_2d[i][1], ms=5.0, zorder=2, marker='o')
        plt.annotate(wordlist[i], (X_2d[i][0], X_2d[i][1]))

    
    plt.ioff()
    plt.savefig("w2v_plot_202103.png")

if __name__ == "__main__":
    createPlot('五輪')
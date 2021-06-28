from gensim.models import word2vec

def useModel(word, mod):

    model = word2vec.Word2Vec.load(mod)
    words = model.wv.most_similar(positive=[word])

    res = 'Similar words to ' + word
    for w in words:
        res = res + '\n' + w[0] + ': ' + str(w[1])

    print(res)

if __name__ == "__main__":
    path_to_model = './models/model_202101/'
    modelname = 'tweetsOlympic_202101.model'
    model = path_to_model + modelname
    useModel('コロナ', model)
from gensim.models import word2vec
import logging
import pickle

def createModel(corp):
    logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

    # corpus aus pickle
    with open(corp, mode='rb') as f:
        sentences = pickle.load(f)

    # Wenn man .txt daten verwendet hier:
    #sentences = word2vec.LineSentence(corp)

    # skip-gram & hierarchical softmax verwenden
    model = word2vec.Word2Vec(sentences, sg=1, size=100, min_count=3, window=5, hs=1) 
    
    model.save('tweetsOlympic_202103.model')

if __name__ == "__main__":
    createModel('./corpus_202103.pickle')
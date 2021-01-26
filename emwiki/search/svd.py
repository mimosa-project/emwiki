from gensim import models, corpora, similarities
import pickle

def singular_value_analysis(input_txt):
    doc = []
    doc_append = doc.append
    with open(input_txt) as f:
        lines = f.readlines()
        for line in lines:
            doc_append(line.split())

    dictionary = corpora.Dictionary(doc)
    dictionary.save('search/data/search_dictionary.dict')

    # BoW表現に変換
    bow_corpus = [dictionary.doc2bow(d) for d in doc]

    # ベクトル化した文書をTF-IDF表現に変換
    tfidf_model = models.TfidfModel(bow_corpus) 
    tfidf_corpus = tfidf_model[bow_corpus] 

    tfidf_model.save('search/data/tfidf.model')
    corpora.MmCorpus.serialize('search/data/tfidf_corpus.mm', tfidf_corpus)

    # 作成したコーパスと辞書からLSIモデルを作成
    # LSIモデルから次元圧縮したコーパスを作成
    lsi_model = models.LsiModel(tfidf_corpus, id2word=dictionary, num_topics=300) 
    lsi_corpus = lsi_model[tfidf_corpus]

    lsi_model.save('search/data/lsi_topics300.model')

    # 類似度を求めるためのindexの作成
    index = similarities.MatrixSimilarity(lsi_corpus)
    index.save('search/data/lsi_index.index')

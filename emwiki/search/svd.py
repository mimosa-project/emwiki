import os
from gensim import models, corpora, similarities
from django.conf import settings


def singular_value_analysis(input_txt):
    doc = []
    doc_append = doc.append
    with open(input_txt) as f:
        lines = f.readlines()
        for line in lines:
            doc_append(line.split())

    dictionary = corpora.Dictionary(doc)
    dictionary.save(os.path.join(
        settings.SEARCH_INDEX_DIR, 'search_dictionary.dict'))

    # BoW表現に変換
    bow_corpus = [dictionary.doc2bow(d) for d in doc]

    # ベクトル化した文書をTF-IDF表現に変換
    tfidf_model = models.TfidfModel(bow_corpus)
    tfidf_corpus = tfidf_model[bow_corpus]

    tfidf_model.save(os.path.join(settings.SEARCH_INDEX_DIR, 'tfidf.model'))
    corpora.MmCorpus.serialize(os.path.join(
        settings.SEARCH_INDEX_DIR, 'tfidf_corpus.mm'), tfidf_corpus)

    # 作成したコーパスと辞書からLSIモデルを作成
    # LSIモデルから次元圧縮したコーパスを作成
    lsi_model = models.LsiModel(
        tfidf_corpus, id2word=dictionary, num_topics=300)
    lsi_corpus = lsi_model[tfidf_corpus]

    lsi_model.save(os.path.join(settings.SEARCH_INDEX_DIR, 'lsi_topics300.model'))

    # 類似度を求めるためのindexの作成
    index = similarities.MatrixSimilarity(lsi_corpus)
    index.save(os.path.join(settings.SEARCH_INDEX_DIR, 'lsi_index.index'))

import os
import pickle
import re

from gensim import corpora, models, similarities

from django.conf import settings
from search.parse_abs import process_for_search_word


class TheoremSearcher:
    def search(self, search_word, count_top, index_dir=None):
        if not index_dir:
            index_dir = settings.SEARCH_INDEX_DIR

        tfidf = models.TfidfModel.load(
            os.path.join(index_dir, 'tfidf.model'))
        lsi = models.LsiModel.load(os.path.join(
            index_dir, 'lsi_topics300.model'))
        dictionary = corpora.Dictionary.load(os.path.join(
            index_dir, 'search_dictionary.dict'))

        index = similarities.MatrixSimilarity.load(
            os.path.join(index_dir, 'lsi_index.index'))

        query_vector = dictionary.doc2bow(process_for_search_word(search_word).split())

        vec_lsi = lsi[tfidf[query_vector]]
        sims = index[vec_lsi]

        sims = sorted(enumerate(sims), key=lambda item: -item[1])
        result = []
        result_append = result.append

        with open(os.path.join(index_dir, 'tell.pkl'), "rb") as f:
            tell = pickle.load(f)

        for idx in sims[:count_top]:
            search_result = {}
            with open(os.path.join(index_dir, 'abs_dictionary.txt'), "rb") as f:
                f.seek(tell[idx[0]])
                doc_list = f.read(
                    tell[idx[0] + 1] - tell[idx[0]]).decode('utf-8').split()

            # doc_list[0] : theorem or definition
            #         [1] : line
            #         [2] : file_name
            #         [3] : label
            #         [4::] : text
            search_result["label"] = (doc_list[3])
            search_result["text"] = (" ".join(doc_list[4::]))
            search_result["relevance"] = "{:.2f}".format(idx[1])
            search_result["filename"] = (doc_list[2])
            search_result["line_no"] = (doc_list[1])

            result_append(search_result)

        # URLを生成
        for res in result:
            filename, anchor = res['label'].split(':')
            if re.match('def', anchor):
                anchor = anchor.replace('def', 'D')
            else:
                anchor = f"T{anchor}"
            urldict = {'url': f'{filename.lower()}#{anchor}'}
            res.update(urldict)

        return result

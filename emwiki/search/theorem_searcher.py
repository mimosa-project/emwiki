from gensim import corpora, models, similarities
from search.parse_abs import is_variable, processing_variables_with_emparser
import re
import pickle
from collections import defaultdict


class TheoremSearcher:
    def search(self, search_word, count_top):

        search_word = search_word.replace(",", " ")
        search_word = search_word.replace(";", "")
        input_doc = processing_variables_with_emparser(search_word.split())
        input_doc = input_doc.split()

        tfidf = models.TfidfModel.load('search/data/tfidf.model') 
        lsi = models.LsiModel.load('search/data/lsi_topics300.model')
        dictionary = corpora.Dictionary.load('search/data/search_dictionary.dict')

        index = similarities.MatrixSimilarity.load('search/data/lsi_index.index')

        query_vector = dictionary.doc2bow(input_doc)

        vec_lsi = lsi[tfidf[query_vector]]
        sims = index[vec_lsi]
    
        sims = sorted(enumerate(sims), key=lambda item: -item[1])
        result = []
        result_append = result.append

        with open("search/data/tell.pkl", "rb") as f:
            tell = pickle.load(f)

        for idx in sims[:count_top]:
            search_result = {}
            with open("search/data/abs_dictionary.txt", "rb") as f:
                f.seek(tell[idx[0]])
                doc_list = f.read(tell[idx[0]+1]-tell[idx[0]]).decode('utf-8').split()

            # doc_list[0] : theorem or definition
            #         [1] : line
            #         [2] : file_name
            #         [3] : label
            #         [4::] : text
            search_result["label"] = (doc_list[3])
            search_result["text"] = (" ".join(doc_list[4::]))
            search_result["relevance"] = (idx[1])
            search_result["filename"] = (doc_list[2])
            search_result["line_no"] = (doc_list[1])
    
            result_append(search_result)

        ##並べ替え
        result = sorted(result, key=lambda x:x['relevance'], reverse=True)

        # URLを生成
        for res in result:
            url = 'http://mizar.org/version/current/html/' + res['label'].split(':')[0].lower() + '.html#t' + res['label'].split(':')[1]
            urldict = {'url': url}
            res.update(urldict)


        return result

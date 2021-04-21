from collections import defaultdict
import os
import pickle
import re

from django.urls import reverse
from gensim import corpora, models, similarities

from emwiki.settings import DATA_FOR_SEARCH_DIR, VCT_DIR
from search.parse_abs import is_variable, lexer, rename_variable_and_symbol

class TheoremSearcher:
    def search(self, search_word, count_top):
        search_word = search_word.replace(",", " ")
        search_word = search_word.replace(";", "")
        input_doc = rename_variable_and_symbol(search_word.split(), lexer)
        input_doc = input_doc.split()

        tfidf = models.TfidfModel.load(os.path.join(DATA_FOR_SEARCH_DIR, 'tfidf.model')) 
        lsi = models.LsiModel.load(os.path.join(DATA_FOR_SEARCH_DIR, 'lsi_topics300.model'))
        dictionary = corpora.Dictionary.load(os.path.join(DATA_FOR_SEARCH_DIR, 'search_dictionary.dict'))

        index = similarities.MatrixSimilarity.load(os.path.join(DATA_FOR_SEARCH_DIR, 'lsi_index.index'))

        query_vector = dictionary.doc2bow(input_doc)

        vec_lsi = lsi[tfidf[query_vector]]
        sims = index[vec_lsi]
    
        sims = sorted(enumerate(sims), key=lambda item: -item[1])
        result = []
        result_append = result.append

        with open(os.path.join(DATA_FOR_SEARCH_DIR, 'tell.pkl'), "rb") as f:
            tell = pickle.load(f)

        for idx in sims[:count_top]:
            search_result = {}
            with open(os.path.join(DATA_FOR_SEARCH_DIR, 'abs_dictionary.txt'), "rb") as f:
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

        # URLを生成
        for res in result:
            filename, anchor = res['label'].split(':')
            path = reverse('article:index', kwargs=dict(filename=filename.lower()))
            if re.match('def', anchor):
                anchor = anchor.replace('def', 'D')
            else:
                anchor = f"T{anchor}"
            urldict = {'url': f'{path}#{anchor}'}
            res.update(urldict)

        return result

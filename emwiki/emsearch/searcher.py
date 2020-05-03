from article.classes import ArticleHandler
import re
from difflib import SequenceMatcher
import json
from mmlreference.symbols import SymbolIndex
from emwiki.settings import SYMBOL_INDEX_PATH


class SearchResult():

    def __init__(self):
        self.weight = 0
        self.subject = ''
        self.category = ''
        self.link = ''

    def set(self, weight, subject, category, link):
        self.weight = weight
        self.subject = subject
        self.category = category
        self.link = link

    def get_as_dict(self):
        return {
            'weight': self.weight,
            'subject': self.subject,
            'category': self.category,
            'link': self.link
        }


class Searcher():

    def __init__(self):
        self.results = []
    
    def search_all(self, query):
        self.search_article(query)
        self.search_symbol(query)

    def search_article(self, query):
        file_list = [article_handler.article_name for article_handler in ArticleHandler.bundle_create()]
        file_list.sort()
        for filename in file_list:
            query_len, file_len = len(query), len(filename)
            weight = max([SequenceMatcher(None, query, filename[i:i + query_len]).ratio() for i in range(file_len - query_len + 1)], default=0)
            if weight > 0.8:
                searchresult = SearchResult()
                searchresult.set(
                    weight,
                    filename,
                    'article',
                    f'article/{filename}.html'
                )
                self.results.append(searchresult)
        self.results.sort(key=lambda symbolcontent: symbolcontent.weight, reverse=True)

    def search_symbol(self, query):
        symbolindex = SymbolIndex()
        symbolindex.read(SYMBOL_INDEX_PATH)
        for symbolcontent in symbolindex.symbolcontents:
            query_len, symbol_len = len(query), len(symbolcontent.symbol)
            weight = max([SequenceMatcher(None, query, symbolcontent.symbol[i:i + query_len]).ratio() for i in range(symbol_len - query_len + 1)], default=0)
            if weight > 0.8:
                searchresult = SearchResult()
                searchresult.set(
                    weight,
                    symbolcontent.symbol,
                    symbolcontent.type,
                    f'mmlreference/{symbolcontent.symbol}'
                )
                self.results.append(searchresult)
        self.results.sort(key=lambda symbolcontent: symbolcontent.weight, reverse=True)

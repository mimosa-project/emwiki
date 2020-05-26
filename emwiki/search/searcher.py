from functools import reduce
from operator import and_

from django.db.models import Q

from contents.article.models import Article
from contents.symbol.models import Symbol


class Searcher:

    def __init__(self):
        self.articlesearcher = ArticleSearcher()
        self.symbolsearcher = SymbolSearcher()
    
    def search(self, query_text, category):
        if category == 'All':
            results = []
            results.extend(self.articlesearcher.search(query_text))
            results.extend(self.symbolsearcher.search(query_text))
            return results
        elif category == 'Article':
            return self.articlesearcher.search(query_text)
        elif category == 'Symbol':
            return self.symbolsearcher.search(query_text)


class ArticleSearcher:
    
    def __init__(self):
        pass

    def search(self, query_text):
        queryset = Article.objects.order_by('name')
        if query_text:
            query_text_replaced = query_text.replace(' ', '')
            # Create a query to search for a Article that includes
            # all the characters of "query_text_replaced"
            # in Article.name
            query = reduce(
                and_, [Q(name__icontains=q) for q in query_text_replaced]
            )
            return queryset.filter(query)
        else:
            return queryset


class SymbolSearcher:

    def __init__(self):
        pass

    def search(self, query_text):
        queryset = Symbol.objects.order_by('name')
        if query_text:
            query_text_replaced = query_text.replace(' ', '')
            # Create a query to search for a Symbol that includes
            # all the characters of "query_text_replaced"
            # in Symbol.name
            query = reduce(
                and_, [Q(name__icontains=q) for q in query_text_replaced]
            )
            return queryset.filter(query)
        else:
            return queryset

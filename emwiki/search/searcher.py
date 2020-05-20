from contents.symbol.models import Symbol
from contents.article.models import Article
from difflib import SequenceMatcher
from django.db.models import Q
import urllib
from functools import reduce
from operator import and_


class SearchResult():

    def __init__(self, subject, category, link):
        self.subject = subject
        self.category = category
        self.link = link

    def get_as_dict(self):
        return {
            'subject': self.subject,
            'category': self.category,
            'link': self.link
        }


class Searcher():

    def __init__(self):
        self.results = []
    
    def search(self, query_text, category):
        if category == 'all':
            self.search_article(query_text)
            self.search_symbol(query_text)
        elif category == 'article':
            self.search_article(query_text)
        elif category == 'symbol':
            self.search_symbol(query_text)

    def search_article(self, query_text):
        queryset = Article.objects.order_by('name')
        if query_text:
            query_text_replaced = query_text.replace(' ', '')
            # Create a query to search for a Article that includes
            # all the characters of "query_text_replaced"
            # in Article.name
            query = reduce(
                and_, [Q(name__icontains=q) for q in query_text_replaced]
            )
            for q in queryset.filter(query):
                result = SearchResult(
                    q.name, 'article', q.get_absolute_url()
                )
                self.results.append(result)
        else:
            for q in queryset:
                result = SearchResult(
                    q.name, 'article', q.get_absolute_url()
                )
                self.results.append(result)

    def search_symbol(self, query_text):
        queryset = Symbol.objects.order_by('name')
        if query_text:
            query_text_replaced = query_text.replace(' ', '')
            # Create a query to search for a Symbol that includes
            # all the characters of "query_text_replaced"
            # in Symbol.name
            query = reduce(
                and_, [Q(name__icontains=q) for q in query_text_replaced]
            )
            for q in queryset.filter(query):
                result = SearchResult(
                    q.name, 'symbol', q.get_absolute_url()
                )
                self.results.append(result)
        else:
            for q in queryset:
                result = SearchResult(
                    q.name, 'symbol', q.get_absolute_url()
                )
                self.results.append(result)

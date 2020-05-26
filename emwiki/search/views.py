from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from search.searcher import Searcher
import json
import os
from emwiki.settings import BASE_DIR
from django.views.generic import TemplateView
from contents.article.models import Article
from contents.symbol.models import Symbol


class SearchView(TemplateView):
    template_name = 'search/index.html'
    categorys = {
        'Article': {
            'color': Article.color
        },
        'Symbol': {
            'color': Symbol.color
        }
    }
    
    def get_context_data(self, **kwargs):
        query_text = self.request.GET.get('search_query', default='')
        query_category = self.request.GET.get('search_category', default='All')
        searcher = Searcher()
        result_objects = searcher.search(query_text, query_category)

        context = super().get_context_data(**kwargs)
        context.update({
            'query_text': query_text,
            'query_category': query_category,
            'result_objects': result_objects
        })
        return context


@require_http_methods(["GET", ])
def get_keywords(request):
    keywords = []
    article_names = [article.name for article in Article.objects.all().order_by('name')]
    symbol_names = [symbol.name for symbol in Symbol.objects.all().order_by('name')]
    keywords.extend(article_names)
    keywords.extend(symbol_names)
    return JsonResponse({'keywords': keywords})

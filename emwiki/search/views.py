from collections import OrderedDict

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView

from contents.article.models import Article
from contents.article.searcher import ArticleSearcher
from contents.symbol.models import Symbol
from contents.symbol.searcher import SymbolSearcher

from search.theorem_searcher import TheoremSearcher

class SearchView(TemplateView):
    template_name = 'search/index.html'
    search_targets = {
        Article.get_category(): Article,
        Symbol.get_category(): Symbol
    }

    def __init__(self):
        self.searchers = OrderedDict()
        self.searchers[Article.get_category()] = ArticleSearcher()
        self.searchers[Symbol.get_category()] = SymbolSearcher()

    def get_context_data(self, **kwargs):
        query_text = self.request.GET.get('search_query', default='')
        query_category = self.request.GET.get('search_category', default='All')

        contents = []
        if query_category != 'All' or query_text != '':
            for category, searcher in self.searchers.items():
                if query_category == 'All' or query_category == category:
                    contents.extend(searcher.search(query_text))

        context = super().get_context_data(**kwargs)
        context.update({
            'query_text': query_text,
            'query_category': query_category,
            'result_objects': contents
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


class SearchTheoremView(TemplateView):
    template_name= 'search/search-theorem.html'

    def get_context_data(self, **kwargs):
        query_text = self.request.GET.get('search_query', default='')
        order_by = self.request.GET.get('order_by', default='Relevance')

        #検索
        search_results = TheoremSearcher.Searcher(query_text)

        #並べ替え
        if order_by == "Label : ASC":
            search_results = sorted(search_results, key=lambda x:x['Label'])
        
        elif order_by == "Label : DESC":
            search_results = sorted(search_results, key=lambda x:x['Label'], reverse=True)

        elif order_by == "Text : ASC":
            search_results = sorted(search_results, key=lambda x:x['Text'])
        
        elif order_by == "Text : DESC":
            search_results = sorted(search_results, key=lambda x:x['Text'], reverse=True)

        else:
            search_results = sorted(search_results, key=lambda x:x['Relevance'], reverse=True)

        context = super().get_context_data(**kwargs)
        context.update({
            'query_text': query_text,
            'result_list': search_results,
            'order_by': order_by
        })
        return context
from collections import OrderedDict

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView

from contents.article.models import Article
from contents.article.searcher import ArticleSearcher
from contents.symbol.models import Symbol
from contents.symbol.searcher import SymbolSearcher


class SearchView(TemplateView):
    template_name = 'search/index.html'
    search_targets = {
        Article.category: Article,
        Symbol.category: Symbol
    }

    def __init__(self):
        self.searchers = OrderedDict()
        self.searchers[Article.category] = ArticleSearcher()
        self.searchers[Symbol.category] = SymbolSearcher()
    
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

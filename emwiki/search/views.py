from collections import OrderedDict

from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.generic import TemplateView

from contents.article.models import Article
from contents.article.searcher import ArticleSearcher
from contents.symbol.models import Symbol
from contents.symbol.searcher import SymbolSearcher

from search.theorem_searcher import TheoremSearcher
from search.models import Theorem, SearchHistory, SearchResult

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
    template_name= 'search/search_theorem.html'

    def get_context_data(self, **kwargs):
        query_text = self.request.GET.get('search_query', default='')
        order_by = self.request.GET.get('order_by', default='relevance')
        context = super().get_context_data(**kwargs)

        if query_text:
            ##検索
            searcher = TheoremSearcher()
            search_results = searcher.search(query_text)
            search_results = sorted(search_results, key=lambda x:x['relevance'], reverse=True)

            ##クエリをデータベースに登録
            search_history_obj = SearchHistory.register_search_history(query_text)

            ##検索結果の中から定理のテーブルに登録されていない定理をテーブルに保存
            Theorem.register_theorem(search_results)

            ##検索履歴に対しての検索結果の情報をデータベースに保存
            search_results = SearchResult.register_search_result(search_results, search_history_obj)

            ##contextの情報を更新
            context.update({
                'query_text': query_text,
                'result_list': search_results,
                'order_by': order_by
            })

        return context


    ##ajaxによるクリック情報を受け取った場合
    def post(self,request):
        button_type = request.POST.get("button_type", None)
        id = request.POST.get("id", None)
        res = {'id': id}

        ##検索結果に対するクリック情報を更新
        SearchResult.update_search_result(button_type, id)
        
        return JsonResponse(res)
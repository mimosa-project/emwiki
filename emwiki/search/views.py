from django.http import JsonResponse
from django.urls import reverse
from django.views.defaults import bad_request
from django.views.generic import TemplateView

from search.theorem_searcher import TheoremSearcher
from search.models import Theorem, History, HistoryItem


class SearchTheoremView(TemplateView):
    template_name = 'search/index.html'

    def get(self, request, **kwargs):
        context = super().get_context_data(**kwargs)
        search_query = request.GET.get('search_query', default='')
        context.update({
            'context_for_js': {
                'search_uri': reverse('search:index'),
                'article_base_uri': reverse('article:index', kwargs=dict(name_or_filename="temp")).replace('temp', ''),
                'article_html_uri': reverse('article:htmls'),
                'comments_uri': reverse('article:comments'),
                'bibs_uri': reverse('article:bibs'),
                'is_authenticated': self.request.user.is_authenticated,
            }
        })
        # getのパラメータがない場合はtopページを表示
        if not search_query:
            return self.render_to_response(context)
        # ascii文字以外を含む場合
        elif max([ord(char) for char in search_query]) >= 128:
            return bad_request(request, SyntaxError, template_name='search/bad_request.html')
        else:
            # 検索
            searcher = TheoremSearcher()
            search_results = searcher.search(search_query, 100)
            # 検索結果の中から定理のテーブルに登録されていない定理をテーブルに保存
            Theorem.register_theorem(search_results)
            # クエリをデータベースに登録
            history = History.objects.create(query=search_query)
            # 検索履歴に対しての検索結果の情報をデータベースに保存
            HistoryItem.register_history_item(search_results, history)
            # 検索結果のIDをデータベースから取得
            HistoryItem.collect_history_item_id(search_results, history)
            # 関連度順に並べ替え
            search_results = sorted(search_results, key=lambda x: x['relevance'], reverse=True)
            return JsonResponse({"searchResults": search_results})

    # ajaxによるクリック情報を受け取った場合
    def post(self, request):
        button_type = request.POST.get("button_type", None)
        id = request.POST.get("id", None)

        # 検索結果に対するクリック情報を更新
        HistoryItem.update_history_item(id, button_type)

        return JsonResponse({'id': id})

from django.http import JsonResponse
from django.urls import reverse
from django.views.decorators.http import require_http_methods
from django.views.defaults import bad_request
from django.views.generic import TemplateView

from search.theorem_searcher import TheoremSearcher
from search.models import Theorem, History, HistoryItem


class SearchTheoremView(TemplateView):
    template_name= 'search/search_theorem.html'

    def get(self, request, **kwargs):
        query_text = request.GET.get('search_query', default='')
        order_by = request.GET.get('order_by', default='relevance')
        context = super().get_context_data(**kwargs)

        if not query_text:
            pass
        # ascii文字以外を含む場合
        elif max([ord(char) for char in query_text]) >= 128:
            return bad_request(request, SyntaxError,template_name='search/bad_request.html')
        else:
            # 検索
            searcher = TheoremSearcher()
            search_results = searcher.search(query_text, 100)
            if search_results:
                # 検索結果の中から定理のテーブルに登録されていない定理をテーブルに保存
                Theorem.register_theorem(search_results)
                # クエリをデータベースに登録
                history = History.objects.create(query=query_text)
                # 検索履歴に対しての検索結果の情報をデータベースに保存
                HistoryItem.register_history_item(search_results, history)
                # 検索結果のIDをデータベースから取得
                HistoryItem.collect_history_item_id(search_results, history)
                # 関連度順に並べ替え
                search_results = sorted(search_results, key=lambda x:x['relevance'], reverse=True)
            # contextの情報を更新
            context.update({
                'query_text': query_text,
                'result_list': search_results,
                'order_by': order_by,
                'context_for_js': {
                    'search_uri': reverse('search:search_theorem')
                }
            })
        return self.render_to_response(context)

    # ajaxによるクリック情報を受け取った場合
    def post(self, request):
        button_type = request.POST.get("button_type", None)
        id = request.POST.get("id", None)

        # 検索結果に対するクリック情報を更新
        HistoryItem.update_history_item(id, button_type)

        return JsonResponse({'id': id})

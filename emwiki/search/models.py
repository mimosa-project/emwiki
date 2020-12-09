from django.db import models

class Theorem(models.Model):
    label = models.CharField(max_length=30)
    theorem = models.TextField()

    def __str__(self):
        return self.label

    ##テーブルに登録されていない定理を登録
    @classmethod
    def register_theorem(cls, search_results):
            registered_theorems = Theorem.objects.values_list('label', flat=True)
            for search_result in search_results:
                if search_result['label'] not in registered_theorems:
                    new_theorem = Theorem(label=search_result['label'], theorem=search_result['text'])
                    new_theorem.save()

class SearchHistory(models.Model):
    query = models.TextField('query')

    def __str__(self):
        return self.query

    ##検索履歴を登録
    @classmethod
    def register_search_history(cls, query_text):
            search_history_obj = SearchHistory(query=query_text)
            search_history_obj.save()
            return search_history_obj

class SearchResult(models.Model):
    search_history = models.ForeignKey(SearchHistory, on_delete=models.CASCADE)
    theorem = models.ForeignKey(Theorem, on_delete=models.CASCADE)
    relevance = models.FloatField()
    click = models.BooleanField()
    favorite = models.BooleanField()

    def __str__(self):
        return self.theorem.label

    ##検索結果をデータベースに登録し, 登録時のキーをリストに追加
    @classmethod
    def register_search_result(cls, search_results, search_history):
            for search_result in search_results:
                result_info = SearchResult(relevance=search_result['relevance'], click=False, favorite=False)
                result_info.search_history = SearchHistory.objects.get(pk=search_history.id)
                result_info.theorem = Theorem.objects.get(label=search_result['label'])
                result_info.save()
                iddict = {'id': result_info.id}
                search_result.update(iddict)

            return search_results

    ##urlまたはお気に入りボタンがクリックれたとき, 情報を更新
    @classmethod
    def update_search_result(cls, button_type, id):

        ##お気に入りボタンがクリックされたとき
        if button_type == 'fav':
            search_result = SearchResult.objects.get(id=id)
            search_result.favorite = not search_result.favorite
            search_result.save()

        ##URlがクリックされたとき
        if button_type == 'url':
            search_result = SearchResult.objects.get(id=id)
            search_result.click = True
            search_result.save()




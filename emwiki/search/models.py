from django.db import models

class Theorem(models.Model):
    label = models.CharField(max_length=30, db_index=True)
    theorem = models.TextField()

    def __str__(self):
        return self.label

    ##テーブルに登録されていない定理を登録
    @classmethod
    def register_theorem(cls, search_results):
            registered_theorems = set(Theorem.objects.values_list('label', flat=True))
            new_theorems = []
            for search_result in search_results:
                if search_result['label'] not in registered_theorems:
                    theorem = Theorem(label=search_result['label'], theorem=search_result['text'])
                    new_theorems.append(theorem)

            Theorem.objects.bulk_create(new_theorems)

class History(models.Model):
    query = models.TextField('query')

    def __str__(self):
        return self.query


class HistoryItem(models.Model):
    history = models.ForeignKey(History, on_delete=models.CASCADE)
    theorem = models.ForeignKey(Theorem, on_delete=models.CASCADE)
    relevance = models.FloatField()
    click = models.BooleanField()
    favorite = models.BooleanField()

    def __str__(self):
        return self.theorem.label

    ##検索結果をデータベースに登録し, 登録時のキーをリストに追加
    @classmethod
    def register_history_item(cls, search_results, history):
            new_history_items = []
            for search_result in search_results:
                history_item = HistoryItem(relevance=search_result['relevance'], click=False, favorite=False)
                history_item.history = History.objects.get(pk=history.id)
                history_item.theorem = Theorem.objects.get(label=search_result['label'])
                new_history_items.append(history_item)

            HistoryItem.objects.bulk_create(new_history_items)

    @classmethod
    def update_search_results_id(cls, search_results, history):
        #ラベル順に並べ替え
        search_results = sorted(search_results, key=lambda x:x['label'])
        new_history_item_list = HistoryItem.objects.filter(history=history).order_by('theorem__label').all()
        return [
            dict(search_results[i].items(), id=new_history_item_list[i].id)
            for i in range(len(search_results))
        ]

    ##urlまたはお気に入りボタンがクリックれたとき, 情報を更新
    @classmethod
    def update_history_item(cls, id, button_type):

        ##お気に入りボタンがクリックされたとき
        if button_type == 'fav':
            history_item = HistoryItem.objects.get(id=id)
            history_item.favorite = not history_item.favorite
            history_item.save()

        ##URlがクリックされたとき
        if button_type == 'url':
            history_item = HistoryItem.objects.get(id=id)
            history_item.click = True
            history_item.save()





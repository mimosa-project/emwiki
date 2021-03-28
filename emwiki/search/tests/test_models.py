from django.test import TestCase

from search.models import Theorem, History, HistoryItem
from search.theorem_searcher import TheoremSearcher

class TheoremTest(TestCase):
    def setUp(self):
        # クエリを設定し検索
        self.query_text = "j < i implies i -' (j + 1) + 1 = i -' j;"
        self.number_of_results = 100
        searcher = TheoremSearcher()
        self.search_results = searcher.search(self.query_text, self.number_of_results)

    def test_register_theorem(self):
        # 検索結果の中から定理のテーブルに登録されていない定理をテーブルに保存
        Theorem.register_theorem(self.search_results)

        # 検索結果の件数の数だけ定理が登録されるか
        theorem_count_label = Theorem.objects.filter(label__isnull=False).count()
        theorem_count_text = Theorem.objects.filter(theorem__isnull=False).count()
        self.assertEqual(self.number_of_results, theorem_count_label)
        self.assertEqual(self.number_of_results, theorem_count_text)

        # 定理が2重登録されていないか
        Theorem.register_theorem(self.search_results)
        theorem_count_label = Theorem.objects.filter(label__isnull=False).count()
        theorem_count_text = Theorem.objects.filter(theorem__isnull=False).count()
        self.assertEqual(self.number_of_results, theorem_count_label)
        self.assertEqual(self.number_of_results, theorem_count_text)

class HistoryItemTest(TestCase):
    def setUp(self):
        # クエリを設定し検索
        self.query_text = "j < i implies i -' (j + 1) + 1 = i -' j;"
        self.number_of_results = 100
        searcher = TheoremSearcher()
        self.search_results = searcher.search(self.query_text, self.number_of_results)

    def test_register_history_item(self):
        # 検索結果の中から定理のテーブルに登録されていない定理をテーブルに保存
        Theorem.register_theorem(self.search_results)
        # クエリをデータベースに登録
        self.history = History.objects.create(query=self.query_text)
        # 検索履歴に対しての検索結果の情報をデータベースに保存
        HistoryItem.register_history_item(self.search_results, self.history)

        # 検索結果の件数の数だけ検索結果情報が登録されるか
        history_item_count_history = HistoryItem.objects.filter(history__isnull=False).count()
        history_item_count_theorem = HistoryItem.objects.filter(theorem__isnull=False).count()
        history_item_count_relevance = HistoryItem.objects.filter(relevance__isnull=False).count()
        history_item_count_favorite = HistoryItem.objects.filter(favorite__isnull=False).count()
        history_item_count_click = HistoryItem.objects.filter(click__isnull=False).count()
        self.assertEqual(self.number_of_results, history_item_count_history)
        self.assertEqual(self.number_of_results, history_item_count_theorem)
        self.assertEqual(self.number_of_results, history_item_count_relevance)
        self.assertEqual(self.number_of_results, history_item_count_favorite)
        self.assertEqual(self.number_of_results, history_item_count_click)

    def test_collect_history_item_id(self):
        # 検索結果の中から定理のテーブルに登録されていない定理をテーブルに保存
        Theorem.register_theorem(self.search_results)
        # クエリをデータベースに登録
        self.history = History.objects.create(query=self.query_text)
        # 検索履歴に対しての検索結果の情報をデータベースに保存
        HistoryItem.register_history_item(self.search_results, self.history)
        # 検索結果のIDをデータベースから取得
        HistoryItem.collect_history_item_id(self.search_results, self.history)

        # DBのidと表示データのidが一致しているか
        db_id_list = HistoryItem.objects.values_list('id', flat=True).order_by('theorem__label')
        search_results_order_by_label = sorted(self.search_results, key=lambda x:x['label'])
        for i in range(self.number_of_results):
            self.assertEqual(db_id_list[i], search_results_order_by_label[i]['id'])

    def test_update_history_item(self):
        # 検索結果の中から定理のテーブルに登録されていない定理をテーブルに保存
        Theorem.register_theorem(self.search_results)
        # クエリをデータベースに登録
        self.history = History.objects.create(query=self.query_text)
        # 検索履歴に対しての検索結果の情報をデータベースに保存
        HistoryItem.register_history_item(self.search_results, self.history)
        # 検索結果のIDをデータベースから取得
        HistoryItem.collect_history_item_id(self.search_results, self.history)

        # お気に入りボタンを押した場合
        id = self.search_results[0]['id']
        button_type = "fav"
        HistoryItem.update_history_item(id, button_type)
        history_item = HistoryItem.objects.get(id=id)
        self.assertEqual(history_item.favorite, True)

        # もう一度押したとき解除されるか
        HistoryItem.update_history_item(id, button_type)
        history_item = HistoryItem.objects.get(id=id)
        self.assertEqual(history_item.favorite, False)

        # URLボタンを押したとき
        button_type = "url"
        HistoryItem.update_history_item(id, button_type)
        history_item = HistoryItem.objects.get(id=id)
        self.assertEqual(history_item.click, True)

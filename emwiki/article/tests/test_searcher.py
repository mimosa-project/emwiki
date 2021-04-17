from django.test import TestCase

from article.models import Article
from article.article_builder import ArticleBuilder
from article.searcher import ArticleSearcher
from emwiki.settings import TEST_RAW_MIZFILE_DIR


class ArticleSearcherTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.builder = ArticleBuilder()
        cls.builder.from_dir = TEST_RAW_MIZFILE_DIR
        cls.builder.create_models()

    @classmethod
    def tearDownClass(cls):
        cls.builder.delete_models()

    def test_search(self):
        searcher = ArticleSearcher()

        query_text = 'abcmiz_0'
        queryset = searcher.search(query_text)
        self.assertEqual(len(queryset), 1)
        self.assertEqual(queryset[0].name, 'abcmiz_0')

        query_text = ''
        queryset = searcher.search(query_text)
        self.assertEqual(len(queryset), len(Article.objects.all()))

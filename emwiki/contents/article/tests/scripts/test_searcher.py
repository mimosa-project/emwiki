import glob
import os

from django.test import TestCase

from contents.contents.tests.scripts.test_searcher import ContentSearcherTest
from contents.article.models import Article
from contents.article.scripts.searcher import ArticleSearcher
from contents.article.scripts.initializer import ArticleInitializer
from emwiki.settings import TEST_RAW_HTMLIZEDMML_DIR, TEST_CACHE_DIR


class ArticleSearcherTest(TestCase, ContentSearcherTest):

    @classmethod
    def setUpClass(cls):
        initializer = ArticleInitializer()
        initializer.raw_htmlizedmml_dir = TEST_RAW_HTMLIZEDMML_DIR
        initializer.product_htmlizedmml_dir = TEST_CACHE_DIR
        initializer.initialize()

    @classmethod
    def tearDownClass(cls):
        cache_html_paths = glob.glob(os.path.join(TEST_CACHE_DIR, '*.html'))
        for path in cache_html_paths:
            os.remove(path)

    def test_search(self):
        query_text = 'abcmiz_0'
        searcher = ArticleSearcher()
        queryset = searcher.search(query_text)
        self.assertEqual(len(queryset), 1)
        self.assertEqual(queryset[0].name, 'abcmiz_0')

        query_text = ''
        searcher.search(query_text)
        queryset = searcher.search(query_text)
        self.assertEqual(len(queryset), len(Article.objects.all()))
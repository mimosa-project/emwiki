import glob
import os
import shutil

from django.test import TestCase

from contents.contents.tests.scripts.test_searcher import ContentSearcherTest
from contents.article.models import Article
from contents.article.scripts.searcher import ArticleSearcher


class ArticleSearcherTest(TestCase, ContentSearcherTest):

    @classmethod
    def setUpClass(cls):
        from contents.article.scripts.initializer import ArticleInitializer
        from emwiki.settings import TEST_RAW_HTMLIZEDMML_DIR, TEST_OUTPUTS_DIR
        cache_dir = os.path.join(TEST_OUTPUTS_DIR, 'cache')
        cls.from_dir = TEST_RAW_HTMLIZEDMML_DIR
        cls.to_dir = cache_dir
        os.mkdir(cache_dir)

        initializer = ArticleInitializer()
        initializer.raw_htmlizedmml_dir = cls.from_dir
        initializer.product_htmlizedmml_dir = cls.to_dir
        initializer.initialize()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.to_dir)

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
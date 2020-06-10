import glob
import os

from django.test import TestCase

from contents.contents.tests.scripts.test_searcher import ContentSearcherTest
from contents.symbol.models import Symbol
from contents.symbol.scripts.searcher import SymbolSearcher
from contents.symbol.scripts.initializer import SymbolInitializer
from emwiki.settings import TEST_RAW_HTMLIZEDMML_DIR, TEST_CACHE_DIR


class SymbolSearcherTest(TestCase, ContentSearcherTest):

    @classmethod
    def setUpClass(cls):
        initializer = SymbolInitializer()
        initializer.raw_htmlizedmml_dir = TEST_RAW_HTMLIZEDMML_DIR
        initializer.product_htmlizedmml_dir = TEST_CACHE_DIR
        initializer.initialize()

    @classmethod
    def tearDownClass(cls):
        cache_html_paths = glob.glob(os.path.join(TEST_CACHE_DIR, '*.html'))
        for path in cache_html_paths:
            os.remove(path)

    def test_search(self):
        query_text = ''
        searcher = SymbolSearcher()
        queryset = searcher.search(query_text)
        # self.assertEqual(len(queryset), 1)
        # self.assertEqual(queryset[0].name, 'abcmiz_0')

        query_text = ''
        searcher.search(query_text)
        queryset = searcher.search(query_text)
        # self.assertEqual(len(queryset), len(Symbol.objects.all()))
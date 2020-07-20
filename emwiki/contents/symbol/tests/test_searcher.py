from django.test import TestCase

from contents.symbol.models import Symbol
from contents.symbol.searcher import SymbolSearcher
from contents.symbol.symbol_builder import SymbolBuilder
from emwiki.settings import TEST_RAW_HTMLIZEDMML_DIR


class SymbolSearcherTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.builder = SymbolBuilder()
        cls.builder.from_dir = TEST_RAW_HTMLIZEDMML_DIR
        cls.builder.create_models()

    @classmethod
    def tearDownClass(cls):
        cls.builder.delete_models()

    def test_search(self):
        searcher = SymbolSearcher()

        query_text = '1-1-connectives'
        queryset = searcher.search(query_text)
        self.assertEqual(1, len(queryset))
        self.assertEqual(queryset[0].name, '1-1-connectives')

        query_text = ''
        queryset = searcher.search(query_text)
        self.assertEqual(len(queryset), len(Symbol.objects.all()))

from contents.symbol.symbol_builder import SymbolBuilder
from contents.symbol.models import Symbol
from emwiki.settings import TEST_RAW_HTMLIZEDMML_DIR
from django.test import TestCase


class SymbolBuilderTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.builder = SymbolBuilder()
        cls.builder.from_dir = TEST_RAW_HTMLIZEDMML_DIR

    @classmethod
    def tearDownClass(cls):
        cls.builder.delete_models()

    def test_delete_models(self):
        self.builder.create_models()
        self.builder.delete_models()
        self.assertEqual(0, len(Symbol.objects.all()))

    def test_create_models(self):
        self.builder.create_models()
        self.assertEqual(262, len(Symbol.objects.all()))

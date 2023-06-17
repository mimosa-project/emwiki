from symbol.symbol_builder import SymbolBuilder
from symbol.models import Symbol
from django.conf import settings
from django.test import TestCase


class SymbolBuilderTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.builder = SymbolBuilder()
        cls.builder.from_dir = settings.TEST_MML_HTML_DIR

    def test_delete_models(self):
        self.builder.create_models()
        self.builder.delete_models()
        self.assertEqual(0, len(Symbol.objects.all()))

    def test_create_models(self):
        self.builder.create_models()
        self.assertEqual(262, len(Symbol.objects.all()))

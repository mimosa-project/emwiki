from django.test import TestCase

from symbol.symbol_builder import SymbolBuilder
from symbol.models import Symbol
from django.conf import settings


class SymbolTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.builder = SymbolBuilder()
        cls.builder.from_dir = settings.TEST_MML_HTML_DIR
        cls.builder.create_models()

    @classmethod
    def tearDownClass(cls):
        cls.builder.delete_models()

    def test_attributes(self):
        for symbol in Symbol.objects.all():
            self.assertIsNotNone(symbol.name)
            self.assertIsNotNone(symbol.filename)
            self.assertFalse(symbol.name.endswith('.html'))

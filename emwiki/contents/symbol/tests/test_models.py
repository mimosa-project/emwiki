import os

from django.test import TestCase, Client

from contents.symbol.symbol_builder import SymbolBuilder
from contents.symbol.models import Symbol
from emwiki.settings import TEST_RAW_HTMLIZEDMML_DIR


class SymbolTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.builder = SymbolBuilder()
        cls.builder.from_dir = TEST_RAW_HTMLIZEDMML_DIR
        cls.builder.create_models()

    @classmethod
    def tearDownClass(cls):
        cls.builder.delete_models()

    def test_get_model(self):
        name = 'is_applicable_to'
        model = Symbol.get_model(name=name)
        self.assertEqual(model.name, name)

        name = 'is_applicable_to'
        model = Symbol.get_model(name=name)
        self.assertEqual(model.name, name)

        filename = '0.html'
        model = Symbol.get_model(filename=filename)
        self.assertEqual(model.filename, filename)

    def test_attributes(self):
        for symbol in Symbol.objects.all():
            self.assertIsNotNone(symbol.name)
            self.assertIsNotNone(symbol.filename)
            self.assertEqual(symbol.get_category(), 'Symbol')
            self.assertIsNotNone(symbol.get_color())
            self.assertTrue(os.path.exists(symbol.get_file_dir()))
            self.assertFalse(symbol.name.endswith('.html'))

    def test_url_methods(self):
        client = Client()
        for symbol in Symbol.objects.all():
            absolute_response = client.get(symbol.get_absolute_url())
            self.assertEqual(absolute_response.status_code, 200)
            self.assertIsNotNone(symbol.get_static_url())

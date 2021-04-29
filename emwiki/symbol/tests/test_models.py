import os

from django.template.loader import get_template
from django.test import TestCase, Client
from django.template.exceptions import TemplateSyntaxError

from symbol.symbol_builder import SymbolBuilder
from symbol.models import Symbol
from django.conf import settings


class SymbolTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.builder = SymbolBuilder()
        cls.builder.from_dir = settings.TEST_RAW_HTMLIZEDMML_DIR
        cls.builder.create_models()

    @classmethod
    def tearDownClass(cls):
        cls.builder.delete_models()

    def test_attributes(self):
        for symbol in Symbol.objects.all():
            self.assertIsNotNone(symbol.name)
            self.assertIsNotNone(symbol.filename)
            self.assertTrue(os.path.exists(symbol.get_htmlfile_dir()))
            self.assertFalse(symbol.name.endswith('.html'))

    def test_url_methods(self):
        client = Client()
        for symbol in Symbol.objects.all():
            try:
                absolute_response = client.get(symbol.get_absolute_url())
            except TemplateSyntaxError:
                print(symbol)
                raise TemplateSyntaxError

            self.assertEqual(absolute_response.status_code, 200)
            self.assertIsNotNone(get_template(symbol.template_path))

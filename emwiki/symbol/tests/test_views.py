import os
import shutil
from symbol.models import Symbol
from symbol.symbol_builder import SymbolBuilder
from symbol.symbol_html_builder import SymbolHtmlBuilder

from django.conf import settings
from django.template.loader import get_template
from django.test import Client, TestCase, override_settings

TEMPLATES = settings.TEMPLATES
TEMPLATES[0]["DIRS"].append(os.path.join(settings.BASE_DIR, "symbol", "tests", "templates"))


@override_settings(TEMPLATES=TEMPLATES)
class SymbolTest(TestCase):
    test_templates_dir = os.path.join(settings.BASE_DIR, "symbol", "tests", "templates", "symbol", "symbol_html")

    @classmethod
    def setUpClass(cls):
        cls.symbol_builder = SymbolBuilder()
        cls.symbol_builder.from_dir = settings.TEST_RAW_MML_MML_DIR
        cls.symbol_builder.create_models()
        cls.symbol_html_builder = SymbolHtmlBuilder()
        cls.symbol_html_builder.from_dir = settings.TEST_MML_HTML_DIR
        cls.symbol_html_builder.to_dir = cls.test_templates_dir
        cls.symbol_html_builder.update_files()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.test_templates_dir)
        cls.symbol_builder.delete_models()

    def test_get(self):
        client = Client()
        for symbol in Symbol.objects.all():
            absolute_response = client.get(symbol.get_absolute_url(), follow=True)
            self.assertEqual(absolute_response.status_code, 200)
            self.assertIsNotNone(get_template(symbol.template_url))

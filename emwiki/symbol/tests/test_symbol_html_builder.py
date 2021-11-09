import glob
import os
import shutil
from symbol.symbol_html_builder import SymbolHtmlBuilder

from django.conf import settings
from django.test import TestCase


class SymbolHtmlBuilderTest(TestCase):

    @classmethod
    def setUpClass(cls):
        if os.path.exists(settings.TEST_OUTPUT_PRODUCT_SYMBOLHTML_DIR):
            shutil.rmtree(settings.TEST_OUTPUT_PRODUCT_SYMBOLHTML_DIR)
        os.mkdir(settings.TEST_OUTPUT_PRODUCT_SYMBOLHTML_DIR)
        cls.builder = SymbolHtmlBuilder()
        cls.builder.from_dir = settings.TEST_MML_HTML_DIR
        cls.builder.to_dir = settings.TEST_OUTPUT_PRODUCT_SYMBOLHTML_DIR

    @classmethod
    def tearDownClass(cls):
        cls.builder.update_files()

    def test_update_files(self):
        self.builder.update_files()
        product_paths = glob.glob(os.path.join(
            settings.TEST_OUTPUT_PRODUCT_SYMBOLHTML_DIR, '*.html'))
        self.assertEqual(262, len(product_paths))

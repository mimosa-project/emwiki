import glob
import os
import shutil

from symbol.symbol_html_builder import SymbolHtmlBuilder
from emwiki.settings import TEST_RAW_HTMLIZEDMML_DIR, TEST_OUTPUT_PRODUCT_SYMBOLHTML_DIR
from django.test import TestCase


class SymbolHtmlBuilderTest(TestCase):

    @classmethod
    def setUpClass(cls):
        if os.path.exists(TEST_OUTPUT_PRODUCT_SYMBOLHTML_DIR):
            shutil.rmtree(TEST_OUTPUT_PRODUCT_SYMBOLHTML_DIR)
        os.mkdir(TEST_OUTPUT_PRODUCT_SYMBOLHTML_DIR)
        cls.builder = SymbolHtmlBuilder()
        cls.builder.from_dir = TEST_RAW_HTMLIZEDMML_DIR
        cls.builder.to_dir = TEST_OUTPUT_PRODUCT_SYMBOLHTML_DIR

    @classmethod
    def tearDownClass(cls):
        cls.builder.create_files()

    def test_delete_files(self):
        self.builder.delete_files()
        product_paths = glob.glob(os.path.join(TEST_OUTPUT_PRODUCT_SYMBOLHTML_DIR, '*.html'))
        self.assertEqual(0, len(product_paths))

    def test_create_files(self):
        self.builder.create_files()
        product_paths = glob.glob(os.path.join(TEST_OUTPUT_PRODUCT_SYMBOLHTML_DIR, '*.html'))
        self.assertEqual(262, len(product_paths))

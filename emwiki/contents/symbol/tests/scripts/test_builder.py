import glob
import os

from contents.symbol.scripts.builder import SymbolBuilder
from contents.contents.tests.scripts.test_builder import ContentBuilder
from emwiki.settings import TEST_RAW_HTMLIZEDMML_DIR, TEST_PRODUCT_SYMBOLHTML_DIR

from django.test import TestCase


class SymbolBuilderTest(TestCase, ContentBuilder):

    @classmethod
    def setUpClass(cls):
        product_symbolhtml_paths = glob.glob(os.path.join(TEST_PRODUCT_SYMBOLHTML_DIR, '*.html'))
        for path in product_symbolhtml_paths:
            os.remove(path)

    @classmethod
    def tearDownClass(cls):
        pass

    def test_bulk_build(self):
        builder = SymbolBuilder()
        builder.bulk_build(TEST_RAW_HTMLIZEDMML_DIR, TEST_PRODUCT_SYMBOLHTML_DIR)
        raw_htmlizedmml_paths = glob.glob(os.path.join(TEST_RAW_HTMLIZEDMML_DIR, '*.html'))
        product_symbolhtml_paths = glob.glob(os.path.join(TEST_PRODUCT_SYMBOLHTML_DIR, '*.html'))
        self.assertEqual(len(builder.processor.contents), len(product_symbolhtml_paths))

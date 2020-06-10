import glob
import os
import shutil

from django.test import TestCase

from contents.symbol.scripts.initializer import SymbolInitializer
from contents.symbol.models import Symbol
from contents.contents.tests.scripts.test_initializer import ContentInitializerTest
from emwiki.settings import TEST_RAW_HTMLIZEDMML_DIR, TEST_CACHE_DIR, TEST_PRODUCT_SYMBOLHTML_DIR


class SymbolInitializerTest(TestCase, ContentInitializerTest):

    @classmethod
    def setUpClass(cls):
        product_symbolhtml_paths = glob.glob(os.path.join(TEST_PRODUCT_SYMBOLHTML_DIR, '*.html'))
        for path in product_symbolhtml_paths:
            os.remove(path)

    @classmethod
    def tearDownClass(cls):
        cache_paths = glob.glob(os.path.join(TEST_CACHE_DIR, '*.html'))
        for path in cache_paths:
            os.remove(path)

    def test_initialize(self):
        initializer = SymbolInitializer()
        initializer.raw_htmlizedmml_dir = TEST_RAW_HTMLIZEDMML_DIR
        initializer.product_symbolhtml_dir = TEST_PRODUCT_SYMBOLHTML_DIR
        initializer.initialize()

        raw_htmlizedmml_paths = glob.glob(os.path.join(TEST_RAW_HTMLIZEDMML_DIR, '*.html'))
        product_symbolhtml_paths = glob.glob(os.path.join(TEST_PRODUCT_SYMBOLHTML_DIR, '*.html'))
        self.assertEqual(len(Symbol.objects.all()), len(product_symbolhtml_paths))

    def test_generate_files(self):
        pass

    def test_delete_models(self):
        pass

    def test_create_models(self):
        Symbol.objects.all().delete()
        initializer = SymbolInitializer()
        initializer.raw_htmlizedmml_dir = TEST_RAW_HTMLIZEDMML_DIR
        initializer.product_symbolhtml_dir = TEST_CACHE_DIR
        initializer._create_models()

        paths = glob.glob(os.path.join(TEST_PRODUCT_SYMBOLHTML_DIR, '*.html'))
        self.assertEqual(len(Symbol.objects.all()), len(paths))

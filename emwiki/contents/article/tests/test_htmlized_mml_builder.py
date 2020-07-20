import glob
import os
import shutil

from contents.article.htmlized_mml_builder import HtmlizedMmlBuilder
from emwiki.settings import TEST_RAW_HTMLIZEDMML_DIR, TEST_OUTPUT_PRODUCT_HTMLIZEDMML_DIR
from django.test import TestCase


class HtmlizedMmlBuilderTest(TestCase):

    @classmethod
    def setUpClass(cls):
        if os.path.exists(TEST_OUTPUT_PRODUCT_HTMLIZEDMML_DIR):
            shutil.rmtree(TEST_OUTPUT_PRODUCT_HTMLIZEDMML_DIR)
        os.mkdir(TEST_OUTPUT_PRODUCT_HTMLIZEDMML_DIR)
        cls.builder = HtmlizedMmlBuilder()
        cls.builder.from_dir = TEST_RAW_HTMLIZEDMML_DIR
        cls.builder.to_dir = TEST_OUTPUT_PRODUCT_HTMLIZEDMML_DIR

    @classmethod
    def tearDownClass(cls):
        cls.builder.create_files()

    def test_delete_files(self):
        self.builder.delete_files()
        product_paths = glob.glob(os.path.join(TEST_OUTPUT_PRODUCT_HTMLIZEDMML_DIR, '*.html'))
        self.assertEqual(0, len(product_paths))

    def test_create_files(self):
        self.builder.create_files()
        product_paths = glob.glob(os.path.join(TEST_OUTPUT_PRODUCT_HTMLIZEDMML_DIR, '*.html'))
        self.assertEqual(11, len(product_paths))

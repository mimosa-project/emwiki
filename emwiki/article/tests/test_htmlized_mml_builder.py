import glob
import os
import shutil

from article.htmlized_mml_builder import HtmlizedMmlBuilder
from django.conf import settings
from django.test import TestCase


class HtmlizedMmlBuilderTest(TestCase):

    @classmethod
    def setUpClass(cls):
        if os.path.exists(settings.TEST_OUTPUT_PRODUCT_HTMLIZEDMML_DIR):
            shutil.rmtree(settings.TEST_OUTPUT_PRODUCT_HTMLIZEDMML_DIR)
        os.mkdir(settings.TEST_OUTPUT_PRODUCT_HTMLIZEDMML_DIR)
        cls.builder = HtmlizedMmlBuilder()
        cls.builder.from_dir = settings.TEST_MML_HTML_DIR
        cls.builder.to_dir = settings.TEST_OUTPUT_PRODUCT_HTMLIZEDMML_DIR

    @classmethod
    def tearDownClass(cls):
        cls.builder.update_files()

    def test_update_files(self):
        self.builder.update_files()
        product_paths = glob.glob(os.path.join(
            settings.TEST_OUTPUT_PRODUCT_HTMLIZEDMML_DIR, '*.html'))
        self.assertEqual(11, len(product_paths))

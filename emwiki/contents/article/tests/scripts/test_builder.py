import glob
import os

from contents.article.scripts.builder import ArticleBuilder
from contents.contents.tests.scripts.test_builder import ContentBuilder
from emwiki.settings import TEST_RAW_HTMLIZEDMML_DIR, TEST_PRODUCT_HTMLIZEDMML_DIR

from django.test import TestCase


class ArticleBuilderTest(TestCase, ContentBuilder):

    @classmethod
    def setUpClass(cls):
        product_htmlizedmml_paths = glob.glob(os.path.join(TEST_PRODUCT_HTMLIZEDMML_DIR, '*.html'))
        for path in product_htmlizedmml_paths:
            os.remove(path)

    @classmethod
    def tearDownClass(cls):
        pass

    def test_bulk_build(self):
        builder = ArticleBuilder()
        builder.bulk_build(TEST_RAW_HTMLIZEDMML_DIR, TEST_PRODUCT_HTMLIZEDMML_DIR)
        raw_htmlizedmml_paths = glob.glob(os.path.join(TEST_RAW_HTMLIZEDMML_DIR, '*.html'))
        product_htmlizedmml_paths = glob.glob(os.path.join(TEST_PRODUCT_HTMLIZEDMML_DIR, '*.html'))
        self.assertEqual(len(raw_htmlizedmml_paths), len(product_htmlizedmml_paths))

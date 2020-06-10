import glob
import os

from django.test import TestCase, Client

from contents.article.scripts.initializer import ArticleInitializer
from contents.article.models import Article
from emwiki.settings import TEST_RAW_HTMLIZEDMML_DIR, \
    TEST_PRODUCT_HTMLIZEDMML_DIR, PRODUCT_HTMLIZEDMML_DIR


class ArticleTest(TestCase):

    @classmethod
    def setUpClass(cls):
        article_initializer = ArticleInitializer()
        article_initializer.raw_htmlizedmml_dir = TEST_RAW_HTMLIZEDMML_DIR
        article_initializer.product_htmlizedmml_dir = TEST_PRODUCT_HTMLIZEDMML_DIR
        article_initializer.initialize()

    @classmethod
    def tearDownClass(cls):
        product_htmlizedmml_paths = glob.glob(os.path.join(TEST_PRODUCT_HTMLIZEDMML_DIR, '*.html'))
        for path in product_htmlizedmml_paths:
            os.remove(path)
    
    def test_attributes(self):
        for article in Article.objects.all():
            self.assertIsNotNone(article.name)
            self.assertEqual(article.category, 'Article')
            self.assertIsNotNone(article.color)
            self.assertFalse(article.name.endswith('.html'))

    def test_url_methods(self):
        client = Client()
        for article in Article.objects.all():
            filepath = os.path.join(PRODUCT_HTMLIZEDMML_DIR, article.name + '.html')
            if os.path.exists(filepath):
                absolute_response = client.get(article.get_absolute_url())
                self.assertEqual(absolute_response.status_code, 200)

                self.assertIsNotNone(article.get_static_url())

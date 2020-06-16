import glob
import os
import shutil

from django.test import TestCase, Client


class ArticleTest(TestCase):

    @classmethod
    def setUpClass(cls):
        from emwiki.settings import TEST_OUTPUTS_DIR, TEST_RAW_HTMLIZEDMML_DIR
        
        cls.from_dir = TEST_RAW_HTMLIZEDMML_DIR
        cls.to_dir = os.path.join(TEST_OUTPUTS_DIR, 'cache')
        os.mkdir(cls.to_dir)

    @classmethod
    def setUpTestData(cls):
        from contents.article.scripts.initializer import ArticleInitializer

        article_initializer = ArticleInitializer()
        article_initializer.raw_htmlizedmml_dir = cls.from_dir
        article_initializer.product_htmlizedmml_dir = cls.to_dir
        article_initializer.initialize()

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.to_dir)
    
    def test_attributes(self):
        from contents.article.models import Article

        for article in Article.objects.all():
            self.assertIsNotNone(article.name)
            self.assertEqual(article.category, 'Article')
            self.assertIsNotNone(article.color)
            self.assertFalse(article.name.endswith('.html'))

    def test_url_methods(self):
        from contents.article.models import Article
        from emwiki.settings import PRODUCT_HTMLIZEDMML_DIR

        client = Client()
        for article in Article.objects.all():
            filepath = os.path.join(PRODUCT_HTMLIZEDMML_DIR, article.name + '.html')
            if os.path.exists(filepath):
                absolute_response = client.get(article.get_absolute_url())
                self.assertEqual(absolute_response.status_code, 200)
                self.assertIsNotNone(article.get_static_url())

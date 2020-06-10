import os

from django.test import TestCase, Client

from contents.article.scripts.initializer import ArticleInitializer
from contents.article.models import Article
from emwiki.settings import TEST_MML_ARTICLES_ORIGINAL_DIR, \
    TEST_MML_ARTICLES_DIR


class ArticleTest(TestCase):

    def setUp(self):
        article_initializer = ArticleInitializer()
        article_initializer.initialize(
            TEST_MML_ARTICLES_ORIGINAL_DIR,
            TEST_MML_ARTICLES_DIR
        )
    
    def test_attributes(self):
        for article in Article.objects.all():
            self.assertIsNotNone(article.name)
            self.assertEqual(article.category, 'Article')
            self.assertIsNotNone(article.color)
            self.assertFalse(article.name.endswith('.html'))

    def test_directory_methods(self):
        for article in Article.objects.all():
            self.assertTrue(os.path.exists(article.get_static_dir()))
            self.assertTrue(os.path.exists(article.get_original_dir()))

    def test_path_methods(self):
        for article in Article.objects.all():
            self.assertTrue(os.path.exists(article.get_static_path()))
            mml_commented_dirname = os.path.dirname(article.get_commented_path())
            self.assertTrue(os.path.exists(mml_commented_dirname))
            self.assertTrue(os.path.exists(article.get_original_path()))
            self.assertTrue(os.path.exists(article.get_mml_path()))

    def test_url_methods(self):
        client = Client()
        for article in Article.objects.all():
            absolute_response = client.get(article.get_absolute_url())
            self.assertEqual(absolute_response.status_code, 200)

            static_response = client.get(article.get_static_url())
            print(article.get_static_url())
            self.assertEqual(static_response.status_code, 200)

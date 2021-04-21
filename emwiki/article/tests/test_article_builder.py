from article.article_builder import ArticleBuilder
from article.models import Article
from emwiki.settings import TEST_MIZFILE_DIR, TEST_MIZFILE_DIR
from django.test import TestCase


class ArticleBuilderTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.builder = ArticleBuilder()
        cls.builder.from_dir = TEST_MIZFILE_DIR

    @classmethod
    def tearDownClass(cls):
        cls.builder.delete_models()

    def test_delete_models(self):
        self.builder.delete_models()
        self.assertEqual(0, len(Article.objects.all()))

    def test_create_articles(self):
        self.builder.create_models()
        self.assertEqual(1, len(Article.objects.all()))

    def test_create_comments(self):
        self.builder.from_dir = TEST_MIZFILE_DIR
        self.builder.create_models()
        article = Article.objects.get(name='abcmiz_0')
        self.assertIsNotNone(article)
        self.assertEqual(241, len(article.comment_set.all()))

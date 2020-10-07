from contents.article.article_builder import ArticleBuilder
from contents.article.models import Article
from emwiki.settings import TEST_RAW_MIZFILE_DIR, TEST_COMMENTED_MIZFILE_DIR
from django.test import TestCase


class HistoryManagementTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.builder = ArticleBuilder()
        cls.builder.from_dir = TEST_RAW_MIZFILE_DIR

    @classmethod
    def tearDownClass(cls):
        cls.builder.delete_models()

    def test_delete_models(self):
        self.builder.delete_models()
        self.assertEqual(0, len(Article.objects.all()))
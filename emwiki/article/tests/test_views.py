import os

from article.article_builder import ArticleBuilder
from article.htmlized_mml_builder import HtmlizedMmlBuilder
from article.models import Article
from django.conf import settings
from django.template.loader import get_template
from django.test import Client, TestCase, override_settings

TEMPLATES = settings.TEMPLATES
TEMPLATES[0]["DIRS"].append(os.path.join(settings.BASE_DIR, "article", "tests", "templates"))


@override_settings(TEMPLATES=TEMPLATES)
class ArticleTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.article_builder = ArticleBuilder()
        cls.article_builder.from_dir = settings.TEST_RAW_MML_MML_DIR
        cls.article_builder.create_models()
        cls.htmlized_mml_builder = HtmlizedMmlBuilder()
        cls.htmlized_mml_builder.from_dir = settings.TEST_MML_HTML_DIR
        cls.htmlized_mml_builder.to_dir = os.path.join(settings.BASE_DIR, "article", "tests", "templates", "article", "htmlized_mml")
        cls.htmlized_mml_builder.delete_files()
        cls.htmlized_mml_builder.create_files()

    @classmethod
    def tearDownClass(cls):
        cls.article_builder.delete_models()
        cls.htmlized_mml_builder.delete_files()

    def test_get(self):
        client = Client()
        for article in Article.objects.all():
            absolute_response = client.get(article.get_absolute_url(), follow=True)
            self.assertEqual(absolute_response.status_code, 200)
            self.assertIsNotNone(get_template(article.template_url))

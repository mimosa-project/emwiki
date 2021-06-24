from django.template.loader import get_template
from django.test import TestCase, Client

from article.article_builder import ArticleBuilder
from article.models import Article, Comment
from django.conf import settings


class ArticleTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.builder = ArticleBuilder()
        cls.builder.from_dir = settings.TEST_RAW_MML_MML_DIR
        cls.builder.create_models()

    @classmethod
    def tearDownClass(cls):
        cls.builder.delete_models()

    def test_attributes(self):
        for article in Article.objects.all():
            self.assertIsNotNone(article.name)
            self.assertFalse(article.name.endswith('.html'))

    def test_url_methods(self):
        client = Client()
        for article in Article.objects.all():
            absolute_response = client.get(article.get_absolute_url())
            self.assertEqual(absolute_response.status_code, 200)
            self.assertIsNotNone(get_template(article.template_url))


class CommentTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.builder = ArticleBuilder()
        cls.builder.from_dir = settings.TEST_MML_MML_DIR
        cls.builder.create_models()
        cls.article = Article.objects.get(name='abcmiz_0')

    @classmethod
    def tearDownClass(cls):
        cls.builder.delete_models()

    def test_attributes(self):
        comment_answers = [
            {'block': 'registration', 'block_order': 1,
                'text': 'This is test\nline 2\nline 3'},
            {'block': 'definition', 'block_order': 1, 'text': '\nThis is test\n'},
            {'block': 'definition', 'block_order': 2,
                'text': '$$This is test of MathJax$$\n$\star $'},
        ]
        for comment_answer in comment_answers:
            comment = Comment.objects.get(
                block=comment_answer['block'],
                block_order=comment_answer['block_order']
            )
            self.assertEqual(comment.article, self.article)
            self.assertEqual(comment.block, comment_answer['block'])
            self.assertEqual(comment.block_order,
                             comment_answer['block_order'])
            self.assertEqual(comment.text, comment_answer['text'])

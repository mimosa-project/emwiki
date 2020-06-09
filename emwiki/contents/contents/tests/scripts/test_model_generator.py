from django.test import TestCase

from contents.article.initializers.model_generator \
    import ArticleModelGenerator, CommentModelGenerator
from contents.article.models import Article
from emwiki.settings import TEST_MML_ARTICLES_ORIGINAL_DIR


class ArticleModelGeneratorTest(TestCase):
    names = [
        'abcmiz_0',
        'abcmiz_1',
        'abcmiz_a',
        'abian',
        'afinsq_1',
        'altcat_3',
        'altcat_5',
        'aofa_a00',
        'armstrng',
        'boolealg',
        'filerec1'
    ]

    def test_generate(self):
        article_generator = ArticleModelGenerator(Article)
        from_dir = TEST_MML_ARTICLES_ORIGINAL_DIR
        articles = article_generator.generate(from_dir)
        for article in articles:
            self.assertEqual(article.category, 'Article')
            self.assertIn(article.name, self.names)
        self.assertEqual(len(articles), len(self.names))

    
class CommentModelGeneratorTest(TestCase):

    def test_generate(self):
        article_generator = ArticleModelGenerator(Article)
        from_dir = TEST_MML_ARTICLES_ORIGINAL_DIR
        articles = article_generator.generate(from_dir)
        comment_generator = CommentModelGenerator()
        comments = comment_generator.generate(articles)

        for comment in comments:
            self.assertIn(comment.article, articles)
            self.assertIsNotNone(comment.block)
            self.assertIsNotNone(comment.block_order)
            self.assertIsNotNone(comment.text)
        self.assertEqual(len(comments), 3)

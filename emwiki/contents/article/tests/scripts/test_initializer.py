from django.test import TestCase

from contents.article.initializers.initializer import ArticleInitializer

from emwiki.settings import TEST_MML_ARTICLES_ORIGINAL_DIR, TEST_MML_ARTICLES_DIR


class InitializerTest(TestCase):

    def test_initialize(self):
        initializer = ArticleInitializer()
        initializer.initialize(
            TEST_MML_ARTICLES_ORIGINAL_DIR,
            TEST_MML_ARTICLES_DIR
        )

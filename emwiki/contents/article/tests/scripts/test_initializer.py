from django.test import TestCase

from contents.article.scripts.initializer import ArticleInitializer
from contents.article.models import Article
from contents.contents.tests.scripts.test_initializer import ContentInitializerTest
from emwiki.settings import TEST_RAW_HTMLIZEDMML_DIR, TEST_CACHE_DIR, TEST_PRODUCT_HTMLIZEDMML_DIR



class InitializerTest(TestCase):

    def test_initialize(self):
        initializer = ArticleInitializer()
        initializer.initialize(
            TEST_MML_ARTICLES_ORIGINAL_DIR,
            TEST_MML_ARTICLES_DIR
        )

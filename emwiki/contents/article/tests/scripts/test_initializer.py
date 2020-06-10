import glob
import os
import shutil

from django.test import TestCase

from contents.article.scripts.initializer import ArticleInitializer
from contents.article.models import Article
from contents.contents.tests.scripts.test_initializer import ContentInitializerTest
from emwiki.settings import TEST_RAW_HTMLIZEDMML_DIR, TEST_CACHE_DIR, TEST_PRODUCT_HTMLIZEDMML_DIR


class ArticleInitializerTest(TestCase, ContentInitializerTest):

    def setUp(self):
        articles = []
        raw_htmlizedmml_paths = glob.glob(os.path.join(TEST_RAW_HTMLIZEDMML_DIR, '*.html'))
        for path in raw_htmlizedmml_paths:
            basename = os.path.basename(path)
            name = os.path.splitext(basename)[0]
            article = Article(name)
            articles.append(article)
        Article.objects.bulk_create(articles)

    @classmethod
    def setUpClass(cls):
        product_htmlizedmml_paths = glob.glob(os.path.join(TEST_PRODUCT_HTMLIZEDMML_DIR, '*.html'))
        for path in product_htmlizedmml_paths:
            os.remove(path)

    @classmethod
    def tearDownClass(cls):
        cache_paths = glob.glob(os.path.join(TEST_CACHE_DIR, '*.html'))
        for path in cache_paths:
            os.remove(path)

    def test_initialize(self):
        initializer = ArticleInitializer()
        initializer.raw_htmlizedmml_dir = TEST_RAW_HTMLIZEDMML_DIR
        initializer.product_htmlizedmml_dir = TEST_PRODUCT_HTMLIZEDMML_DIR
        initializer.initialize()

        raw_html_paths = glob.glob(os.path.join(TEST_RAW_HTMLIZEDMML_DIR, '*.html'))
        product_html_paths = glob.glob(os.path.join(TEST_PRODUCT_HTMLIZEDMML_DIR, '*.html'))
        self.assertEqual(len(Article.objects.all()), len(raw_html_paths))
        self.assertEqual(len(product_html_paths), len(raw_html_paths))

    def test_generate_files(self):
        pass

    def test_delete_models(self):
        pass

    def test_create_models(self):
        Article.objects.all().delete()
        initializer = ArticleInitializer()
        initializer.raw_htmlizedmml_dir = TEST_RAW_HTMLIZEDMML_DIR
        initializer.product_htmlizedmml_dir = TEST_CACHE_DIR
        initializer._create_models()

        paths = glob.glob(os.path.join(TEST_PRODUCT_HTMLIZEDMML_DIR, '*.html'))
        self.assertEqual(Article.objects.all().count(), len(paths))

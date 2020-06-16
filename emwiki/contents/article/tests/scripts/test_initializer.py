import glob
import os
import shutil

from django.test import TestCase

from contents.article.scripts.initializer import ArticleInitializer
from contents.article.models import Article
from contents.contents.tests.scripts.test_initializer import ContentInitializerTest


class ArticleInitializerTest(TestCase, ContentInitializerTest):

    def setUp(self):
        articles = []
        raw_htmlizedmml_paths = glob.glob(os.path.join(self.from_dir, '*.html'))
        for path in raw_htmlizedmml_paths:
            basename = os.path.basename(path)
            name = os.path.splitext(basename)[0]
            article = Article(name)
            articles.append(article)
        Article.objects.bulk_create(articles)

    @classmethod
    def setUpClass(cls):
        from emwiki.settings import TEST_RAW_HTMLIZEDMML_DIR, TEST_PRODUCT_HTMLIZEDMML_DIR, TEST_OUTPUTS_DIR
        cache_dir = os.path.join(TEST_OUTPUTS_DIR, 'cache')
        cls.from_dir = TEST_RAW_HTMLIZEDMML_DIR
        cls.to_dir = cache_dir
        os.mkdir(cache_dir)
        cls.initializer = ArticleInitializer()
        cls.initializer.raw_htmlized_dir = cls.from_dir
        cls.initializer.product_htmlizedmml_dir = self.to_dir

    @classmethod
    def tearDownClass(cls):
        shutil.rmtree(cls.to_dir)

    def test_created_article_models(self):
        self.initializer.initialize()
        raw_html_paths = glob.glob(os.path.join(self.from_dir, '*.html'))
        raw_html_paths_names_set = set([os.path.splitext(os.path.basename(path))[0] for path in raw_html_paths])
        created_model_names_set = set([article.name for article in Article.objects.all()])
        self.assertSetEqual(raw_html_paths_names_set, created_model_names_set)

    def test_product_htmlizedmml_files(self):
        self.initializer.initialize()

        raw_html_paths = glob.glob(os.path.join(self.from_dir, '*.html'))
        raw_html_path_basenames_set = set([os.path.basename(path) for path in raw_html_paths])

        product_html_paths = glob.glob(os.path.join(self.to_dir, '*.html'))
        product_html_path_basenames_set = set([os.path.basename(path) for path in product_html_paths])

        self.assertSetEqual(raw_html_path_basenames, product_html_path_basenames_set)

    def test_generate_files(self):
        pass

    def test_delete_models(self):
        self.initializer._delete_models()
        self.assertEqual(len(Article.objects.all()), 0)

    def test_create_models(self):
        Article.objects.all().delete()
        initializer = ArticleInitializer()
        initializer.raw_htmlizedmml_dir = self.from_dir
        initializer.product_htmlizedmml_dir = self.to_dir
        initializer._create_models()

        paths = glob.glob(os.path.join(self.from_dir, '*.html'))
        self.assertEqual(Article.objects.all().count(), len(paths))

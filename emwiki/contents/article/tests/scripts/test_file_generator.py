import glob
import os

from django.test import TestCase

from contents.article.initializers.file_generator \
    import ArticleFileGenerator, Content
from emwiki.settings import TEST_MML_ARTICLES_ORIGINAL_DIR, \
    TEST_MML_ARTICLES_DIR


class ArticleFileGeneratorTest(TestCase):

    def test_generate(self):
        generator = ArticleFileGenerator()
        from_dir = TEST_MML_ARTICLES_ORIGINAL_DIR
        to_dir = TEST_MML_ARTICLES_DIR
        generator.generate(from_dir, to_dir)
        from_html_paths = glob.glob(os.path.join(from_dir, "*.html"))
        to_html_paths = glob.glob(os.path.join(to_dir, '*.html'))
        self.assertEqual(len(from_html_paths), len(to_html_paths))


class ContentTest(TestCase):

    def get_test_paths(self):
        return glob.glob(os.path.join(TEST_MML_ARTICLES_ORIGINAL_DIR, "*.html"))

    def test_read(self):
        html_paths = self.get_test_paths()
        for path in html_paths:
            content = Content()
            content.read(path)
            self.assertIsNotNone(content.root)
            self.assertIsNone(content.text)

    def test_build(self):
        html_paths = self.get_test_paths()
        for path in html_paths:
            content = Content()
            content.read(path)
            content.build()
            self.assertIsNotNone(content.text)

    def test_write(self):
        html_paths = self.get_test_paths()
        for path in html_paths:
            content = Content()
            content.read(path)
            content.build()
            basename = os.path.basename(path)
            to_path = os.path.join(TEST_MML_ARTICLES_DIR, basename)
            content.write(to_path)
            self.assertTrue(os.path.exists(to_path))

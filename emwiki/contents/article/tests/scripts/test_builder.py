import glob
import os

from django.test import TestCase
from lxml import html

from contents.article.scripts.builder import ArticleBuilder
from contents.contents.tests.scripts.test_builder import ContentBuilder
from emwiki.settings import TEST_RAW_HTMLIZEDMML_DIR, TEST_PRODUCT_HTMLIZEDMML_DIR


class ArticleBuilderTest(TestCase, ContentBuilder):

    @classmethod
    def setUpClass(cls):
        from contents.article.scripts.builder import ArticleBuilder
        from emwiki.settings import TEST_OUTPUT_PRODUCT_HTMLIZEDMML_DIR, TEST_RAW_HTMLIZEDMML_DIR

        cls.from_dir = TEST_RAW_HTMLIZEDMML_DIR
        cls.from_paths = glob.glob(os.path.join(cls.from_dir, '*.html'))
        cls.to_dir = TEST_OUTPUT_PRODUCT_HTMLIZEDMML_DIR
        builder = ArticleBuilder()
        builder.bulk_build(cls.from_dir, cls.to_dir)
        cls.to_paths = glob.glob(os.path.join(cls.to_dir, '*.html'))

    @classmethod
    def tearDownClass(cls):
        pass

    def test_number_of_files(self):
        self.assertEqual(len(self.from_paths), len(self.to_paths))

    def test_html_head_has_base(self):
        for to_path in self.to_paths:
            root = html.parse(to_path)
            base = root.xpath('//head/base')[0]
            self.assertEqual(base.attrib['href'], '/static/mml_articles/')
            self.assertEqual(base.attrib['target'], '_self')

    def test_html_head_has_mathjax(self):
        for to_path in self.to_paths:
            root = html.parse(to_path)
            script_of_mathjax = root.xpath('//head/script[@id="MathJax-script"]')[0]
            self.assertEqual(script_of_mathjax.attrib['id'], 'MathJax-script')

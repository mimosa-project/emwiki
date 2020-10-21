import os
import difflib as diff

from django.test import TestCase

from contents.article.models import Article
from contents.article.miz_file import MizFile
from contents.article.article_builder import ArticleBuilder
from contents.contents.tests.test_file import FileTest
from emwiki.settings import TEST_OUTPUTS_DIR, TEST_MIZFILE_DIR,\
    TEST_RAW_MIZFILE_DIR


class MizFileTest(TestCase, FileTest):
    from_path = os.path.join(TEST_MIZFILE_DIR, 'abcmiz_0.miz')
    bad_path = 'abcmiz'
    to_path = os.path.join(TEST_OUTPUTS_DIR, 'abcmiz_0.miz')

    @classmethod
    def setUpClass(cls):
        cls.builder = ArticleBuilder()
        cls.builder.from_dir = TEST_MIZFILE_DIR
        cls.builder.delete_models()
        cls.builder.create_models()
        cls.article = Article.objects.get(name='abcmiz_0')

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls.to_path):
            os.remove(cls.to_path)
        cls.builder.delete_models()

    def test_constractor(self):
        MizFile(self.from_path)
        MizFile(self.bad_path)

    def test_read(self):
        mizfile = MizFile(self.from_path)
        mizfile.read()
        self.assertIsNotNone(mizfile.text)
        mizfile.path = self.bad_path
        with self.assertRaises(FileNotFoundError):
            mizfile.read()

    def test_write(self):
        mizfile = MizFile(self.from_path)
        mizfile.read()
        mizfile.path = self.to_path
        mizfile.write()
        self.assertTrue(os.path.exists(self.to_path))

        with open(self.from_path, 'r') as f:
            from_text = f.read()
        with open(self.to_path, 'r') as f:
            to_text = f.read()
        self.assertEqual(from_text, to_text)

    def test_embed(self):
        raw_mizfile = MizFile(os.path.join(TEST_RAW_MIZFILE_DIR, 'abcmiz_0.miz'))
        commented_mizfile = MizFile(os.path.join(TEST_MIZFILE_DIR, 'abcmiz_0.miz'))

        raw_mizfile.read()
        commented_mizfile.read()

        raw_mizfile.embed(self.article.comment_set.all())

        self.assertEqual(raw_mizfile.text, commented_mizfile.text)

    def test_extract(self):
        raw_mizfile = MizFile(os.path.join(TEST_RAW_MIZFILE_DIR, 'abcmiz_0.miz'))
        commented_mizfile = MizFile(os.path.join(TEST_MIZFILE_DIR, 'abcmiz_0.miz'))

        raw_mizfile.read()
        commented_mizfile.read()
        comments = commented_mizfile.extract(self.article)

        self.assertEqual(commented_mizfile.text, raw_mizfile.text)

        self.assertEqual(len(comments), 238)

    def test_restorebility(self):
        raw_mizfile = MizFile(os.path.join(TEST_RAW_MIZFILE_DIR, 'abcmiz_0.miz'))
        before_text = ''
        after_text = ''

        raw_mizfile.read()
        before_text = raw_mizfile.text
        raw_mizfile.embed(self.article.comment_set.all())
        raw_mizfile.extract(self.article)
        after_text = raw_mizfile.text

        self.assertEqual(before_text, after_text)

import os

from django.test import TestCase

from contents.article.models import Article
from contents.contents.scripts.mizfile_archiver import MizFileArchiver
from emwiki.settings import TEST_RAW_MIZFILE_DIR, TEST_COMMENTED_MIZFILE_DIR, \
    TEST_CACHE_DIR
 

class MizFileArchiverTest(TestCase):

    def setUp(self):
        Article.objects.all().delete()
        self.mizfile_archiver = MizFileArchiver()
        self.mizfile_archiver.raw_mizfile_dir = TEST_RAW_MIZFILE_DIR
        self.mizfile_archiver.commented_mizfile_dir = TEST_COMMENTED_MIZFILE_DIR
        Article.objects.create(name='abcmiz_0')
        Article.objects.create(name='test')
        self.article_exists = Article.objects.get(name='abcmiz_0')
        self.article_not_exists = Article.objects.get(name='test')

    def test_push(self):
        self.mizfile_archiver.commented_mizfile_dir = TEST_CACHE_DIR
        self.mizfile_archiver.push(self.article_exists)
        with self.assertRaises(Exception):
            self.mizfile_archiver.push(self.article_not_exists)

    def test_pull(self):
        comments = self.mizfile_archiver.pull(self.article_exists)
        self.assertEqual(len(comments), 3)

import os

from article.downloader import Downloader
from emwiki.settings import TEST_DOWNLOAD_MML_DIR, TEST_DOWNLOAD_HTML_DIR
from django.test import TestCase


class DownloaderTest(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.mml_url = 'http://mizar.org/version/current/mml'
        cls.html_url = 'http://mizar.org/version/current/html'

    @classmethod
    def tearDownClass(cls):
        pass

    def test_read_index(self):
        downloaders = []
        downloaders.append(Downloader(self.mml_url, '.miz'))
        downloaders.append(Downloader(self.html_url, '.html'))

        for downloader in downloaders:
            downloader.read_index()
            self.assertEqual(1358, len(downloader.urls))

    def test_download(self):
        mml_downloader = Downloader(self.mml_url, '.miz')
        html_downloader = Downloader(self.html_url, '.html')

        mml_downloader.read_index()
        mml_downloader.urls = mml_downloader.urls[:5]
        mml_downloader.download(TEST_DOWNLOAD_MML_DIR)
        self.assertEqual(len(os.listdir(TEST_DOWNLOAD_MML_DIR)), 6)

        html_downloader.read_index()
        html_downloader.urls = html_downloader.urls[:5]
        html_downloader.download(TEST_DOWNLOAD_HTML_DIR)
        self.assertEqual(len(os.listdir(TEST_DOWNLOAD_HTML_DIR)), 6)

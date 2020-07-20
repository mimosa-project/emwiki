import os
from unittest import TestCase

from contents.symbol.symbol_maker.downloader import Downloader

"""
class TestDownloader(TestCase):
    @classmethod
    def setUpClass(cls):
        cls._local_dir = os.path.dirname(__file__)
        cls._local_dir = cls._local_dir.replace('\\', '/')
        cls._to_dir = cls._local_dir + "/tmp"
        if not os.path.exists(cls._to_dir):
            os.makedirs(cls._to_dir)

    @classmethod
    def tearDownClass(cls):
        if os.path.exists(cls._to_dir):
            os.removedirs(cls._to_dir)

    def setUp(self):
        pass

    def tearDown(self):
        for file in os.listdir(self._to_dir):
            os.remove(self._to_dir + "/" + file)

    def test_handle_starttag(self):
        pass

    def test_read_index(self):
        downloader = Downloader()
        path = "file:///" + self._local_dir + "/testdata/downloader/page_index.html"
        path = path.replace('\\', '/')
        downloader.read_index(path)
        self.assertEqual(len(downloader.files), 1195)
        self.assertEqual(downloader.files[0], 'abcmiz_0.html')

    def test_download(self):
        pass
"""
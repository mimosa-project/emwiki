from abc import ABCMeta, abstractmethod
import os

from django.test import TestCase

from contents.contents.scripts.files import MizFile, HtmlizedMmlFile
from emwiki.settings import TEST_RAW_MIZFILE_DIR, TEST_CACHE_DIR, TEST_RAW_HTMLIZEDMML_DIR


class FileTest(metaclass=ABCMeta):

    @abstractmethod
    def test_constractor(self):
        pass

    @abstractmethod
    def test_read(self):
        pass

    @abstractmethod
    def test_write(self):
        pass


class MizFileTest(TestCase, FileTest):
    from_path = os.path.join(TEST_RAW_MIZFILE_DIR, 'abcmiz_0.miz')
    bad_path = 'abcmiz'
    to_path = os.path.join(TEST_CACHE_DIR, 'abcmiz_0.miz')

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


class HtmlizedMmlFileTest(TestCase, FileTest):
    from_path = os.path.join(TEST_RAW_HTMLIZEDMML_DIR, 'abcmiz_0.html')
    bad_path = 'abcmiz'
    to_path = os.path.join(TEST_CACHE_DIR, 'abcmiz_0.html')

    def test_constractor(self):
        HtmlizedMmlFile(self.from_path)

    def test_read(self):
        htmlizedmmlfile = HtmlizedMmlFile(self.from_path)
        htmlizedmmlfile.read()
        self.assertIsNotNone(htmlizedmmlfile.root)
        htmlizedmmlfile.path = self.bad_path
        with self.assertRaises(Exception):
            htmlizedmmlfile.read()
            
    def test_write(self):
        htmlizedmmlfile = HtmlizedMmlFile(self.from_path)
        htmlizedmmlfile.read()
        htmlizedmmlfile.path = self.to_path
        htmlizedmmlfile.write()

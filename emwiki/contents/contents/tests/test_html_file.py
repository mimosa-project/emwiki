import os

from django.test import TestCase

from contents.contents.html_file import HtmlFile
from contents.contents.tests.test_file import FileTest
from emwiki.settings import TEST_OUTPUTS_DIR, TEST_RAW_HTMLIZEDMML_DIR


class HtmlFileTest(TestCase, FileTest):
    from_path = os.path.join(TEST_RAW_HTMLIZEDMML_DIR, 'abcmiz_0.html')
    bad_path = 'abcmiz'
    to_path = os.path.join(TEST_OUTPUTS_DIR, 'abcmiz_0.html')

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.to_path)

    def test_constractor(self):
        HtmlFile(self.from_path)
        HtmlFile(self.bad_path)

    def test_read(self):
        html_file = HtmlFile(self.from_path)
        html_file.read()
        self.assertIsNotNone(html_file.root)
        html_file.path = self.bad_path
        with self.assertRaises(Exception):
            html_file.read()

    def test_write(self):
        html_file = HtmlFile(self.from_path)
        html_file.read()
        html_file.path = self.to_path
        html_file.write()
        self.assertTrue(os.path.exists(self.to_path))

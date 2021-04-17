import os
from unittest import TestCase

from symbol.symbol_maker.reader import Reader
from emwiki.settings import TEST_RAW_HTMLIZEDMML_DIR


class TestElement(TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def read_by_name(self, name):
        path = os.path.join(TEST_RAW_HTMLIZEDMML_DIR, name + ".html")
        path = path.replace('\\', '/')
        reader = Reader()
        reader.read(path)
        return reader

    @staticmethod
    def filter_by_type(elements, typename):
        return [e for e in elements if e.type() == typename]

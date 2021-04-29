import os
from unittest import TestCase

from symbol.symbol_maker.reader import Reader
from django.conf import settings


class TestElement(TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def read_by_name(self, name):
        path = os.path.join(settings.TEST_RAW_HTMLIZEDMML_DIR, name + ".html")
        path = path.replace('\\', '/')
        reader = Reader()
        reader.read(path)
        return reader

    @staticmethod
    def filter_by_type(elements, typename):
        return [e for e in elements if e.type() == typename]

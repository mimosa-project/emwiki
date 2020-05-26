#!/usr/bin/env python
# encoding: utf-8
__author__ = 'nakasho'

from unittest import TestCase
from mmlfrontend.reader import Reader
import os.path


class TestElement(TestCase):
    @classmethod
    def setUpClass(cls):
        cls._local_dir = os.path.dirname(os.path.dirname(__file__))
        cls._local_dir = cls._local_dir.replace('\\', '/')

    @classmethod
    def tearDownClass(cls):
        pass

    def read_by_name(self, name):
        path = "file:///" + self._local_dir + "/data/reader/" + name + ".html"
        path = path.replace('\\', '/')
        reader = Reader()
        reader.read(path)
        return reader

    @staticmethod
    def filter_by_type(elements, typename):
        return [e for e in elements if e.type() == typename]

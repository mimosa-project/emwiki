#!/usr/bin/env python
# encoding: utf-8
from unittest import TestCase
from mmlfrontend.writer import IndexWriter

__author__ = 'nakasho'


class TestIndexWriter(TestCase):
    def test_escape_characters(self):
        self.assertEqual('\\\\', IndexWriter.escape_characters('\\'))
        self.assertEqual('\\\'', IndexWriter.escape_characters('\''))
        self.assertEqual('\\"', IndexWriter.escape_characters('"'))
        self.assertEqual("\\\\\\'\\\"", IndexWriter.escape_characters("\\'\""))

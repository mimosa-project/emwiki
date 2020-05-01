#!/usr/bin/env python
# encoding: utf-8
__author__ = 'nakasho'

import glob
import os
import os.path
import time
from mmlfrontend.reader import *
from mmlfrontend.composer import *
from mmlfrontend.writer import *
from mmlfrontend.elements.element import *
import locale
from natsort import humansorted
locale.setlocale(locale.LC_ALL, '')

from emwiki.settings import BASE_DIR


class Processor:
    def __init__(self):
        Element._total_num = 0
        self.elements = []
        self.contents = []

    def execute(self, from_dir, to_dir):
        self.read(from_dir)
        self.compose()
        self.write(to_dir)

    def read(self, from_dir):
        htmls = glob.glob(from_dir + "/*.html")
        htmls = humansorted(htmls)

        total_count = len(htmls)
        for i, html in enumerate(htmls):
            print("reading {}/{}".format(i, total_count))
            reader = Reader()
            reader.read(html)
            self.elements += reader.elements

    def compose(self):
        print("composing...")
        composer = Composer()
        composer.elements = self.elements
        composer.build()
        self.contents = composer.contents

    def write(self, to_dir):
        index_writer = IndexWriter()
        index_writer.contents = self.contents
        index_writer.write(to_dir + '/js/mml-index.js')

        contents_dir = to_dir + '/mml-contents'
        if not os.path.exists(contents_dir):
            time.sleep(0.01)
            os.mkdir(contents_dir)

        total_count = len(self.contents)
        for i, content in enumerate(self.contents):
            if i % 10 == 0:
                print("writing {}/{}".format(i, total_count))
            content_writer = ContentWriter()
            content_writer.content = content
            content_writer.write(contents_dir + '/' + content.filename())

if __name__ == '__main__':
    from_dir = os.path.join(BASE_DIR, 'static', 'mizar_html')
    to_dir = os.path.join(BASE_DIR, 'mmlreference', 'templates', 'mmlreference')
    processor = Processor()
    processor.execute(from_dir, to_dir)

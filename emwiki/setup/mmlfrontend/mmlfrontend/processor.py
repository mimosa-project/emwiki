#!/usr/bin/env python
# encoding: utf-8
__author__ = 'nakasho'

import glob
import os
import os.path
import time
from setup.mmlfrontend.mmlfrontend.reader import Reader
from setup.mmlfrontend.mmlfrontend.composer import Composer
from setup.mmlfrontend.mmlfrontend.writer import ContentWriter
from setup.mmlfrontend.mmlfrontend.elements.element import Element
from setup.mmlfrontend.mmlfrontend.models import SymbolInitializer
from setup.mmlfrontend.mmlfrontend.models import SymbolInitializer
import locale
from natsort import humansorted

locale.setlocale(locale.LC_ALL, '')

import django
django.setup()
from emwiki.settings import BASE_DIR, MML_ARTICLES_DIR, MML_SYMBOLS_DIR
import urllib
from contents.article.models import Article


class Processor:
    def __init__(self):
        Element._total_num = 0
        self.elements = []
        self.contents = []
        self.articles = []

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
            basename = os.path.basename(html)
            article = Article(name=os.path.splitext(basename)[0])
            self.elements += reader.elements
            self.articles.append(article)
            
    def compose(self):
        print("composing...")
        composer = Composer()
        composer.elements = self.elements
        composer.build()
        self.contents = composer.contents

    def write(self, to_dir):
        model_writer = ModelWriter()
        model_writer.contents = self.contents
        model_writer.articles = self.articles
        model_writer.write()

        contents_dir = to_dir
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
    from_dir = os.path.join(BASE_DIR, 'setup', 'mmlfrontend', 'tests', 'data', 'reader')  #MML_ARTICLES_DIR
    to_dir = MML_SYMBOLS_DIR
    processor = Processor()
    processor.execute(from_dir, to_dir)

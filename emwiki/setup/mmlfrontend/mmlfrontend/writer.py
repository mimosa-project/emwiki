#!/usr/bin/env python
# encoding: utf-8
__author__ = 'nakasho'

import codecs
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'emwiki.settings')
import django
import os.path
django.setup()
from contents.article.models import Article, Comment
from contents.article.classes import MizFile
from contents.symbol.models import Symbol


class ModelWriter:
    def __init__(self):
        self.contents = []
        self.articles = []

    def write(self):
        Symbol.objects.all().delete()
        Article.objects.all().delete()
        symbols = []
        articles = []
        comments = []
        for content in self.contents:
            symbol = Symbol(
                name=content.symbol,
                filename=content.filename()
            )
            symbols.append(symbol)
        for article in self.articles:
            articles.append(article)
            if os.path.exists(article.get_commented_path()):
                print('exists')
                mizfile = MizFile()
                mizfile.read(article.get_commented_path())
                comments.extend(mizfile.extract_comments(article))

        print('Symbols:', len(symbols))
        print('Articles:', len(articles))
        print('Comments:', len(comments))
        Symbol.objects.bulk_create(symbols)
        Article.objects.bulk_create(articles)
        Comment.objects.bulk_create(comments)


class ContentWriter:
    def __init__(self):
        self.content = None

    def write(self, path):
        with codecs.open(path, 'w', 'utf-8-sig') as fp:
            fp.write("<!DOCTYPE html>\n"
                     "<html lang='en'>\n")
            self.write_header(fp)
            self.write_body(fp)
            fp.write("</html>\n")

    def write_header(self, fp):
        fp.write("<head>\n"
                 "<meta charset='UTF-8'>\n"
                 "<title>" + self.content.symbol + "</title>\n"
                 "</head>\n")

    def write_body(self, fp):
        fp.write("<body>\n")
        self.content.write(fp)
        fp.write("</body>\n")

if __name__ == '__main__':
    pass

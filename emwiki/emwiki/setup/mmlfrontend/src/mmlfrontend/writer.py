#!/usr/bin/env python
# encoding: utf-8
__author__ = 'nakasho'

import re
import codecs
from mmlfrontend.content import Content


class IndexWriter:
    def __init__(self):
        self.contents = []

    def write(self, path):
        types = ['"' + c.type + '"' for c in self.contents]
        symbols = ['"' + self.escape_characters(c.symbol) + '"' for c in self.contents]
        filenames = ['"' + self.escape_characters(c.filename()) + '"' for c in self.contents]
        with codecs.open(path, 'w', 'utf-8-sig') as fp:
            fp.write('var index_data = {"symbols": [' + ','.join(symbols) + '], ')
            fp.write('"types": [' + ','.join(types) + '], ')
            fp.write('"filenames": [' + ','.join(filenames) + ']};')

    @staticmethod
    def escape_characters(str):
        return re.sub(r'([\\\'"])', r'\\\1', str)


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

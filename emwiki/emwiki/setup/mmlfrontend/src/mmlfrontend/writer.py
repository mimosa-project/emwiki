#!/usr/bin/env python
# encoding: utf-8
__author__ = 'nakasho'

import re
import codecs
from mmlfrontend.content import Content
import json


class IndexWriter:
    def __init__(self):
        self.contents = []

    def write(self, path):
        index_dict = {}
        for content in self.contents:
            index_dict[content.filename()] = {
                'type': content.type,
                'symbol': content.symbol
            }
        with open(path, 'w') as f:
            json.dump(index_dict, f)


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

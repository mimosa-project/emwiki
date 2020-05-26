#!/usr/bin/env python
# encoding: utf-8
__author__ = 'nakasho'

from contents.symbol.initialization.elements.element import Element


class Content:
    _total_num = 0

    def __init__(self):
        self.type = ''
        self.symbol = ''
        self.elements = []
        self.id = Content._total_num
        Content._total_num += 1

    @staticmethod
    def escape_html_characters(s):
        return s.replace('<', '&lt;')

    def filename(self):
        return str(self.id) + '.html'

    def write(self, fp):
        self.write_summary(fp)
        for i, e in enumerate(self.elements):
            e.write(fp, i+1)

    def write_summary(self, fp):
        fp.write("<div class='mml-summary'>\n")
        title = "List of Definitions (" + str(len(self.elements)) + ")"
        rep = self.elements[0]
        fp.write("<h1>" + rep.type() + " " + self.escape_html_characters(rep.symbol) + "</h1>\n"
                 "<h2>" + title + "</h2>\n"
                 "<ol>\n")
        for i, e in enumerate(self.elements):
            fp.write("<li>" + e.element_link_html(e)
                     + " [" + e.source_link_html(e) + "]</li>\n")
        fp.write("</ol>\n"
                 "</div>\n")
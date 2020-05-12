#!/usr/bin/env python
# encoding: utf-8
__author__ = 'nakasho'

from mmlfrontend.content import Content
import locale
from natsort import humansorted
locale.setlocale(locale.LC_ALL, '')


class Composer:
    def __init__(self):
        self.elements = []
        self.contents = []
        self.link2element = {}

    def build(self):
        print("  build_contents")
        self.build_contents()
        print("  resolve_relations")
        self.resolve_relations()
        print("  collect_relations")
        self.collect_relations()
        print("  adjust_elements")
        self.adjust_elements()

    def build_contents(self):
        contents_dict = {}

        for element in self.elements:
            if element.type() in ["cluster", "reduce"]:
                continue
            key = (element.type(), element.symbol)
            if not key in contents_dict:
                content = Content()
                content.symbol = element.symbol
                content.type = element.type()
                contents_dict[key] = content
            contents_dict[key].elements.append(element)
            element.content = contents_dict[key]

        self.contents = list(contents_dict.values())
        # See https://pypi.python.org/pypi/natsort
        self.contents = humansorted(self.contents, key=lambda x: (x.symbol, x.type))

    def resolve_relations(self):
        # create link2element
        link2element = {}
        for element in self.elements:
            if element.anchor is not None:
                link = element.filename + '.html#' + element.anchor
                link2element[link] = element

        for element in self.elements:
            element.resolve_relations(link2element)

    def collect_relations(self):
        for element in self.elements:
            element.collect_relations(self.elements)

    def adjust_elements(self):
        for element in self.elements:
            element.adjust()

if __name__ == '__main__':
    pass

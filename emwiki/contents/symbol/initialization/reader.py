#!/usr/bin/env python
# encoding: utf-8
__author__ = 'nakasho'

from builtins import staticmethod
import os.path
from lxml import html
from contents.symbol.initialization.elements.pred import Pred
from contents.symbol.initialization.elements.struct import Struct
from contents.symbol.initialization.elements.mode import Mode
from contents.symbol.initialization.elements.func import Func
from contents.symbol.initialization.elements.attr import Attr
from contents.symbol.initialization.elements.cluster import Cluster
from contents.symbol.initialization.elements.reduce import Reduce


class Reader:
    """
    A Reader is correspond to one HTML page.
    """
    def __init__(self):
        self.elements = []

    def read(self, path):
        root = html.parse(path).getroot()
        Reader.remove_proof_blocks(root)

        klasses = [Pred, Struct, Mode, Func, Attr, Cluster, Reduce]
        for klass in klasses:
            elements = klass.create_elements(root)
            for element in elements:
                basename = os.path.basename(path)
                element.filename = os.path.splitext(basename)[0]
            self.elements += elements

    @staticmethod
    def remove_proof_blocks(root):
        proofs = root.xpath("//div[@typeof='oo:Proof']")
        for node in proofs:
            parent = node.getparent()
            parent.remove(node)

        hides = root.xpath("//span[@class='hide']")
        for node in hides:
            parent = node.getparent()
            parent.remove(node)

if __name__ == '__main__':
    pass

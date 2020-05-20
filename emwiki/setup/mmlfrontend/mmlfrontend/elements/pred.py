#!/usr/bin/env python
# encoding: utf-8
__author__ = 'nakasho'

from lxml import html
from setup.mmlfrontend.mmlfrontend.elements.element import Element


class Pred(Element):
    """
    Predicate-Definition = "pred" Predicate-Pattern [ "means" Definiens ] ";" Correctness-Conditions { Predicate-Property } .
    Predicate-Pattern = [ Loci ] Predicate-Symbol [ Loci ] .
    Loci = Locus { "," Locus } .
    Locus = Variable-Identifier .
    """
    @classmethod
    def type(cls):
        return "pred"

    def __init__(self):
        super().__init__()
        self.arguments = []

    def collect_relations(self, elements):
        substitution = self.substitute_redundant_definitions()
        try:
            for node in self.defblock.iter():
                if node == self.keyword_node:
                    return
                if node.tag == 'span' and 'title' in node.attrib and 'data-link' in node.attrib:
                    title = node.attrib['title']
                    link = node.attrib['data-link']
                    keywords = [':struct.', ':mode.', ':NM.']
                    if len([k for k in keywords if k in title]) > 0:
                        index = int(link.split('#ELM')[1])
                        e = elements[index]
                        if not self in e.relations:
                            e.relations.append(self)
        finally:
            self.restore_nodes(substitution)

    '''
    def find_arguments(self):
        #print("argument symbol is {}".format(self.find_argument_symbol()))
        return []

    def find_argument_symbols(self):
        order = self.order_in_defblock()
        defblock = deepcopy(self.defblock)
        sentences = self.lexicalize_defblock(defblock)

        keyword_sentences = [s for s in sentences if len(s) > 0 and self.keyword() in s[0:2]]
        # print("order = {}, len = {}".format(order, len(keyword_sentences)))
        assert len(keyword_sentences) > order
        sentence = keyword_sentences[order]

        if self.keyword() == 'pred' and 'means' in sentence:
            sentence = sentence[0:sentence.index('means')]
        if self.keyword() in ['synonym', 'antonym'] and 'for' in sentence:
            sentence = sentence[0:sentence.index('for')]
        removals = [self.symbol, 'synonym', 'antonym', 'redefine', 'pred']
        return [s for i, s in enumerate(sentence) if not s in removals]
    '''


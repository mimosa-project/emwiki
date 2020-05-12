#!/usr/bin/env python
# encoding: utf-8
__author__ = 'nakasho'

from mmlfrontend.elements.element import Element


class Reduce(Element):
    @classmethod
    def type(cls):
        return "reduce"

    def find_symbol(self):
        return None

    def find_defblock(self):
        node = self.keyword_node

        keyword = "registration"
        finder = "./ancestor::div/span[@class='kw' and contains(text(),'" + keyword + "')]/.."
        candidates = node.xpath(finder)
        if len(candidates):
            return candidates[0]
        else:
            return None

    def find_main_sentence(self):
        candidates = self.keyword_node.xpath("ancestor::div[@typeof = 'oo:Theorem']")
        if len(candidates):
            return candidates[0]
        else:
            return None

    def is_redefine(self):
        return False

    def is_synonym(self):
        return False

    def is_antonym(self):
        return False

    def collect_relations(self, elements):
        substitution = self.substitute_redundant_definitions()
        try:
            for node in self.defblock.iter():
                if node.getprevious() == self.main_sentence:
                    return
                if node.tag == 'span' and 'title' in node.attrib and 'data-link' in node.attrib:
                    title = node.attrib['title']
                    link = node.attrib['data-link']
                    keywords = [':func.', ':attr.']
                    if len([k for k in keywords if k in title]) > 0:
                        index = int(link.split('#ELM')[1])
                        e = elements[index]
                        if not self in e.relations:
                            e.relations.append(self)
        finally:
            self.restore_nodes(substitution)

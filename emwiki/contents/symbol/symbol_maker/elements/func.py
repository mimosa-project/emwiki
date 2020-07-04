#!/usr/bin/env python
# encoding: utf-8
__author__ = 'nakasho'

from lxml import html
from .element import Element


class Func(Element):
    """
    Functor-Definition = "func" Functor-Pattern [ Specification ] [ ( "means" | "equals" ) Definiens ] ";" Correctness-Conditions { Functor-Property } .
    Functor-Pattern = [ Functor-Loci ] Functor-Symbol [ Functor-Loci ] | Left-Functor-Bracket Loci Right-Functor-Bracket .
    Functor-Property = ( "commutativity" | "idempotence" | "involutiveness" | "projectivity" ) Justification ";" .
    Functor-Synonym = "synonym" Functor-Pattern "for" Functor-Pattern ";" .
    Functor-Loci = Locus | "(" Loci ")" .
    Functor-Symbol = Symbol .
    Left-Functor-Bracket = Symbol | "{" | "[" .
    Right-Functor-Bracket = Symbol | "}" | "]" .
    """
    @classmethod
    def type(cls):
        return "func"

    def find_symbol(self):
        finder = "./following::a[contains(@title, ':func.') or contains(@title, ':NK.')][1]"
        candidates = self.keyword_node.xpath(finder)
        if len(candidates) > 0:
            func_symbol = candidates[0]
            name = func_symbol.text.strip()

            if self.keyword_node.text.strip() == 'func':
                title = func_symbol.attrib.get('title')
                finder = "./following-sibling::*[@title='" + title + "']"
                rights = func_symbol.xpath(finder)
                if len(rights) > 0:
                    name += rights[0].text.strip()
            return name
        else:
            return None

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

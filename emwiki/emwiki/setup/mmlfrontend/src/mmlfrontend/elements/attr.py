#!/usr/bin/env python
# encoding: utf-8
__author__ = 'nakasho'

from mmlfrontend.elements.element import Element


class Attr(Element):
    """
    Attribute-Definition = "attr" Attribute-Pattern "means" Definiens ";" Correctness-Conditions .
    Attribute-Pattern = Locus "is" [ Attribute-Loci ] Attribute-Symbol .
    Attribute-Synonym = "synonym" Attribute-Pattern "for" Attribute-Pattern ";" .
    Attribute-Antonym = "antonym" Attribute-Pattern "for" Attribute-Pattern ";" .
    Attribute-Symbol = Symbol .
    Attribute-Loci = Loci | "(" Loci ")" .
    """
    @classmethod
    def type(cls):
        return "attr"

    @classmethod
    def collect_keyword_nodes(cls, root):
        candidates = super().collect_keyword_nodes(root)
        # remove redundant that are not definitions
        results = []
        for node in candidates:
            if node.text.strip() == 'attr':
                if node.xpath("ancestor::div[@typeof='oo:Definition']"):
                    results.append(node)
            else:
                # synonym and antonym
                results.append(node)
        return results

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

#!/usr/bin/env python
# encoding: utf-8
__author__ = 'nakasho'

import re
from setup.mmlfrontend.mmlfrontend.elements.element import Element


class Mode(Element):
    """
    Mode-Definition = "mode" Mode-Pattern ( [ Specification ] [ "means" Definiens ] ";" Correctness-Conditions | "is" Type-Expression ";" ) .
    Mode-Pattern = Mode-Symbol [ "of" Loci ] .
    Mode-Symbol = Symbol | "set" .
    """
    @classmethod
    def type(cls):
        return "mode"

    def find_symbol(self):
        node = self.keyword_node
        if node.text.strip() == "mode" and node.xpath("parent::a[contains(@name, 'NM')]"):
            candidates = node.xpath("../text()")
        else:
            # regular pattern or synonym
            candidates = node.xpath("./following::a[contains(@title, ':mode.')][1]/text()")
        name = candidates[0].strip()

        if name.endswith(' of'):
            name = name[:-3]

        # # if symbol is followed by "of", include it.
        # ms = self.main_sentence
        # if ms is not None:
        #     text = ms.text_content()
        #     m = re.search("mode[^;]*?(->|means)", text)
        #     if m and "of" in m.group(0).split():
        #         name += " of"
        # elif node.text.strip() == "synonym":
        #     text = self.defblock.text_content()
        #     m = re.search("synonym\s+" + name + "\s+of", text)
        #     if m:
        #         name += " of"

        return name

    def collect_relations(self, elements):
        substitution = self.substitute_redundant_definitions()
        try:
            for node in self.defblock.iter():
                if node.tag == 'span' and 'title' in node.attrib and 'data-link' in node.attrib:
                    title = node.attrib['title']
                    link = node.attrib['data-link']
                    keywords = [':struct.', ':mode.', ':NM.']
                    if len([k for k in keywords if k in title]) > 0:
                        index = int(link.split('#ELM')[1])
                        e = elements[index]
                        if not (e == self or self in e.relations):
                            e.relations.append(self)
        finally:
            self.restore_nodes(substitution)

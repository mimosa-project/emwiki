#!/usr/bin/env python
# encoding: utf-8
__author__ = 'nakasho'

from .element import Element


class Struct(Element):
    """
    Structure-Definition = "struct" [ "(" Ancestors ")" ] Structure-Symbol [ "over" Loci ] "(#" Fields "#)" ";" .
    """

    @classmethod
    def type(cls):
        return "struct"

    def find_symbol(self):
        name = super().find_symbol()

        if name.endswith(' over'):
            name = name[:-5]
        """
        # if symbol is followed by "over", include it.
        gp = self.keyword_node.getparent().getparent()
        text = gp.text_content()
        m = re.search("struct[^;]*?->", text)
        if m and "over" in m.group(0).split():
            name += " over"
        """

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

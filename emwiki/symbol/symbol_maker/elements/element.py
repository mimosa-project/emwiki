#!/usr/bin/env python
# encoding: utf-8
from builtins import classmethod
import re
from lxml import html
import locale
from natsort import humansorted
locale.setlocale(locale.LC_ALL, '')

__author__ = 'nakasho'


class Element:
    _total_num = 0

    def __init__(self):
        self.symbol = ""
        self.filename = ""
        self.anchor = None
        self.keyword_node = None
        self.defblock = None
        self.main_sentence = None
        self.content = None
        self.id = Element._total_num
        self.relations = []
        Element._total_num += 1

    @classmethod
    def type(cls):
        return ""

    @classmethod
    def create_elements(cls, root):
        nodes = cls.collect_keyword_nodes(root)

        elements = []
        for node in nodes:
            element = cls()
            element.keyword_node = node
            element.resolve_members()
            elements.append(element)
        return elements

    @classmethod
    def collect_keyword_nodes(cls, root):
        finder = "//span[@class='kw']"
        candidates = root.xpath(finder)

        results = []
        for node in candidates:
            keyword = node.text.strip()
            if keyword == cls.type():
                results.append(node)
            elif keyword == 'synonym' or keyword == 'antonym':
                maybes = node.xpath('./following::a[@title][1]')
                if len(maybes):
                    title = maybes[0].attrib.get('title')
                    if re.search(':' + cls.type() + '.', title):
                        results.append(node)
        return results

    @staticmethod
    def escape_html_characters(s):
        return s.replace('<', '&lt;')

    def find_symbol(self):
        node = self.keyword_node
        finder = "./following::a[contains(@title, ':" + self.type() + ".')][1]/text()"
        candidates = node.xpath(finder)
        if len(candidates):
            return candidates[0].strip()
        else:
            return None

    def keyword(self):
        return self.keyword_node.text.strip()

    def find_defblock(self):
        node = self.keyword_node

        keyword = "definition"
        if node.text.strip() != self.type():
            # synonym or antonym
            keyword = "notation"

        finder = "./ancestor::div/span[@class='kw' and contains(text(),'" + keyword + "')]/.."
        candidates = node.xpath(finder)
        if len(candidates):
            return candidates[0]
        else:
            return None

    def find_main_sentence(self):
        candidates = self.keyword_node.xpath("ancestor::div[@typeof = 'oo:Definition']")
        if len(candidates):
            return candidates[0]
        else:
            return None

    def find_anchor(self):
        # Find name attribute above keyword node
        if self.keyword_node is not None:
            nodes = self.keyword_node.xpath('ancestor-or-self::node()[@name]')
            if len(nodes):
                return nodes[0].attrib.get("name")
        return None

    def is_redefine(self):
        prev = self.keyword_node.getprevious()
        if prev is not None and prev.attrib.get('class') == 'kw':
            if prev.text.strip() == 'redefine':
                return True
        uncle = self.keyword_node.getparent().getprevious()
        if uncle is not None and uncle.attrib.get('class') == 'kw':
            if uncle.text.strip() == 'redefine':
                return True
        return False

    def is_synonym(self):
        return self.keyword() == "synonym"

    def is_antonym(self):
        return self.keyword() == "antonym"

    def resolve_members(self):
        """
        Purpose:
            Erase redundant information
            Parse and set information to attributes that are frequently accessed
        """
        self.defblock = self.find_defblock()
        self.main_sentence = self.find_main_sentence()
        self.symbol = self.find_symbol()
        self.anchor = self.find_anchor()

    def resolve_relations(self, link2element):
        self.change_links_in_defblock(link2element)

    def collect_relations(self, elements):
        pass

    def change_links_in_defblock(self, link2element):
        if self.defblock is None:
            return
        for a in self.defblock.xpath(".//a[@href]"):
            href = a.attrib.get('href')
            if href in link2element:
                element = link2element[href]
                a.attrib['data-link'] = element.data_link()
            else:
                a.attrib['data-href'] = href
            a.tag = 'span'
            del a.attrib['href']

    def adjust(self):
        # shrink nodes: class = 'txt'
        txt_nodes = self.defblock.xpath(".//*[@class='txt']")
        for node in txt_nodes:
            parent = node.getparent()
            child = node.getchildren()[0]
            node.remove(child)
            parent.replace(node, child)

    def data_link(self):
        return self.content.filename() + "#" + self.html_id()

    def html_id(self):
        return 'ELM' + str(self.id)

    def write(self, fp, i):
        fp.write(f'''
            <div class='card mml-element mt-2'  id='{self.html_id()}'>
                <div class='card-header'>
                    <h3>{str(i)}. {self.element_link_html(self)} [{self.source_link_html(self)}]</h3>
                </div>
                <div class='card-body'>
        
        ''')
        self.write_source_code(fp)
        self.write_relations(fp)
        fp.write('''
                </div>
            </div>
        ''')

    @staticmethod
    def source_link_html(e):
        href = e.filename + ".html"
        if e.anchor is not None:
            href += "#" + e.anchor
        return "<span data-href='" + href + "'>" + e.filename + "</span>"

    @staticmethod
    def element_link_html(element):
        return ("<span data-link='" + element.data_link() + "'>" +
                Element.escape_html_characters(element.symbol) + "</span>")

    def write_source_code(self, fp):
        # Markup main sentences
        self.add_to_attr(self.main_sentence, 'class', 'main-sentence')
        try:
            source_code = html.tostring(self.defblock, pretty_print=True, encoding='utf-8').decode('utf-8')
            fp.write(f'''
                <div class='source'>
                    <h4>Source <span class='defined-in'> [{self.source_link_html(self)}]</span></h4>
                    <div class='source-box bg-light p-3'>
                        {source_code}
                    </div>
                </div>
            ''')
        finally:
            self.remove_from_attr(self.main_sentence, 'class', 'main-sentence')

    def write_relations(self, fp):
        if len(self.relations) > 0:
            fp.write('''
                <div class='reference'>
                    <h4>Referenced In</h4>
            ''')
            for t in ['struct', 'mode', 'pred', 'attr', 'func', 'cluster', 'reduce']:
                self.write_relations_per_type(fp, t)
            fp.write('</div>')

    def write_relations_per_type(self, fp, type):
        elements = [e for e in self.relations if e.type() == type]
        elements = humansorted(elements, key=lambda e: (e.symbol, e.filename))
        if len(elements) > 0:
            fp.write(f'''
                <div class="related-{type}">
                     <table class="table table-sm table-hover table-borderd table-responsive">
                     <thead><tr><th colspan="2">{type}</th></tr></thead>
                     <tbody>
            ''')
            if type in ["cluster", "reduce"]:
                for e in elements:
                    fp.write("<tr><td>" + e.main_sentence.text_content() + "</td>")
                    fp.write("<td>" + self.source_link_html(e) + "</td></tr>\n")
            else:
                for e in elements:
                    fp.write("<tr><td>" + self.element_link_html(e) + "</td>")
                    fp.write("<td>" + self.source_link_html(e) + "</td></tr>\n")
            fp.write("</tbody>\n"
                     "</table>\n"
                     "</div>\n")

    @staticmethod
    def add_to_attr(node, attr, value):
        if node is None:
            return
        values = node.attrib.get(attr)
        if values is None:
            values = value
        else:
            values += ' ' + value
        node.attrib[attr] = values

    @staticmethod
    def remove_from_attr(node, attr, value):
        if node is None:
            return
        values = node.attrib.get(attr)
        if value in values:
            values = values.replace(value, '').replace('  ', ' ')
        node.attrib[attr] = values

    def substitute_redundant_definitions(self):
        substitution = {}
        definitions = self.defblock.xpath(".//div[@typeof='oo:Definition']")
        definitions += self.defblock.xpath(".//div[@typeof='oo:Theorem']")
        for node in definitions:
            if node != self.main_sentence:
                sub = html.fromstring("<div></div>")
                node.getparent().replace(node, sub)
                substitution[node] = sub
        return substitution

    @staticmethod
    def restore_nodes(substitution):
        for node, sub in substitution.items():
            sub.getparent().replace(sub, node)

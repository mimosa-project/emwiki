#!/usr/bin/env python
# encoding: utf-8
__author__ = 'nakasho'


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
        fp.write('<v-col cols="9" id="content" class="pl-6">')
        self.write_summary(fp)
        for i, e in enumerate(self.elements):
            e.write(fp, i + 1)
        fp.write('</v-col>')

        fp.write('<v-col cols="3" id="scrollspy">')
        self.write_scrollspy(fp)
        fp.write('</v-col>')

    def write_summary(self, fp):
        rep = self.elements[0]
        fp.write(f'''
            <div class="mml-summary">
                <p class="text-h2">{self.escape_html_characters(rep.symbol)}</p>
                <v-divider></v-divider>
                <p class="text-h4 mb-5">{rep.type()}</p>
        ''')

        fp.write(f'''
                <v-card outlined class="px-5 py-3">
                    <div>
                        <p class='text-h5'>List of Definitions ({str(len(self.elements))})</p>
                        <ol class='section-nav'>
        ''')
        for i, e in enumerate(self.elements):
            fp.write(f'''
                            <li class="toc-entry toc-h2">
                                {e.element_link_html(e)}[{e.source_link_html(e)}]
                            </li>
            ''')
        fp.write('''
                        </ol>
                    </div>
                </v-card>
            </div>
        ''')

    def write_scrollspy(self, fp):
        fp.write(f'''
            <nav id="list-of-definitions" class="d-none d-lg-block" style="position: sticky;" aria-label="Secondary navigation">
                <v-card outlined>
                    <v-card-title>{str(len(self.elements))} Definitions</v-card-title>
                    <v-card-text class="body-1">
                        <ol class="section-nav">
        ''')

        for i, e in enumerate(self.elements):
            fp.write(f'''
                <li class="toc-entry toc-h2">
                    {e.element_link_html(e)}[{e.source_link_html(e)}]
                </li>
            ''')

        fp.write('''
                        </ol>
                    </v-card-text">
                </v-card>
            </nav>
        ''')

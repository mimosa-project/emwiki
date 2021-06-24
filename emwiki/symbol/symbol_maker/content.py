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
        fp.write('<div id="content" class="col-9 pl-3">')
        self.write_summary(fp)
        for i, e in enumerate(self.elements):
            e.write(fp, i + 1)
        fp.write('</div>')

        fp.write('<div id="scrollspy" class="col-3" >')
        self.write_scrollspy(fp)
        fp.write('</div>')

    def write_summary(self, fp):
        rep = self.elements[0]
        fp.write(f'''
            <div class="mml-summary">
                <h1 class="d-inline">{self.escape_html_characters(rep.symbol)}</h1>
                <hr class="mb-0">
                <h4 class="mb-5">{rep.type()}</h4>
        ''')

        fp.write(f'''
                <div class='card mb-5'>
                    <div class='card-body'>
                        <h5 class='card-title'>List of Definitions ({str(len(self.elements))})</h5>
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
                </div>
            </div>
        ''')

    def write_scrollspy(self, fp):
        fp.write(f'''
            <nav id="list-of-definitions" class="d-none d-xl-block bd-toc sticky-top" aria-label="Secondary navigation">
                <h4>{str(len(self.elements))} Definitions</h4>
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
            </nav>
        ''')

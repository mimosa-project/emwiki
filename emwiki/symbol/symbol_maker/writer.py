#!/usr/bin/env python
# encoding: utf-8
__author__ = 'nakasho'

import codecs


class Writer:
    def __init__(self):
        self.content = None

    def write(self, path):
        with codecs.open(path, 'w', 'utf-8-sig') as fp:
            fp.write("<!DOCTYPE html>\n"
                     "<html lang='en'>\n")
            self.write_header(fp)
            self.write_body(fp)
            fp.write("</html>\n")

    def write_header(self, fp):
        fp.write(f'''
                <head>
                    <meta charset='UTF-8'>
                    <title>{self.content.symbol}</title>
                </head>
                ''')

    def write_body(self, fp):
        fp.write('''
            <body data-spy="scroll" data-target="#list-of-definitions">
            <main class="container-fluid">
            <div class="row">
        ''')
        self.content.write(fp)
        fp.write('''
            </div>
            </main>
            </body>
        ''')


if __name__ == '__main__':
    pass

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
                    <link rel='stylesheet' href='/static/symbol/CSS/iframe.css' type='text/css' />

                    <!-- Bootstrap -->
                    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
                    <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.4.1/jquery.min.js"></script>
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
            <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.7/umd/popper.min.js" integrity="sha384-UO2eT0CpHqdSJQ6hJty5KVphtPhzWj9WO1clHTMGa3JDZwrnQq4sF86dIHNDz0W1" crossorigin="anonymous"></script>
            <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/js/bootstrap.min.js" integrity="sha384-JjSmVgyd0p3pXB1rRibZUAYoIIy6OrQ6VrjIEaFf/nJGzIxFDsf4x0xIM+B07jRM" crossorigin="anonymous"></script>
            </body>
        ''')

if __name__ == '__main__':
    pass

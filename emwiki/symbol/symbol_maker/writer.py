#!/usr/bin/env python
# encoding: utf-8
__author__ = 'nakasho'

import codecs


class Writer:
    def __init__(self):
        self.content = None

    def write(self, path):
        with codecs.open(path, 'w', 'utf-8-sig') as fp:
            fp.write('''
                <div data-spy="scroll" data-target="#list-of-definitions">
                <div class="container-fluid">
                <div class="row">
            ''')
            self.content.write(fp)
            fp.write('''
                </div>
                </div>
                </div>
            ''')


if __name__ == '__main__':
    pass

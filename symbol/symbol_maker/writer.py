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
                <v-container fluid>
                <v-row>
            ''')
            self.content.write(fp)
            fp.write('''
                </v-row>
                </v-container>
            ''')


if __name__ == '__main__':
    pass

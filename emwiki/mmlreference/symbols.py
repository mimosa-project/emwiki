import json


class SymbolContent():

    def __init__(self):
        self.filename = ''
        self.symbol = ''
        self.type = ''

    def set(self, filename, symbol, type):
        self.filename = filename
        self.symbol = symbol
        self.type = type


class SymbolIndex():

    def __init__(self):
        self.symbolcontents = []

    def read(self, path):
        with open(path, 'r') as f:
            index_dict = json.load(f)
        for key, value in index_dict.items():
            symbolcontent = SymbolContent()
            symbolcontent.set(key, value['symbol'], value['type'])
            self.symbolcontents.append(symbolcontent)

    def find_symbolcontent_from_filename(self, filename):
        for symbolcontent in self.symbolcontents:
            if filename == symbolcontent.filename:
                return symbolcontent
        return

    def find_symbolcontent_from_symbol(self, symbol):
        for symbolcontent in self.symbolcontents:
            if symbol == symbolcontent.symbol:
                return symbolcontent
        return

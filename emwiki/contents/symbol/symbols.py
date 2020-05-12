import json
from contents.symbol.models import Symbol


class SymbolIndex():

    def __init__(self):
        self.symbols = []

    def read(self, index_path):
        with open(index_path, 'r') as f:
            index_dict = json.load(f)
        for key, value in index_dict.items():
            symbol = Symbol(
                symbol=value['symbol'],
                type=value['type'],
                filename=key
            )
            self.symbols.append(symbol)

    def save(self):
        for symbol in self.symbols:
            symbol.save()

import json
from natsort import humansorted

from symbol.models import Symbol


class SymbolJavascriptBuilder:
    # Symbolアプリケーションで使用するJavascritを生成する
    # var index_data ={
    #     "symbols": ["!", "!=", "\"",...],
    #     "types": ["func", "pred", "func",..],
    #     "filenames": ["2069.html", "3499.html", "43.html",...]
    # }
    def create_files(self, path):
        symbols = list(Symbol.objects.all())
        symbols = humansorted(symbols, key=lambda a: a.name)
        name_list = []
        type_list = []
        filename_list = []
        for symbol in symbols:
            name_list.append(symbol.name)
            type_list.append(symbol.type)
            filename_list.append(symbol.filename)
        dict = {}
        dict["symbols"] = name_list
        dict["types"] = type_list
        dict["filenames"] = filename_list
        with open(path, mode='w', encoding='utf-8') as f:
            f.write("var index_data = ")
            json.dump(dict, f)

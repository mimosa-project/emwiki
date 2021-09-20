import json
import os
from symbol.models import Symbol

from django.conf import settings


class SymbolJavascriptBuilder:
    path = os.path.join(
        settings.BASE_DIR, 'symbol', 'static', 'symbol', 'JavaScript', 'mml-index.js'
    )

    # Symbolアプリケーションで使用するJavascritを生成する
    # var index_data ={
    #     "symbols": ["!", "!=", "\"",...],
    #     "types": ["func", "pred", "func",..],
    #     "filenames": ["2069.html", "3499.html", "43.html",...]
    # }
    def create_files(self):
        print('Building javascript for symbol')
        symbols = list(Symbol.objects.all())
        symbols.sort(key=lambda a: a.name.lower())
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
        with open(self.path, mode='w', encoding='utf-8') as f:
            f.write("var index_data = ")
            json.dump(dict, f)

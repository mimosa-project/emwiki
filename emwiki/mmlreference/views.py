from django.shortcuts import render
from emwiki.settings import SYMBOL_INDEX_PATH
import json
from django.http.response import JsonResponse, HttpResponseNotFound
import os
import urllib
from .symbols import SymbolIndex

# Create your views here.


def index(request, symbol):
    context = {}
    return render(request, f'mmlreference/index.html', context)


def index_json(request):
    symbol_encoded = request.GET.get('symbol', None)
    filename = request.GET.get('filename', None)
    if filename or symbol_encoded:
        symbolindex = SymbolIndex()
        symbolindex.read(SYMBOL_INDEX_PATH)
    if filename:
        symbolcontent = symbolindex.find_symbolcontent_from_filename(filename)
    elif symbol_encoded:
        symbol = urllib.parse.unquote(symbol_encoded)
        symbolcontent = symbolindex.find_symbolcontent_from_symbol(symbol)
    else:
        return
    if not symbolcontent:
        return
    response_dict = {
        'url_subdirectory': 'mmlreference',
        'static_subdirectory': os.path.join('static', 'mml-contents'),
        'filename': symbolcontent.filename,
        'symbol': symbolcontent.symbol,
        'type': symbolcontent.type
    }
    return JsonResponse(response_dict)

from django.shortcuts import render
from django.http.response import JsonResponse
import os
import urllib
from contents.symbol.models import Symbol
from emwiki.settings import STATIC_SYMBOLS_URL

# Create your views here.


def index(request, symbol):
    context = {}
    return render(request, f'symbol/index.html', context)


def index_json(request):
    symbol_encoded = request.GET.get('symbol', None)
    filename = request.GET.get('filename', None)
    if filename:
        symbol = Symbol.objects.get(filename=filename)
    elif symbol_encoded:
        symbol_decoded = urllib.parse.unquote(symbol_encoded)
        symbol = Symbol.objects.get(symbol=symbol_decoded)
    else:
        return
    if not symbol:
        return
    response_dict = {
        'url_subdirectory': 'symbol',
        'static_subdirectory': STATIC_SYMBOLS_URL,
        'filename': symbol.filename,
        'symbol': symbol.symbol,
        'type': symbol.type
    }
    return JsonResponse(response_dict)

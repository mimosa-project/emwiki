from django.shortcuts import render
from emwiki.settings import MML_REFERENCE_INDEX_PATH
import json
from django.http.response import JsonResponse, HttpResponseNotFound
import os
import urllib

# Create your views here.


def index(request, symbol):
    context = {}
    return render(request, f'mmlreference/index.html', context)


def index_json(request):
    symbol_encoded = request.GET.get('symbol', None)
    filename = request.GET.get('filename', None)
    if filename or symbol_encoded:
        with open(MML_REFERENCE_INDEX_PATH, 'r') as f:
            index_dict = json.load(f)
    if filename:
        pass
    elif symbol_encoded:
        symbol = urllib.parse.unquote(symbol_encoded)
        filename_candidates = \
            [key for key, item in index_dict.items() if item['symbol'] == symbol]
        if filename_candidates:
            filename = filename_candidates[0]
        else:
            return
    else:
        return
    response_dict = {
        'url_subdirectory': 'mmlreference',
        'static_subdirectory': os.path.join('static', 'mml-contents'),
        'filename': filename,
        'symbol': index_dict[filename]['symbol'],
        'type': index_dict[filename]['type']
    }
    return JsonResponse(response_dict)

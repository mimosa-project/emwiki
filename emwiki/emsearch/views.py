from django.shortcuts import render
from django.http import JsonResponse
from emsearch.searcher import Searcher
import json
import os
from emwiki.settings import BASE_DIR
# Create your views here.


def index(request):
    search_query = request.GET.get('search_query', default='')
    categorys_json_path = os.path.join(BASE_DIR, 'emsearch','search_settings', "categorys.json")
    with open(categorys_json_path, 'r', encoding="utf-8") as f:
        categorys = json.load(f)
    context = {
        'search_query': search_query,
        'categorys': categorys
    }
    return render(request, 'emsearch/index.html', context)


def search(request):
    query = request.GET.get('search_query', default='')
    searcher = Searcher()
    searcher.search_all(query)
    context = {
        'search_results': [result.get_as_dict() for result in searcher.results],
        'search_query': query,
    }
    return JsonResponse(context)


def get_keywords(request):
    keywords_json_path = os.path.join(BASE_DIR, 'emsearch','search_settings', "keywords.json")
    with open(keywords_json_path, 'r', encoding="utf-8") as f:
        keywords = json.load(f)
    return JsonResponse(keywords)

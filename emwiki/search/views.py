from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from search.searcher import Searcher
import json
import os
from emwiki.settings import BASE_DIR
# Create your views here.


def index(request):
    search_query = request.GET.get('search_query', default='')
    categorys_json_path = os.path.join(BASE_DIR, 'search', 'search_settings', "categorys.json")
    with open(categorys_json_path, 'r', encoding="utf-8") as f:
        categorys = json.load(f)
    context = {
        'search_query': search_query,
        'categorys': categorys
    }
    return render(request, 'search/index.html', context)


@require_http_methods(["GET", ])
def search(request):
    query = request.GET.get('search_query', default='')
    searcher = Searcher()
    searcher.search_all(query)
    context = {
        'search_results': [result.get_as_dict() for result in searcher.results],
        'search_query': query,
    }
    return JsonResponse(context)


@require_http_methods(["GET", ])
def get_keywords(request):
    keywords_json_path = os.path.join(BASE_DIR, 'search', 'search_settings', "keywords.json")
    with open(keywords_json_path, 'r', encoding="utf-8") as f:
        keywords = json.load(f)
    return JsonResponse(keywords)

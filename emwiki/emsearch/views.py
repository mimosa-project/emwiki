from django.shortcuts import render
from django.http import JsonResponse
from .seacher import search
import json
import os
from emwiki.settings import BASE_DIR
# Create your views here.


def index(request):
    search_query = request.GET.get('search_query')
    search_results = search(search_query)
    return render(request, 'emsearch/index.html', context={'search_results': search_results, 'search_query': search_query})


def get_keywords(request):
    keywords_json_path = os.path.join(BASE_DIR, 'emsearch','search_settings', "keywords.json")
    with open(keywords_json_path, 'r', encoding="utf-8") as f:
        keywords = json.load(f)
    return JsonResponse(keywords)

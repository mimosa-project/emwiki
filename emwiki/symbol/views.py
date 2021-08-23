from django.conf import settings
from django.core import serializers
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.decorators.cache import cache_page

from .models import Symbol

class SymbolIndexView(View):
    def get(self, request):
        context = dict()
        # you can use these variables in index.js
        context["context_for_js"] = {
            'adjust_name_url': reverse('symbol:adjust_name'),
            # nameの空文字指定ができないため，'content-name'で仮作成し，削除している
            'article_base_uri': reverse(
                'article:index',
                kwargs=dict(filename='content-name')
            ).replace('content-name', ''),
            'symbol_base_uri': reverse('symbol:index')
        }
        return render(request, 'symbol/index.html', context)

class SymbolView(View):
    def get(self, request, filename):
        path = "symbol/symbol_html/" + filename
        return render(request, path)

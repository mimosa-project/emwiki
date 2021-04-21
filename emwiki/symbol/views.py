import os

from django.core import serializers
from django.shortcuts import redirect, get_object_or_404, render
from django.http import HttpResponse
from django.urls import reverse
from django.views import View
from django.views.decorators.cache import cache_page

from .models import Symbol


class SymbolView(View):
    def get(self, request, name):
        try:
            symbol = Symbol.objects.get(name=str(name).replace('.html', ''))
        except Symbol.DoesNotExist:
            symbol = get_object_or_404(Symbol, filename=name)
            return redirect(symbol)
        context = dict()
        # you can use these variables in index.html
        context["symbol"] = symbol
        # you can use these variables in index.js
        context["context_for_js"] = {
            'names_url': reverse('symbol:names'),
            # nameの空文字指定ができないため，'content-name'で仮作成し，削除している
            'article_base_uri': reverse(
                'article:index',
                kwargs=dict(filename='content-name')
            ).replace('content-name', ''),
        }
        return render(request, 'symbol/index.html', context)


@cache_page(60*60*24*365)
def get_names(request):
    return HttpResponse(
            serializers.serialize(
                'json', Symbol.objects.order_by("name").all()
            ),
            content_type='application/json'
        )

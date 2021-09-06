from django.conf import settings
from django.core import serializers
from django.http import HttpResponse, HttpResponseNotFound
from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.views.decorators.cache import cache_page

from .models import Symbol


class SymbolView(View):
    def get(self, request, name):
        symbol = Symbol.objects.get(name=str(name).replace('.html', ''))
        context = dict()
        # you can use these variables in index.html
        context["symbol"] = symbol
        # you can use these variables in index.js
        context["context_for_js"] = {
            'names_url': reverse('symbol:names') + f"?MIZAR_VERSION={settings.MIZAR_VERSION}",
            'adjust_name_url': reverse('symbol:adjust_name'),
            # nameの空文字指定ができないため，'content-name'で仮作成し，削除している
            'article_base_uri': reverse(
                'article:index',
                kwargs=dict(filename='content-name')
            ).replace('content-name', ''),
        }
        return render(request, 'symbol/index.html', context)


def adjust_name(request):
    requested_name = request.GET.get("name")
    if Symbol.objects.filter(filename=requested_name).exists():
        return HttpResponse(Symbol.objects.get(filename=requested_name).name)
    elif Symbol.objects.filter(name=requested_name).exists():
        return HttpResponse(requested_name)
    else:
        return HttpResponseNotFound


@cache_page(60 * 60 * 24)
def get_names(request):
    symbols = list(Symbol.objects.all())
    symbols.sort(key=lambda a: a.name.lower())
    return HttpResponse(
        serializers.serialize(
            'json', symbols
        ),
        content_type='application/json'
    )

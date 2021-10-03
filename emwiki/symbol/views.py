import os
import re

from django.shortcuts import render
from django.urls import reverse
from django.views import View
from django.http import Http404

from .models import Symbol


class SymbolIndexView(View):
    def get(self, request):
        context = dict()
        # you can use these variables in index.js
        context["context_for_js"] = {
            'article_base_uri': reverse('article:index'),
            'symbol_base_uri': reverse('symbol:index')
        }
        return render(request, 'symbol/index.html', context)


class SymbolView(View):
    def get(self, request, filename):
        # 「数字 + .html」(例：2096.html)以外でのリクエストでは404を返す
        if(re.match("[0-9]+.html", filename)):
            path = os.path.join(Symbol.get_htmlfile_dir(), filename)
            if os.path.exists(path):
                return render(request, path)
            else:
                raise Http404("Symbol html does not exist")
        else:
            raise Http404("Symbol html does not exist")

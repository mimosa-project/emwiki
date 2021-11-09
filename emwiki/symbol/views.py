from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, Http404
from django.urls import reverse
from django.views import View

from .models import Symbol


class SymbolView(View):
    def get(self, request, name):
        context = dict()
        # you can use these variables in index.js
        context["context_for_js"] = {
            'symbol_html_uri': reverse('symbol:htmls'),
            'names_uri': reverse('symbol:names')
        }
        context['article_base_uri'] = reverse('article:index', kwargs=dict(name_or_filename="temp")).replace('temp', '')
        return render(request, 'symbol/index.html', context)


class SymbolIndexView(View):
    def get(self, request):
        return JsonResponse({'index': [
            dict(name=symbol.name) for symbol in Symbol.objects.all()
        ]})


class SymbolHtmlView(View):
    def get(self, request):
        if 'symbol_name' in request.GET:
            symbol = get_object_or_404(Symbol, name=request.GET.get("symbol_name"))
            return render(request, symbol.template_path)
        else:
            raise Http404()

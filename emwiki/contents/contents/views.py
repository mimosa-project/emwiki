from django.shortcuts import render
from django.http import JsonResponse
import urllib
from contents.symbol.models import Symbol
from contents.article.models import Article
import os
from django.urls import reverse
from django.views.generic import TemplateView


class ContentView(TemplateView):
    template_name = 'contents/index.html'

    def get_context_data(self, **kwargs):
        kwargs['name'] = os.path.splitext(kwargs['name'])[0]
        context = super().get_context_data(**kwargs)
        context["js_url"] = kwargs['category'].lower() + '/JavaScript/index.js'
        context["context_for_js"] = {
            'category': kwargs['category'],
            'name': kwargs['name'],
            'submit_comment_url': reverse('article:submit_comment'),
            'order_comments_url': reverse('article:order_comments')
        }
        return context


def normalize_content_url(request):
    category = request.GET.get('category', None)
    name_encoded = request.GET.get('name', None)
    filename = request.GET.get('filename', None)
    name = urllib.parse.unquote(name_encoded)
    if category == 'Article':
        content = Article.objects.get(name=name)
    elif category == 'Symbol':
        if filename:
            content = Symbol.objects.get(filename=filename)
        else:
            content = Symbol.objects.get(name=name)
    index = {
        'category': category,
        'name': content.name,
        'url': content.get_absolute_url(),
        'iframe_url': content.get_static_url()
    }
    return JsonResponse(index)

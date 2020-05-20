from django.shortcuts import render
from django.http import JsonResponse
import urllib
from contents.symbol.models import Symbol
from contents.article.models import Article
import os
from django.urls import reverse


def index(request, category, name):
    name = os.path.splitext(name)[0]
    context = {
        'category': category,
        'name': name,
        'js_url': category + '/JavaScript/index.js',
        'context_js': {
            'category': category,
            'name': name,
            'submit_comment_url': reverse('article:submit_comment'),
            'order_comments_url': reverse('article:order_comments')
        }
    }
    return render(request, f'contents/index.html', context)


def index_json(request):
    category = request.GET.get('category', None)
    name_encoded = request.GET.get('name', None)
    filename = request.GET.get('filename', None)
    name = urllib.parse.unquote(name_encoded)
    if category == 'article':
        content = Article.objects.get(name=name)
    elif category == 'symbol':
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

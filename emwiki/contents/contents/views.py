from django.shortcuts import render
from django.http import JsonResponse
import urllib
from .models import Symbol, Article
import os


def index(request, type, name):
    name = os.path.splitext(name)[0]
    context = {
        'type': type,
        'name': name,
        'js_url': type + '/JavaScript/index.js',
        'context_js': {
            'type': type,
            'name': name
        }
    }
    return render(request, f'contents/index.html', context)


def index_json(request):
    type = request.GET.get('type', None)
    name_encoded = request.GET.get('name', None)
    name = urllib.parse.unquote(name_encoded)
    print('type:', type)
    print('name:', name)

    if type == 'article':
        content = Article.objects.get(name=name)
    elif type == 'symbol':
        content = Symbol.objects.get(name=name)
    else:
        return
    index = {
        'type': type,
        'name': content.name,
        'url': content.get_absolute_url(),
        'iframe_url': content.get_static_url()
    }
    return JsonResponse(index)
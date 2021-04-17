from functools import reduce
from operator import and_, or_
import os
import urllib

from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.generic import TemplateView

from article.models import Article
from symbol.models import Symbol


class ContentView(TemplateView):
    template_name = 'contents/index.html'

    def get_context_data(self, **kwargs):
        kwargs['name'] = os.path.splitext(kwargs['name'])[0]
        context = super().get_context_data(**kwargs)
        context["context_for_js"] = {
            'category': kwargs['category'].title(),
            'name': kwargs['name'],
            'contents_normalize_content_url': reverse('contents:normalize_content_url'),
            # nameの空文字指定ができないため，'content-name'で仮作成し，削除している
            'contents_base_uri': reverse(
                'contents:index',
                kwargs=dict(category=kwargs['category'].title(), name='content-name')
            ).replace('content-name', ''),
            'article_base_uri': reverse(
                'contents:index',
                kwargs=dict(category='Article', name='content-name')
            ).replace('content-name', ''),
            'submit_comment_url': reverse('article:submit_comment'),
            'order_comments_url': reverse('article:order_comments'),
            'order_names_uri': reverse(f"{kwargs['category'].lower()}:order_names")
        }
        if context['category'].title() == 'Article':
            context['bib_path'] = f'article/fmbibs/{context["name"]}.bib'
        context["js_url"] = kwargs['category'].lower() + '/JavaScript/index.js'
        return context


def normalize_content_url(request):
    category = request.GET.get('category', None)
    name_encoded = request.GET.get('name', None)
    filename = request.GET.get('filename', None)
    name = urllib.parse.unquote(name_encoded)
    content = None
    if category == 'Article':
        content = Article.get_model(name=name, filename=filename)
    elif category == 'Symbol':
        content = Symbol.get_model(name=name, filename=filename)
    index = {
        'category': category,
        'name': content.name,
        'url': content.get_absolute_url(),
        'iframe_url': content.get_static_url()
    }
    return JsonResponse(index)

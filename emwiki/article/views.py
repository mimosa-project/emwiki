import json
import os

from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse, HttpResponseForbidden
from django.http.response import JsonResponse
from django.utils.decorators import method_decorator
from django.urls import reverse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views import View
from django.views.generic import TemplateView

from .models import Article, Comment
from emwiki.settings import RAW_HTMLIZEDMML_DIR


class ArticleView(TemplateView):
    template_name = "article/index.html"

    def get_context_data(self, **kwargs):
        article = Article.objects.get(name=kwargs["name"])
        kwargs['name'] = os.path.splitext(kwargs['name'])[0]
        context = super().get_context_data(**kwargs)
        context['name'] = article.name
        context['template_path'] = f"article/htmlized_mml/{kwargs['name']}.html"
        context['bib_path'] = f'article/fmbibs/{context["name"]}.bib'
        context["context_for_js"] = {
            'comments': list(Comment.objects.filter(article=article).values()),
            'comment_url': reverse('article:comment'),
        }
        return context


class ProofView(View):
    def get(self, request, article_name, proof_name):
        return HttpResponse(
            open(os.path.join(RAW_HTMLIZEDMML_DIR, 'proofs', article_name, proof_name)).read(),
            content_type='application/xml'
        )


class CommentView(View):

    def get(self, request):
        json_str = request.body.decode("utf-8")
        params = json.loads(json_str)['params']
        query = Comment.objects
        if params.exists('article_name'):
            query = query.filter(
                article=Article.object.get(name=params["article_name"])
            )
        if params.exists('block'):
            query = query.filter(
                block=params['block']
            )
        if params.exists('block_order'):
            query = query.filter(
                block_order=querys["block_order"]
            )
        return HttpResponse(
            serializers.serialize('json', query.all(), content_type='application/json')
        )

    @method_decorator(login_required)
    def post(self, request):
        article_name = request.POST.get('article_name', None)
        block = request.POST.get('block', None)
        block_order = request.POST.get("block_order", None)
        text = request.POST.get('comment', None)
        article = Article.objects.get(name=article_name)
        if Comment.objects.filter(article=article, block=block, block_order=block_order).exists():
            comment = Comment.objects.get(article=article, block=block, block_order=block_order)
        else:
            comment = Comment(article=article, block=block, block_order=block_order, text='')
        comment.text = text
        comment.save()
        article.save_db2mizfile()
        article.commit_mizfile(request.user.username)
        return HttpResponse(status=201)

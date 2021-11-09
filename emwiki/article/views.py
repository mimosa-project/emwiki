import os

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.http import HttpResponse, JsonResponse, Http404
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from .models import Article, Comment


class ArticleView(View):
    def get(self, request, name_or_filename):
        context = dict()
        context["context_for_js"] = {
            'article_base_uri': reverse('article:htmls'),
            'comments_uri': reverse('article:comments'),
            'bibs_uri': reverse('article:bibs'),
            'names_uri': reverse('article:names'),
            'is_authenticated': self.request.user.is_authenticated,
        }
        return render(request, "article/index.html", context)


class ArticleIndexView(View):
    def get(self, request):
        return JsonResponse({'index': [
            dict(name=article.name) for article in Article.objects.all()
        ]})


class ArticleHtmlView(View):
    def get(self, request, *args, **kwargs):
        if 'article_name' in request.GET:
            article = get_object_or_404(Article, name=request.GET.get('article_name'))
            return render(request, article.template_url)
        else:
            raise Http404()


class BibView(View):
    def get(self, request):
        if 'article_name' in request.GET:
            article_name = request.GET.get("article_name")
            bib_file_path = os.path.join(settings.MML_FMBIBS_DIR, f'{article_name}.bib')
            if os.path.exists(bib_file_path):
                with open(bib_file_path, "r") as f:
                    bib_text = f.read()
            else:
                bib_text = f"{bib_file_path} not found"
            return JsonResponse({"bib_text": bib_text})


class ProofView(View):
    def get(self, request, article_name, proof_name):
        return HttpResponse(
            open(os.path.join(settings.MML_HTML_DIR, 'proofs',
                 article_name, proof_name)).read(),
            content_type='application/xml'
        )


class RefView(View):
    def get(self, request, article_name, ref_name):
        return HttpResponse(
            open(os.path.join(settings.MML_HTML_DIR,
                 'refs', article_name, ref_name)).read(),
            content_type='application/xml'
        )


class CommentView(View):

    def get(self, request, *args, **kwargs):
        query = Comment.objects
        if 'article_name' in request.GET:
            query = query.filter(
                article=Article.objects.get(
                    name=request.GET.get("article_name"))
            )
        if 'block' in request.GET:
            query = query.filter(
                block=request.GET.get('block')
            )
        if 'block_order' in request.GET:
            query = query.filter(
                block_order=int(request.GET.get("block_order"))
            )
        return HttpResponse(
            serializers.serialize('json', query.all()), content_type='application/json'
        )

    @method_decorator(login_required)
    def post(self, request):
        article_name = request.POST.get('article_name', None)
        block = request.POST.get('block', None)
        block_order = request.POST.get("block_order", None)
        text = request.POST.get('comment', None)
        article = Article.objects.get(name=article_name)
        if Comment.objects.filter(article=article, block=block, block_order=block_order).exists():
            comment = Comment.objects.get(
                article=article, block=block, block_order=block_order)
        else:
            comment = Comment(article=article, block=block,
                              block_order=block_order, text='')
        comment.text = text
        comment.save()
        article.save_db2mizfile()
        article.commit_mizfile(request.user.username)
        return HttpResponse(status=201)

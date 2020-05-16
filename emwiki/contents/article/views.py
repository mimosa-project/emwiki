from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
import os
from emwiki.settings import STATIC_ARTICLES_URL
from .models import Article, Comment
from .classes import MizFile
import json


@ensure_csrf_cookie
def submit_comment(request):
    article_name = request.POST.get('article_name', None)
    block = request.POST.get('block', None)
    block_order = request.POST.get("block_order", None)
    text = request.POST.get('comment', None)
    article = Article.objects.get(name=article_name)
    comment = Comment(article, block, block_order, text)
    comment.save()
    mizfile = MizFile()
    mizfile.read(article.get_mml_path())
    mizfile.embed_comment(article.comment_set.all())
    mizfile.write(article.get_commented_path())
    return HttpResponse()


def order_comments(request):
    comments = []
    json_str = request.body.decode("utf-8")
    querys = json.loads(json_str)['querys']
    for query in querys:
        article_name = query['article_name']
        block = query['block']
        block_order = query['block_order']
        article = Article.objects.get(name=article_name)
        if Comment.objects.filter(article=article, block=block, block_order=block_order).exists():
            comment = Comment.objects.get(article=article, block=block, block_order=block_order)
            comments.append({
                'aritcle_name': comment.article.name,
                'block': comment.block,
                'block_order': comment.block_order,
                'text': comment.text
            })
    return JsonResponse({'comments': comments})

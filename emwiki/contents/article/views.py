import json

import git
from django.http import HttpResponse, HttpResponseForbidden
from django.http.response import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie

from contents.article.miz_file import MizFile
from .models import Article, Comment
from emwiki.settings import LOCAL_COMMENT_REPOSITORY


@ensure_csrf_cookie
def submit_comment(request):
    if not request.user.is_authenticated:
        return HttpResponseForbidden('<h1>403 Forbidden</h1>', content_type='text/html')
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
    mizfile = MizFile(article.get_mizfile_path())
    mizfile.read()
    mizfile.extract(article)
    mizfile.embed(article.comment_set.all())
    mizfile.write()
    LOCAL_COMMENT_REPOSITORY.git.checkout('mml_commented_test')

    commit_message = f'Update {article.name}\n\nUsername: {request.user.username}'
    LOCAL_COMMENT_REPOSITORY.git.add(mizfile.path)
    LOCAL_COMMENT_REPOSITORY.index.commit(commit_message)
    origin = git.remote.Remote(repo=LOCAL_COMMENT_REPOSITORY, name='origin')
    origin.push('mml_commented_test')
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
        text = ''
        if Comment.objects.filter(article=article, block=block, block_order=block_order).exists():
            comment = Comment.objects.get(article=article, block=block, block_order=block_order)
            text = comment.text
        comments.append({
            'article_name': article_name,
            'block': block,
            'block_order': block_order,
            'text': text
        })
    return JsonResponse({'comments': comments})

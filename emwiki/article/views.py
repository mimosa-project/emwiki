from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from .classes import Article
from .classes import Comment


@ensure_csrf_cookie
def render_article(request):
    file_list = Article.all_names()
    file_path = 'optional/start.html'
    context = {'file_path': file_path, 'file_list': file_list}
    return render(request, 'article/article.html', context)


def recieve_comment(request):
    file_name = request.POST.get('id', None)
    block = request.POST.get('block', None)
    block_order = request.POST.get("block_order", None)
    comment = request.POST.get('comment', None)
    article_name = file_name
    Comment(article_name, block, block_order, comment).save()
    return HttpResponse()


def send_comment(request, article_name):
    """send comments using JSON

    Args:
        request: HttpRequestObject
        article_name: article_name ex."abcmiz_0.html"

    Returns:
        A JSON like this

        {'comments': {
            'theorem': {1: "comment_text", 2: "comment_text", 3...},
            'definition': {1: "comment_text", 2: "comment_text", 3...},
            ...
        }
    """
    return_json = {'comments': {block: {} for block in Article.TARGET_BLOCK}}
    for comment in Article(article_name).comments():
        return_json['comments'][comment.block][comment.order] = comment.text
    return JsonResponse(return_json)


def push_all_comment(request):
    print("push start")
    for article in Article.all():
        article.embed()
    print("push end")
    return HttpResponse()


def pull_all_comment(request):
    print("pull start")
    for article in Article.all():
        article.extract()
    print("pull end")
    return HttpResponse()

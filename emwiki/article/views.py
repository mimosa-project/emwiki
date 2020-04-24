from django.shortcuts import render
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from .classes import ArticleHandler


@ensure_csrf_cookie
def render_article(request):
    file_list = [article_handler.article_name for article_handler in ArticleHandler.bundle_create()]
    file_path = 'optional/start.html'
    context = {'file_path': file_path, 'file_list': file_list}
    return render(request, 'article/article.html', context)


def update_comment(request):
    file_name = request.POST.get('id', None)
    block = request.POST.get('block', None)
    block_order = request.POST.get("block_order", None)
    text = request.POST.get('comment', None)
    article_name = file_name
    article_handler = ArticleHandler(article_name)
    article_handler.store_comment(block, block_order, text)
    article_handler.embed_comment_to_mml()
    return HttpResponse()


def send_comment_to_template(request, article_name):
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
    article_handler = ArticleHandler(article_name)
    return_json = article_handler.get_comment_dict()
    return JsonResponse(return_json)


def make_all_commented_mml_file(request):
    for article_handler in ArticleHandler.bundle_create():
        article_handler.embed_comment_to_mml()
    return HttpResponse()

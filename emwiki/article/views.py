from django.shortcuts import render
import os
import glob
from emwiki.settings import BASE_DIR
from .comment import make_commentedmizar_file
from django.http import HttpResponse
from django.http.response import JsonResponse


def render_article(request):
    file_list = glob.glob(os.path.join(BASE_DIR, 'static/mizar_html/*.html'))
    file_list = [absolute_path.rsplit("/", 1)[1] for absolute_path in file_list]
    file_path = 'optional/start.html'
    context = {'file_path': file_path, 'file_list': file_list}
    return render(request, 'article/article.html', context)


def recieve_comment(request):
    file_name = request.POST.get('id', None)
    content = request.POST.get('content', None)
    content_number = request.POST.get("content_number", None)
    article_name = file_name
    comment_path = os.path.join(BASE_DIR, f'article/data/comment/{article_name}')
    if not os.path.exists(comment_path):
        os.mkdir(comment_path)
    with open(f'{comment_path}/{content}_{content_number}', "w") as f:
        f.write(request.POST.get("comment", None))
    return HttpResponse()


def send_comment(request, article_name):
    """send commentes using JSON

    Args:
        request: HttpRequestObject
        article_name: article_name ex."abcmiz_0.html"

    Returns:
        A JSON like this

        {'commentes': {
            'theorem': {1: "comment_text", 2: "comment_text", 3...},
            'definition': {1: "comment_text", 2: "comment_text", 3...},
            ...
        }
    """
    return_json = {
        'commentes': {},
    }
    commentes_path = os.path.join(BASE_DIR, f'article/data/comment/{article_name}/')
    commentes_path_list = glob.glob(commentes_path + '*')

    for comment_path in commentes_path_list:
        comment_name = comment_path.rsplit("/", 1)[1]
        content = comment_name.split("_")[0]
        content_number = comment_name.split("_")[1]
        return_json["commentes"][content] = {}
        with open(comment_path, "r") as f:
            return_json['commentes'][content][content_number] = f.read()
    return JsonResponse(return_json)


def apply_commentedmizar(request):
    file_list = glob.glob(os.path.join(BASE_DIR, 'static/mizar_html/*.html'))
    file_list = [absolute_path.rsplit("/", 1)[1] for absolute_path in file_list]
    file_list = [extention_name.rsplit(".", 1)[0] for extention_name in file_list]
    print("apply start")
    for article_name in file_list:
        make_commentedmizar_file(article_name)
    print("apply end")
    return HttpResponse()

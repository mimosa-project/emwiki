from django.shortcuts import render
import os
import glob
from emwiki.settings import BASE_DIR
from .sketch import make_sketchedmizar_file
from django.http import HttpResponse
from django.http.response import JsonResponse


def render_article(request):
    file_list = glob.glob(os.path.join(BASE_DIR, 'static/mizar_html/*.html'))
    file_list = [absolute_path.rsplit("/", 1)[1] for absolute_path in file_list]
    file_path = 'optional/start.html'
    context = {'file_path': file_path, 'file_list': file_list}
    return render(request, 'article/article.html', context)


def recieve_sketch(request):
    file_name = request.POST.get('id', None)
    content = request.POST.get('content', None)
    content_number = request.POST.get("content_number", None)
    article_name = file_name
    sketch_path = os.path.join(BASE_DIR, f'article/data/sketch/{article_name}')
    if not os.path.exists(sketch_path):
        os.mkdir(sketch_path)
    with open(f'{sketch_path}/{content}_{content_number}', "w") as f:
        f.write(request.POST.get("sketch", None))
    return HttpResponse()


def send_sketch(request, article_name):
    """send sketches using JSON

    Args:
        request: HttpRequestObject
        article_name: article_name ex."abcmiz_0.html"

    Returns:
        A JSON like this

        {'sketches': {
            'theorem': {1: "sketch_text", 2: "sketch_text", 3...},
            'definition': {1: "sketch_text", 2: "sketch_text", 3...},
            ...
        }
    """
    return_json = {
        'sketches': {},
    }
    sketches_path = os.path.join(BASE_DIR, f'article/data/sketch/{article_name}/')
    sketches_path_list = glob.glob(sketches_path + '*')

    for sketch_path in sketches_path_list:
        sketch_name = sketch_path.rsplit("/", 1)[1]
        content = sketch_name.split("_")[0]
        content_number = sketch_name.split("_")[1]
        return_json["sketches"][content] = {}
        with open(sketch_path, "r") as f:
            return_json['sketches'][content][content_number] = f.read()
    return JsonResponse(return_json)


def apply_sketchedmizar(request):
    file_list = glob.glob(os.path.join(BASE_DIR, 'static/mizar_html/*.html'))
    file_list = [absolute_path.rsplit("/", 1)[1] for absolute_path in file_list]
    file_list = [extention_name.rsplit(".", 1)[0] for extention_name in file_list]
    print("apply start")
    for article_name in file_list:
        make_sketchedmizar_file(article_name)
    print("apply end")
    return HttpResponse()

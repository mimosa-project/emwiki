from django.shortcuts import render
import os
import glob
from emwiki.settings import BASE_DIR
from django.http import HttpResponse, HttpResponseBadRequest
from django.urls import reverse
from django.http.response import JsonResponse
import json


def renderer(request):
    file_list = glob.glob(os.path.join(BASE_DIR, 'static/mizar_html/*.html'))
    file_list = [absolute_path.rsplit("/", 1)[1] for absolute_path in file_list]
    file_path = 'optional/start.html'
    context = {'file_path':file_path, 'file_list':file_list}
    return render(request, 'article/article.html', context)

def sketchReciever(request):
    file_name = request.POST.get('id',None)
    content = request.POST.get('content',None)
    content_name = request.POST.get("name",None)
    article_name = file_name.replace(".html", "")
    content_path = os.path.join(BASE_DIR, f'static/mizar_html/{content}/{article_name}/')
    sketch_path = os.path.join(BASE_DIR, f'article/data/mizar_sketch/{content}/{article_name}')
    contents_path_list = glob.glob(content_path+'*')
    contents_name_list = [absolute_path.rsplit("/", 1)[1] for absolute_path in contents_path_list]
    
    if content_name in contents_name_list:
        if not os.path.exists(sketch_path):
            os.mkdir(sketch_path)
        with open(sketch_path+"/"+content_name, "w") as f:
            f.write(request.POST.get("sketch",None))
        return HttpResponse()
    else:
        raise HttpResponseBadRequest

def dataSender(request, article_name):
    return_json = {
        'refs': {},
        'proofs': {},
    }
    refs_path = os.path.join(BASE_DIR, f'static/mizar_html/refs/{article_name}/')
    proofs_path = os.path.join(BASE_DIR, f'static/mizar_html/proofs/{article_name}/')
    refs_sketches_path = os.path.join(BASE_DIR, f'article/data/mizar_sketch/refs/{article_name}/')
    proofs_sketches_path = os.path.join(BASE_DIR, f'article/data/mizar_sketch/proofs/{article_name}/')
    
    refs_path_list = glob.glob(refs_path+'*')
    refs_name_list = [absolute_path.rsplit("/", 1)[1] for absolute_path in refs_path_list]
    proofs_path_list = glob.glob(proofs_path+'*')
    proofs_name_list = [absolute_path.rsplit("/", 1)[1] for absolute_path in proofs_path_list]

    for refs_name in refs_name_list:
        sketch_path = refs_sketches_path + refs_name
        return_json['refs'][refs_name] = ''
        if os.path.exists(sketch_path):
            with open(sketch_path, "r") as f:
                return_json['refs'][refs_name] = f.read()
    
    for proofs_name in proofs_name_list:
        sketch_path = proofs_sketches_path + proofs_name
        return_json['proofs'][proofs_name] = ''
        if os.path.exists(sketch_path):
            with open(sketch_path, "r") as f:
                return_json['proofs'][proofs_name] = f.read()
    return JsonResponse(return_json)

    

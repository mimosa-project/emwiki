from django.shortcuts import render

from django.http import HttpResponse
import os

import glob

from emwiki.settings import BASE_DIR
# Create your views here.

def index(request):
    return HttpResponse("Hello World!!")

def detail(request):
    #osを使って、contextにstaticのディレクトリ構造を渡したい
    file_list = glob.glob(os.path.join(BASE_DIR, 'display/static/display/html/*.html'))
    file_list = [i.rsplit("/",1)[1] for i in file_list if ".html" in i]
    context = {'file_path':"display/"+str(request.GET.get('id')), 'file_list':file_list}
    return render(request, "display/detail.html",context)

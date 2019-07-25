from django.shortcuts import render

from django.http import HttpResponse
import os

import glob

from emwiki.settings import BASE_DIR
# Create your views here.

def index(request):
    return HttpResponse("Hello World!!")

def detail(request):
    file_list = glob.glob(os.path.join(BASE_DIR, 'static/html/*.html'))
    file_list = [i.rsplit("/",1)[1] for i in file_list if ".html" in i]
    if request.GET.get('id'):
        file_path = str(request.GET.get('id'))
    else:
        file_path = 'pages/start.html'
    context = {'file_path': file_path, 'file_list':file_list}
    return render(request, "display/detail.html",context)

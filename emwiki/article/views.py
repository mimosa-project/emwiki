from django.shortcuts import render
import os
import glob
from emwiki.settings import BASE_DIR

# Create your views here.

def article(request):
    file_list = glob.glob(os.path.join(BASE_DIR, 'static/mizar_html/*.html'))
    file_list = [absolute_path.rsplit("/", 1)[1] for absolute_path in file_list]
    if request.GET.get('id'):
        file_path = "mizar_html/" + str(request.GET.get('id'))
    else:
        file_path = 'optional/start.html'
    context = {'file_path':file_path, 'file_list':file_list}
    return render(request, 'article/article.html', context)
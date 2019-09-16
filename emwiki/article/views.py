from django.shortcuts import render
import os
import glob
from emwiki.settings import BASE_DIR
from django.http import HttpResponse
from django.urls import reverse


def renderer(request):
    file_list = glob.glob(os.path.join(BASE_DIR, 'static/mizar_html/*.html'))
    file_list = [absolute_path.rsplit("/", 1)[1] for absolute_path in file_list]
    file_path = 'optional/start.html'
    context = {'file_path':file_path, 'file_list':file_list}
    return render(request, 'article/article.html', context)

def dataReciever(request):
    if 'content' in request.POST:
        file_name = request.POST.get('id',None)
        if 'proof_sketch' == request.POST.get('content',None):
            proof_name = request.POST.get("proof_name",None)
            file_name = file_name.replace(".html", "")
            proof_list = glob.glob(os.path.join(BASE_DIR, 'static/mizar_html/proofs/'+file_name.replace(".html","")+'/*'))
            proof_list = [absolute_path.rsplit("/", 1)[1] for absolute_path in proof_list]
            sketch_path = os.path.join(BASE_DIR, "article/data/mizar_sketch/"+file_name.replace(".html",""))
            if proof_name in proof_list:
                if not os.path.exists(sketch_path):
                    os.mkdir(sketch_path)
                with open(sketch_path+"/"+proof_name, "w") as f:
                    f.write(request.POST.get("proof_sketch",None))
                return HttpResponse()
            else:
                print('proof not found')
                return HttpResponse()
    else:
        return HttpResponse()

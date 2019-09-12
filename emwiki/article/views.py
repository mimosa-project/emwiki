from django.shortcuts import render
import os
import glob
from emwiki.settings import BASE_DIR
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse

# Create your views here.

def article(request):
    file_list = glob.glob(os.path.join(BASE_DIR, 'static/mizar_html/*.html'))
    file_list = [absolute_path.rsplit("/", 1)[1] for absolute_path in file_list]
    if request.GET.get('id'):
        file_name = str(request.GET.get('id'))
        file_path = "mizar_html/" + file_name
        context = {'file_list':file_list, 'file_path':file_path}
        if "proof_name" in request.GET:
            proof_name = request.GET.get("proof_name")
            proof_list = glob.glob(os.path.join(BASE_DIR, 'static/mizar_html/proofs/'+file_name.replace(".html","")+'/*'))
            proof_list = [absolute_path.rsplit("/", 1)[1] for absolute_path in proof_list]
            sketch_path = os.path.join(BASE_DIR, "article/data/mizar_sketch/"+file_name.replace(".html",""))
            if not "proof_sketch" in request.GET:
                #proof_sketch引数がなかった時の処理
                print("error:proof_sketch not found")
            elif not proof_name in proof_list:    
                #proofが見つからなかった時の処理
                print("error:proof not found")
            else:
                if not os.path.exists(sketch_path):
                    os.mkdir(sketch_path)
                with open(sketch_path+"/"+proof_name, "w") as f:
                    f.write(request.GET.get("proof_sketch"))
            return HttpResponseRedirect(reverse("article:article") + "?id=" + file_name)
    else:
        file_path = 'optional/start.html'
        context = {'file_path':file_path, 'file_list':file_list}
    return render(request, 'article/article.html', context)
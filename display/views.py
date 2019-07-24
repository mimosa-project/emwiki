from django.shortcuts import render

from django.http import HttpResponse

# Create your views here.

def index(request):
    return HttpResponse("Hello World!!")

def detail(request):
    context = {'file_path':"display/"+str(request.GET.get('id'))}
    return render(request, "display/detail.html",context)
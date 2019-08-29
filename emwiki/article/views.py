from django.shortcuts import render

# Create your views here.

def article(request):
    context = {}
    return render(request, 'article/article.html', context)
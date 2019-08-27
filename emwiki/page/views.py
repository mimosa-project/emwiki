from django.shortcuts import render

# Create your views here.

def page(request):
    context = {}
    return render(request, 'page/page.html', context)

from django.shortcuts import render
import os
from emwiki.settings import BASE_DIR
import json
# Create your views here.


def index(request, filename):
    context = {
        'filename': f'mmlreference/mml-contents/{filename}.html'
    }
    return render(request, f'mmlreference/index.html', context)

from django.shortcuts import render
import os
from emwiki.settings import BASE_DIR
import json
# Create your views here.


def index(request, filename):
    context = {
        'filename': f'/static/mml-contents/{filename}'
    }
    return render(request, f'mmlreference/index.html', context)

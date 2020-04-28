from django.shortcuts import render
import os
from emwiki.settings import BASE_DIR
import json
# Create your views here.


def index(request, filename):
    mml_index_path = os.path.join(BASE_DIR, 'mmlreference', 'mml_index.json')
    with open(mml_index_path, 'r') as f:
        index_data = json.load(f)
    context = {
        'filename': filename,
        'symbol': index_data[filename]['symbol'],
        'type': index_data[filename]['type']
    }
    return render(request, 'mmlreference/index.html', context)

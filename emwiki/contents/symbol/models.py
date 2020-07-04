import os

from django.db import models

from contents.contents.models import Content
from emwiki.settings import STATIC_SYMBOLS_URL, PRODUCT_SYMBOLHTML_DIR


class Symbol(Content):
    filename = models.CharField(max_length=20)
    category = 'Symbol'
    color = '#F9C270'
    file_dir = PRODUCT_SYMBOLHTML_DIR

    def get_static_url(self):
        return STATIC_SYMBOLS_URL + self.filename

    def get_file_path(self):
        return os.path.join(self.file_dir, f'{self.filename}.html')

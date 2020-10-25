import os

from django.db import models

from contents.contents.models import Content
from emwiki.settings import STATIC_SYMBOLS_URL, PRODUCT_SYMBOLHTML_DIR


class Symbol(Content):
    filename = models.CharField(max_length=20)

    @classmethod
    def get_category(cls):
        return 'Symbol'

    @classmethod
    def get_color(cls):
        return '#F9C270'

    @classmethod
    def get_htmlfile_dir(cls):
        return PRODUCT_SYMBOLHTML_DIR

    @classmethod
    def get_model(cls, name=None, filename=None):
        if filename:
            model = Symbol.objects.get(filename=filename)
        elif name:
            model = Symbol.objects.get(name=name)
        else:
            raise ValueError

        return model

    def get_static_url(self):
        return STATIC_SYMBOLS_URL + self.filename

    def get_htmlfile_path(self):
        return os.path.join(self.file_dir, f'{self.filename}')

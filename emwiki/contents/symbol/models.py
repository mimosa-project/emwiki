from django.db import models
from contents.contents.models import Content
from emwiki.settings import STATIC_SYMBOLS_URL, MML_SYMBOLS_DIR
import os


class Symbol(Content):
    filename = models.CharField(max_length=50)
    color = '#F9C270'

    def get_static_url(self):
        return STATIC_SYMBOLS_URL + self.filename
    
    def get_static_path(self):
        return os.path.join(MML_SYMBOLS_DIR, self.name + '.html')

    @classmethod
    def get_static_dir(cls):
        return MML_SYMBOLS_DIR

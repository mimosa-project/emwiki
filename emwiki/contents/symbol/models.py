from django.db import models

from contents.contents.models import Content
from emwiki.settings import STATIC_SYMBOLS_URL


class Symbol(Content):
    filename = models.CharField(max_length=20)
    category = 'Symbol'
    color = '#F9C270'

    def get_static_url(self):
        return STATIC_SYMBOLS_URL + self.filename

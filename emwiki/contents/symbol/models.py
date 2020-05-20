from django.db import models
from contents.contents.models import Content
from django.urls import reverse_lazy
from emwiki.settings import STATIC_SYMBOLS_URL


class Symbol(Content):
    filename = models.CharField(max_length=50)
    
    def get_absolute_url(self):
        return reverse_lazy('contents:index', kwargs={'category': 'symbol', 'name': self.name})

    def get_static_url(self):
        return STATIC_SYMBOLS_URL + self.filename

from django.db import models
from emwiki.settings import STATIC_SYMBOLS_URL, STATIC_ARTICLES_URL
from django.urls import reverse_lazy
# Create your models here.


class Content(models.Model):
    # 抽象基底クラス
    name = models.CharField(primary_key=True, max_length=50)
    filename = models.CharField(max_length=50)

    class Meta:
        abstract = True

    def __str__(self):
        return self.name


class Symbol(Content):
    
    def get_absolute_url(self):
        return reverse_lazy('contents:index', kwargs={'type': 'symbol', 'name': self.name})

    def get_static_url(self):
        return STATIC_SYMBOLS_URL + self.filename


class Article(Content):
    
    def get_absolute_url(self):
        return reverse_lazy('contents:index', kwargs={'type': 'article', 'name': self.name})

    def get_static_url(self):
        return STATIC_ARTICLES_URL + self.filename

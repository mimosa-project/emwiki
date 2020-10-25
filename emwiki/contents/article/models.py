import textwrap
import os

from django.db import models

from contents.contents.models import Content
from emwiki.settings import STATIC_ARTICLES_URL, PRODUCT_HTMLIZEDMML_DIR, MIZFILE_DIR


class Article(Content):

    mizfile_dir = MIZFILE_DIR

    @classmethod
    def get_category(cls):
        return 'Article'

    @classmethod
    def get_color(cls):
        return '#EF845C'

    @classmethod
    def get_htmlfile_dir(cls):
        return PRODUCT_HTMLIZEDMML_DIR

    @classmethod
    def get_model(cls, name=None, filename=None):
        if filename:
            name = os.path.splitext(filename)[0]
        elif name:
            pass
        else:
            raise ValueError

        return Article.objects.get(name=name)

    def get_static_url(self):
        return STATIC_ARTICLES_URL + self.name + '.html'

    def get_htmlfile_path(self):
        return os.path.join(self.get_htmlfile_dir(), f'{self.name}.html')

    def get_mizfile_path(self):
        return os.path.join(self.mizfile_dir, f'{self.name}.miz')


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    block = models.CharField(max_length=20)
    block_order = models.IntegerField()
    text = models.TextField(blank=True, null=True)

    HEADER = "::: "
    LINE_MAX_LENGTH = 75

    def __str__(self):
        return f'{self.article.name}:{self.block}_{self.block_order}'

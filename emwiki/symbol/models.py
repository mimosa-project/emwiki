import os

from django.db import models
from django.urls import reverse

from django.conf import settings


class Symbol(models.Model):
    name = models.CharField(primary_key=True, max_length=50)
    filename = models.CharField(max_length=20)
    type = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.name}:{self.filename}'

    @classmethod
    def get_htmlfile_dir(cls):
        return settings.PRODUCT_SYMBOLHTML_DIR

    @property
    def template_path(self):
        return f"symbol/symbol_html/{self.filename}"

    def get_htmlfile_path(self):
        return os.path.join(self.file_dir, f'{self.filename}')

    def get_absolute_url(self):
        return reverse("symbol:index", kwargs=dict(name=self.name))

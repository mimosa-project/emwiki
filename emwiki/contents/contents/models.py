from django.db import models
from django.urls import reverse_lazy


class Content(models.Model):
    # 抽象基底クラス
    name = models.CharField(primary_key=True, max_length=50)
    category = None
    color = None
    file_dir = None

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.get_category()}:{self.name}'

    @classmethod
    def get_category(cls):
        return NotImplementedError

    @classmethod
    def get_color(cls):
        return NotImplementedError

    @classmethod
    def get_file_dir(cls):
        return NotImplementedError

    @classmethod
    def get_model(cls, name=None, filename=None):
        return NotImplementedError

    def get_absolute_url(self):
        return reverse_lazy(
            'contents:index',
            kwargs={'category': self.get_category(), 'name': self.name}
        )

    def get_static_url(self):
        return NotImplementedError

    def get_file_path(self):
        return NotImplementedError

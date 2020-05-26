from django.db import models
from django.urls import reverse_lazy
from emwiki.settings import MML_ARTICLES_ORIGINAL_DIR


class Content(models.Model):
    # 抽象基底クラス
    name = models.CharField(primary_key=True, max_length=50)
    category = models.CharField(max_length=20)
    color = '#000000'
    
    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.category}:{self.name}'

    def get_absolute_url(self):
        return reverse_lazy('contents:index', kwargs={'category': self.category, 'name': self.name})

    def get_static_url(self):
        pass

    def get_static_path(self):
        pass

    @classmethod
    def get_static_dir(cls):
        pass

    @classmethod
    def get_original_dir(cls):
        return MML_ARTICLES_ORIGINAL_DIR

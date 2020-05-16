from django.db import models


class Content(models.Model):
    # 抽象基底クラス
    name = models.CharField(primary_key=True, max_length=50)
    
    class Meta:
        abstract = True

    def __str__(self):
        return self.name

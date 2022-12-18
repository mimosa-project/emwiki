from django.db import models
from django.urls import reverse


class Explanation(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()

    def __str__(self): # モデルが直接呼び出された時に返す値を定義
        return self.title # 記事タイトルを返す



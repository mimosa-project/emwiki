from django.db import models
from django.urls import reverse


class Explanation(models.Model):
    title = models.CharField(
        blank=True,
        null=True,
        max_length=200,
        unique=True,
        # error_messages={
        #     'unique': ("A document with this title already exists."),
        # }
    )
    text = models.TextField(blank=True, null=True)


    def __str__(self): # モデルが直接呼び出された時に返す値を定義
        return self.pk, self.title # 記事タイトルを返す



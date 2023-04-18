from django.db import models
# from django.urls import reverse


class Explanation(models.Model):
    title = models.CharField(max_length=200, unique=True)
    text = models.TextField()

    def __str__(self):
        return self.title

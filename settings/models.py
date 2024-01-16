from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


class Settings(models.Model):
    github_id = models.CharField(max_length=100, default='', blank=True)
    repository_url = models.CharField(max_length=100, default='', blank=True)
    isChecked = models.BooleanField(default=False)
    
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1)

    def __str__(self):
        return f"{self.user.username}, {self.github_id}"
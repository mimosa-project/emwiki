from django.db import models
from django.conf import settings
# import subprocess
from django.utils import timezone


class Explanation(models.Model):
    title = models.CharField(max_length=200, unique=True)
    text = models.TextField()
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title, self.author, self.created_at, self.updated_at

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)

    def commit_explanation_creates(self):
        commit_message = f'Create {self.text}\n {self.author}\n'
        settings.EXPLANATION_REPO.git.add('models.py')
        settings.EXPLANATION_REPO.git.commit('--allow-empty', '-m', commit_message)

    def commit_explanation_changes(self):
        commit_message = f'Update {self.text}\n {self.author}\n'
        settings.EXPLANATION_REPO.git.add('models.py')
        settings.EXPLANATION_REPO.git.commit('--allow-empty', '-m', commit_message)

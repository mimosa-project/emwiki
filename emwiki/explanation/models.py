import os

from django.db import models
from django.conf import settings
from django.utils import timezone


class Explanation(models.Model):
    title = models.CharField(max_length=200, unique=True)
    text = models.TextField()
    preview = models.TextField(default='no preview')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True, blank=True)
    related_articles = models.ManyToManyField('article.Article', related_name='explanations')

    def __str__(self):
        return f"{self.title}, {self.author}"

    def save(self, *args, **kwargs):
        self.updated_at = timezone.now()
        return super().save(*args, **kwargs)

    def get_explanationfile_path(self):
        return os.path.join(settings.EMWIKI_CONTENTS_EXPLANATON_DIR, 'explanation.txt')

    def commit_explanation_creates(self):
        commit_message = f'Create {self.title}\n {self.author}\n'
        settings.EMWIKI_CONTENTS_EXPLANATION_REPO.git.add(self.get_explanationfile_path())
        settings.EMWIKI_CONTENTS_EXPLANATION_REPO.index.commit(commit_message)

    def commit_explanation_changes(self):
        commit_message = f'Update {self.title}\n {self.author}\n'
        settings.EMWIKI_CONTENTS_EXPLANATION_REPO.git.add(self.get_explanationfile_path())
        settings.EMWIKI_CONTENTS_EXPLANATION_REPO.index.commit(commit_message)

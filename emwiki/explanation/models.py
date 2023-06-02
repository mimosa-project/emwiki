from django.db import models
from django.conf import settings
import subprocess
# from django.contrib.auth import get_user_model
from django.utils import timezone

# User = get_user_model()
# default_author = User.objects.first()
# default_created_at = timezone.now()


class Explanation(models.Model):
    title = models.CharField(max_length=200, unique=True)
    text = models.TextField()
    # author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=default_author)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
    
    def commit_explanation_creates(self):
        commit_message = f'Create {self.title}\t {self.text}\n'
        subprocess.call(['git', 'add', 'explanation/models.py'])
        subprocess.call(['git', 'commit', '-m', commit_message])

    def commit_explanation_changes(self):
        commit_message = f'Update {self.title}\t {self.text}\n'
        subprocess.call(['git', 'add', 'explanation/models.py'])
        subprocess.call(['git', 'commit', '-m', commit_message])

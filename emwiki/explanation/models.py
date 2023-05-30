from django.db import models
import subprocess


class Explanation(models.Model):
    title = models.CharField(max_length=200, unique=True)
    text = models.TextField()

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

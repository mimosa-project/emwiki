# import os

from django.db import models
# from django.conf import settings
import subprocess
# from django.urls import reverse


class Explanation(models.Model):
    title = models.CharField(max_length=200, unique=True)
    text = models.TextField()
    # explanation_dir = settings.EXPLANATON_DOCUMENTS_DIR

    def __str__(self):
        return self.title
    
    def commit_model_changes(self):
        commit_message = f'Update {self.title}\n'
        subprocess.call(['git', 'add', 'explanation/models.py'])
        subprocess.call(['git', 'commit', '-m', commit_message])

    # モデルの作成や変更後に実行するコード
    # commit_model_changes()
    
    # def get_explanation_path(self):
    #     return os.path.join(self.explanation_dir, f'{self.title}.md')
    
    # def commit_explanationtext(self):
    #     commit_message = f'Update {self.title}\n'
    #     settings.EXPLANATON_DOCUMENTS_REPO.git.add(self.get_explanation_path())
    #     settings.EXPLANATON_DOCUMENTS_REPO.index.commit(commit_message)
    #     print(commit_message)
               
    # def save_explanationtext(self):
    #     print(self.text)
    

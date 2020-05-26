from django.db import models
from contents.contents.models import Content
from emwiki.settings import STATIC_ARTICLES_URL, MML_COMMENTED_DIR, MML_DIR, \
    MML_ARTICLES_DIR, MML_ARTICLES_ORIGINAL_DIR
import textwrap
import os


class Article(Content):
    color = '#EF845C'

    def get_static_url(self):
        return STATIC_ARTICLES_URL + self.name + '.html'

    def get_static_path(self):
        return os.path.join(MML_ARTICLES_DIR, self.name + '.html')

    def get_commented_path(self):
        return os.path.join(MML_COMMENTED_DIR, self.name + '.miz')

    def get_mml_path(self):
        return os.path.join(MML_DIR, self.name + '.miz')

    def get_original_path(self):
        return os.path.join(MML_ARTICLES_ORIGINAL_DIR, self.name + '.html')

    @classmethod
    def get_static_dir(cls):
        return MML_ARTICLES_DIR


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    block = models.CharField(max_length=20)
    block_order = models.IntegerField()
    text = models.TextField(blank=True, null=True)

    HEADER = "::: "
    LINE_MAX_LENGTH = 75

    def format_text(self):
        """format comment text
        
        Returns:
            string: format comment text
        """
        comment_lines = []
        for line in self.text.splitlines():
            for cut_line in textwrap.wrap(line, self.LINE_MAX_LENGTH):
                comment_lines.append(f'{self.HEADER}{cut_line}')
        return '\n'.join(comment_lines)

    def __str__(self):
        return f'{self.article.name}:{self.block}_{self.block_order}'

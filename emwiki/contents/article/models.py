import textwrap
import os

from django.db import models

from contents.contents.models import Content
from emwiki.settings import STATIC_ARTICLES_URL, PRODUCT_HTMLIZEDMML_DIR, \
    RAW_MIZFILE_DIR, COMMENTED_MIZFILE_DIR


class Article(Content):
    category = 'Article'
    color = '#EF845C'
    file_dir = PRODUCT_HTMLIZEDMML_DIR

    raw_mizfile_dir = RAW_MIZFILE_DIR
    commented_mizfile_dir = COMMENTED_MIZFILE_DIR

    def get_static_url(self):
        return STATIC_ARTICLES_URL + self.name + '.html'

    def get_file_path(self):
        return os.path.join(self.file_dir, f'{self.name}.html')

    def get_raw_mizfile_path(self):
        return os.path.join(self.raw_mizfile_dir, f'{self.name}.miz')

    def get_commented_mizfile_path(self):
        return os.path.join(self.commented_mizfile_dir, f'{self.name}.miz')


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
        if self.text == '':
            lines = []
        else:
            lines = self.text.split('\n')
        for line in lines:
            if len(line) > self.LINE_MAX_LENGTH:
                for cut_line in textwrap.wrap(line, self.LINE_MAX_LENGTH):
                    comment_lines.append(f'{self.HEADER}{cut_line}')
            else:
                comment_lines.append(f'{self.HEADER}{line}')
        return '\n'.join(comment_lines)

    def __str__(self):
        return f'{self.article.name}:{self.block}_{self.block_order}'

import os

from django.conf import settings
from django.db import models
from django.urls import reverse

from article.miz_text_converter import MizTextConverter


class Article(models.Model):
    name = models.CharField(primary_key=True, max_length=50)
    mizfile_dir = settings.EMWIKI_CONTENTS_MML_DIR

    def __str__(self):
        return f'{self.name}'

    @classmethod
    def get_htmlfile_dir(cls):
        return settings.PRODUCT_HTMLIZEDMML_DIR

    @property
    def template_url(self):
        return f"article/htmlized_mml/{self.name}.html"

    def get_absolute_url(self):
        """Get self absolute url.

        This method is also used by Django flamework.

        Returns:
            text: self absolute url.
        """
        return reverse(
            'article:index',
            kwargs={'filename': self.name}
        )

    def get_htmlfile_path(self):
        return os.path.join(self.get_htmlfile_dir(), f'{self.name}.html')

    def get_mizfile_path(self):
        return os.path.join(self.mizfile_dir, f'{self.name}.miz')

    def load_mizfile2db(self):
        """Renew comments in databse by .miz files.
        """
        with open(self.get_mizfile_path(), 'r') as f:
            text = f.read()
        miztextconverter = MizTextConverter()
        comments = miztextconverter.extract_comments(text)

        comment_model_instances = []
        for comment in comments:
            comment_model_instances.append(
                Comment(
                    article=self,
                    text=comment['text'],
                    block=comment['block'],
                    block_order=comment['block_order']
                )
            )
        self.comment_set.all().delete()
        Comment.objects.bulk_create(comment_model_instances)

    def save_db2mizfile(self):
        """Overwrite .miz file with comments in database.
        """
        with open(self.get_mizfile_path(), 'r') as f:
            text = f.read()
        comments = [
            {
                'text': comment.text,
                'block': comment.block,
                'block_order': comment.block_order
            }
            for comment in Comment.objects.all()
        ]
        miztextconverter = MizTextConverter()
        raw_text = miztextconverter.remove_comments(text)
        commented_text = miztextconverter.embed_comments(raw_text, comments)
        with open(self.get_mizfile_path(), 'w') as f:
            f.write(commented_text)

    def commit_mizfile(self, username):
        commit_message = f'Update {self.name}\n\nUsername: {username}'
        settings.EMWIKI_CONTENTS_REPO.git.add(self.get_mizfile_path())
        settings.EMWIKI_CONTENTS_REPO.index.commit(commit_message)


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    block = models.CharField(max_length=20)
    block_order = models.IntegerField()
    text = models.TextField(blank=True, null=True)

    HEADER = "::: "
    LINE_MAX_LENGTH = 75

    def __str__(self):
        return f'{self.article.name}:{self.block}_{self.block_order}'

import git
import os

from django.db import models

from contents.contents.models import Content
from emwiki.settings import STATIC_ARTICLES_URL, PRODUCT_HTMLIZEDMML_DIR,\
     MIZFILE_DIR, LOCAL_COMMENT_REPOSITORY_DIR, COMMENT_PUSH_BRANCH
from contents.article.miz_text_converter import MizTextConverter


class Article(Content):

    mizfile_dir = MIZFILE_DIR

    @classmethod
    def get_category(cls):
        return 'Article'

    @classmethod
    def get_color(cls):
        return '#EF845C'

    @classmethod
    def get_htmlfile_dir(cls):
        return PRODUCT_HTMLIZEDMML_DIR

    @classmethod
    def get_model(cls, name=None, filename=None):
        if filename:
            name = os.path.splitext(filename)[0]
        elif name:
            pass
        else:
            raise ValueError

        return Article.objects.get(name=name)

    def get_static_url(self):
        return STATIC_ARTICLES_URL + self.name + '.html'

    def get_htmlfile_path(self):
        return os.path.join(self.get_htmlfile_dir(), f'{self.name}.html')

    def get_mizfile_path(self):
        return os.path.join(self.mizfile_dir, f'{self.name}.miz')

    def load_mizfile2db(self):
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
        Comment.objects.all().delete()
        Comment.objects.bulk_create(comment_model_instances)

    def save_db2mizfile(self):
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

    def push_mizfile2origin(self, username):
        repo = git.Repo(LOCAL_COMMENT_REPOSITORY_DIR)
        repo.git.checkout(COMMENT_PUSH_BRANCH)
        commit_message = f'Update {self.name}\n\nUsername: {username}'
        repo.git.add(self.get_mizfile_path())
        repo.index.commit(commit_message)
        origin = git.remote.Remote(repo=repo, name='origin')
        origin.push(COMMENT_PUSH_BRANCH)


class Comment(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE)
    block = models.CharField(max_length=20)
    block_order = models.IntegerField()
    text = models.TextField(blank=True, null=True)

    HEADER = "::: "
    LINE_MAX_LENGTH = 75

    def __str__(self):
        return f'{self.article.name}:{self.block}_{self.block_order}'

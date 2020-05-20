import glob
import os
from contents.article.models import Article, Comment
from contents.article.classes import MizFile


class ArticleInitializer():
    def __init__(self):
        pass

    @classmethod
    def initialize(cls, from_dir):
        Article.objects.all().delete()
        print(os.path.join(from_dir, "*.miz"))
        htmls = glob.glob(os.path.join(from_dir, "*.miz"))
        articles = []
        print(f'creating { len(htmls)} Articles')
        for i, html in enumerate(htmls):
            basename = os.path.basename(html)
            article = Article(name=os.path.splitext(basename)[0])
            articles.append(article)
        print(f'{len(articles)} articles were initialized')
        Article.objects.bulk_create(articles)


class CommentInitializer():
    def __init__(self):
        pass

    @classmethod
    def initialize(cls, articles):
        Comment.objects.all().delete()
        comments = []
        for article in articles:
            if os.path.exists(article.get_commented_path()):
                mizfile = MizFile()
                mizfile.read(article.get_commented_path())
                comments.extend(mizfile.extract_comments(article))
        print(f'{len(comments)} comments were initialized')
        Comment.objects.bulk_create(comments)

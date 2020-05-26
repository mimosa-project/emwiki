import glob
import os

from tqdm import tqdm

from contents.article.classes import ArticleArchiver
from contents.article.models import Article


class ArticleGenerator():

    def __init__(self):
        self.mml_paths = []
        self.articles = []

    def read(self, from_dir):
        self.mml_paths = glob.glob(os.path.join(from_dir, "*.html"))

    def generate(self):
        print(f'generating {len(self.mml_paths)} Articles')
        for path in tqdm(self.mml_paths):
            basename = os.path.basename(path)
            article = Article(category='Article', name=os.path.splitext(basename)[0])
            self.articles.append(article)


class CommentGenerator():
    def __init__(self):
        self.comments = []

    def generate(self, articles):
        print('generating Comments')
        for article in tqdm(articles):
            articleadaptor = ArticleArchiver(article)
            self.comments.extend(articleadaptor.extract())

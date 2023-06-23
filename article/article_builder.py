import glob
import os

from django.conf import settings
from tqdm import tqdm

from article.models import Article, Comment


class ArticleBuilder:
    """Articleテーブルを作成する.

    Attributes:
        from_dir(os.path): Directory where commented .miz file exists.
    """
    from_dir = settings.MML_MML_DIR

    def __init__(self):
        self.objects = []

    def delete_models(self):
        Article.objects.all().delete()
        Comment.objects.all().delete()
        print('Deleted all Articles, Comments')

    def create_models(self):
        html_paths = glob.glob(os.path.join(self.from_dir, "*.miz"))
        articles = []
        for from_path in tqdm(
                html_paths, desc='Creating Article Models'):
            basename = os.path.basename(from_path)
            name = os.path.splitext(basename)[0]
            article = Article(name)
            articles.append(article)
        Article.objects.bulk_create(articles)

        for article in tqdm(Article.objects.all(), desc='Creating Comment Models'):
            article.mizfile_dir = self.from_dir
            article.load_mizfile2db()

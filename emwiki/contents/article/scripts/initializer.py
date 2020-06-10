import glob
import os

from contents.contents.scripts.initializer import ContentInitializer
from contents.article.models import Article
from contents.article.scripts.builder import ArticleBuilder
from emwiki.settings import RAW_HTMLIZEDMML_DIR, PRODUCT_HTMLIZEDMML_DIR


class ArticleInitializer(ContentInitializer):

    def __init__(self):
        self.builder = ArticleBuilder()
        self.raw_htmlizedmml_dir = RAW_HTMLIZEDMML_DIR
        self.product_htmlizedmml_dir = PRODUCT_HTMLIZEDMML_DIR

    def _generate_files(self):
        self.builder.bulk_build(
            self.raw_htmlizedmml_dir,
            self.product_htmlizedmml_dir
        )

    def _delete_models(self):
        Article.objects.all().delete()

    def _create_models(self):
        articles = []
        html_paths = glob.glob(os.path.join(self.product_htmlizedmml_dir, "*.html"))
        for path in html_paths:
            basename = os.path.basename(path)
            name = os.path.splitext(basename)[0]
            article = Article(name=name)
            articles.append(article)
        Article.objects.bulk_create(articles)

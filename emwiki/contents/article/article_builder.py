import glob
import os
from tqdm import tqdm

from contents.article.miz_file import MizFile
from contents.article.models import Article, Comment
from contents.contents.content_builder import ContentBuilder
from emwiki.settings import COMMENTED_MIZFILE_DIR


class ArticleBuilder(ContentBuilder):
    from_dir = COMMENTED_MIZFILE_DIR

    def delete_models(self):
        Article.objects.all().delete()
        Comment.objects.all().delete()
        print('Deleted all Articles, Comments')

    def create_models(self):
        print('Create Articles, Comments')
        print('    from ', self.from_dir)
        html_paths = glob.glob(os.path.join(self.from_dir, "*.miz"))
        articles = []
        comments = []
        for from_path in tqdm(html_paths):
            basename = os.path.basename(from_path)
            name = os.path.splitext(basename)[0]
            article = Article(name)
            articles.append(article)

            mizfile = MizFile(from_path)
            mizfile.read()
            comments.extend(mizfile.extract(article))

        Article.objects.bulk_create(articles)
        print('Created Articles')
        Comment.objects.bulk_create(comments)
        print('Created Comments')

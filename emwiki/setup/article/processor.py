from contents.article.models import Article
from .content import Content
from .models import ArticleInitializer, CommentInitializer
from tqdm import tqdm


class Processor:
    def __init__(self):
        pass

    def execute(self, from_dir):
        ArticleInitializer.initialize(from_dir)
        CommentInitializer.initialize(Article.objects.all())

        print(f'executing')
        for article in tqdm(Article.objects.all()):
            content = Content()
            content.read(article.get_original_path())
            content.build()
            content.write(article.get_static_path())

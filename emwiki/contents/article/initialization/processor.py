from contents.article.models import Article, Comment

from .files import FileGenerator
from .models import ArticleGenerator, CommentGenerator


class Processor:
    def __init__(self):
        pass

    def execute(self):
        from_dir = Article.get_original_dir()
        to_dir = Article.get_static_dir()

        articlegenerator = ArticleGenerator()
        commentgenerator = CommentGenerator()
        
        articlegenerator.read(from_dir)
        articlegenerator.generate()
        
        commentgenerator.generate(articlegenerator.articles)

        print('Remove all Articles')
        Article.objects.all().delete()
        print('Remove all Comments')
        Comment.objects.all().delete()

        print('Create Articles')
        Article.objects.bulk_create(articlegenerator.articles)
        print('Create Comments')
        Comment.objects.bulk_create(commentgenerator.comments)

        filegenerator = FileGenerator()
        print('Generate and Create Article Files')
        filegenerator.generate(from_dir, to_dir)

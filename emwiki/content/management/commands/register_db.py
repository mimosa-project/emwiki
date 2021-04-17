from django.core.management.base import BaseCommand

from article.article_builder import ArticleBuilder
from content.content_initializer import ContentInitializer
from symbol.symbol_builder import SymbolBuilder


class Command(BaseCommand):
    # python manage.py help count_entryで表示されるメッセージ
    help = 'Register models about  Article, Comment, Symbol'

    def add_arguments(self, parser):
        parser.add_argument('target')

    # コマンドが実行された際に呼ばれるメソッド
    def handle(self, *args, **options):
        self.stdout.write('Start initializing emwiki contents')

        target = options['target']
        contents_initializers = []
        article_builder = ArticleBuilder()
        symbol_builder = SymbolBuilder()
        article_initializer = ContentInitializer(article_builder)
        symbol_initializer = ContentInitializer(symbol_builder)

        if target == 'all':
            contents_initializers.append(article_initializer)
            contents_initializers.append(symbol_initializer)
        elif target == 'article':
            contents_initializers.append(article_initializer)
        elif target == 'symbol':
            contents_initializers.append(symbol_initializer)

        for initializer in contents_initializers:
            initializer.initialize()

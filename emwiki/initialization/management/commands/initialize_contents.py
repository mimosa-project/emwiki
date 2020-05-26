from django.core.management.base import BaseCommand

from contents.article.initialization.processor import Processor as ArticleProcessor
from contents.symbol.initialization.processor import Processor as SymbolProcessor


class Command(BaseCommand):
    # python manage.py help count_entryで表示されるメッセージ
    help = 'Initialize models and HTML files about  Article, Comment, Symbol'

    # コマンドが実行された際に呼ばれるメソッド
    def handle(self, *args, **options):
        self.stdout.write('Start initializing emwiki contents')
        articleprocessor = ArticleProcessor()
        articleprocessor.execute()

        symbolprocessor = SymbolProcessor()
        symbolprocessor.execute()

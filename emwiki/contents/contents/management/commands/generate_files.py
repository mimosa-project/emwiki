from django.core.management.base import BaseCommand

from contents.article.article_builder import ArticleBuilder
from contents.article.htmlized_mml_builder import HtmlizedMmlBuilder
from contents.contents.content_initializer import ContentInitializer
from contents.contents.html_initializer import HtmlInitializer
from contents.symbol.symbol_builder import SymbolBuilder
from contents.symbol.symbol_html_builder import SymbolHtmlBuilder


class Command(BaseCommand):
    # python manage.py help count_entryで表示されるメッセージ
    help = 'Initialize models and HTML files about  Article, Comment, Symbol'

    def add_arguments(self, parser):
        parser.add_argument('target')

    # コマンドが実行された際に呼ばれるメソッド
    def handle(self, *args, **options):
        self.stdout.write('Start initializing emwiki contents')

        target = options['target']
        html_initializers = []
        htmlized_mml_builder = HtmlizedMmlBuilder()
        symbol_html_builder = SymbolHtmlBuilder()
        htmlized_mml_initializer = HtmlInitializer(htmlized_mml_builder)
        symbol_html_initializer = HtmlInitializer(symbol_html_builder)

        if target == 'all':
            html_initializers.append(htmlized_mml_initializer)
            html_initializers.append(symbol_html_initializer)
        elif target == 'article':
            html_initializers.append(htmlized_mml_initializer)
        elif target == 'symbol':
            html_initializers.append(symbol_html_initializer)

        for initializer in html_initializers:
            initializer.initialize()

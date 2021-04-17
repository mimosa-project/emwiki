from django.core.management.base import BaseCommand

from article.article_builder import ArticleBuilder
from article.htmlized_mml_builder import HtmlizedMmlBuilder
from content.content_initializer import ContentInitializer
from content.html_initializer import HtmlInitializer
from symbol.symbol_builder import SymbolBuilder
from symbol.symbol_html_builder import SymbolHtmlBuilder
from search.data_generator_for_search import DataGeneratorForSearch


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
        data_generator_for_search = DataGeneratorForSearch()

        if target == 'all':
            html_initializers.append(htmlized_mml_initializer)
            html_initializers.append(symbol_html_initializer)
            data_generator_for_search.generate_data_for_search()
        elif target == 'article':
            html_initializers.append(htmlized_mml_initializer)
        elif target == 'symbol':
            html_initializers.append(symbol_html_initializer)
        elif target == 'search':
            data_generator_for_search.generate_data_for_search()

        for initializer in html_initializers:
            initializer.initialize()

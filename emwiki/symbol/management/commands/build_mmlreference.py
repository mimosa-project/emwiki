from django.core.management.base import BaseCommand

from symbol.symbol_html_builder import SymbolHtmlBuilder


class Command(BaseCommand):
    # python manage.py help count_entryで表示されるメッセージ
    help = 'Initialize models and HTML files about  Article, Comment, Symbol'

    # コマンドが実行された際に呼ばれるメソッド
    def handle(self, *args, **options):
        self.stdout.write('Start initializing emwiki contents')
        symbol_html_builder = SymbolHtmlBuilder()
        symbol_html_builder.create_files()

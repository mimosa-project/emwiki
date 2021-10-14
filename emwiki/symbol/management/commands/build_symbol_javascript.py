import os

from django.conf import settings
from django.core.management.base import BaseCommand

from symbol.symbol_javascript_builder import SymbolJavascriptBuilder


class Command(BaseCommand):
    # python manage.py help count_entryで表示されるメッセージ
    help = 'Create javascript for Symbol'

    # DBの内容を元に作成するので, コマンド"load_symbols"の後に実行する
    # コマンドが実行された際に呼ばれるメソッド
    def handle(self, *args, **options):
        self.stdout.write('Start creating javascript for Symbol')
        symbol_javascript_builder = SymbolJavascriptBuilder()
        symbol_javascript_builder.create_files(
            os.path.join(settings.SYMBOL_JAVASCRIPT_DIR, 'mml-index.js')
        )

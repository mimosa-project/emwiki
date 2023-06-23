from django.core.management.base import BaseCommand

from symbol.symbol_builder import SymbolBuilder


class Command(BaseCommand):
    # python manage.py help count_entryで表示されるメッセージ
    help = 'Register models about  Article, Comment, Symbol'

    # コマンドが実行された際に呼ばれるメソッド
    def handle(self, *args, **options):
        self.stdout.write('Start initializing emwiki contents')

        symbol_builder = SymbolBuilder()
        symbol_builder.delete_models()
        symbol_builder.create_models()

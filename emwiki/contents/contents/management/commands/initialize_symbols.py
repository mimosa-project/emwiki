from django.core.management.base import BaseCommand

from contents.symbol.scripts.initializer import SymbolInitializer


class Command(BaseCommand):
    # python manage.py help count_entryで表示されるメッセージ
    help = 'Initialize models and HTML files about Symbol'

    # コマンドが実行された際に呼ばれるメソッド
    def handle(self, *args, **options):
        self.stdout.write('Start initializing symbol contents')

        initializer = SymbolInitializer
        initializer.initialize()

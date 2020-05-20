from django.core.management.base import BaseCommand
from setup.processor import Processor


class Command(BaseCommand):
    # python manage.py help count_entryで表示されるメッセージ
    help = 'Setup models and HTML files about  Article, Comment, Symbol'

    # コマンドが実行された際に呼ばれるメソッド
    def handle(self, *args, **options):
        self.stdout.write('Setup emwiki!')
        processor = Processor()
        processor.execute()

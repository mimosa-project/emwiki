import os

from django.core.management.base import BaseCommand

from article.downloader import Downloader
from emwiki.settings import BASE_DIR


class Command(BaseCommand):
    # python manage.py help count_entryで表示されるメッセージ
    help = 'Initialize models and HTML files about  Article, Comment, Symbol'

    def add_arguments(self, parser):
        parser.add_argument('target')

    # コマンドが実行された際に呼ばれるメソッド
    def handle(self, *args, **options):
        self.stdout.write('Start initializing emwiki contents')
        target = options['target']

        if target == 'mml':
            path = 'http://mizar.org/version/current/mml'
            extension = '.miz'
            to_dir = os.path.abspath(os.path.join(BASE_DIR, 'contents', 'mizarfiles', 'emwiki-contents', 'mml'))
            downloader = Downloader(path, extension)
        elif target == 'html':
            path = 'http://mizar.org/version/current/html'
            extension = '.html'
            to_dir = os.path.abspath(os.path.join(BASE_DIR, 'contents', 'mizarfiles', 'htmlized_mml'))
            downloader = Downloader(path, extension)
        else:
            self.stdout.write('Bad argument')
            return
        downloader.read_index()
        if not os.path.exists(to_dir):
            os.makedirs(to_dir)
        downloader.download(to_dir)

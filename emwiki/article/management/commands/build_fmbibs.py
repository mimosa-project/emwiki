from django.core.management.base import BaseCommand

from article.bib_builder import BibBuilder


class Command(BaseCommand):
    # python manage.py help count_entryで表示されるメッセージ
    help = 'Generate HTMLized MML'

    # コマンドが実行された際に呼ばれるメソッド
    def handle(self, *args, **options):
        self.stdout.write('Start generating HTMLized MML')
        bib_builder = BibBuilder()
        bib_builder.build()

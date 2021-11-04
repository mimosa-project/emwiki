from django.core.management.base import BaseCommand

from article.htmlized_mml_builder import HtmlizedMmlBuilder


class Command(BaseCommand):
    # python manage.py help count_entryで表示されるメッセージ
    help = 'Generate HTMLized MML'

    # コマンドが実行された際に呼ばれるメソッド
    def handle(self, *args, **options):
        self.stdout.write('Start generating HTMLized MML')
        htmlized_mml_builder = HtmlizedMmlBuilder()
        htmlized_mml_builder.update_files()

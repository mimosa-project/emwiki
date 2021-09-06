from django.core.management.base import BaseCommand

from search.data_generator_for_search import DataGeneratorForSearch


class Command(BaseCommand):
    # python manage.py help count_entryで表示されるメッセージ
    help = 'Initialize models and HTML files about  Article, Comment, Symbol'

    # コマンドが実行された際に呼ばれるメソッド
    def handle(self, *args, **options):
        self.stdout.write('Start generate data for search.')
        data_generator_for_search = DataGeneratorForSearch()
        data_generator_for_search.generate_data_for_search()

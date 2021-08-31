from django.core.management.base import BaseCommand
from graph.create_graph import create_graph
from graph.retrieve_dependency import make_miz_dependency


class Command(BaseCommand):
    # python manage.py help count_entryで表示されるメッセージ
    help = 'Generate graph json files'

    # コマンドが実行された際に呼ばれるメソッド
    def handle(self, *args, **options):
        self.stdout.write('Start generating dot_graph.json')
        node2targets_mml = make_miz_dependency()
        create_graph(node2targets_mml, 'dot_graph')

from django.core.management.base import BaseCommand

from article.article_builder import ArticleBuilder


class Command(BaseCommand):
    # python manage.py help count_entryで表示されるメッセージ
    help = 'Register models about  Article, Comment, Symbol'

    # コマンドが実行された際に呼ばれるメソッド
    def handle(self, *args, **options):
        self.stdout.write('Start initializing emwiki contents')
        article_builder = ArticleBuilder()
        article_builder.delete_models()
        article_builder.create_models()

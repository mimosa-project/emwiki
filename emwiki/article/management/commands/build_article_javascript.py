import os

from django.conf import settings
from django.core.management.base import BaseCommand

from article.article_javascript_builder import ArticleJavascriptBuilder


class Command(BaseCommand):
    # python manage.py help count_entryで表示されるメッセージ
    help = 'Create javascript for Article'

    # DBの内容を元に作成するので, コマンド"load_articles"の後に実行する
    # コマンドが実行された際に呼ばれるメソッド
    def handle(self, *args, **options):
        self.stdout.write('Start creating javascript for Article')
        article_javascript_builder = ArticleJavascriptBuilder()
        article_javascript_builder.create_files(
            os.path.join(settings.ARTICLE_JAVASCRIPT_DIR, 'article_names.js')
        )

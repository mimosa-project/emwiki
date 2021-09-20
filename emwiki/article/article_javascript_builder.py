import json
import os
import shutil
from article.models import Article

from django.conf import settings


class ArticleJavascriptBuilder:
    path = os.path.join(settings.BASE_DIR, 'article', 'static', 'article', 'JavaScript', 'article_names.js')

    # Articleアプリケーションで使用するJavascritを生成する
    # var article_names = ["abcmiz_0", "abcmiz_1", "abcmiz_a",...]
    def create_files(self):
        print('Building javascript for Article')
        article_names = list(Article.objects.order_by("name").values_list('name', flat=True))
        with open(self.path, mode='w', encoding='utf-8') as f:
            f.write("var article_names = ")
            json.dump(article_names, f)

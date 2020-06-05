from django.apps import AppConfig

from emwiki.settings import ARTICLE_DIR


class ArticleConfig(AppConfig):
    name = 'contents.article'
    path = ARTICLE_DIR

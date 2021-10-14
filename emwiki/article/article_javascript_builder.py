import json
from natsort import humansorted

from article.models import Article


class ArticleJavascriptBuilder:
    # Articleアプリケーションで使用するJavascritを生成する
    # var article_names = ["abcmiz_0", "abcmiz_1", "abcmiz_a",...]
    def create_files(self, path):
        articles = list(Article.objects.all())
        articles = humansorted(articles, key=lambda a: a.name)
        article_names = []
        for article in articles:
            article_names.append(article.name)
        with open(path, mode='w', encoding='utf-8') as f:
            f.write("var article_names = ")
            json.dump(article_names, f)

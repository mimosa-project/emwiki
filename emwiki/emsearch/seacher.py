from article.classes import ArticleHandler
import re
from difflib import SequenceMatcher


def search(search_query):
    search_results = []
    search_results += search_article(search_query)
    search_results.sort(key=lambda x: x['weight'], reverse=True)
    return search_results


def search_article(search_query):
    search_results = []
    file_list = [article_handler.article_name for article_handler in ArticleHandler.bundle_create()]
    file_list.sort()
    for filename in file_list:
        search_len, file_len = len(search_query), len(filename)
        weight = max([SequenceMatcher(None, search_query, filename[i:i + search_len]).ratio() for i in range(file_len - search_len + 1)], default=0)
        if weight > 0.8:
            search_results.append(
                {
                    'weight': weight,
                    'subject': filename,
                    'category': 'article',
                    'link': f'article/{filename}.html',
                }
            )
    return search_results

from article.classes import ArticleHandler
import re


def search(search_query):
    print(search_query)
    search_results = []
    search_results += get_article_result(search_query)
    # search_results = [{'subject': 'abcmiz_0.html', 'attributes': 'html', 'link': '/article'}, {'subject': 'abcmiz_1.html', 'attributes': 'html', 'link': '/article'}]
    return search_results

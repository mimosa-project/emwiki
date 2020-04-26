from article.classes import ArticleHandler
import re


def search(search_query):
    search_results = []
    search_results += get_article_result(search_query)
    return search_results


def get_article_result(search_query):
    result_weight_list = []
    result_list = []
    file_list = [article_handler.article_name for article_handler in ArticleHandler.bundle_create()]
    file_list.sort()
    for filename in file_list:
        match_length = len(re.findall('[' + search_query + ']|' + search_query, filename, flags=re.IGNORECASE))
        if match_length > len(search_query):
            weight = (len(search_query) - (match_length - len(search_query))) / len(search_query)
        else:
            weight = match_length / len(search_query)
        if weight > 0.8:
            result_weight_list.append({'name': filename, 'weight': weight})
    result_weight_list.sort(key=lambda x: x['weight'], reverse=True)
    for result in result_weight_list:
        result_list.append(
            {
                'subject': result['name'],
                'attributes': 'html',
                'link': 'article/' + result['name'] + '.html'
            }
        )
    return result_list

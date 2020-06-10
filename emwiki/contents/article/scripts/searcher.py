from functools import reduce
from operator import and_

from django.db.models import Q

from contents.article.models import Article
from contents.contents.scripts.searcher import ContentSearcher


class ArticleSearcher(ContentSearcher):

    def search(self, query_text):
        queryset = Article.objects.order_by('name')
        if query_text:
            query_text_replaced = query_text.replace(' ', '')
            # Create a query to search for a Article that includes
            # all the characters of "query_text_replaced"
            # in Article.name
            query = reduce(
                and_, [Q(name__icontains=q) for q in query_text_replaced]
            )
            return queryset.filter(query)
        else:
            return queryset

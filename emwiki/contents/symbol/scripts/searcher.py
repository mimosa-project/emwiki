from functools import reduce
from operator import and_

from django.db.models import Q

from contents.contents.scripts.content_searcher import ContentSearcher
from contents.symbol.models import Symbol


class SymbolSearcher(ContentSearcher):

    def search(self, query_text):
        queryset = Symbol.objects.order_by('name')
        if query_text:
            query_text_replaced = query_text.replace(' ', '')
            # Create a query to search for a Symbol that includes
            # all the characters of "query_text_replaced"
            # in Symbol.name
            query = reduce(
                and_, [Q(name__icontains=q) for q in query_text_replaced]
            )
            return queryset.filter(query)
        else:
            return queryset

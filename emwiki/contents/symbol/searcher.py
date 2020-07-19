from functools import reduce
from operator import and_, or_

from django.db.models import Q

from contents.contents.searcher import ContentSearcher
from contents.symbol.models import Symbol


class SymbolSearcher(ContentSearcher):

    def search(self, query_text):
        queryset = Symbol.objects.order_by('name')
        results = []
        if query_text:
            queries = query_text.split()

            # 完全一致
            query = reduce(
                or_, [Q(name__iexact=q) for q in queries]
            )
            results.extend(queryset.filter(query))
            queryset = queryset.exclude(query)

            # 前方一致
            query = Q(name__istartswith=queries[0])
            results.extend(queryset.filter(query))
            queryset = queryset.exclude(query)

            # 部分一致(and)
            query = reduce(
                and_, [Q(name__icontains=q) for q in queries]
            )
            results.extend(queryset.filter(query))
            queryset = queryset.exclude(query)

            # 後方一致
            # query = Q(name__iendswith=queries[-1])
            # results.extend(queryset.filter(query))
            # queryset = queryset.exclude(query)

            return results
        else:
            results = queryset
            return results

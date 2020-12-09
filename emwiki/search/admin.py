from django.contrib import admin

from search.models import Theorem, SearchHistory, SearchResult

admin.site.register(Theorem)
admin.site.register(SearchHistory)
admin.site.register(SearchResult)
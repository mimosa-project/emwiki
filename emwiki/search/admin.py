from django.contrib import admin

from search.models import Theorem, History, HistoryItem

admin.site.register(Theorem)
admin.site.register(History)
admin.site.register(HistoryItem)
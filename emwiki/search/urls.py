from django.urls import path

from . import views

app_name = 'search'
urlpatterns = [
    path('', views.index, name='index'),
    path('search', views.search, name='search'),
    path('get_keywords', views.get_keywords, name='get_keywords'),
]

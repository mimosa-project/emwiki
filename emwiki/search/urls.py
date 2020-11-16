from django.urls import path

from . import views

app_name = 'search'
urlpatterns = [
    path('', views.SearchView.as_view(), name='search'),
    path('get_keywords', views.get_keywords, name='get_keywords'),
    path('search-theorem/', views.SearchTheoremView.as_view(), name='search-theorem'),
]

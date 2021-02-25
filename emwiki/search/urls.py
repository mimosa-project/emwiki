from django.urls import path
from . import views

app_name = 'search'
urlpatterns = [
    path('search_theorem/', views.SearchTheoremView.as_view(), name='search_theorem'),
]

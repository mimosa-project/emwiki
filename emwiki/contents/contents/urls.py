from django.urls import path

from . import views

app_name = 'contents'
urlpatterns = [
    path('normalize_content_url', views.normalize_content_url, name='normalize_content_url'),
    path('<str:category>/<path:name>', views.ContentView.as_view(), name='index'),
]

from django.urls import path

from . import views

app_name = 'contents'
urlpatterns = [
    path('index_json', views.index_json, name='index_json'),
    path('<str:type>/<path:name>', views.index, name='index')
]

from django.urls import path

from . import views

app_name = 'symbol'
urlpatterns = [
    path('index_json', views.index_json, name='index_json'),
    path('<path:symbol>', views.index, name='index')
]

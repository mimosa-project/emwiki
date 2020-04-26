from django.urls import path

from . import views

app_name = 'emserach'
urlpatterns = [
    path('', views.index, name='index'),
    path('get_keywords', views.get_keywords, name='get_keywords'),
]

from django.urls import path

from . import views

app_name = 'article'
urlpatterns = [
    path('', views.renderer, name='renderer'),
    path('data/sketch/', views.recieveSketch, name='recieveSketch'),
    path('data/sketch/<str:article_name>', views.sendSketch, name='sendSketch'),
]
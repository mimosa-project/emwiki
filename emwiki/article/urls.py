from django.urls import path

from . import views

app_name = 'article'
urlpatterns = [
    path('', views.renderer, name='renderer'),
    path('sketch/', views.sketchReciever, name='sketchReciever'),
    path('data/<str:article_name>', views.dataSender, name='dataSender'),
]
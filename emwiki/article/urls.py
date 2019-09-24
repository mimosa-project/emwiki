from django.urls import path

from . import views

app_name = 'article'
urlpatterns = [
    path('', views.renderer, name='renderer'),
    path('data/', views.dataReciever, name='dataReciever'),
    path('data/mizar_sketch/<path:path>', views.dataSender, name='dataSender'),
]
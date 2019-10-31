from django.urls import path

from . import views

app_name = 'article'
urlpatterns = [
    path('', views.render_article, name='render_article'),
    path('data/sketch/', views.recieve_sketch, name='recieve_sketch'),
    path('data/sketchedmizar', views.apply_sketchedmizar, name='apply_sketchedmizar'),
    path('data/sketch/<str:article_name>', views.sendSketch, name='sendSketch'),
]

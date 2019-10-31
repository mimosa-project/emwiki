from django.urls import path

from . import views

app_name = 'article'
urlpatterns = [
    path('', views.render_article, name='render_article'),
    path('sketch', views.render_sketch, name='render_sketch'),
    path('data/sketch/', views.recieve_sketch, name='recieve_sketch'),
    path('data/sketchedmizar', views.apply_sketchedmizar, name='apply_sketchedmizar'),
]

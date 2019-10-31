from django.urls import path

from . import views

app_name = 'article'
urlpatterns = [
    path('', views.render_article, name='render_article'),
    path('data/comment/', views.recieve_comment, name='recieve_comment'),
    path('data/commentedmizar', views.apply_commentedmizar, name='apply_commentedmizar'),
    path('data/comment/<str:article_name>', views.send_comment, name='send_comment'),
]

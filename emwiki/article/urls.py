from django.urls import path

from . import views

app_name = 'article'
urlpatterns = [
    path('', views.render_article, name='render_article'),
    path('data/comment/', views.recieve_comment, name='recieve_comment'),
    path('data/push/comment', views.push_all_comment, name='push_all_comment'),
    path('data/pull/comment', views.pull_all_comment, name='pull_all_comment'),
    path('data/comment/<str:article_name>', views.send_comment, name='send_comment'),
]

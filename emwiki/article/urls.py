from django.urls import path

from . import views

app_name = 'article'
urlpatterns = [
    path('', views.render_article, name='render_article'),
    path('make_all_commented_mml_file', views.make_all_commented_mml_file, name='make_all_commented_mml_file'),
    path('submit_comment', views.update_comment, name='update_comment'),
    path('order_comment/<str:article_name>', views.send_comment_to_template, name='send_comment_to_template'),
]

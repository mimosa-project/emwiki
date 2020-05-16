from django.urls import path

from . import views

app_name = 'article'
urlpatterns = [
    path('submit_comment', views.submit_comment, name='submit_comment'),
    path('order_comments', views.order_comments, name='order_comments'),
]

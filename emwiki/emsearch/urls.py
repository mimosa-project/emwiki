from django.urls import path

from . import views

app_name = 'emserach'
urlpatterns = [
    path('', views.render_article, name='render_article'),
]

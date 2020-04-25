from django.urls import path

from . import views

app_name = 'mmlreference'
urlpatterns = [
    path('', views.index, name='index'),
]

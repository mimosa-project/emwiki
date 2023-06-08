from django.urls import path

from . import views

app_name = 'graph'
urlpatterns = [
    path('', views.GraphView.as_view(), name='index'),
]

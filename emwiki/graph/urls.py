from django.urls import path

from . import views

app_name = 'graph'
urlpatterns = [
    path('', views.emgraph, name='emgraph'),
]

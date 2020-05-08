from django.urls import path

from . import views

urlpatterns = [
    path('emgraph/', views.emgraph, name='emgraph'),
]

from django.urls import path

from . import views

urlpatterns = [
    path('emwiki', views.detail, name='detail'),
]
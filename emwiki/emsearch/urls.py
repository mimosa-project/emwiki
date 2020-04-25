from django.urls import path

from . import views

app_name = 'emserach'
urlpatterns = [
    path('', views.ajax_search, name='ajax_search'),
]

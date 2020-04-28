from django.urls import path

from . import views

app_name = 'mmlreference'
urlpatterns = [
    path('<str:filename>', views.index, name='index'),
]

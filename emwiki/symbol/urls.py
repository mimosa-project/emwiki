from django.urls import path, re_path

from . import views

app_name = 'symbol'
urlpatterns = [
    path('', views.SymbolIndexView.as_view(), name='index'),
    path('<path:filename>', views.SymbolView.as_view(), name='symbol')
]

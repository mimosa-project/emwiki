from django.urls import path

from . import views

app_name = 'symbol'
urlpatterns = [
    path('', views.SymbolIndexView.as_view(), name='index'),
    path('<path:filename>', views.SymbolView.as_view(), name='symbol')
]

from django.urls import path

from . import views

app_name = 'symbol'
urlpatterns = [
    path('names', views.SymbolIndexView.as_view(), name='names'),
    path('htmls', views.SymbolHtmlView.as_view(), name='htmls'),
    path('<path:name>', views.SymbolView.as_view(), name='index'),
]

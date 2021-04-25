from django.urls import path

from . import views

app_name = 'symbol'
urlpatterns = [
    path('names', views.get_names, name='names'),
    path('adjust-name', views.adjust_name, name='adjust_name'),
    path('<path:name>', views.SymbolView.as_view(), name='index'),
]

from django.urls import path, re_path

from . import views

app_name = 'symbol'
urlpatterns = [
    path('names', views.get_names, name='names'),
    path('adjust-name', views.adjust_name, name='adjust_name'),
    re_path('^.*$', views.SymbolView.as_view(), name='index'),
]

# urlpatterns = [
#     path('names', views.get_names, name='names'),
#     path('adjust-name', views.adjust_name, name='adjust_name'),
#     path('<path:name>', views.SymbolView.as_view(), name='index'),
# ]
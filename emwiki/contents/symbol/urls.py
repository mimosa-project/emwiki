from django.urls import path

from . import views

app_name = 'symbol'
urlpatterns = [
    path('order_symbol_names', views.order_symbol_names, name='order_symbol_names'),
]

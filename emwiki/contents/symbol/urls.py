from django.urls import path

from . import views

app_name = 'symbol'
urlpatterns = [
    path('order_names', views.order_names, name='order_names'),
]

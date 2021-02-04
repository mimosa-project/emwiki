from django.urls import path

from . import views

app_name = 'home'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('usage/', views.UsageView.as_view(), name='usage')
]

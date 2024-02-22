from django.urls import path
from . import views

app_name = 'settings'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('registration', views.RegistrationView.as_view(), name='registration'),
    path('change', views.ChangeView.as_view(), name='change'),
    path('develop', views.DevelopView.as_view(), name='develop'),
]

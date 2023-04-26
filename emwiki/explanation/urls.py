from django.urls import path
from . import views

app_name = 'explanation'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('create', views.CreateView.as_view(), name='create'),
    path('explanation', views.ExplanationView.as_view(), name='explanation'),
    path('detail/<str:title>', views.DetailView.as_view(), name='detail'),
    path('detail/<str:title>/update', views.UpdateView.as_view(), name='update'),
    path('detail/<str:title>/delete', views.DeleteView.as_view(), name='delete'),
]

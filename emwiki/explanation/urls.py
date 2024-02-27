from django.urls import path
from . import views

app_name = 'explanation'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('create', views.CreateView.as_view(), name='create'),
    path('explanation', views.ExplanationView.as_view(), name='explanation'),
    path('titles', views.ExplanationTitleView.as_view(), name='titles'),
    path('detail/<str:title>', views.DetailView.as_view(), name='detail'),
    path('detail/<str:title>/update', views.UpdateView.as_view(), name='update'),
    path('detail/<str:title>/delete', views.DeleteView.as_view(), name='delete'),
    path('<str:name_or_filename>', views.ArticleView.as_view(), name='article'),
    path('proofs/<str:article_name>/<str:proof_name>', views.ProofView.as_view(), name='proofs'),
    path('refs/<str:article_name>/<str:ref_name>', views.RefView.as_view(), name='refs'),
    # path('names', views.ArticleIndexView.as_view(), name='names'),
]

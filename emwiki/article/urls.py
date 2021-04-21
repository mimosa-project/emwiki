from django.urls import path
from django.views.decorators.cache import cache_page

from . import views

app_name = 'article'
urlpatterns = [
    path('proofs/<str:article_name>/<str:proof_name>', views.ProofView.as_view(), name='proofs'),
    path('refs/<str:article_name>/<str:ref_name>', views.RefView.as_view(), name='refs'),
    path('comments', views.CommentView.as_view(), name='comment'),
    path('names', views.get_names, name="names"),
    path('<path:filename>', cache_page(60)(views.ArticleView.as_view()), name='index'),
]

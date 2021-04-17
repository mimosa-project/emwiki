from django.urls import path
from . import views

app_name = 'article'
urlpatterns = [
    path('proofs/<str:article_name>/<str:proof_name>', views.ProofView.as_view(), name='proofs'),
    path('comments', views.CommentView.as_view(), name='comment'),
    path('<path:name>', views.ArticleView.as_view(), name='index'),
]

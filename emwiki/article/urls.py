from django.urls import path

from . import views

app_name = 'article'
urlpatterns = [
    path('proofs/<str:article_name>/<str:proof_name>', views.ProofView.as_view(), name='proofs'),
    path('refs/<str:article_name>/<str:ref_name>', views.RefView.as_view(), name='refs'),
    path('bibs', views.BibView.as_view(), name='bibs'),
    path('comments', views.CommentView.as_view(), name='comments'),
    path('names', views.ArticleIndexView.as_view(), name='names'),
    path('htmls', views.ArticleHtmlView.as_view(), name='htmls'),
    path('<str:name_or_filename>', views.ArticleView.as_view(), name='index'),
]

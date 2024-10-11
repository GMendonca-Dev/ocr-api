from django.urls import path
from .views import FullTextSearchView

urlpatterns = [
    path('pesquisa/', FullTextSearchView.as_view(), name='pesquisa'),
]

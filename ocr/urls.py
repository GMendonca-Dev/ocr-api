from django.urls import path
from .views import SearchConteudo, SearchConteudo2

urlpatterns = [
    path('pesquisa/', SearchConteudo.as_view(), name='pesquisa'),
    path('pesquisafull/', SearchConteudo2.as_view(), name='pesquisafull'),
]

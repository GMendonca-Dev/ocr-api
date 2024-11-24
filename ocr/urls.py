from django.urls import path
from .views import SearchConteudo, SearchConteudo2, search

urlpatterns = [
    path('pesquisa/', SearchConteudo.as_view(), name='pesquisa'),
    path('pesquisafull/', SearchConteudo2.as_view(), name='pesquisafull'),
    path('search/', search, name='websearch'),  # Define a URL como '/search/'

]

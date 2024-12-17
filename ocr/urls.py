from django.urls import path
from . import views  # import SearchConteudo, SearchConteudo2, search

# urlpatterns = [
#     # path('pesquisa/', SearchConteudo.as_view(), name='pesquisa'),
#     # path('pesquisafull/', SearchConteudo2.as_view(), name='pesquisafull'),
#     # path('search/', search, name='websearch'),  # Define a URL como '/search/'

# ]


urlpatterns = [
    path('pesquisa/conteudo/', views.pesquisa_conteudo, name='pesquisa_conteudo'),
    path('pesquisa/search-vector/', views.pesquisa_search_vector, name='pesquisa_search_vector'),
    path('pesquisa/conteudo-phraseto/', views.pesquisa_conteudo_phraseto, name='pesquisa_conteudo_phraseto'),
    path('pesquisa/combined/', views.pesquisa_combined, name='pesquisa_combined'),
]
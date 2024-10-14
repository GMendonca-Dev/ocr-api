from django.shortcuts import render
from django.views import View
from django.contrib.postgres.search import SearchQuery, SearchRank
from .models import DocumentosOcr


# class FullTextSearchView(View):
#     template_name = 'pesquisa.html'

#     def get(self, request):
#         query = request.GET.get('q', None)  # Recebe o termo de pesquisa do usuário
#         resultados = []

#         if query:
#             # Criar um objeto SearchQuery com a linguagem portuguesa
#             search_query = SearchQuery(query, config='portuguese')

#             # Fazer a pesquisa utilizando o campo search_vector e ordenar por rank
#             resultados = DocumentosOcr.objects.annotate(
#                 rank=SearchRank('search_vector', search_query)
#             ).filter(search_vector=search_query).order_by('-rank')

#         context = {
#             'query': query,
#             'resultados': resultados
#         }
#         return render(request, self.template_name, context)



# from django.shortcuts import render
# from django.views import View
# from django.contrib.postgres.search import SearchQuery, SearchRank
# from .models import DocumentosOcr


# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.shortcuts import render
# from django.contrib.postgres.search import SearchQuery, SearchRank
# from .models import DocumentosOcr


# class FullTextSearchView(View):
#     template_name = 'pesquisa.html'
#     paginate_by = 10  # Define o número de resultados por página

#     def get(self, request):
#         query = request.GET.get('q', None)
#         resultados = DocumentosOcr.objects.none()  # Queryset vazio padrão

#         if query:
#             if query.startswith('"') and query.endswith('"'):
#                 search_query = SearchQuery(query.strip('"'), search_type='phrase', config='portuguese')
#             else:
#                 search_query = SearchQuery(query, config='portuguese')

#             # Fazer a pesquisa utilizando o campo search_vector e ordenar por rank
#             resultados = DocumentosOcr.objects.annotate(
#                 rank=SearchRank('search_vector', search_query)
#             ).filter(search_vector=search_query).order_by('-rank')

#         # Paginação
#         paginator = Paginator(resultados, self.paginate_by)
#         page = request.GET.get('page', 1)

#         try:
#             paginated_resultados = paginator.page(page)
#         except PageNotAnInteger:
#             paginated_resultados = paginator.page(1)
#         except EmptyPage:
#             paginated_resultados = paginator.page(paginator.num_pages)

#         context = {
#             'query': query,
#             'resultados': paginated_resultados,
#         }
#         return render(request, self.template_name, context)


# from django.shortcuts import render
# from django.views import View
# from django.contrib.postgres.search import SearchQuery, SearchRank, TrigramSimilarity
# from .models import DocumentosOcr
# from django.db.models import Q


# class FullTextSearchView(View):
#     template_name = 'pesquisa.html'

#     def get(self, request):
#         query = request.GET.get('q', None)  # Recebe o termo de pesquisa do usuário
#         resultados = []

#         if query:
#             # Verifica se o termo de pesquisa está entre aspas
#             if query.startswith('"') and query.endswith('"'):
#                 # Retira as aspas e cria uma busca por frase exata
#                 search_query = SearchQuery(query.strip('"'), search_type='phrase', config='portuguese')
#             else:
#                 # Busca normal por palavras individuais
#                 search_query = SearchQuery(query, config='portuguese')

#             # Fazer a pesquisa utilizando o campo search_vector e ordenar por rank
#             resultados = DocumentosOcr.objects.annotate(
#                 search_rank=SearchRank('search_vector', search_query),
#                 trigram_sim=TrigramSimilarity('conteudo', query)  # Use o campo de texto original
#             ).filter(
#                 Q(search_vector=search_query) | Q(trigram_sim__gt=0.1)
#             ).order_by('-search_rank', '-trigram_sim')

#         context = {
#             'query': query,
#             'resultados': resultados
#         }
#         return render(request, self.template_name, context)

# from django.shortcuts import render
# from django.views import View
# from .models import DocumentosOcr
# from django.db.models import Q


# class FullTextSearchView(View):
#     template_name = 'pesquisa.html'

#     def get(self, request):
#         query = request.GET.get('q', None)  # Recebe o termo de pesquisa do usuário
#         resultados = []

#         if query:
#             # Fazer a pesquisa utilizando __icontains para busca insensível a maiúsculas e minúsculas
#             resultados = DocumentosOcr.objects.filter(
#                 Q(conteudo__icontains=query) |
#                 Q(nome_original__icontains=query) |
#                 Q(email_usuario__icontains=query)
#             ).order_by('nome_original')

#         context = {
#             'query': query,
#             'resultados': resultados
#         }
#         return render(request, self.template_name, context)


from django.views.generic import ListView
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.db.models import Q
from .models import DocumentosOcr
import re

def build_tsquery(query_string):
    # Remove caracteres especiais
    query_string = re.sub(r'[^\w\s]', '', query_string)
    words = query_string.split()
    tsquery = ' & '.join([f"{word}:*" for word in words])
    return tsquery

class FullTextSearchView(ListView):
    model = DocumentosOcr
    template_name = 'pesquisa.html'
    context_object_name = 'resultados'
    paginate_by = 20  # Número de resultados por página

    def get_queryset(self):
        query = self.request.GET.get('q', '').strip()
        if query:
            tsquery = build_tsquery(query)
            search_query = SearchQuery(tsquery, search_type='raw', config='portuguese')
            search_vector = SearchVector('conteudo', config='portuguese')

            fts_results = DocumentosOcr.objects.annotate(
                rank=SearchRank(search_vector, search_query)
            ).filter(rank__gte=0.1).order_by('-rank')

            if fts_results.exists():
                return fts_results
            else:
                return DocumentosOcr.objects.filter(conteudo__icontains=query)
        else:
            return DocumentosOcr.objects.none()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context

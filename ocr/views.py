
# from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
# from django.shortcuts import render
# from .models import DocumentosOcr
# from django.views.generic import ListView

# class SearchConteudo(ListView):
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
from django.views import View
# from django.contrib.postgres.search import SearchQuery, SearchRank
# from .models import DocumentosOcr


# from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# from django.shortcuts import render
# from django.contrib.postgres.search import SearchQuery, SearchRank
# from .models import DocumentosOcr
# from django.views.generic import ListView


# class SearchConteudo(ListView):
#     template_name = 'pesquisa.html'
#     paginate_by = 200  # Define o número de resultados por página

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


from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.postgres.search import SearchQuery, SearchRank, TrigramSimilarity
from .models import DocumentosOcr
from django.db.models import Q


class SearchConteudo2(ListView):
    template_name = 'pesquisafull.html'

    def get(self, request):
        query = request.GET.get('q', None)  # Recebe o termo de pesquisa do usuário
        resultados = []

        if query:
            # Verifica se o termo de pesquisa está entre aspas
            if query.startswith('"') and query.endswith('"'):
                # Retira as aspas e cria uma busca por frase exata
                search_query = SearchQuery(query.strip('"'), search_type='phrase', config='portuguese')
            else:
                # Busca normal por palavras individuais
                search_query = SearchQuery(query, config='portuguese')

            # Fazer a pesquisa utilizando o campo search_vector e ordenar por rank
            resultados = DocumentosOcr.objects.annotate(
                search_rank=SearchRank('search_vector', search_query),
                trigram_sim=TrigramSimilarity('conteudo', query)  # Use o campo de texto original
            ).filter(
                Q(search_vector=search_query) | Q(trigram_sim__gt=0.1)
            ).order_by('-search_rank', '-trigram_sim')

        context = {
            'query': query,
            'resultados': resultados
        }
        return render(request, self.template_name, context)

# from django.shortcuts import render
# from django.views import View
# from .models import DocumentosOcr
# from django.db.models import Q


class SearchConteudo(View):
    template_name = 'pesquisa.html'

    def get(self, request):
        query = request.GET.get('q', None)  # Recebe o termo de pesquisa do usuário
        resultados = []

        if query:
            # Fazer a pesquisa utilizando __icontains para busca insensível a maiúsculas e minúsculas
            resultados = DocumentosOcr.objects.filter(
                Q(conteudo__icontains=query) |
                Q(nome_original__icontains=query) 
                #Q(email_usuario__icontains=query)
            ).order_by('nome_original')

        context = {
            'query': query,
            'resultados': resultados
        }
        return render(request, self.template_name, context)


# class SearchConteudo2(ListView):
#     model = DocumentosOcr
#     template_name = 'pesquisafull.html'
#     context_object_name = 'resultados'
#     paginate_by = 200  # Número de resultados por página

#     def get_queryset(self):
#         term = self.request.GET.get('q')
#         if term:
#             query = SearchQuery(term, config='portuguese')
#             qs = DocumentosOcr.objects.annotate(
#                 rank=SearchRank('search_vector', query)
#             ).filter(
#                 search_vector=query
#             ).order_by('-rank')
#         else:
#             qs = DocumentosOcr.objects.order_by('-id')
#         return qs

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['query'] = self.request.GET.get('q') or ''
#         return context


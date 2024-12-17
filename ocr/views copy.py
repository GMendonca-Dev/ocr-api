from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.postgres.search import SearchQuery, SearchRank, TrigramSimilarity, SearchVector
from .models import DocumentosOcr
from django.db.models import Q

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



# class SearchConteudo2(ListView):
#     template_name = 'pesquisafull.html'

#     def get(self, request):
#         query = request.GET.get('q', None)  # Recebe o termo de pesquisa do usuário
#         resultados = []

#         if query:
#             # Remove espaços extras da query
#             query = query.strip()

#             # Verifica se o termo de pesquisa está entre aspas para busca por frase exata
#             if query.startswith('"') and query.endswith('"'):
#                 # Remove as aspas para a busca
#                 search_query = SearchQuery(query.strip('"'), search_type='phrase', config='portuguese')
#             else:
#                 # Busca por palavras individuais
#                 search_query = SearchQuery(query, config='portuguese')

#             # Adiciona um vetor de busca incluindo `unaccent` para evitar problemas de acentuação
#             search_vector = SearchVector('conteudo', config='portuguese')  # Use unaccent se necessário no índice

#             # Fazer a pesquisa utilizando o campo search_vector e trigram similarity
#             resultados = DocumentosOcr.objects.annotate(
#                 searchVector=search_vector,
#                 search_rank=SearchRank(search_vector, search_query),
#                 trigram_sim=TrigramSimilarity('conteudo', query)
#             ).filter(
#                 Q(search_vector=search_query) | Q(trigram_sim__gt=0.05)
#             ).order_by('-search_rank', '-trigram_sim')

#         context = {
#             'query': query,
#             'resultados': resultados
#         }
#         return render(request, self.template_name, context)


class SearchConteudo2(ListView):
    template_name = 'pesquisafull.html'

    def get(self, request):
        query = request.GET.get('q', None)  # Recebe o termo de pesquisa do usuário
        resultados = []

        if query:
            # Remove espaços extras da query
            query = query.strip()

            # Configura a busca FTS sem stemming (config='simple')
            search_query = SearchQuery(query, config='simple', search_type='plain')

            # Anotações para FTS, similaridade trigram e busca simples
            resultados = DocumentosOcr.objects.annotate(
                search_vector_annotated=SearchVector('conteudo', config='simple'),  # SearchVector sem stemming
                search_rank=SearchRank('search_vector_annotated', search_query),    # Rankeamento por FTS
                trigram_sim=TrigramSimilarity('conteudo', query)                   # Similaridade trigram
            ).filter(
                Q(search_vector_annotated=search_query) |  # Busca FTS
                Q(conteudo__icontains=query) |            # Busca simples (substring)
                Q(trigram_sim__gt=0.2)                   # Busca aproximada com trigram
            ).order_by('-search_rank', '-trigram_sim')      # Ordena por relevância

        context = {
            'query': query,
            'resultados': resultados
        }
        return render(request, self.template_name, context)





# class SearchConteudo2(ListView):
#     template_name = 'pesquisafull.html'

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
#                 Q(search_vector=search_query) | Q(trigram_sim__gt=0.05)
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


class SearchConteudo(View):
    template_name = 'pesquisa.html'

    def get(self, request):
        query = request.GET.get('q', None)  # Recebe o termo de pesquisa do usuário
        resultados = []

        if query:
            # Fazer a pesquisa utilizando __icontains para busca insensível a maiúsculas e minúsculas
            resultados = DocumentosOcr.objects.filter(
                Q(conteudo__icontains=query))  # |
                #Q(nome_original__icontains=query) 
                #Q(email_usuario__icontains=query)
        #    ) #.order_by('nome_original')

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


#  Teste HTMX

from django.contrib.postgres.search import SearchQuery, SearchRank
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def search(request):
    documentos = []
    q = ""

    if request.method == "POST":
        q = request.POST.get("q", "").strip()  # Captura o termo de pesquisa
        if q:
            # Busca com Full-Text Search usando SearchQuery
            search_query = SearchQuery(q, search_type="websearch")
            documentos = DocumentosOcr.objects.annotate(
                search_rank=SearchRank('search_vector', search_query)
            ).filter(search_vector=search_query).order_by('-search_rank')

    # Verifica se é uma requisição HTMX
    if request.headers.get('HX-Request'):
        return render(request, "partials/_documentos_list.html", {"documentos": documentos})

    # Para requisições normais, renderiza o layout completo
    return render(request, "pesquisaHTMX.html", {"documentos": documentos, "query": q})


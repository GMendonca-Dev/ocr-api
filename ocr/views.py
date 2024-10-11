# from django.shortcuts import render
# from django.views import View
# from django.contrib.postgres.search import SearchQuery, SearchRank
# from .models import DocumentosOcr


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



from django.shortcuts import render
from django.views import View
from django.contrib.postgres.search import SearchQuery, SearchRank
from .models import DocumentosOcr


class FullTextSearchView(View):
    template_name = 'pesquisa.html'

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
                rank=SearchRank('search_vector', search_query)
            ).filter(search_vector=search_query).order_by('-rank')

        context = {
            'query': query,
            'resultados': resultados
        }
        return render(request, self.template_name, context)

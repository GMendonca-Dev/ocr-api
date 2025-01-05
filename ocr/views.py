from datetime import datetime
from django.shortcuts import render
from django.db.models import Q
from django.contrib.postgres.search import SearchQuery, SearchVector
from .models import DocumentosOcr  # Substitua pelo nome correto do modelo



def pesquisa_conteudo(request):
    """
    Função que realiza a pesquisa de conteúdo com base na consulta e tipo especificado.
    Recebe a consulta e o tipo de pesquisa como parâmetros.
    """
    query = request.GET.get('q', '')
    tipo = request.GET.get('tipo', 'simples')  # 'simples' por padrão
    resultados = []
    duration = 0  # Inicializa a duração como zero

    if query:
        start_time = datetime.now()  # Início da contagem do tempo
        #print(f"Início da pesquisa: {start_time}")

        if tipo == 'simples':
            resultados = list(DocumentosOcr.objects.filter(conteudo__icontains=query))
        elif tipo == 'composto':
            # Aqui você pode implementar a lógica para tratar palavras compostas
            resultados = list(DocumentosOcr.objects.filter(conteudo__icontains=query))

        end_time = datetime.now()  # Fim da contagem do tempo
        duration = (end_time - start_time).total_seconds()  # Duração da pesquisa em segundos
        # print(f"Fim da pesquisa: {end_time}")
        # print(f"Tempo de pesquisa: {duration:.4f} segundos, finalizado em {end_time}")

    return render(request, 'pesquisa.html', {
        'query': query,        # Mantém o valor da pesquisa
        'resultados': resultados,
        'tipo': tipo,
        'duration': duration,
        'termo_pesquisado': query
    })


# def pesquisa_search_vector(request):
#     """
#     Função que realiza uma pesquisa utilizando vetores de busca.
#     Recebe a consulta e o tipo de pesquisa como parâmetros.
#     """
#     query = request.GET.get('q', '')
#     tipo = request.GET.get('tipo', 'simples')  # Simples por padrão
#     resultados = []
#     duration = 0

#     if query:
#         start_time = datetime.now()  # Início da contagem do tempo
#         # print(start_time)
#         # print(datetime.now())
#         if tipo == 'simples':
#             search_query = SearchQuery(query, config='simple')
#             resultados = list(DocumentosOcr.objects.filter(search_vector=search_query))        
#         elif tipo == 'composto':
#             search_query = SearchQuery(query, search_type='phrase', config='simple')
#             resultados = list(DocumentosOcr.objects.filter(search_vector=search_query))
#         duration = (datetime.now() - start_time).total_seconds() # Duração da pesquisa
      
#     return render(request, 'pesquisafull.html', {
#         'query': '',  # Limpa o campo de pesquisa
#         'resultados': resultados,
#         'tipo': tipo,
#         'duration': duration,
#         'termo_pesquisado': query

# # ##### FUNCIONANDO ###########
# def pesquisa_search_vector(request):
#     """
#     Função que realiza uma pesquisa utilizando vetores de busca,
#     com a possibilidade de filtrar por pasta.
#     """
#     query = request.GET.get('q', '')
#     pasta = request.GET.get('pasta', '')  # Filtro pela pasta
#     tipo = request.GET.get('tipo', 'simples')  # Simples por padrão
#     resultados = []
#     duration = 0

#     # Obter as opções de pastas distintas do banco de dados
#     opcoes_pasta = DocumentosOcr.objects.values_list('pasta', flat=True).distinct().order_by('pasta')

#     if query:
#         start_time = datetime.now()  # Início da contagem do tempo
#         search_query = None

#         # Configuração da busca por tipo
#         if tipo == 'simples':
#             search_query = SearchQuery(query, config='simple')
#         elif tipo == 'composto':
#             search_query = SearchQuery(query, search_type='phrase', config='simple')

#         # Adiciona o filtro de pasta, se fornecido
#         filtros = Q(search_vector=search_query)
#         if pasta:
#             filtros &= Q(pasta__icontains=pasta)

#         # Executa a pesquisa
#         resultados = list(DocumentosOcr.objects.filter(filtros).order_by('-id'))
#         duration = (datetime.now() - start_time).total_seconds()  # Duração da pesquisa

#     return render(request, 'pesquisafull.html', {
#         'query': query,
#         'resultados': resultados,
#         'tipo': tipo,
#         'pasta': pasta,
#         'opcoes_pasta': opcoes_pasta,  # Passa as opções de pasta para o template
#         'duration': duration,
#         'termo_pesquisado': query
#     })




def pesquisa_search_vector(request):
    """
    Função que realiza uma pesquisa utilizando vetores de busca,
    com a possibilidade de filtrar por pasta.
    """
    query = request.GET.get('q', '')
    pasta = request.GET.get('pasta', '')  # Filtro pela pasta
    tipo = request.GET.get('tipo', 'simples')  # Simples por padrão
    resultados = []
    duration = 0

    # Obter as opções de pastas distintas do banco de dados
    opcoes_pasta = DocumentosOcr.objects.values_list('pasta', flat=True).distinct().order_by('pasta')

    if query:
        start_time = datetime.now()  # Início da contagem do tempo

        # Configuração do tipo de busca
        if tipo == 'simples':
            search_query = SearchQuery(query, config='simple')
        elif tipo == 'composto':
            search_query = SearchQuery(query, search_type='phrase', config='simple')  # Frase exata

        # Adiciona o filtro de pasta (case-sensitive para alinhar ao SQL)
        filtros = Q(search_vector=search_query)
        if pasta:
            filtros &= Q(pasta=pasta)

        # Executa a pesquisa e ordena por id ascendente
        resultados = list(DocumentosOcr.objects.filter(filtros).order_by('id'))  # Ordem ASC
        duration = (datetime.now() - start_time).total_seconds()  # Duração da pesquisa

    return render(request, 'pesquisafull.html', {
        'query': query,
        'resultados': resultados,
        'tipo': tipo,
        'pasta': pasta,
        'opcoes_pasta': opcoes_pasta,  # Passa as opções de pasta para o template
        'duration': duration,
        'termo_pesquisado': query
    })


#     })


# def pesquisa_conteudo_phraseto(request):
#     """
#     Função que realiza uma pesquisa de conteúdo utilizando busca por frase e busca básica.
#     Recebe a consulta e o tipo de pesquisa como parâmetros.
#     """
#     query = request.GET.get('q', '')
#     tipo = request.GET.get('tipo', 'simples')  # Simples por padrão
#     resultados = []
#     duration = 0

#     if query:
#         start_time = datetime.now()  # Início da contagem do tempo
#         #print(start_time)
#         if tipo == 'frase':
#             search_query = SearchQuery(query, search_type='phrase', config='simple')
#             resultados = list(DocumentosOcr.objects.filter(Q(search_vector=search_query) | Q(conteudo__icontains=query)))
#         else:
#             resultados = list(DocumentosOcr.objects.filter(conteudo__icontains=query))
#         duration = (datetime.now() - start_time).total_seconds()# Duração da pesquisa

#     return render(request, 'pesquisa_conteudo_phraseto.html', {
#         'query': '',  # Limpa o campo de pesquisa
#         'resultados': resultados,
#         'tipo': tipo,
#         'duration': duration,
#         'termo_pesquisado': query
#     })


def pesquisa_conteudo_phraseto(request):
    """
    Função que realiza uma pesquisa de conteúdo utilizando busca por frase e busca básica,
    com a possibilidade de filtrar por pasta.
    """
    query = request.GET.get('q', '')
    pasta = request.GET.get('pasta', '')  # Filtro pela pasta
    tipo = request.GET.get('tipo', 'simples')  # Simples por padrão
    resultados = []
    duration = 0

    if query:
        start_time = datetime.now()  # Início da contagem do tempo
        search_query = None

        # Configuração da busca por tipo
        if tipo == 'frase':
            search_query = SearchQuery(query, search_type='phrase', config='simple')
            filtros = Q(search_vector=search_query) | Q(conteudo__icontains=query)
        else:
            filtros = Q(conteudo__icontains=query)

        # Adiciona o filtro de pasta, se fornecido
        if pasta:
            filtros &= Q(pasta__icontains=pasta)

        # Executa a pesquisa
        resultados = list(DocumentosOcr.objects.filter(filtros))
        duration = (datetime.now() - start_time).total_seconds()  # Duração da pesquisa

    return render(request, 'pesquisa_conteudo_phraseto.html', {
        'query': query,
        'resultados': resultados,
        'tipo': tipo,
        'pasta': pasta,
        'duration': duration,
        'termo_pesquisado': query
    })



# def pesquisa_combined(request):
#     """
#     Função que realiza uma pesquisa combinada utilizando busca por vetor e busca básica.
#     Recebe a consulta e o tipo de pesquisa como parâmetros.
#     """
#     query = request.GET.get('q', '')
#     tipo = request.GET.get('tipo', 'simples')  # Simples por padrão
#     resultados = []
#     duration = 0

#     if query:
#         start_time = datetime.now()  # Início da contagem do tempo
#         #print(start_time)
#         if tipo == 'simples':
#             search_query = SearchQuery(query, config='simple')
#         elif tipo == 'frase':
#             search_query = SearchQuery(query, search_type='phrase', config='simple')

#         resultados = list(DocumentosOcr.objects.filter(
#             Q(search_vector=search_query) |
#             Q(conteudo__icontains=query)  # Caso queira incluir busca básica
#         ))
#         duration = (datetime.now() - start_time).total_seconds()# Duração da pesquisa

#     return render(request, 'pesquisa_combined.html', {
#         'query': '',  # Limpa o campo de pesquisa
#         'resultados': resultados,
#         'tipo': tipo,
#         'duration': duration,
#         'termo_pesquisado': query
#     })


def pesquisa_combined(request):
    """
    Função que realiza uma pesquisa combinada utilizando busca por vetor e busca básica,
    com a possibilidade de filtrar por pasta.
    """
    query = request.GET.get('q', '')  # Termo de busca
    pasta = request.GET.get('pasta', '')  # Filtro pela pasta
    tipo = request.GET.get('tipo', 'simples')  # Tipo de pesquisa (simples por padrão)
    resultados = []
    duration = 0

    if query:
        start_time = datetime.now()  # Início da contagem do tempo
        search_query = None

        # Configuração da busca por tipo
        if tipo == 'simples':
            search_query = SearchQuery(query, config='simple')
        elif tipo == 'frase':
            search_query = SearchQuery(query, search_type='phrase', config='simple')

        # Construção da consulta
        filtros = Q(search_vector=search_query) | Q(conteudo__icontains=query)
        if pasta:
            filtros &= Q(pasta__icontains=pasta)  # Adiciona o filtro pela pasta

        # Realiza a pesquisa
        resultados = list(DocumentosOcr.objects.filter(filtros))
        duration = (datetime.now() - start_time).total_seconds()  # Duração da pesquisa

    return render(request, 'pesquisa_combined.html', {
        'query': query,
        'resultados': resultados,
        'tipo': tipo,
        'pasta': pasta,
        'duration': duration,
        'termo_pesquisado': query
    })

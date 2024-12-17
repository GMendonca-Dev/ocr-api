from datetime import datetime
from django.shortcuts import render
from django.db.models import Q
from django.contrib.postgres.search import SearchQuery, SearchVector
from .models import DocumentosOcr  # Substitua pelo nome correto do modelo


# def pesquisa_conteudo(request):
#     """
#     Função que realiza a pesquisa de conteúdo com base na consulta e tipo especificado.
#     Recebe a consulta e o tipo de pesquisa como parâmetros.
#     """
#     query = request.GET.get('q', '')
#     tipo = request.GET.get('tipo', 'simples')  # Simples por padrão
#     resultados = []
#     duration = 0

#     if query:
#         start_time = time.time() # Início da contagem do tempo
#         print(start_time)
#         if tipo == 'simples':
#             resultados = DocumentosOcr.objects.filter(conteudo__icontains=query)
#         elif tipo == 'composto':
#             # Aqui você pode implementar a lógica para tratar palavras compostas
#             resultados = DocumentosOcr.objects.filter(conteudo__icontains=query)
#         duration = time.time() - start_time  # Duração da pesquisa
#         print(f"Tempo de pesquisa: {duration:.4f} segundos")

#     return render(request, 'pesquisa.html', {
#         'query': '',  # Limpa o campo de pesquisa
#         'resultados': resultados,
#         'tipo': tipo,
#         'duration': duration,
#         'termo_pesquisado': query
#     })


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


def pesquisa_search_vector(request):
    """
    Função que realiza uma pesquisa utilizando vetores de busca.
    Recebe a consulta e o tipo de pesquisa como parâmetros.
    """
    query = request.GET.get('q', '')
    tipo = request.GET.get('tipo', 'simples')  # Simples por padrão
    resultados = []
    duration = 0

    if query:
        start_time = datetime.now()  # Início da contagem do tempo
        # print(start_time)
        # print(datetime.now())
        if tipo == 'simples':
            search_query = SearchQuery(query, config='simple')
            resultados = list(DocumentosOcr.objects.filter(search_vector=search_query))        
        elif tipo == 'composto':
            search_query = SearchQuery(query, search_type='phrase', config='simple')
            resultados = list(DocumentosOcr.objects.filter(search_vector=search_query))
        duration = (datetime.now() - start_time).total_seconds() # Duração da pesquisa
      
    return render(request, 'pesquisafull.html', {
        'query': '',  # Limpa o campo de pesquisa
        'resultados': resultados,
        'tipo': tipo,
        'duration': duration,
        'termo_pesquisado': query
    })


def pesquisa_conteudo_phraseto(request):
    """
    Função que realiza uma pesquisa de conteúdo utilizando busca por frase e busca básica.
    Recebe a consulta e o tipo de pesquisa como parâmetros.
    """
    query = request.GET.get('q', '')
    tipo = request.GET.get('tipo', 'simples')  # Simples por padrão
    resultados = []
    duration = 0

    if query:
        start_time = datetime.now()  # Início da contagem do tempo
        #print(start_time)
        if tipo == 'frase':
            search_query = SearchQuery(query, search_type='phrase', config='simple')
            resultados = list(DocumentosOcr.objects.filter(Q(search_vector=search_query) | Q(conteudo__icontains=query)))
        else:
            resultados = list(DocumentosOcr.objects.filter(conteudo__icontains=query))
        duration = (datetime.now() - start_time).total_seconds()# Duração da pesquisa

    return render(request, 'pesquisa_conteudo_phraseto.html', {
        'query': '',  # Limpa o campo de pesquisa
        'resultados': resultados,
        'tipo': tipo,
        'duration': duration,
        'termo_pesquisado': query
    })


def pesquisa_combined(request):
    """
    Função que realiza uma pesquisa combinada utilizando busca por vetor e busca básica.
    Recebe a consulta e o tipo de pesquisa como parâmetros.
    """
    query = request.GET.get('q', '')
    tipo = request.GET.get('tipo', 'simples')  # Simples por padrão
    resultados = []
    duration = 0

    if query:
        start_time = datetime.now()  # Início da contagem do tempo
        #print(start_time)
        if tipo == 'simples':
            search_query = SearchQuery(query, config='simple')
        elif tipo == 'frase':
            search_query = SearchQuery(query, search_type='phrase', config='simple')

        resultados = list(DocumentosOcr.objects.filter(
            Q(search_vector=search_query) |
            Q(conteudo__icontains=query)  # Caso queira incluir busca básica
        ))
        duration = (datetime.now() - start_time).total_seconds()# Duração da pesquisa

    return render(request, 'pesquisa_combined.html', {
        'query': '',  # Limpa o campo de pesquisa
        'resultados': resultados,
        'tipo': tipo,
        'duration': duration,
        'termo_pesquisado': query
    })
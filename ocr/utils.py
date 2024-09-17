from django.contrib.postgres.search import SearchVector


def indexar_texto(documento):
    documento.search_vector = SearchVector('texto_extraido', 'titulo')
    documento.save()

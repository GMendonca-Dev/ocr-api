from django.db import models
from django.contrib.postgres.search import SearchVectorField, SearchVector, SearchRank, SearchQuery
from django.contrib.postgres.indexes import GinIndex
from django.urls import reverse
from django.db.models.signals import pre_save
from django.dispatch import receiver


class DocumentosOcr(models.Model):
    # id = models.BigAutoField(auto_created=True, primary_key=True, serialize=True, verbose_name='ID')
    id_documento = models.CharField(max_length=18)
    email_usuario = models.CharField(max_length=50, null=True, blank=True, verbose_name="Usuario")
    num_op = models.CharField(max_length=10, null=True, blank=True, verbose_name="Num")
    ano_op = models.CharField(max_length=6, null=True, blank=True, verbose_name="Op")
    nome_original = models.CharField(max_length=255, null=True, blank=True, verbose_name="Nome")
    arquivo = models.CharField(max_length=255, null=True, blank=True, verbose_name="Arquivo")
    extensao_arquivo = models.CharField(max_length=10, null=True, blank=True, verbose_name="Extensão")
    pasta = models.CharField(max_length=150, null=True, blank=True, verbose_name="Pasta")
    caminho = models.TextField(null=True, blank=True, verbose_name="Caminho")
    numero_pagina = models.IntegerField(null=True, blank=True, verbose_name="Página")
    conteudo = models.TextField(blank=True, null=True, verbose_name="Conteúdo")
    data_leitura = models.DateTimeField(auto_now_add=True, verbose_name="Leitura")
  
    # Campo para armazenar o vetor de busca de texto completo
    #search_vector = SearchVectorField(null=True, blank=True)

    # @classmethod
    # def search(cls, query):
    #     search_query = SearchQuery(query)
    #     return cls.objects.annotate(
    #         rank=SearchRank('search_vector', search_query)
    #     ).filter(search_vector=search_query).order_by('-rank')
    
    class Meta:
        verbose_name = "OCR Documentos"
        verbose_name_plural = "OCR Documentos"
        constraints = [
            models.UniqueConstraint(fields=['id_documento', 'nome_original'], name='unique_id_documento_nome')
        ]

        # indexes = [
        #     GinIndex(fields=['search_vector']),
        # ]

    def __str__(self):
        return self.nome_original
    
    # Indexa o texto extraído do documento
    # def indexar_texto(documento):
    #     documento.search_vector = SearchVector('conteudo', 'nome_original')
    #     documento.save()

    # @classmethod
    # def indexar_texto(cls, queryset):
    #     queryset.update(search_vector=SearchVector(F('conteudo'), F('nome_original'), config='portuguese'))


class DocumentosOcrErros(models.Model):
    # id = models.BigAutoField(auto_created=True, primary_key=True, serialize=True, verbose_name='ID')
    id_documento = models.CharField(max_length=18, verbose_name="Id")
    email_usuario = models.CharField(max_length=50, null=True, blank=True, default="N/A", verbose_name="Usuário")
    num_op = models.CharField(max_length=10, null=True, blank=True, default="N/A", verbose_name="Op")
    ano_op = models.CharField(max_length=6, null=True, blank=True, default="N/A", verbose_name="Ano")
    nome_original = models.CharField(max_length=255, null=True, blank=True, default="N/A")
    arquivo = models.CharField(max_length=255, null=True, blank=True, default="N/A", verbose_name="Arquivo")
    extensao_arquivo = models.CharField(max_length=10, null=True, blank=True, default="N/A")
    pasta = models.CharField(max_length=150, null=True, blank=True, default="N/A")
    caminho = models.TextField(null=True, blank=True, default="N/A")
    numero_pagina = models.IntegerField(null=True, blank=True, default="N/A", verbose_name="Pasta")
    erro = models.TextField(blank=True, null=True, default="N/A", verbose_name="Erro")
    data_insercao = models.DateTimeField(auto_now_add=True, verbose_name="Inserção")

    class Meta:
        verbose_name = "Erros OCR Documentos"
        verbose_name_plural = "Erros OCR Documentos"
        constraints = [
            models.UniqueConstraint(fields=['id_documento', 'nome_original'], name='erros_unique_id_documento_nome')
        ]

    def __str__(self):
        return self.nome_original if self.nome_original else "N/A"

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})


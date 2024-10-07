from django.db import models
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.search import SearchVector
from django.db.models import F


class DocumentosOcr(models.Model):
    # id = models.BigAutoField(auto_created=True, primary_key=True, serialize=True, verbose_name='ID')
    id_documento = models.CharField(max_length=18)
    nome_original = models.CharField(max_length=255, null=True, blank=True)
    arquivo = models.CharField(max_length=255, null=True, blank=True)
    extensao_arquivo = models.CharField(max_length=10, null=True, blank=True)
    pasta = models.CharField(max_length=150, null=True, blank=True)
    caminho = models.TextField(null=True, blank=True)
    numero_pagina = models.IntegerField(null=True, blank=True)
    conteudo = models.TextField(blank=True, null=True)
    data_leitura = models.DateTimeField(auto_now_add=True)
    #docs_extraidos = models.FilePathField(path='/docs_extraidos')
    search_vector = SearchVectorField(null=True)
    
    class Meta:
        verbose_name = "OCR Documentos"
        verbose_name_plural = "OCR Documentos"
        constraints = [
            models.UniqueConstraint(fields=['id_documento', 'nome_original'], name='unique_id_documento_nome')
        ]

    def __str__(self):
        return self.nome_original
    
    # Indexa o texto extraído do documento
    # def indexar_texto(documento):
    #     documento.search_vector = SearchVector('conteudo', 'nome_original')
    #     documento.save()

    @classmethod
    def indexar_texto(cls, queryset):
        queryset.update(search_vector=SearchVector(F('conteudo'), F('nome_original'), config='portuguese'))


class DocumentosOcrErros(models.Model):
    # id = models.BigAutoField(auto_created=True, primary_key=True, serialize=True, verbose_name='ID')
    id_documento = models.CharField(max_length=18)
    nome_original = models.CharField(max_length=255, null=True, blank=True)
    arquivo = models.CharField(max_length=255, null=True, blank=True)
    extensao_arquivo = models.CharField(max_length=10, null=True, blank=True)
    pasta = models.CharField(max_length=150, null=True, blank=True)
    caminho = models.TextField(null=True, blank=True)
    numero_pagina = models.IntegerField(null=True, blank=True)
    erro = models.TextField(blank=True, null=True)
    data_insercao = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Erros OCR Documentos"
        verbose_name_plural = "Erros OCR Documentos"
        constraints = [
            models.UniqueConstraint(fields=['id_documento', 'nome_original'], name='erros_unique_id_documento_nome')
        ]
        

    def __str__(self):
        return self.nome_original

    def get_absolute_url(self):
        return reverse("_detail", kwargs={"pk": self.pk})


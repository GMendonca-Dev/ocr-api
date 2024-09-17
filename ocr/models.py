from django.db import models
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.search import SearchVector


class Documento(models.Model):
    id_documento = models.CharField(max_length=100)
    titulo = models.CharField(max_length=255)
    caminho_arquivo = models.FilePathField(path='/path/to/save/documents')
    texto_extraido = models.TextField(blank=True, null=True)
    data_upload = models.DateTimeField(auto_now_add=True)
    search_vector = SearchVectorField(null=True)
    data_leitura = models.DateTimeField(null=True, blank=True)
    ocr = models.BooleanField(default=False)  # Flag que indica se o OCR foi realizado

    def __str__(self):
        return self.titulo
    
    # Indexa o texto extraído do documento
    def indexar_texto(documento):
        documento.search_vector = SearchVector('texto_extraido', 'titulo')
        documento.save()

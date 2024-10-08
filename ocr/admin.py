from django.contrib import admin
from . models import DocumentosOcr, DocumentosOcrErros


@admin.register(DocumentosOcrErros)
# class DocumentosOcrErrosAdmin(admin.ModelAdmin):
#     list_display = ('id_documento',)

#     def __str__(self):
#         # Lista de todos os campos que podem ser usados para representar o objeto
#         campos = [self.nome_original, self.id_documento, self.email_usuario, self.num_op, self.ano_op, 
#                   self.arquivo, self.extensao_arquivo, self.pasta, self.caminho, self.numero_pagina, self.erro]

#         # Verifica cada campo e retorna o primeiro valor que não seja None ou "[Null]"
#         for campo in campos:
#             if campo and campo != "[Null]":
#                 return str(campo)
        
#         # Se todos os campos forem None ou "[Null]", retorna uma string padrão
#         return "Informação indisponível"


@admin.register(DocumentosOcr)
class DocumentosOcrAdmin(admin.ModelAdmin):
    list_display = (
        "id_documento",
        "email_usuario",
        "num_op",
        "ano_op",
        "arquivo",
        "extensao_arquivo",
        "numero_pagina",
        "conteudo_t",  # Usando o método truncado
    )

    readonly_fields = ('id_documento', 'email_usuario', 'num_op', 'ano_op', 'nome_original', 'arquivo',
                       'extensao_arquivo', 'pasta', 'caminho', 'numero_pagina')

    list_filter = ('email_usuario', 'num_op', 'ano_op', 'extensao_arquivo',)
    list_per_page = 8  # Número de registros por página

    search_fields = (
        "id_documento",
        "email_usuario",
        "num_op",
        "ano_op",
        "nome_original",
        "arquivo",
        "conteudo_t",
    )

    def conteudo_t(self, obj):
        max_length = 50  # Número de caracteres a serem exibidos
        print(f"Debug: Valor do campo conteudo - {obj.conteudo}")  # Linha de depuração
        if obj.conteudo and len(obj.conteudo) > max_length:
            return f"{obj.conteudo[:max_length]}..."
        return obj.conteudo or "N/A"  # Exibe "N/A" se conteudo for None ou vazio



# @admin.register(DocumentosOcr)
# class DocumentosOcrAdmin(admin.ModelAdmin):
#     list_display = (
#         "id_documento",
#         "email_usuario",
#         "num_op",
#         "ano_op",
#         "arquivo",
#         "extensao_arquivo",
#         "numero_pagina",
#         "conteudo_truncado",  # Usando o método truncado
       
#     )
#     readonly_fields = ('id_documento', 'email_usuario', 'num_op', 'ano_op', 'nome_original', 'arquivo',
#                        'extensao_arquivo', 'pasta', 'caminho', 'numero_pagina', 'conteudo',)
#     list_filter = ('email_usuario', 'num_op', 'ano_op', 'extensao_arquivo', )
#     list_per_page = 8  # Número de registros por página

#     search_fields = (
#         "id_documento",
#         "email_usuario",
#         "num_op",
#         "ano_op",
#         "nome_original",
#         "arquivo",
#         "conteudo",
#     )

#     def conteudo_truncado(self, obj):
#         max_length = 50  # Número de caracteres a serem exibidos
#         if len(obj.conteudo) > max_length:
#             return f"{obj.conteudo[:max_length]}..."
#         return obj.conteudo

#     conteudo_truncado.short_description = "Conteúdo"  # Nome que aparecerá no cabeçalho da coluna

#     # def email(self, obj):
#     #     return obj.email

#     # def nome_original(self, obj):
#     #     return obj.nome_original

#     # def ano_op(self, obj):
#     #     return obj.ano_op

#     # def num_op(self, obj):
#     #     return obj.num_op

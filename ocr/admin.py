from django.contrib import admin
from . models import DocumentosOcr, DocumentosOcrErros
from django.contrib.postgres.search import SearchQuery, SearchRank
import logging
from django.db.models import F, Q

logger = logging.getLogger(__name__)


class DocumentosOcrAdmin(admin.ModelAdmin):
    # Campos pelos quais queremos aplicar os filtros
    list_filter = ('email_usuario', 'num_op', 'ano_op', 'arquivo', 'numero_pagina', 'data_leitura')
    
    # Campos a serem exibidos na tabela do Django Admin
    list_display = (
        'id_documento',
        'email_usuario',
        'num_op',
        'ano_op',
        'arquivo',
        'numero_pagina',
        'conteudo_resumido',
        'data_formatada'
    )
    # search_fields = (
        
    #     "email_usuario",
    #     "num_op",
    #     "ano_op",
    #     "nome_original",
    #     "arquivo",
    #     "conteudo",
    # )

    # Todos os campos como leitura
    readonly_fields = [field.name for field in DocumentosOcr._meta.fields]

    # Definir paginação para 20 itens por página (ajuste conforme necessário)
    list_per_page = 10

    def conteudo_resumido(self, obj):
        return obj.conteudo[:50] + ('...' if len(obj.conteudo) > 50 else '')

    conteudo_resumido.short_description = 'Conteúdo'

    # # Exemplo de Personalização dos campos com cabeçalhos amigáveis
    # def id_documento_custom(self, obj):
    #     return obj.id_documento
    # id_documento_custom.short_description = 'Id '  # Nome personalizado

    # def data_formatada(self, obj):
    #     # Formata a data no formato dd/mm/aaaa às hh:mm
    #     # return obj.data_insercao.strftime("%d/%m/%Y às %H:%M")
    #     return obj.data_leitura.strftime("%d/%m/%Y")
    
    def data_formatada(self, obj):
        # Formata a data no formato dd/mm/aaaa
        return obj.data_leitura.strftime("%d/%m/%Y") if obj.data_leitura else ''

    data_formatada.short_description = "Leitura"

    data_formatada.short_description = "Leitura"  # Nome que aparecerá no cabeçalho da coluna

    # Sobrescreve o método de busca no Django Admin
    
    # O campo de busca é o campo 'search_vector' do modelo DocumentosOcr
    search_fields = ['conteudo']  # O campo onde o texto foi armazenado


admin.site.register(DocumentosOcr, DocumentosOcrAdmin)


class DocumentosOcrErrosAdmin(admin.ModelAdmin):
    # Campos de filtro
    list_filter = ("id_documento",'num_op', 'ano_op', 'email_usuario', 'arquivo', 'erro')
    
    # Campos a serem exibidos no Django Admin
    # list_display = ("id_documento_custom", 'email_usuario_custom','num_op_custom', 'ano_op_custom', 'email_usuario_custom', 'arquivo_custom', 'erro', "data_formatada")
    list_display = ("id_documento", 'email_usuario','num_op', 'ano_op', 'email_usuario', 'arquivo', 'erro', "data_formatada")
    
    # Todos os campos como leitura
    readonly_fields = [field.name for field in DocumentosOcrErros._meta.fields]
    search_fields = (
            
            "email_usuario",
            "num_op",
            "ano_op",
            "nome_original",
            "arquivo",
            "erro",
        )
    # Define a paginação
    list_per_page = 10

    # def arquivo_custom(self, obj):
    #     return obj.arquivo
    # arquivo_custom.short_description = 'Nome do Arquivo'  # Nome personalizado

    def numero_pagina_custom(self, obj):
        return obj.numero_pagina
    numero_pagina_custom.short_description = 'Página'  # Nome personalizado

    # def data_insercao_custom(self, obj):
    #     return obj.data_insercao
    # data_insercao_custom.short_description = 'Data de Leitura'  # Nome personalizado

    def data_formatada(self, obj):
        # Formata a data no formato dd/mm/aaaa às hh:mm
        # return obj.data_insercao.strftime("%d/%m/%Y às %H:%M")
        return obj.data_insercao.strftime("%d/%m/%Y")

    data_formatada.short_description = "Inserção"  # Nome que aparecerá no cabeçalho da coluna


admin.site.register(DocumentosOcrErros, DocumentosOcrErrosAdmin)
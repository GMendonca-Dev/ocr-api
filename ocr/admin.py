from django.contrib import admin
from . models import DocumentosOcr, DocumentosOcrErros


class DocumentosOcrAdmin(admin.ModelAdmin):
    # Campos pelos quais queremos aplicar os filtros
    list_filter = ('email_usuario', 'num_op', 'ano_op', 'arquivo', 'numero_pagina', 'data_leitura')
    
    # Campos a serem exibidos na tabela do Django Admin
    # list_display = ("id_documento", 'email_usuario', 'num_op', 'ano_op', 'arquivo', 'numero_pagina','conteudo_resumido', 'data_leitura')
    list_display = (
        'id_documento_custom',
        'email_usuario_custom',
        'num_op_custom',
        'ano_op_custom',  
        'arquivo_custom', 
        'numero_pagina_custom', 
        'conteudo_resumido', 
        'data_leitura_custom'
    )
    search_fields = (
        
        "email_usuario",
        "num_op",
        "ano_op",
        "nome_original",
        "arquivo",
        "conteudo",
    )
    # Todos os campos como leitura
    readonly_fields = [field.name for field in DocumentosOcr._meta.fields]

    # Definir paginação para 20 itens por página (ajuste conforme necessário)
    list_per_page = 10

    def conteudo_resumido(self, obj):
        return obj.conteudo[:50] + ('...' if len(obj.conteudo) > 50 else '')

    conteudo_resumido.short_description = 'Conteúdo'

        # Personalização dos campos com cabeçalhos amigáveis
    def id_documento_custom(self, obj):
        return obj.email_usuario
    id_documento_custom.short_description = 'Id do documento'  # Nome personalizado

    def email_usuario_custom(self, obj):
        return obj.email_usuario
    email_usuario_custom.short_description = 'Usuário (Email)'  # Nome personalizado

    def ano_op_custom(self, obj):
        return obj.ano_op
    ano_op_custom.short_description = 'Ano'  # Nome personalizado

    def num_op_custom(self, obj):
        return obj.num_op
    num_op_custom.short_description = 'Op'  # Nome personalizado

    def arquivo_custom(self, obj):
        return obj.arquivo
    arquivo_custom.short_description = 'Nome do Arquivo'  # Nome personalizado

    def numero_pagina_custom(self, obj):
        return obj.numero_pagina
    numero_pagina_custom.short_description = 'Página'  # Nome personalizado

    def data_leitura_custom(self, obj):
        return obj.data_leitura
    data_leitura_custom.short_description = 'Data de Leitura'  # Nome personalizado


admin.site.register(DocumentosOcr, DocumentosOcrAdmin)


class DocumentosOcrErrosAdmin(admin.ModelAdmin):
    # Campos pelos quais queremos aplicar os filtros
    list_filter = ("id_documento",'num_op', 'ano_op', 'email_usuario', 'arquivo', 'erro')
    
    # Campos a serem exibidos na tabela do Django Admin
    list_display = ("id_documento",'num_op', 'ano_op', 'email_usuario', 'arquivo', 'erro', "data_insercao")

    # Todos os campos como leitura
    readonly_fields = [field.name for field in DocumentosOcrErros._meta.fields]


admin.site.register(DocumentosOcrErros, DocumentosOcrErrosAdmin)
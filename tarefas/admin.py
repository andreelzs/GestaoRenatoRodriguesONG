from django.contrib import admin
from .models import Tarefa

@admin.register(Tarefa)
class TarefaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'status', 'prioridade', 'voluntario_responsavel', 'data_prevista_conclusao', 'data_criacao')
    search_fields = ('titulo', 'descricao', 'voluntario_responsavel__nome_completo')
    list_filter = ('status', 'prioridade', 'data_prevista_conclusao', 'data_criacao', 'voluntario_responsavel')
    readonly_fields = ('data_criacao', 'data_conclusao_efetiva')
    date_hierarchy = 'data_criacao'

    fieldsets = (
        (None, {
            'fields': ('titulo', 'descricao', 'status', 'prioridade')
        }),
        ('Responsáveis e Prazos', {
            'fields': ('voluntario_responsavel', 'atribuido_por', 'data_prevista_conclusao', 'data_conclusao_efetiva')
        }),
        ('Outras Informações', {
            'fields': ('observacoes', 'data_criacao'),
            'classes': ('collapse',)
        }),
    )

    # Para facilitar a seleção de voluntário e usuário, feito o uso de raw_id_fields
    raw_id_fields = ('voluntario_responsavel', 'atribuido_por')

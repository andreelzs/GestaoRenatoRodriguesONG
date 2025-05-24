from django.contrib import admin
from .models import Voluntario

@admin.register(Voluntario)
class VoluntarioAdmin(admin.ModelAdmin):
    list_display = ('nome_completo', 'cpf', 'telefone', 'ativo', 'data_cadastro')
    search_fields = ('nome_completo', 'cpf')
    list_filter = ('ativo', 'data_cadastro')
    readonly_fields = ('data_cadastro',) # Campos que não devem ser editáveis no admin
    
    fieldsets = (
        (None, {
            'fields': ('usuario', 'nome_completo', 'cpf', 'data_nascimento', 'ativo')
        }),
        ('Contato', {
            'fields': ('telefone', 'endereco', 'email_voluntario') # Supondo que queira adicionar um email específico para voluntário
        }),
        ('Detalhes da ONG', {
            'fields': ('areas_interesse', 'disponibilidade')
        }),
        ('Datas Importantes', {
            'fields': ('data_cadastro',),
            'classes': ('collapse',) # Para agrupar e poder esconder
        }),
    )
    
    # Se o modelo Voluntario não tiver 'email_voluntario', remova-o dos fieldsets
    # ou adicione o campo ao modelo. Por agora, vou remover para evitar erro.
    # Corrigindo fieldsets:
    fieldsets = (
        (None, {
            'fields': ('usuario', 'nome_completo', 'cpf', 'data_nascimento', 'ativo')
        }),
        ('Contato', {
            'fields': ('telefone', 'endereco') 
        }),
        ('Detalhes da ONG', {
            'fields': ('areas_interesse', 'disponibilidade')
        }),
        ('Datas Importantes', {
            'fields': ('data_cadastro',),
            'classes': ('collapse',) 
        }),
    )

    # Para facilitar a seleção do usuário, podemos usar raw_id_fields
    raw_id_fields = ('usuario',)

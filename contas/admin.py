from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

class UsuarioAdminPersonalizado(UserAdmin): # Renomeado
    # Adicione campos personalizados ao list_display, fieldsets, etc., se necessário
    # Por exemplo, para mostrar 'tipo_usuario' na lista de usuários:
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'tipo_usuario')
    
    # Para adicionar 'tipo_usuario' aos fieldsets (para edição):
    # Copie os fieldsets padrão de UserAdmin e adicione o seu campo.
    # Os fieldsets padrão podem ser encontrados na documentação do Django ou no código fonte.
    # Aqui está um exemplo simplificado adicionando ao fieldset 'Personal info':
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {'fields': ('tipo_usuario',)}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Informações Adicionais', {'fields': ('tipo_usuario',)}),
    )

admin.site.register(Usuario, UsuarioAdminPersonalizado) # Atualizado aqui também

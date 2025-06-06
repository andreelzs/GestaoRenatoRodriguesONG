from django.shortcuts import render
from voluntarios.models import Voluntario # Importar o modelo Voluntario

def pagina_inicial(request):
    mensagem_boas_vindas_display = '' 
    
    if request.user.is_authenticated:
        nome_usuario = request.user.get_full_name()
        if not nome_usuario:
            nome_usuario = request.user.first_name
        
        # Tenta obter o nome do perfil Voluntario se os campos de User não estiverem preenchidos
        if not nome_usuario:
            try:
                voluntario_perfil = Voluntario.objects.get(usuario=request.user)
                if voluntario_perfil.nome_completo:
                    nome_usuario = voluntario_perfil.nome_completo
            except Voluntario.DoesNotExist:
                # Usuário não tem perfil de voluntário, ou nome_completo não preenchido
                pass # nome_usuario continua None ou com valor anterior

        if not nome_usuario:
            nome_usuario = request.user.username
            
        mensagem_boas_vindas_display = f'Bem vindo! Você está logado como: {nome_usuario}.'
    else:
        mensagem_boas_vindas_display = 'Faça login para acessar o sistema. Caso ainda não tenha uma conta, entre em contato com a administração da ONG'


    contexto = {
        'titulo_pagina': 'Bem-vindo ao Sistema de Gestão da ONG Renato Rodrigues!',
        'mensagem_boas_vindas': mensagem_boas_vindas_display 
    }
    return render(request, 'core/pagina_inicial.html', contexto)

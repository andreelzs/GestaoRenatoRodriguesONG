from django.shortcuts import render

def pagina_inicial(request):
    # Aqui você pode adicionar lógica para buscar dados para a página inicial, se necessário
    # Por exemplo, buscar notícias recentes, estatísticas, etc.
    contexto = {
        'titulo_pagina': 'Bem-vindo ao Sistema de Gestão da ONG!',
        'mensagem_boas_vindas': 'Este é o portal para gerenciar voluntários, beneficiários e tarefas.'
    }
    return render(request, 'core/pagina_inicial.html', contexto)

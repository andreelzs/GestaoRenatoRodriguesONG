from django.shortcuts import render

def pagina_inicial(request):
    contexto = {
        'titulo_pagina': 'Bem-vindo ao Sistema de Gestão da ONG!',
        'mensagem_boas_vindas': 'Este é o portal para gerenciar voluntários, beneficiários e tarefas.'
    }
    return render(request, 'core/pagina_inicial.html', contexto)

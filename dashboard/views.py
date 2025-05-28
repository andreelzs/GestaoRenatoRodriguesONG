from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from voluntarios.models import Voluntario
from beneficiarios.models import Beneficiario
from tarefas.models import Tarefa
import json # Para passar dados para o JavaScript

@login_required
def painel_principal(request):
    # Dados para os gráficos
    # 1. Contagem de tarefas por status
    tarefas_por_status = Tarefa.objects.values('status').annotate(total=Count('status')).order_by('status')
    status_labels = [dict(Tarefa.STATUS_TAREFA).get(item['status'], item['status']) for item in tarefas_por_status]
    status_data = [item['total'] for item in tarefas_por_status]

    # 2. Contagem de voluntários (ativos vs inativos - exemplo)
    #    Ou poderia ser por área de interesse, etc.
    voluntarios_ativos = Voluntario.objects.filter(ativo=True).count()
    voluntarios_inativos = Voluntario.objects.filter(ativo=False).count()
    voluntario_status_labels = ['Ativos', 'Inativos']
    voluntario_status_data = [voluntarios_ativos, voluntarios_inativos]

    # 3. Contagem de beneficiários por faixa etária (exemplo simplificado)
    #    Para um gráfico real de faixa etária, seria necessário calcular as idades
    #    e agrupá-las em faixas. Aqui, vamos usar gênero como exemplo mais simples.
    beneficiarios_por_genero = Beneficiario.objects.values('genero').annotate(total=Count('genero')).order_by('genero')
    genero_labels = [dict(Beneficiario.GENERO_CHOICES).get(item['genero'], item['genero']) for item in beneficiarios_por_genero]
    genero_data = [item['total'] for item in beneficiarios_por_genero]
    
    # 4. Contagem de beneficiários por escolaridade
    beneficiarios_por_escolaridade = Beneficiario.objects.values('escolaridade').annotate(total=Count('escolaridade')).order_by('escolaridade')
    escolaridade_labels = [dict(Beneficiario.ESCOLARIDADE_CHOICES).get(item['escolaridade'], item['escolaridade']) for item in beneficiarios_por_escolaridade]
    escolaridade_data = [item['total'] for item in beneficiarios_por_escolaridade]

    # 5. Contagem de voluntários por disponibilidade (dia/turno)
    dias_semana_map = {
        "Segunda": "seg", "Terça": "ter", "Quarta": "qua", 
        "Quinta": "qui", "Sexta": "sex", "Sábado": "sab", "Domingo": "dom"
    }
    turnos_map = {"Manhã": "m", "Tarde": "t", "Noite": "n"}
    
    disp_labels = list(dias_semana_map.keys())
    disp_datasets = []

    for nome_turno, abrev_turno in turnos_map.items():
        turno_data = []
        for nome_dia, abrev_dia in dias_semana_map.items():
            campo_filtro = f"disp_{abrev_dia}_{abrev_turno}"
            count = Voluntario.objects.filter(ativo=True, **{campo_filtro: True}).count()
            turno_data.append(count)
        disp_datasets.append({
            "label": nome_turno,
            "data": turno_data,
            # Você pode adicionar cores específicas por turno aqui, ex:
            # "backgroundColor": "rgba(54, 162, 235, 0.5)" para Manhã, etc.
        })

    contexto = {
        'titulo_pagina': 'Dashboard Principal',
        'total_voluntarios': Voluntario.objects.count(),
        'total_beneficiarios': Beneficiario.objects.count(),
        'total_tarefas_pendentes': Tarefa.objects.filter(status='PEND').count(),
        'total_tarefas_concluidas': Tarefa.objects.filter(status='CONC').count(),
        
        'status_labels_json': json.dumps(status_labels),
        'status_data_json': json.dumps(status_data),
        'voluntario_status_labels_json': json.dumps(voluntario_status_labels),
        'voluntario_status_data_json': json.dumps(voluntario_status_data),
        'genero_labels_json': json.dumps(genero_labels),
        'genero_data_json': json.dumps(genero_data),
        'escolaridade_labels_json': json.dumps(escolaridade_labels),
        'escolaridade_data_json': json.dumps(escolaridade_data),

        'disp_labels_json': json.dumps(disp_labels),
        'disp_datasets_json': json.dumps(disp_datasets),
    }
    return render(request, 'dashboard/painel_principal.html', contexto)

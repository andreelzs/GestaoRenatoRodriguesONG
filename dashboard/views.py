from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from django.db.models.functions import Lower
from datetime import date, timedelta, datetime # Adicionado datetime para strptime
from voluntarios.models import Voluntario
from beneficiarios.models import Beneficiario
from tarefas.models import Tarefa
from cursos.models import Certificado # Adicionado para gráficos de cursos
import json # Para passar dados para o JavaScript

@login_required
def painel_principal(request):
    aba_param = request.GET.get('aba', 'voluntarios') # Padrão para 'voluntarios'

    # Dados para os gráficos
    # 1. Contagem de tarefas por status
    tarefas_por_status = Tarefa.objects.values('status').annotate(total=Count('status')).order_by('status')
    status_labels = [dict(Tarefa.STATUS_TAREFA).get(item['status'], item['status']) for item in tarefas_por_status]
    status_data = [item['total'] for item in tarefas_por_status]

    # 2. Contagem de voluntários 
    voluntarios_ativos = Voluntario.objects.filter(ativo=True).count()
    voluntarios_inativos = Voluntario.objects.filter(ativo=False).count()
    voluntario_status_labels = ['Ativos', 'Inativos']
    voluntario_status_data = [voluntarios_ativos, voluntarios_inativos]

    # 3. Contagem de beneficiários por faixa etária 
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
            campo_filtro = f"disp_{abrev_dia}_{abrev_turno}" # Ajustar se o nome do campo for diferente
            count = Voluntario.objects.filter(ativo=True, **{campo_filtro: True}).count()
            turno_data.append(count)
        disp_datasets.append({
            "label": nome_turno,
            "data": turno_data,
        })

     # 6. Tarefas por Prioridade (Ativas)
    tarefas_ativas_por_prioridade = Tarefa.objects.exclude(status='CONC').values('prioridade').annotate(total=Count('id')).order_by('prioridade')
    prioridade_labels = [dict(Tarefa.PRIORIDADE_TAREFA).get(item['prioridade'], str(item['prioridade'])) for item in tarefas_ativas_por_prioridade]
    prioridade_data = [item['total'] for item in tarefas_ativas_por_prioridade]

    # 7. Beneficiários por Faixa Etária
    hoje = date.today()
    faixas_etarias = {
        "0-10 anos": 0, "11-17 anos": 0, "18-25 anos": 0, 
        "26-35 anos": 0, "36-50 anos": 0, "51+ anos": 0, "Idade N/D": 0
    }
    for b in Beneficiario.objects.all():
        if b.data_nascimento:
            idade = hoje.year - b.data_nascimento.year - ((hoje.month, hoje.day) < (b.data_nascimento.month, b.data_nascimento.day))
            if 0 <= idade <= 10: faixas_etarias["0-10 anos"] += 1
            elif 11 <= idade <= 17: faixas_etarias["11-17 anos"] += 1
            elif 18 <= idade <= 25: faixas_etarias["18-25 anos"] += 1
            elif 26 <= idade <= 35: faixas_etarias["26-35 anos"] += 1
            elif 36 <= idade <= 50: faixas_etarias["36-50 anos"] += 1
            elif idade >= 51: faixas_etarias["51+ anos"] += 1
        else:
            faixas_etarias["Idade N/D"] += 1
    faixa_etaria_labels = list(faixas_etarias.keys())
    faixa_etaria_data = list(faixas_etarias.values())

    # 8. Beneficiários por Localização (Cidade) - Top 10
    benef_por_cidade = Beneficiario.objects.annotate(cidade_lower=Lower('cidade')).values('cidade_lower').annotate(total=Count('id')).order_by('-total').filter(cidade_lower__isnull=False)[:10]
    cidade_labels = [item['cidade_lower'].title() if item['cidade_lower'] else "N/D" for item in benef_por_cidade]
    cidade_data = [item['total'] for item in benef_por_cidade]

    # 9. Beneficiários por Renda Familiar Aproximada
    faixas_renda = {
        "Até R$1.500": 0, "R$1.501 - R$3.000": 0,
        "R$3.001 - R$5.000": 0, "Acima de R$5.000": 0, "Não Informado": 0
    }
    for b in Beneficiario.objects.all():
        if b.renda_familiar_aproximada is not None:
            if b.renda_familiar_aproximada <= 1500: faixas_renda["Até R$1.500"] += 1
            elif 1501 <= b.renda_familiar_aproximada <= 3000: faixas_renda["R$1.501 - R$3.000"] += 1
            elif 3001 <= b.renda_familiar_aproximada <= 5000: faixas_renda["R$3.001 - R$5.000"] += 1
            else: faixas_renda["Acima de R$5.000"] += 1
        else:
            faixas_renda["Não Informado"] += 1
    renda_labels = list(faixas_renda.keys())
    renda_data = list(faixas_renda.values())

    # 10. Certificados por Curso (com filtro de período opcional)
    cert_data_inicio_param = request.GET.get('cert_data_inicio')
    cert_data_fim_param = request.GET.get('cert_data_fim')

    cert_por_curso_qs = Certificado.objects.all()

    if cert_data_inicio_param:
        try:
            data_inicio_obj = datetime.strptime(cert_data_inicio_param, '%Y-%m-%d').date()
            cert_por_curso_qs = cert_por_curso_qs.filter(data_emissao_certificado__gte=data_inicio_obj)
        except ValueError:
            pass # Ignorar data inválida
    
    if cert_data_fim_param:
        try:
            data_fim_obj = datetime.strptime(cert_data_fim_param, '%Y-%m-%d').date()
            cert_por_curso_qs = cert_por_curso_qs.filter(data_emissao_certificado__lte=data_fim_obj)
        except ValueError:
            pass # Ignorar data inválida

    cert_por_curso = cert_por_curso_qs.values('curso__nome_curso').annotate(total=Count('id')).order_by('-total')
    curso_cert_labels = [item['curso__nome_curso'] for item in cert_por_curso]
    curso_cert_data = [item['total'] for item in cert_por_curso]
    
    contexto = {
        'titulo_pagina': 'Dashboard Principal',
        'total_voluntarios': Voluntario.objects.count(),
        'total_beneficiarios': Beneficiario.objects.count(),
        'total_tarefas_pendentes': Tarefa.objects.filter(status='PEND').count(),
        'total_tarefas_concluidas': Tarefa.objects.filter(status='CONC').count(),
        
        # Passar os objetos Python diretamente, |json_script fará a serialização
        'status_labels_json': status_labels,
        'status_data_json': status_data,
        'voluntario_status_labels_json': voluntario_status_labels,
        'voluntario_status_data_json': voluntario_status_data,
        'genero_labels_json': genero_labels,
        'genero_data_json': genero_data,
        'escolaridade_labels_json': escolaridade_labels,
        'escolaridade_data_json': escolaridade_data,
        'disp_labels_json': disp_labels,
        'disp_datasets_json': disp_datasets,

        'prioridade_labels_json': prioridade_labels,
        'prioridade_data_json': prioridade_data,
        'faixa_etaria_labels_json': faixa_etaria_labels,
        'faixa_etaria_data_json': faixa_etaria_data,
        'cidade_labels_json': cidade_labels,
        'cidade_data_json': cidade_data,
        'renda_labels_json': renda_labels,
        'renda_data_json': renda_data,
        'curso_cert_labels_json': curso_cert_labels,
        'curso_cert_data_json': curso_cert_data,

        # Para preencher os filtros de data no template
        'cert_data_inicio_form': cert_data_inicio_param,
        'cert_data_fim_form': cert_data_fim_param,
        'aba_atual': aba_param, # Passar a aba atual para o template
    }
    return render(request, 'dashboard/painel_principal.html', contexto)

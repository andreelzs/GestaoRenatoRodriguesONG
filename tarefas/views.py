from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import Tarefa
from .forms import FormularioTarefa
from voluntarios.models import Voluntario # Para filtros ou informações adicionais
from contas.decorators import admin_required # Importar o decorator

@login_required
def listar_tarefas(request):
    # Adicionar filtros
    filtro_status = request.GET.get('status')
    filtro_voluntario_id = request.GET.get('voluntario')
    termo_pesquisa_titulo = request.GET.get('q_titulo')

    tarefas = Tarefa.objects.all()

    if termo_pesquisa_titulo:
        tarefas = tarefas.filter(titulo__icontains=termo_pesquisa_titulo)
    if filtro_status:
        tarefas = tarefas.filter(status=filtro_status)
    if filtro_voluntario_id:
        tarefas = tarefas.filter(voluntario_responsavel_id=filtro_voluntario_id)
    
    # Ordenar por prioridade (maior primeiro), depois por prazo e título
    tarefas = tarefas.order_by('-prioridade', 'data_prevista_conclusao', 'titulo')
    
    voluntarios_ativos = Voluntario.objects.filter(ativo=True)

    contexto = {
        'tarefas': tarefas,
        'titulo_pagina': 'Lista de Tarefas',
        'status_choices': Tarefa.STATUS_TAREFA, # Para o filtro
        'voluntarios_ativos': voluntarios_ativos, # Para o filtro
        'filtro_status_atual': filtro_status,
        'filtro_voluntario_atual': int(filtro_voluntario_id) if filtro_voluntario_id else None,
        'termo_pesquisa_titulo_atual': termo_pesquisa_titulo, # Para preencher o campo de pesquisa
    }
    return render(request, 'tarefas/listar_tarefas.html', contexto)

@login_required
def cadastrar_tarefa(request):
    if request.method == 'POST':
        form = FormularioTarefa(request.POST)
        if form.is_valid():
            try:
                tarefa = form.save(commit=False)
                tarefa.atribuido_por = request.user # Usuário logado que criou a tarefa
                if tarefa.status == 'CONC' and not tarefa.data_conclusao_efetiva:
                    tarefa.data_conclusao_efetiva = timezone.now().date()
                tarefa.save()
                messages.success(request, 'Tarefa cadastrada com sucesso!')
                return redirect('tarefas:listar_tarefas')
            except Exception as e:
                messages.error(request, f'Ocorreu um erro ao cadastrar a tarefa: {e}')
    else:
        form = FormularioTarefa()
    
    contexto = {
        'form': form,
        'titulo_pagina': 'Cadastrar Nova Tarefa'
    }
    return render(request, 'tarefas/formulario_tarefa.html', contexto)

@login_required
def detalhar_tarefa(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, pk=tarefa_id)
    contexto = {
        'tarefa': tarefa,
        'titulo_pagina': f'Detalhes da Tarefa: {tarefa.titulo}'
    }
    return render(request, 'tarefas/detalhar_tarefa.html', contexto)

@login_required
def editar_tarefa(request, tarefa_id):
    tarefa = get_object_or_404(Tarefa, pk=tarefa_id)
    if request.method == 'POST':
        form = FormularioTarefa(request.POST, instance=tarefa)
        if form.is_valid():
            try:
                tarefa_editada = form.save(commit=False)
                # Se o status for mudado para Concluída e não houver data de conclusão, preenche
                if tarefa_editada.status == 'CONC' and not tarefa_editada.data_conclusao_efetiva:
                    tarefa_editada.data_conclusao_efetiva = timezone.now().date()
                # Se o status for mudado de Concluída para outro, limpa a data de conclusão
                elif tarefa.status == 'CONC' and tarefa_editada.status != 'CONC':
                     tarefa_editada.data_conclusao_efetiva = None
                tarefa_editada.save()
                messages.success(request, 'Tarefa atualizada com sucesso!')
                return redirect('tarefas:detalhar_tarefa', tarefa_id=tarefa.id)
            except Exception as e:
                messages.error(request, f'Ocorreu um erro ao atualizar a tarefa: {e}')
    else:
        form = FormularioTarefa(instance=tarefa)
    
    contexto = {
        'form': form,
        'tarefa': tarefa,
        'titulo_pagina': f'Editar Tarefa: {tarefa.titulo}'
    }
    return render(request, 'tarefas/formulario_tarefa.html', contexto)

@login_required
@admin_required # Apenas admin pode excluir tarefas
def excluir_tarefa(request, tarefa_id): # Ou cancelar/arquivar
    tarefa = get_object_or_404(Tarefa, pk=tarefa_id)
    if request.method == 'POST':
        try:
            tarefa.delete()
            messages.success(request, f'Tarefa "{tarefa.titulo}" excluída com sucesso.')
        except Exception as e:
            messages.error(request, f'Erro ao excluir/cancelar a tarefa: {e}')
        return redirect('tarefas:listar_tarefas')
    
    contexto = {
        'tarefa': tarefa,
        'titulo_pagina': f'Confirmar Exclusão da Tarefa: {tarefa.titulo}'
    }
    return render(request, 'tarefas/confirmar_exclusao_tarefa.html', contexto)

# View para atualizar status rapidamente 
@login_required
def atualizar_status_tarefa(request, tarefa_id, novo_status):
    tarefa = get_object_or_404(Tarefa, pk=tarefa_id)
    if novo_status in [s[0] for s in Tarefa.STATUS_TAREFA]:
        tarefa.status = novo_status
        if novo_status == 'CONC' and not tarefa.data_conclusao_efetiva:
            tarefa.data_conclusao_efetiva = timezone.now().date()
        elif tarefa.status == 'CONC' and novo_status != 'CONC': 
            tarefa.data_conclusao_efetiva = None
        tarefa.save()
        messages.success(request, f'Status da tarefa "{tarefa.titulo}" atualizado para "{tarefa.get_status_display()}".')
    else:
        messages.error(request, 'Status inválido.')
    return redirect(request.META.get('HTTP_REFERER', 'tarefas:listar_tarefas'))

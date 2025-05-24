from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Beneficiario
from .forms import FormularioBeneficiario

@login_required
def listar_beneficiarios(request):
    beneficiarios = Beneficiario.objects.filter(ativo=True).order_by('nome_completo')
    contexto = {
        'beneficiarios': beneficiarios,
        'titulo_pagina': 'Beneficiários Cadastrados'
    }
    return render(request, 'beneficiarios/listar_beneficiarios.html', contexto)

@login_required
def cadastrar_beneficiario(request):
    if request.method == 'POST':
        form = FormularioBeneficiario(request.POST)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Beneficiário cadastrado com sucesso!')
                return redirect('beneficiarios:listar_beneficiarios')
            except Exception as e:
                messages.error(request, f'Ocorreu um erro ao cadastrar o beneficiário: {e}')
    else:
        form = FormularioBeneficiario()
    
    contexto = {
        'form': form,
        'titulo_pagina': 'Cadastrar Novo Beneficiário'
    }
    return render(request, 'beneficiarios/formulario_beneficiario.html', contexto)

@login_required
def detalhar_beneficiario(request, beneficiario_id):
    beneficiario = get_object_or_404(Beneficiario, pk=beneficiario_id)
    contexto = {
        'beneficiario': beneficiario,
        'titulo_pagina': f'Detalhes de {beneficiario.nome_completo}'
    }
    return render(request, 'beneficiarios/detalhar_beneficiario.html', contexto)

@login_required
def editar_beneficiario(request, beneficiario_id):
    beneficiario = get_object_or_404(Beneficiario, pk=beneficiario_id)
    if request.method == 'POST':
        form = FormularioBeneficiario(request.POST, instance=beneficiario)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Dados do beneficiário atualizados com sucesso!')
                return redirect('beneficiarios:detalhar_beneficiario', beneficiario_id=beneficiario.id)
            except Exception as e:
                messages.error(request, f'Ocorreu um erro ao atualizar o beneficiário: {e}')
    else:
        form = FormularioBeneficiario(instance=beneficiario)
    
    contexto = {
        'form': form,
        'beneficiario': beneficiario,
        'titulo_pagina': f'Editar Beneficiário: {beneficiario.nome_completo}'
    }
    return render(request, 'beneficiarios/formulario_beneficiario.html', contexto)

@login_required
def excluir_beneficiario(request, beneficiario_id): # Na verdade, inativação
    beneficiario = get_object_or_404(Beneficiario, pk=beneficiario_id)
    if request.method == 'POST':
        try:
            beneficiario.ativo = False
            beneficiario.save()
            messages.success(request, f'Beneficiário {beneficiario.nome_completo} inativado com sucesso.')
        except Exception as e:
            messages.error(request, f'Erro ao inativar o beneficiário: {e}')
        return redirect('beneficiarios:listar_beneficiarios')
    
    contexto = {
        'beneficiario': beneficiario,
        'titulo_pagina': f'Confirmar Inativação de {beneficiario.nome_completo}'
    }
    return render(request, 'beneficiarios/confirmar_exclusao_beneficiario.html', contexto)

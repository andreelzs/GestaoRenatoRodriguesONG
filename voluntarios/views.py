from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required # Para proteger views
from .models import Voluntario
from .forms import FormularioVoluntario

@login_required
def listar_voluntarios(request):
    voluntarios = Voluntario.objects.filter(ativo=True).order_by('nome_completo')
    contexto = {
        'voluntarios': voluntarios,
        'titulo_pagina': 'Voluntários Cadastrados'
    }
    return render(request, 'voluntarios/listar_voluntarios.html', contexto)

@login_required
def cadastrar_voluntario(request):
    if request.method == 'POST':
        form = FormularioVoluntario(request.POST)
        if form.is_valid():
            try:
                form.save() # O método save do formulário já lida com a criação do usuário
                messages.success(request, 'Voluntário cadastrado com sucesso!')
                return redirect('voluntarios:listar_voluntarios')
            except Exception as e:
                messages.error(request, f'Ocorreu um erro ao cadastrar o voluntário: {e}')
        else:
            # Se o formulário não for válido, exibe mensagens de erro já tratadas no formulário
            pass 
    else:
        form = FormularioVoluntario()
    
    contexto = {
        'form': form,
        'titulo_pagina': 'Cadastrar Novo Voluntário'
    }
    return render(request, 'voluntarios/formulario_voluntario.html', contexto)

# Views para Detalhar, Editar e Excluir (a serem implementadas depois)
@login_required
def detalhar_voluntario(request, voluntario_id):
    voluntario = get_object_or_404(Voluntario, pk=voluntario_id)
    contexto = {
        'voluntario': voluntario,
        'titulo_pagina': f'Detalhes de {voluntario.nome_completo}'
    }
    return render(request, 'voluntarios/detalhar_voluntario.html', contexto)

@login_required
def editar_voluntario(request, voluntario_id):
    voluntario = get_object_or_404(Voluntario, pk=voluntario_id)
    if request.method == 'POST':
        form = FormularioVoluntario(request.POST, instance=voluntario)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Dados do voluntário atualizados com sucesso!')
                return redirect('voluntarios:detalhar_voluntario', voluntario_id=voluntario.id)
            except Exception as e:
                messages.error(request, f'Ocorreu um erro ao atualizar o voluntário: {e}')
    else:
        form = FormularioVoluntario(instance=voluntario)
        # Se o voluntário tem um usuário associado, preenche os campos de usuário no formulário
        # O __init__ do formulário já faz isso, mas podemos garantir aqui se necessário.
        # if hasattr(voluntario, 'usuario') and voluntario.usuario:
        #     form.fields['username'].initial = voluntario.usuario.username
        #     form.fields['email'].initial = voluntario.usuario.email
        #     form.fields['password'].required = False
        #     form.fields['confirmar_password'].required = False


    contexto = {
        'form': form,
        'voluntario': voluntario,
        'titulo_pagina': f'Editar Voluntário: {voluntario.nome_completo}'
    }
    return render(request, 'voluntarios/formulario_voluntario.html', contexto)

@login_required
def excluir_voluntario(request, voluntario_id):
    voluntario = get_object_or_404(Voluntario, pk=voluntario_id)
    if request.method == 'POST':
        try:
            # Em vez de excluir, podemos apenas inativar o voluntário e seu usuário
            voluntario.ativo = False
            if hasattr(voluntario, 'usuario') and voluntario.usuario:
                voluntario.usuario.is_active = False
                voluntario.usuario.save()
            voluntario.save()
            messages.success(request, f'Voluntário {voluntario.nome_completo} inativado com sucesso.')
        except Exception as e:
            messages.error(request, f'Erro ao inativar o voluntário: {e}')
        return redirect('voluntarios:listar_voluntarios')
    
    contexto = {
        'voluntario': voluntario,
        'titulo_pagina': f'Confirmar Inativação de {voluntario.nome_completo}'
    }
    return render(request, 'voluntarios/confirmar_exclusao_voluntario.html', contexto)

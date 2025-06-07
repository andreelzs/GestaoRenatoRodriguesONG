from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Certificado, Curso
from beneficiarios.models import Beneficiario
from .forms import CertificadoForm, CursoForm # Adicionado CursoForm
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin 
@login_required
def adicionar_certificado_beneficiario(request, beneficiario_id):
    beneficiario = get_object_or_404(Beneficiario, pk=beneficiario_id)
    if request.method == 'POST':
        form = CertificadoForm(request.POST)
        if form.is_valid():
            certificado = form.save(commit=False)
            certificado.beneficiario = beneficiario
            certificado.save()
            messages.success(request, f"Certificado do curso '{certificado.curso.nome_curso}' adicionado para {beneficiario.nome_completo}.")
            return redirect('beneficiarios:detalhar_beneficiario', pk=beneficiario_id)
        else:
            messages.error(request, "Erro ao adicionar o certificado. Verifique os dados informados.")
    else:
        form = CertificadoForm()

    context = {
        'form': form,
        'beneficiario': beneficiario,
        'titulo_pagina': f"Adicionar Certificado para {beneficiario.nome_completo}"
    }
    return render(request, 'cursos/formulario_certificado.html', context)

@login_required
def editar_certificado_beneficiario(request, certificado_id):
    certificado = get_object_or_404(Certificado, pk=certificado_id)
    beneficiario = certificado.beneficiario
    if request.method == 'POST':
        form = CertificadoForm(request.POST, instance=certificado)
        if form.is_valid():
            form.save()
            messages.success(request, f"Certificado do curso '{certificado.curso.nome_curso}' atualizado para {beneficiario.nome_completo}.")
            return redirect('beneficiarios:detalhar_beneficiario', pk=beneficiario.id)
        else:
            messages.error(request, "Erro ao atualizar o certificado. Verifique os dados informados.")
    else:
        form = CertificadoForm(instance=certificado)

    context = {
        'form': form,
        'beneficiario': beneficiario,
        'certificado': certificado,
        'titulo_pagina': f"Editar Certificado de {beneficiario.nome_completo}"
    }
    return render(request, 'cursos/formulario_certificado.html', context)

@login_required
def excluir_certificado_beneficiario(request, certificado_id):
    certificado = get_object_or_404(Certificado, pk=certificado_id)
    beneficiario_id = certificado.beneficiario.id
    nome_curso = certificado.curso.nome_curso
    nome_beneficiario = certificado.beneficiario.nome_completo

    if request.method == 'POST':
        certificado.delete()
        messages.success(request, f"Certificado do curso '{nome_curso}' para {nome_beneficiario} foi excluído.")
        return redirect('beneficiarios:detalhar_beneficiario', pk=beneficiario_id)

    context = {
        'certificado': certificado,
        'beneficiario': certificado.beneficiario,
        'titulo_pagina': "Confirmar Exclusão de Certificado"
    }
    return render(request, 'cursos/confirmar_exclusao_certificado.html', context)


# Views para Gerenciamento de Cursos da ONG

class CursoListView(LoginRequiredMixin, ListView):
    model = Curso
    template_name = 'cursos/curso_list.html' # Especificar o nome do template
    context_object_name = 'cursos'
    paginate_by = 10 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = "Gerenciar Cursos da ONG"
        return context

class CursoCreateView(LoginRequiredMixin, CreateView):
    model = Curso
    form_class = CursoForm
    template_name = 'cursos/curso_form.html' # Template para criar e atualizar
    success_url = reverse_lazy('cursos:listar_cursos_ong') # Nome da URL para a lista de cursos

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = "Adicionar Novo Curso"
        context['texto_botao'] = "Salvar Novo Curso"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Curso adicionado com sucesso!")
        return super().form_valid(form)

class CursoUpdateView(LoginRequiredMixin, UpdateView):
    model = Curso
    form_class = CursoForm
    template_name = 'cursos/curso_form.html'
    success_url = reverse_lazy('cursos:listar_cursos_ong')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = f"Editar Curso: {self.object.nome_curso}"
        context['texto_botao'] = "Salvar Alterações"
        return context

    def form_valid(self, form):
        messages.success(self.request, "Curso atualizado com sucesso!")
        return super().form_valid(form)

class CursoDeleteView(LoginRequiredMixin, DeleteView):
    model = Curso
    template_name = 'cursos/curso_confirm_delete.html' # Template para confirmar exclusão
    success_url = reverse_lazy('cursos:listar_cursos_ong')
    context_object_name = 'curso' # Para usar {{ curso }} no template

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo_pagina'] = f"Confirmar Exclusão do Curso: {self.object.nome_curso}"
        return context
    
    def post(self, request, *args, **kwargs):
        
        curso_nome = self.get_object().nome_curso
        # Verificar se há certificados associados antes de excluir
        if Certificado.objects.filter(curso=self.get_object()).exists():
            messages.error(request, f"Não é possível excluir o curso '{curso_nome}', pois existem certificados associados a ele. Remova os certificados primeiro.")
            return redirect(self.success_url) # Ou para a página de detalhes do curso, se houver

        messages.success(request, f"Curso '{curso_nome}' excluído com sucesso.")
        return super().delete(request, *args, **kwargs) # Chama o método delete padrão

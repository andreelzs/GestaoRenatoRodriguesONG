from django import forms
from .models import Tarefa
from voluntarios.models import Voluntario 
class FormularioTarefa(forms.ModelForm):
    
    class Meta:
        model = Tarefa
        fields = [
            'titulo', 'descricao', 'status', 'prioridade', 
            'data_prevista_conclusao', 'voluntario_responsavel', 
            'observacoes'
            # 'atribuido_por' não estará no formulário, será pego da request.user
            # 'data_conclusao_efetiva' será preenchida quando o status for 'Concluída'
        ]
        widgets = {
            'descricao': forms.Textarea(attrs={'rows': 4}),
            'observacoes': forms.Textarea(attrs={'rows': 3}),
            'data_prevista_conclusao': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
        }
        labels = {
            'titulo': 'Título da Tarefa',
            'descricao': 'Descrição Detalhada',
            'data_prevista_conclusao': 'Prazo de Entrega (Opcional)',
            'voluntario_responsavel': 'Atribuir ao Voluntário (Opcional)',
        }
        help_texts = {
            'voluntario_responsavel': 'Selecione um voluntário ativo para esta tarefa.',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adicionar classes do Bootstrap e ajustar campos
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs['class'] = 'form-control'
            
            if not field.required:
                field.widget.attrs.pop('required', None)
        
        # Personalizar o queryset do campo voluntario_responsavel para mostrar apenas ativos
        if 'voluntario_responsavel' in self.fields:
            self.fields['voluntario_responsavel'].queryset = Voluntario.objects.filter(ativo=True).order_by('nome_completo')
            self.fields['voluntario_responsavel'].widget.attrs.update({'class': 'form-select'})
        
        # Personalizar o widget do campo status para usar form-select
        if 'status' in self.fields:
            self.fields['status'].widget.attrs.update({'class': 'form-select'})
        
        # Personalizar o widget do campo prioridade para usar form-select
        if 'prioridade' in self.fields:
            self.fields['prioridade'].widget.attrs.update({'class': 'form-select'})

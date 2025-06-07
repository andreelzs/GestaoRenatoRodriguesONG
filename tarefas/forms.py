from django import forms
from .models import Tarefa
from voluntarios.models import Voluntario 
class FormularioTarefa(forms.ModelForm):
    
    class Meta:
        model = Tarefa
        fields = [
            'titulo', 'descricao', 'status', 'prioridade', 
            'data_prevista_conclusao', 'voluntarios_responsaveis', # Alterado aqui
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
            'voluntarios_responsaveis': 'Atribuir aos Voluntários (Opcional)', # Alterado aqui
        }
        help_texts = {
            'voluntarios_responsaveis': 'Selecione um ou mais voluntários ativos para esta tarefa.', # Texto de ajuda atualizado
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Adicionar classes do Bootstrap e ajustar campos
        for field_name, field in self.fields.items():
            if field_name == 'voluntarios_responsaveis': # Pula o campo de checkboxes
                continue

            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs['class'] = 'form-control'
            
            if not field.required: # Linha do if
                field.widget.attrs.pop('required', None) # Esta linha deve estar indentada
        
        # Personalizar o queryset do campo voluntarios_responsaveis para mostrar apenas ativos
        if 'voluntarios_responsaveis' in self.fields: # Alterado aqui
            self.fields['voluntarios_responsaveis'].queryset = Voluntario.objects.filter(ativo=True).order_by('nome_completo')
            self.fields['voluntarios_responsaveis'].widget = forms.CheckboxSelectMultiple()
            # Não é mais necessário remover 'form-control' aqui, pois o loop acima já pula este campo.
            # A classe 'form-control' ou 'form-select' não se aplica bem a CheckboxSelectMultiple diretamente.
            # O Bootstrap geralmente estiliza os inputs 'checkbox' individualmente.
            # Se for necessário um container com scroll para muitos checkboxes, isso pode ser feito no template.
            # Removendo a tentativa de aplicar 'form-select' e 'size' que eram para SelectMultiple.
            # A classe 'form-control' que é adicionada no loop acima para todos os campos será ignorada ou não terá efeito visual desejado em CheckboxSelectMultiple.
            # Podemos remover a adição genérica de 'form-control' para este widget específico se causar problemas.
            # Por enquanto, vamos deixar o loop genérico e ver como o Bootstrap lida com os checkboxes.
            # Se quisermos que cada checkbox tenha a classe 'form-check-input', o Django geralmente faz isso
            # ou o template pode precisar de um loop customizado para renderizar o campo.
            # Vamos testar a renderização padrão primeiro.
        
        # Personalizar o widget do campo status para usar form-select
        if 'status' in self.fields:
            self.fields['status'].widget.attrs.update({'class': 'form-select'})
        
        # Personalizar o widget do campo prioridade para usar form-select
        if 'prioridade' in self.fields:
            self.fields['prioridade'].widget.attrs.update({'class': 'form-select'})

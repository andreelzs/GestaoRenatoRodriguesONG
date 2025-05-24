from django import forms
from .models import Beneficiario

class FormularioBeneficiario(forms.ModelForm):
    class Meta:
        model = Beneficiario
        fields = [
            'nome_completo', 'data_nascimento', 'genero', 'cpf', 'rg',
            'cep', 'logradouro', 'numero_endereco', 'complemento_endereco', 
            'bairro', 'cidade', 'estado',
            'telefone_principal', 'telefone_secundario', 'email',
            'escolaridade', 'ocupacao', 'renda_familiar_aproximada',
            'como_conheceu_ong', 'observacoes', 'ativo'
        ]
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'endereco': forms.Textarea(attrs={'rows': 3}),
            'como_conheceu_ong': forms.Textarea(attrs={'rows': 3}),
            'observacoes': forms.Textarea(attrs={'rows': 3}),
            # Poderíamos adicionar mais widgets para CEP (com máscara), telefone, etc.
        }
        labels = {
            'nome_completo': 'Nome Completo do Beneficiário',
            'numero_endereco': 'Número',
            'complemento_endereco': 'Complemento',
            'estado': 'UF (Ex: SP)',
            'renda_familiar_aproximada': 'Renda Familiar Mensal Aproximada (R$)',
        }
        help_texts = {
            'cpf': 'Formato: XXX.XXX.XXX-XX (Opcional, mas recomendado)',
            'cep': 'Formato: XXXXX-XXX (Opcional)',
            'telefone_principal': 'Formato: (XX) XXXXX-XXXX ou (XX) XXXX-XXXX',
            'renda_familiar_aproximada': 'Use ponto para decimais. Ex: 1500.50',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            # Adiciona a classe 'form-control' do Bootstrap a todos os campos
            if field.widget.attrs.get('class'):
                field.widget.attrs['class'] += ' form-control'
            else:
                field.widget.attrs['class'] = 'form-control'
            
            # Campos opcionais podem não ter o atributo 'required' no widget
            # mas o campo do formulário em si terá.
            # Se o campo não for obrigatório no modelo, não adicionamos 'required' no HTML
            if not field.required:
                field.widget.attrs.pop('required', None)

        # Tratamento especial para o campo 'ativo' (BooleanField) para usar um select
        # ou garantir que o CheckboxInput do Bootstrap seja bem estilizado.
        # Por padrão, o BooleanField usa CheckboxInput, que o Bootstrap estiliza.
        # Se quisermos um select "Sim/Não":
        # self.fields['ativo'].widget = forms.Select(choices=[(True, 'Sim'), (False, 'Não')])
        # self.fields['ativo'].widget.attrs.update({'class': 'form-select'})

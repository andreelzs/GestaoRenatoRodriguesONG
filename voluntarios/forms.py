from django import forms
from .models import Voluntario
from contas.models import Usuario # Precisamos acessar o modelo Usuario

class FormularioVoluntario(forms.ModelForm):
    # Campos do modelo Usuario que queremos no formulário de Voluntario
    # Estes não são campos diretos do modelo Voluntario, então os definimos aqui
    # e os trataremos na view.
    username = forms.CharField(label='Nome de Usuário (para login)', max_length=150)
    email = forms.EmailField(label='Email (para login e contato)', required=False)
    password = forms.CharField(label='Senha (para login)', widget=forms.PasswordInput, min_length=8)
    confirmar_password = forms.CharField(label='Confirmar Senha', widget=forms.PasswordInput, min_length=8)

    class Meta:
        model = Voluntario
        # Incluir campos do modelo Voluntario
        fields = [
            'nome_completo', 'cpf', 'data_nascimento', 
            'telefone', 
            'cep', 'logradouro', 'numero_endereco', 'complemento_endereco', 'bairro', 'cidade', 'estado',
            'areas_interesse',
            # Campos de disponibilidade semanal
            'disp_seg_m', 'disp_seg_t', 'disp_seg_n',
            'disp_ter_m', 'disp_ter_t', 'disp_ter_n',
            'disp_qua_m', 'disp_qua_t', 'disp_qua_n',
            'disp_qui_m', 'disp_qui_t', 'disp_qui_n',
            'disp_sex_m', 'disp_sex_t', 'disp_sex_n',
            'disp_sab_m', 'disp_sab_t', 'disp_sab_n',
            'disp_dom_m', 'disp_dom_t', 'disp_dom_n',
        ]
        # Adicionar widgets se necessário para melhor formatação (ex: DatePicker)
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}, format='%Y-%m-%d'),
            'areas_interesse': forms.Textarea(attrs={'rows': 3}),
            # 'disponibilidade': forms.Textarea(attrs={'rows': 3}), # Removido
            # 'endereco': forms.Textarea(attrs={'rows': 3}), # Removido
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Se estiver editando um voluntário existente, podemos preencher os campos do usuário
        if self.instance and self.instance.pk and hasattr(self.instance, 'usuario'):
            self.fields['username'].initial = self.instance.usuario.username
            self.fields['email'].initial = self.instance.usuario.email
            # Não preenchemos a senha por segurança e usabilidade
            self.fields['password'].required = False
            self.fields['confirmar_password'].required = False
        
        # Adicionar classes do Bootstrap aos campos
        for field_name, field in self.fields.items():
            # Não aplicar 'form-control' a checkboxes, pois pode quebrar a renderização padrão
            if not isinstance(field.widget, forms.CheckboxInput):
                current_class = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f'{current_class} form-control'.strip()
            # Para checkboxes, podemos querer usar 'form-check-input' do Bootstrap 5
            elif isinstance(field.widget, forms.CheckboxInput):
                current_class = field.widget.attrs.get('class', '')
                field.widget.attrs['class'] = f'{current_class} form-check-input'.strip()


    def clean_username(self):
        username = self.cleaned_data.get('username')
        # Se estiver editando e o username não mudou, permite.
        if self.instance and self.instance.pk and hasattr(self.instance, 'usuario') and self.instance.usuario.username == username:
            return username
        # Caso contrário, verifica se o username já existe.
        if Usuario.objects.filter(username=username).exists():
            raise forms.ValidationError("Este nome de usuário já está em uso. Por favor, escolha outro.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Permite email vazio se não for obrigatório
        if not email and not self.fields['email'].required:
            return email
            
        # Se estiver editando e o email não mudou, permite.
        if self.instance and self.instance.pk and hasattr(self.instance, 'usuario') and self.instance.usuario.email == email:
            return email
        # Caso contrário, verifica se o email já existe (se houver um email).
        if email and Usuario.objects.filter(email=email).exists():
            raise forms.ValidationError("Este email já está cadastrado. Por favor, use outro ou deixe em branco se opcional.")
        return email

    def clean_confirmar_password(self):
        password = self.cleaned_data.get("password")
        confirmar_password = self.cleaned_data.get("confirmar_password")

        # Se estamos editando e a senha não foi fornecida, não há nada a validar aqui.
        if self.instance and self.instance.pk and not password:
            return confirmar_password

        if password and confirmar_password and password != confirmar_password:
            raise forms.ValidationError("As senhas não coincidem.")
        return confirmar_password

    def save(self, commit=True):
        # Primeiro, salva o usuário ou o atualiza
        # Se é uma nova instância de Voluntario (sem pk) ou se não tem usuário associado
        is_new_voluntario = not (self.instance and self.instance.pk and hasattr(self.instance, 'usuario'))

        if is_new_voluntario:
            # Cria um novo usuário
            user = Usuario.objects.create_user(
                username=self.cleaned_data['username'],
                email=self.cleaned_data.get('email'), # .get() para campos opcionais
                password=self.cleaned_data['password']
            )
            # Define o tipo de usuário como Colaborador por padrão para voluntários
            user.tipo_usuario = 'COLAB' 
            if commit:
                user.save()
            self.instance.usuario = user
        else:
            # Atualiza o usuário existente
            user = self.instance.usuario
            user.username = self.cleaned_data['username']
            user.email = self.cleaned_data.get('email')
            # Atualiza a senha apenas se uma nova foi fornecida
            if self.cleaned_data.get("password"):
                user.set_password(self.cleaned_data["password"])
            if commit:
                user.save()
        
        # Agora salva a instância de Voluntario
        voluntario = super().save(commit=commit)
        return voluntario

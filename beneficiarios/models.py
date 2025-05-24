from django.db import models

class Beneficiario(models.Model):
    GENERO_CHOICES = [
        ('M', 'Masculino'),
        ('F', 'Feminino'),
        ('O', 'Outro'),
        ('NI', 'Não Informado'),
    ]

    ESCOLARIDADE_CHOICES = [
        ('FI', 'Fundamental Incompleto'),
        ('FC', 'Fundamental Completo'),
        ('MI', 'Médio Incompleto'),
        ('MC', 'Médio Completo'),
        ('SI', 'Superior Incompleto'),
        ('SC', 'Superior Completo'),
        ('PG', 'Pós-graduação'),
        ('NI', 'Não Informado'),
    ]

    nome_completo = models.CharField(max_length=255, verbose_name='Nome Completo')
    data_nascimento = models.DateField(verbose_name='Data de Nascimento')
    genero = models.CharField(max_length=2, choices=GENERO_CHOICES, default='NI', verbose_name='Gênero')
    cpf = models.CharField(max_length=14, unique=True, blank=True, null=True, verbose_name='CPF', help_text='Formato: XXX.XXX.XXX-XX (Opcional)')
    rg = models.CharField(max_length=20, blank=True, null=True, verbose_name='RG', help_text='(Opcional)')
    
    # Endereço
    cep = models.CharField(max_length=9, blank=True, null=True, verbose_name='CEP', help_text='Formato: XXXXX-XXX')
    logradouro = models.CharField(max_length=255, blank=True, null=True, verbose_name='Logradouro')
    numero_endereco = models.CharField(max_length=10, blank=True, null=True, verbose_name='Número')
    complemento_endereco = models.CharField(max_length=100, blank=True, null=True, verbose_name='Complemento')
    bairro = models.CharField(max_length=100, blank=True, null=True, verbose_name='Bairro')
    cidade = models.CharField(max_length=100, blank=True, null=True, verbose_name='Cidade')
    estado = models.CharField(max_length=2, blank=True, null=True, verbose_name='UF') # Sigla do estado, ex: SP

    # Contato
    telefone_principal = models.CharField(max_length=20, blank=True, null=True, verbose_name='Telefone Principal', help_text='Formato: (XX) XXXXX-XXXX')
    telefone_secundario = models.CharField(max_length=20, blank=True, null=True, verbose_name='Telefone Secundário', help_text='(Opcional)')
    email = models.EmailField(max_length=255, blank=True, null=True, verbose_name='E-mail')

    # Informações Socioeconômicas e Educacionais
    escolaridade = models.CharField(max_length=2, choices=ESCOLARIDADE_CHOICES, default='NI', verbose_name='Escolaridade')
    ocupacao = models.CharField(max_length=100, blank=True, null=True, verbose_name='Ocupação/Profissão')
    renda_familiar_aproximada = models.DecimalField(
        max_digits=10, decimal_places=2, blank=True, null=True, 
        verbose_name='Renda Familiar Mensal Aproximada (R$)',
        help_text='Valor em Reais. Ex: 1500.50'
    )
    
    # Outras informações
    como_conheceu_ong = models.TextField(blank=True, null=True, verbose_name='Como conheceu a ONG?')
    observacoes = models.TextField(blank=True, null=True, verbose_name='Observações Adicionais')
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name='Data de Cadastro')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')

    # Campo para calcular idade (não armazenado, mas pode ser um property no modelo)
    @property
    def idade(self):
        from datetime import date
        today = date.today()
        return today.year - self.data_nascimento.year - ((today.month, today.day) < (self.data_nascimento.month, self.data_nascimento.day))

    class Meta:
        verbose_name = 'Beneficiário'
        verbose_name_plural = 'Beneficiários'
        ordering = ['nome_completo']

    def __str__(self):
        return self.nome_completo

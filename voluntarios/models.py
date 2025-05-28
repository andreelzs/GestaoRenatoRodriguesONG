from django.db import models
from django.conf import settings

class Voluntario(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        verbose_name='Usuário',
        help_text='Conta de usuário associada a este voluntário.'
    )
    nome_completo = models.CharField(max_length=255, verbose_name='Nome Completo')
    cpf = models.CharField(max_length=14, unique=True, verbose_name='CPF', help_text='Formato: XXX.XXX.XXX-XX')
    data_nascimento = models.DateField(verbose_name='Data de Nascimento')
    telefone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Telefone Celular', help_text='Formato: (XX) XXXXX-XXXX')
    
    # Endereço
    cep = models.CharField(max_length=9, blank=True, null=True, verbose_name='CEP', help_text='Formato: XXXXX-XXX')
    logradouro = models.CharField(max_length=255, blank=True, null=True, verbose_name='Logradouro')
    numero_endereco = models.CharField(max_length=10, blank=True, null=True, verbose_name='Número')
    complemento_endereco = models.CharField(max_length=100, blank=True, null=True, verbose_name='Complemento')
    bairro = models.CharField(max_length=100, blank=True, null=True, verbose_name='Bairro')
    cidade = models.CharField(max_length=100, blank=True, null=True, verbose_name='Cidade')
    estado = models.CharField(max_length=2, blank=True, null=True, verbose_name='UF') # Sigla do estado, ex: SP

    areas_interesse = models.TextField(blank=True, null=True, verbose_name='Áreas de Interesse', help_text='Descreva as áreas em que o voluntário tem interesse em atuar.')
    
    # Disponibilidade Semanal
    disp_seg_m = models.BooleanField(default=False, verbose_name='Segunda (Manhã)')
    disp_seg_t = models.BooleanField(default=False, verbose_name='Segunda (Tarde)')
    disp_seg_n = models.BooleanField(default=False, verbose_name='Segunda (Noite)')
    disp_ter_m = models.BooleanField(default=False, verbose_name='Terça (Manhã)')
    disp_ter_t = models.BooleanField(default=False, verbose_name='Terça (Tarde)')
    disp_ter_n = models.BooleanField(default=False, verbose_name='Terça (Noite)')
    disp_qua_m = models.BooleanField(default=False, verbose_name='Quarta (Manhã)')
    disp_qua_t = models.BooleanField(default=False, verbose_name='Quarta (Tarde)')
    disp_qua_n = models.BooleanField(default=False, verbose_name='Quarta (Noite)')
    disp_qui_m = models.BooleanField(default=False, verbose_name='Quinta (Manhã)')
    disp_qui_t = models.BooleanField(default=False, verbose_name='Quinta (Tarde)')
    disp_qui_n = models.BooleanField(default=False, verbose_name='Quinta (Noite)')
    disp_sex_m = models.BooleanField(default=False, verbose_name='Sexta (Manhã)')
    disp_sex_t = models.BooleanField(default=False, verbose_name='Sexta (Tarde)')
    disp_sex_n = models.BooleanField(default=False, verbose_name='Sexta (Noite)')
    disp_sab_m = models.BooleanField(default=False, verbose_name='Sábado (Manhã)')
    disp_sab_t = models.BooleanField(default=False, verbose_name='Sábado (Tarde)')
    disp_sab_n = models.BooleanField(default=False, verbose_name='Sábado (Noite)')
    disp_dom_m = models.BooleanField(default=False, verbose_name='Domingo (Manhã)')
    disp_dom_t = models.BooleanField(default=False, verbose_name='Domingo (Tarde)')
    disp_dom_n = models.BooleanField(default=False, verbose_name='Domingo (Noite)')

    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name='Data de Cadastro')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')

    class Meta:
        verbose_name = 'Voluntário'
        verbose_name_plural = 'Voluntários'
        ordering = ['nome_completo']

    def __str__(self):
        return self.nome_completo

    def get_disponibilidade_formatada(self):
        dias_semana = [
            ("Segunda", self.disp_seg_m, self.disp_seg_t, self.disp_seg_n),
            ("Terça", self.disp_ter_m, self.disp_ter_t, self.disp_ter_n),
            ("Quarta", self.disp_qua_m, self.disp_qua_t, self.disp_qua_n),
            ("Quinta", self.disp_qui_m, self.disp_qui_t, self.disp_qui_n),
            ("Sexta", self.disp_sex_m, self.disp_sex_t, self.disp_sex_n),
            ("Sábado", self.disp_sab_m, self.disp_sab_t, self.disp_sab_n),
            ("Domingo", self.disp_dom_m, self.disp_dom_t, self.disp_dom_n),
        ]
        turnos_nomes = ["Manhã", "Tarde", "Noite"]
        disponibilidade_formatada = []
        
        for nome_dia, disp_m, disp_t, disp_n in dias_semana:
            turnos_do_dia = []
            if disp_m:
                turnos_do_dia.append(turnos_nomes[0])
            if disp_t:
                turnos_do_dia.append(turnos_nomes[1])
            if disp_n:
                turnos_do_dia.append(turnos_nomes[2])
            
            if turnos_do_dia:
                disponibilidade_formatada.append({
                    'dia': nome_dia,
                    'turnos': ", ".join(turnos_do_dia)
                })
        return disponibilidade_formatada

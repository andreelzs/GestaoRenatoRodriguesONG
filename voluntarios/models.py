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
    endereco = models.TextField(blank=True, null=True, verbose_name='Endereço Completo')
    areas_interesse = models.TextField(blank=True, null=True, verbose_name='Áreas de Interesse', help_text='Descreva as áreas em que o voluntário tem interesse em atuar.')
    disponibilidade = models.TextField(blank=True, null=True, verbose_name='Disponibilidade', help_text='Ex: Segundas e Quartas à tarde, Finais de semana.')
    data_cadastro = models.DateTimeField(auto_now_add=True, verbose_name='Data de Cadastro')
    ativo = models.BooleanField(default=True, verbose_name='Ativo')

    class Meta:
        verbose_name = 'Voluntário'
        verbose_name_plural = 'Voluntários'
        ordering = ['nome_completo']

    def __str__(self):
        return self.nome_completo

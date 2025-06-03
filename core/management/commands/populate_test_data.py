import datetime
from django.core.management.base import BaseCommand
from django.utils import timezone
from contas.models import Usuario
from voluntarios.models import Voluntario
from tarefas.models import Tarefa

class Command(BaseCommand):
    help = 'Populates the database with sample test data for Voluntarios and Tarefas.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting to populate test data...'))

        users_volunteers_data = [
            {'username': 'voluntario_ana', 'password': 'password123', 'email': 'ana.silva@example.com', 
             'first_name': 'Ana', 'last_name': 'Silva', 'cpf': '111.111.111-11', 
             'data_nascimento': datetime.date(1990, 5, 15), 'telefone': '(11) 91111-1111',
             'areas_interesse': 'Eventos, Arrecadação de fundos', 'disponibilidade': 'Finais de semana'},
            {'username': 'voluntario_bruno', 'password': 'password123', 'email': 'bruno.costa@example.com',
             'first_name': 'Bruno', 'last_name': 'Costa', 'cpf': '222.222.222-22',
             'data_nascimento': datetime.date(1985, 8, 20), 'telefone': '(21) 92222-2222',
             'areas_interesse': 'Aulas de reforço, Mentoria', 'disponibilidade': 'Terças e Quintas à noite'},
            {'username': 'colaborador_carlos', 'password': 'password123', 'email': 'carlos.adm@example.com',
             'first_name': 'Carlos', 'last_name': 'Pereira', 'tipo_usuario': 'ADMIN'} # Not a volunteer, just an admin/collab
        ]

        created_volunteers = []
        created_users = []

        for data in users_volunteers_data:
            user, created = Usuario.objects.get_or_create(
                username=data['username'],
                defaults={
                    'email': data.get('email', ''),
                    'first_name': data.get('first_name', ''),
                    'last_name': data.get('last_name', ''),
                    'tipo_usuario': data.get('tipo_usuario', 'COLAB')
                }
            )
            if created:
                user.set_password(data['password'])
                user.save()
                self.stdout.write(self.style.SUCCESS(f'User "{user.username}" created.'))
            else:
                self.stdout.write(self.style.WARNING(f'User "{user.username}" already exists.'))
            created_users.append(user)

            if 'cpf' in data: # This user is also a volunteer
                voluntario, v_created = Voluntario.objects.get_or_create(
                    cpf=data['cpf'],
                    defaults={
                        'usuario': user,
                        'nome_completo': f"{data['first_name']} {data['last_name']}",
                        'data_nascimento': data['data_nascimento'],
                        'telefone': data.get('telefone'),
                        'endereco': f"Rua Fictícia {len(created_volunteers)+1}, Bairro Exemplo",
                        'areas_interesse': data.get('areas_interesse'),
                        'disponibilidade': data.get('disponibilidade'),
                        'ativo': True
                    }
                )
                if v_created:
                    self.stdout.write(self.style.SUCCESS(f'Voluntario "{voluntario.nome_completo}" created.'))
                    created_volunteers.append(voluntario)
                else:
                    self.stdout.write(self.style.WARNING(f'Voluntario com CPF "{data["cpf"]}" already exists.'))
        
        admin_user = Usuario.objects.filter(tipo_usuario='ADMIN').first()
        if not admin_user and created_users:
            admin_user = created_users[0]

        tarefas_data = [
            {'titulo': 'Organizar doações de alimentos', 'descricao': 'Separar e catalogar alimentos doados esta semana.', 
             'status': 'PEND', 'prioridade': 3, 'data_prevista_conclusao': timezone.now().date() + datetime.timedelta(days=7),
             'voluntario_responsavel': created_volunteers[0] if len(created_volunteers) > 0 else None,
             'atribuido_por': admin_user},
            {'titulo': 'Planejar evento de arrecadação', 'descricao': 'Definir data, local e atividades para o próximo evento.',
             'status': 'FAZE', 'prioridade': 4, 'data_prevista_conclusao': timezone.now().date() + datetime.timedelta(days=30),
             'atribuido_por': admin_user},
            {'titulo': 'Atualizar site da ONG', 'descricao': 'Publicar novas fotos e notícias no site.',
             'status': 'PEND', 'prioridade': 2,
             'voluntario_responsavel': created_volunteers[1] if len(created_volunteers) > 1 else None,
             'atribuido_por': admin_user},
            {'titulo': 'Ligar para doadores', 'descricao': 'Agradecer aos doadores recentes pelas contribuições.',
             'status': 'CONC', 'prioridade': 1, 'data_prevista_conclusao': timezone.now().date() - datetime.timedelta(days=2),
             'data_conclusao_efetiva': timezone.now().date() - datetime.timedelta(days=1),
             'atribuido_por': admin_user},
            {'titulo': 'Preparar material para aula de reforço', 'descricao': 'Criar apostilas e exercícios para as crianças.',
             'status': 'PEND', 'prioridade': 3,
             'voluntario_responsavel': created_volunteers[0] if len(created_volunteers) > 0 else None,
             'atribuido_por': admin_user}
        ]

        for data_t in tarefas_data:
            tarefa, t_created = Tarefa.objects.get_or_create(
                titulo=data_t['titulo'],
                defaults=data_t
            )
            if t_created:
                self.stdout.write(self.style.SUCCESS(f'Tarefa "{tarefa.titulo}" created.'))
            else:
                self.stdout.write(self.style.WARNING(f'Tarefa "{data_t["titulo"]}" already exists.'))

        self.stdout.write(self.style.SUCCESS('Successfully populated test data.'))

from django.urls import path
from . import views

app_name = 'cursos'

urlpatterns = [
    path('beneficiario/<int:beneficiario_id>/adicionar_certificado/', views.adicionar_certificado_beneficiario, name='adicionar_certificado_beneficiario'),
    path('certificado/<int:certificado_id>/editar/', views.editar_certificado_beneficiario, name='editar_certificado_beneficiario'),
    path('certificado/<int:certificado_id>/excluir/', views.excluir_certificado_beneficiario, name='excluir_certificado_beneficiario'),

    # URLs para Gerenciamento de Cursos da ONG
    path('gerenciar/', views.CursoListView.as_view(), name='listar_cursos_ong'),
    path('gerenciar/novo/', views.CursoCreateView.as_view(), name='criar_curso_ong'),
    path('gerenciar/<int:pk>/editar/', views.CursoUpdateView.as_view(), name='editar_curso_ong'),
    path('gerenciar/<int:pk>/excluir/', views.CursoDeleteView.as_view(), name='excluir_curso_ong'),
]

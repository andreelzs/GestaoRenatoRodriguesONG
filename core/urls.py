from django.urls import path
from . import views # Importaremos as views deste app

app_name = 'core' # Define um namespace para as URLs deste app

urlpatterns = [
    path('', views.pagina_inicial, name='pagina_inicial'),
]

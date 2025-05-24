from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views
from django.urls import reverse_lazy

class LoginUsuarioView(auth_views.LoginView):
    template_name = 'contas/login.html'
    # Se o login for bem-sucedido, redireciona para a página inicial do core.
    # Você pode mudar para 'dashboard:painel_principal' ou outra página depois.
    success_url = reverse_lazy('core:pagina_inicial') 

    def form_valid(self, form):
        # Adicionar qualquer lógica extra aqui se necessário após o login válido
        # Por exemplo, adicionar uma mensagem de boas-vindas.
        # from django.contrib import messages
        # messages.success(self.request, f"Bem-vindo(a) de volta, {form.get_user().username}!")
        return super().form_valid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            # Se o usuário já está logado, redireciona para a success_url
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)


class LogoutUsuarioView(auth_views.LogoutView):
    # Após o logout, redireciona para a página inicial do core.
    next_page = reverse_lazy('core:pagina_inicial')

    def dispatch(self, request, *args, **kwargs):
        # Adicionar uma mensagem de logout se desejar
        # from django.contrib import messages
        # if request.user.is_authenticated:
        #     messages.info(request, "Você saiu do sistema.")
        return super().dispatch(request, *args, **kwargs)

# Futuramente, podemos adicionar uma view de cadastro aqui:
# from .forms import FormularioCadastroUsuario
# def cadastro_usuario_view(request):
#     if request.method == 'POST':
#         form = FormularioCadastroUsuario(request.POST)
#         if form.is_valid():
#             user = form.save()
#             # login(request, user) # Opcional: logar o usuário após o cadastro
#             # messages.success(request, 'Cadastro realizado com sucesso! Faça o login.')
#             return redirect('contas:login')
#     else:
#         form = FormularioCadastroUsuario()
#     return render(request, 'contas/cadastro.html', {'form': form})

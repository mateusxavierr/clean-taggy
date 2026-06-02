from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistroClienteForm

def register_view(request):
    # Bloqueia quem já está logado de acessar a página de cadastro
    if request.user.is_authenticated:
        return redirect('dashboard')
        
    if request.method == 'POST':
        form = RegistroClienteForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Faz login do usuário e redireciona automaticamente (Critério de Aceite)
            login(request, user)
            return redirect('dashboard')
    else:
        form = RegistroClienteForm()
        
    return render(request, 'registration/register.html', {'form': form})
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Veiculo

@login_required
def profile(request):
    veiculo_atual = Veiculo.objects.filter(usuario=request.user).first()

    if request.method == 'POST':
        modelo = request.POST.get('modelo')
        placa = request.POST.get('placa')
        tipo_combustivel = request.POST.get('tipo_combustivel')
        categoria = request.POST.get('categoria')
        rendimento = request.POST.get('rendimento_exato')

        if rendimento == '' or rendimento is None:
            rendimento_final = None
        else:
            rendimento_final = float(rendimento.replace(',', '.')) 

        if not veiculo_atual:
            veiculo_atual = Veiculo(usuario=request.user)

        veiculo_atual.modelo = modelo
        veiculo_atual.placa = placa
        veiculo_atual.tipo_combustivel = tipo_combustivel
        veiculo_atual.categoria = categoria
        veiculo_atual.rendimento_exato = rendimento_final
        veiculo_atual.save()

        return redirect('profile') 

    contexto = {
        'veiculo': veiculo_atual
    }

    return render(request, 'api/perfil.html', contexto)
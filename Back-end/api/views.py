<<<<<<< Updated upstream
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Veiculo
=======
from django.shortcuts import render
import json
from .models import Transacao
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Veiculo, RegistroEmissao
from .utils import calcular_emissao_co2
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Veiculo

@login_required
def perfil_usuario(request):
    veiculo_atual = Veiculo.objects.filter(usuario=request.user).first()

    if request.method =='POST':
        modelo = request.POST.get('modelo')
        placa = request.POST.get('placa')
        tipo_combustivel = request.POST.get('tipo_combustivel')
        categoria = request.POST.get('categoria')
        rendimento = request.POST.get('rendimento_exato')

        if rendimento == '' or rendimento is None:
            redimento_final = None
        else:
            rendimento_final = float(rendimento.replace(',','.'))

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

    return render(request, 'api/profile.html', contexto)



@csrf_exempt

def calcular_impacto_viagem(request):
    if request.method != 'POST':
        return JsonResponse({'error': 'Método não permitido. Utilize POST.'}, status=405)

    try:
        data = json.loads(request.body)
        veiculo_id = data.get('veiculo_id')
        distancia_km = data.get('distancia_km')
            
        if not veiculo_id or not distancia_km:
            return JsonResponse({'error': 'Parâmetros obrigatórios: veiculo_id, distancia_km'}, status=400)

        veiculo = Veiculo.objects.get(id=veiculo_id)

        total_co2 = calcular_emissao_co2(
            combustivel = veiculo.tipo_combustivel,
            categoria_veiculo= veiculo.categoria,
            distancia_km = distancia_km,
            rendimento_exato = veiculo.rendimento_exato
        )

        novo_registro = RegistroEmissao.objects.create (
            veiculo = veiculo,
            distancia_percorrida = distancia_km,
            co2_emitido_kg = total_co2,
            usou_fallback = (veiculo.rendimento_exato is None)
        )

        return JsonResponse({
        'status': 'sucesso',
        'registro_id': novo_registro.id,
        'co2_emitido_kg': total_co2,
        'metodologia': 'Média INMETRO (PBEV)' if veiculo.rendimento_exato is None else 'Consumo Exato Informado'
    }, status=201)
        
    except Veiculo.DoesNotExist:
        return JsonResponse({'erro': 'Veículo não encontrado no sistema.'}, status=404)
    except ValueError:
        return JsonResponse({'erro': 'Dados numéricos inválidos para a distância.'}, status=400)
    except Exception as e:
        return JsonResponse({'erro': f'Erro interno no servidor: {str(e)}'}, status=500)

@login_required
def dashboard(request):
    # Aqui simulamos os dados que virão do banco futuramente
    transacoes = Transacao.objects.all().order_by('-data')

    total_co2 = sum(t.co2_economizado for t in transacoes)
    
    context = {
        'transacoes': transacoes,
        'total_co2': total_co2,
        'nome_usuario': 'Gabriel',
        'co2_evitado': '14.2',
        'distancia_km': '432',
        'gastos_reais': '86,50',
        'ultima_passagem': {
            'local': 'Pedágio Rodoanel Sul',
            'data': 'Hoje, 08:42',
            'valor': '9,20'
        }
    }
    

    return render(request, 'api/dashboard.html', context)

@login_required
def history(request):
    # Simulando a lista de passagens 
    history_data = [
        { "id": 1, "location": "Pedágio Rodoanel Sul", "date": "Hoje, 08:42", "amount": "9,20", "savedCo2": "0.2kg", "status": "Pago" },
        { "id": 2, "location": "Pedágio Imigrantes", "date": "Ontem, 18:15", "amount": "33,80", "savedCo2": "0.5kg", "status": "Pago" },
        { "id": 3, "location": "Pedágio Anchieta", "date": "Ontem, 07:30", "amount": "33,80", "savedCo2": "0.4kg", "status": "Pago" },
        { "id": 4, "location": "Pedágio Castello Branco", "date": "12 Mar, 19:40", "amount": "5,40", "savedCo2": "0.1kg", "status": "Pago" },
        { "id": 5, "location": "Pedágio Bandeirantes", "date": "10 Mar, 08:10", "amount": "11,20", "savedCo2": "0.3kg", "status": "Pago" },
    ]
    return render(request, 'api/history.html', {'history_data': history_data})

@login_required
def sustainability(request):
    eco_tips = [
        { "id": 1, "title": "Aceleração Gradual", "desc": "Arranques bruscos gastam mais. Acelere suavemente para cortar até 20% das emissões.", "icon": "gauge", "color": "text-blue-500", "bg": "bg-blue-50", "impact": "Alto Impacto" },
        { "id": 2, "title": "Pressão dos Pneus", "desc": "Pneus descalibrados aumentam o atrito. Verifique a calibragem a cada 15 dias.", "icon": "activity", "color": "text-amber-500", "bg": "bg-amber-50", "impact": "Médio Impacto" },
        { "id": 3, "title": "Uso do Ar-Condicionado", "desc": "Abaixo de 60km/h, abrir as janelas é mais eficiente que o ar-condicionado.", "icon": "thermometer-sun", "color": "text-sky-500", "bg": "bg-sky-50", "impact": "Médio Impacto" },
        { "id": 4, "title": "Manutenção em Dia", "desc": "Filtros limpos garantem a queima ideal, emitindo menos gases tóxicos.", "icon": "settings", "color": "text-purple-500", "bg": "bg-purple-50", "impact": "Alto Impacto" }
    ]
    
    context = {
        'co2_evitado': '14.2',
        'eco_tips': eco_tips
    }
    return render(request, 'api/sustainability.html', context)

@login_required
def community(request):
    ranking_data = [
        { "id": 1, "name": "Maria S.", "points": "18.5kg", "rank": 1, "avatar": "https://images.unsplash.com/photo-1580489944761-15a19d654956?q=80&w=100", "isMe": False },
        { "id": 2, "name": "Gabriel", "points": "14.2kg", "rank": 2, "avatar": "https://images.unsplash.com/photo-1623366302587-b38b1ddaefd9?q=80&w=100", "isMe": True },
        { "id": 3, "name": "Carlos M.", "points": "12.0kg", "rank": 3, "avatar": "https://images.unsplash.com/photo-1659725642410-f00aa78876be?q=80&w=100", "isMe": False },
    ]

    challenges_data = [
        { "id": 1, "title": "Semana sem Ar-Condicionado", "desc": "Faça 5 viagens sem ligar o ar-condicionado em trechos urbanos.", "icon": "zap", "color": "text-purple-500", "bg": "bg-purple-50", "progress": "3/5", "percent": "60%" },
        { "id": 2, "title": "Mestre da Calibragem", "desc": "Registre a calibragem dos pneus no app por 2 quinzenas seguidas.", "icon": "shield-check", "color": "text-blue-500", "bg": "bg-blue-50", "progress": "1/2", "percent": "50%" },
    ]

    return render(request, 'api/community.html', {
        'ranking': ranking_data,
        'challenges': challenges_data
    })
>>>>>>> Stashed changes

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

        if rendimento_final is None:
            veiculo_atual.categoria = obter_categoria_por_modelo(modelo)
        else:
            veiculo_atual.categoria = None

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

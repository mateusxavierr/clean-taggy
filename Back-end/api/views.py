from django.db.models import Sum
from django.shortcuts import render
import json
from .models import Transacao
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Veiculo, RegistroEmissao
from .utils import calcular_emissao_co2, obter_categoria_por_modelo
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Veiculo

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
    transacoes = Transacao.objects.filter(usuario=request.user).order_by('-data')
    
    total_co2 = transacoes.aggregate(Sum('co2_economizado'))['co2_economizado__sum'] or 0.0
    gastos_reais = transacoes.aggregate(Sum('valor_pedagio'))['valor_pedagio__sum'] or 0.0
    
    registros = RegistroEmissao.objects.filter(veiculo__usuario=request.user)
    distancia_km = registros.aggregate(Sum('distancia_percorrida'))['distancia_percorrida__sum'] or 0.0
    
    ultima_passagem_obj = transacoes.first()
    if ultima_passagem_obj:
        ultima_passagem = {
            'local': ultima_passagem_obj.local,
            'data': ultima_passagem_obj.data.strftime('%d/%m/%Y %H:%M'),
            'valor': f"{ultima_passagem_obj.valor_pedagio:.2f}".replace('.', ',')
        }
    else:
        ultima_passagem = None

    context = {
        'transacoes': transacoes[:5],  # Enviando as últimas 5
        'total_co2': f"{total_co2:.2f}",
        'nome_usuario': request.user.first_name or request.user.username,
        'co2_evitado': f"{total_co2:.2f}",
        'distancia_km': f"{distancia_km:.0f}",
        'gastos_reais': f"{gastos_reais:.2f}".replace('.', ','),
        'ultima_passagem': ultima_passagem
    }
    

    return render(request, 'api/dashboard.html', context)

@login_required
def history(request):
    transacoes = Transacao.objects.filter(usuario=request.user).order_by('-data')
    history_data = []
    for t in transacoes:
        history_data.append({
            "id": t.id,
            "location": t.local,
            "date": t.data.strftime('%d %b, %H:%M'),
            "amount": f"{t.valor_pedagio:.2f}".replace('.', ','),
            "savedCo2": f"{t.co2_economizado:.2f}kg",
            "status": "Pago"
        })
    return render(request, 'api/history.html', {'history_data': history_data})

@login_required
def sustainability(request):
    transacoes = Transacao.objects.filter(usuario=request.user)
    total_co2 = transacoes.aggregate(Sum('co2_economizado'))['co2_economizado__sum'] or 0.0

    eco_tips = [
        { "id": 1, "title": "Aceleração Gradual", "desc": "Arranques bruscos gastam mais. Acelere suavemente para cortar até 20% das emissões.", "icon": "gauge", "color": "text-blue-500", "bg": "bg-blue-50", "impact": "Alto Impacto" },
        { "id": 2, "title": "Pressão dos Pneus", "desc": "Pneus descalibrados aumentam o atrito. Verifique a calibragem a cada 15 dias.", "icon": "activity", "color": "text-amber-500", "bg": "bg-amber-50", "impact": "Médio Impacto" },
        { "id": 3, "title": "Uso do Ar-Condicionado", "desc": "Abaixo de 60km/h, abrir as janelas é mais eficiente que o ar-condicionado.", "icon": "thermometer-sun", "color": "text-sky-500", "bg": "bg-sky-50", "impact": "Médio Impacto" },
        { "id": 4, "title": "Manutenção em Dia", "desc": "Filtros limpos garantem a queima ideal, emitindo menos gases tóxicos.", "icon": "settings", "color": "text-purple-500", "bg": "bg-purple-50", "impact": "Alto Impacto" }
    ]
    
    context = {
        'co2_evitado': f"{total_co2:.2f}",
        'eco_tips': eco_tips
    }
    return render(request, 'api/sustainability.html', context)

@login_required
def community(request):
    from django.contrib.auth.models import User
    users = User.objects.annotate(total_co2=Sum('transacao__co2_economizado')).filter(total_co2__gt=0).order_by('-total_co2')
    
    ranking_data = []
    for index, u in enumerate(users[:10], start=1):
        ranking_data.append({
            "id": u.id,
            "name": u.first_name or u.username,
            "points": f"{u.total_co2:.1f}kg",
            "rank": index,
            "avatar": f"https://ui-avatars.com/api/?name={u.username}&background=random",
            "isMe": (u.id == request.user.id)
        })

    challenges_data = [
        { "id": 1, "title": "Semana sem Ar-Condicionado", "desc": "Faça 5 viagens sem ligar o ar-condicionado em trechos urbanos.", "icon": "zap", "color": "text-purple-500", "bg": "bg-purple-50", "progress": "3/5", "percent": "60%" },
        { "id": 2, "title": "Mestre da Calibragem", "desc": "Registre a calibragem dos pneus no app por 2 quinzenas seguidas.", "icon": "shield-check", "color": "text-blue-500", "bg": "bg-blue-50", "progress": "1/2", "percent": "50%" },
    ]

    return render(request, 'api/community.html', {
        'ranking': ranking_data,
        'challenges': challenges_data,
        'regiao_atual': 'São Paulo - SP'
    })

@login_required
def profile(request):
    veiculo_atual = Veiculo.objects.filter(usuario=request.user).first()

    if request.method == 'POST':
        marca = request.POST.get('marca')
        ano = request.POST.get('ano')
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

        veiculo_atual.marca = marca
        if ano and str(ano).isdigit():
            veiculo_atual.ano = int(ano)
        else:
            veiculo_atual.ano = None
        veiculo_atual.modelo = modelo
        veiculo_atual.placa = placa
        veiculo_atual.tipo_combustivel = tipo_combustivel
        
        if rendimento_final is None:
            veiculo_atual.categoria = obter_categoria_por_modelo(modelo)
        else:
            veiculo_atual.categoria = None
            
        veiculo_atual.rendimento_exato = rendimento_final
        veiculo_atual.save()

        return redirect('profile') 

    contexto = {
        'veiculo': veiculo_atual
    }

    return render(request, 'api/profile.html', contexto)
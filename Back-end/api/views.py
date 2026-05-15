from django.shortcuts import render
from .models import Transacao

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

def profile(request):
    return render(request, 'api/profile.html', {'nome_usuario': 'Gabriel T.'})

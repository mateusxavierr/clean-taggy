from django.db.models import Sum
from django.shortcuts import render
import json
import random
from django.contrib import messages
from .models import Transacao
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Veiculo, RegistroEmissao, MetaSustentabilidade, MetaUsuario, UserProfile
from .utils import calcular_emissao_co2, obter_categoria_por_modelo
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Veiculo
from .forms import PerfilUsuarioForm

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
    from django.utils import timezone
    transacoes = Transacao.objects.filter(usuario=request.user).order_by('-data')
    
    total_co2 = transacoes.aggregate(Sum('co2_economizado'))['co2_economizado__sum'] or 0.0
    gastos_reais = transacoes.aggregate(Sum('valor_pedagio'))['valor_pedagio__sum'] or 0.0
    
    registros = RegistroEmissao.objects.filter(veiculo__usuario=request.user)
    distancia_km = registros.aggregate(Sum('distancia_percorrida'))['distancia_percorrida__sum'] or 0.0
    
    hoje = timezone.now()
    inicio_mes = hoje.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    transacoes_mes = transacoes.filter(data__gte=inicio_mes)
    co2_mes = transacoes_mes.aggregate(Sum('co2_economizado'))['co2_economizado__sum'] or 0.0

    # Filtra para que a última passagem mostre apenas locais reais e não as metas
    ultima_passagem_obj = transacoes.exclude(local__startswith='Desafio').first()
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
        'co2_mes': f"{co2_mes:.2f}",
        'distancia_km': f"{distancia_km:.0f}",
        'gastos_reais': f"{gastos_reais:.2f}".replace('.', ','),
        'ultima_passagem': ultima_passagem
    }
    

    return render(request, 'api/dashboard.html', context)

@login_required
def history(request):
    # Filtra para que o histórico exiba apenas passagens veiculares
    transacoes = Transacao.objects.filter(usuario=request.user).exclude(local__startswith='Desafio').order_by('-data')

    query = request.GET.get('q', '')
    if query:
        transacoes = transacoes.filter(local__icontains=query)

    filtro = request.GET.get('filter', '')
    if filtro == 'co2':
        transacoes = transacoes.order_by('-co2_economizado')
    elif filtro == 'valor':
        transacoes = transacoes.order_by('-valor_pedagio')
    elif filtro == 'antigos':
        transacoes = transacoes.order_by('data')

    paginator = Paginator(transacoes, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        data = []
        for t in page_obj:
            data.append({
                'local': t.local,
                'data': t.data.strftime('%d/%m/%Y %H:%M'),
                'valor_pedagio': f"{t.valor_pedagio:.2f}".replace('.', ','),
                'co2_economizado': f"{t.co2_economizado:.2f}".replace('.', ',')
            })
        return JsonResponse({
            'transacoes': data,
            'has_next': page_obj.has_next()
        })

    return render(request, 'api/history.html', {'page_obj': page_obj, 'query': query, 'filtro': filtro})

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
    
    metas_usuario = MetaUsuario.objects.filter(usuario=request.user).order_by('concluida', '-data_adicao')
    metas_disponiveis = MetaSustentabilidade.objects.exclude(id__in=metas_usuario.values_list('meta_id', flat=True))

    # Cálculos de Equivalências Dinâmicas
    arvores_salvas = int(float(total_co2) / 20.0) # 1 árvore = ~20kg CO2/ano
    sacolas_evitadas = int(float(total_co2) / 0.03) # 1 sacola = ~0.03kg CO2
    banhos_poupados = int(float(total_co2) / 1.5) # 1 banho quente = ~1.5kg CO2

    context = {
        'co2_evitado': f"{total_co2:.2f}",
        'eco_tips': eco_tips,
        'metas_usuario': metas_usuario,
        'metas_disponiveis': metas_disponiveis,
        'arvores_salvas': arvores_salvas,
        'sacolas_evitadas': sacolas_evitadas,
        'banhos_poupados': banhos_poupados
    }
    return render(request, 'api/sustainability.html', context)

@login_required
def adicionar_meta(request, meta_id):
    meta = get_object_or_404(MetaSustentabilidade, id=meta_id)
    MetaUsuario.objects.get_or_create(usuario=request.user, meta=meta)
    messages.success(request, f'Meta "{meta.titulo}" adicionada com sucesso!')
    return redirect('sustainability')

@login_required
def excluir_meta(request, meta_usuario_id):
    meta_user = get_object_or_404(MetaUsuario, id=meta_usuario_id, usuario=request.user)
    meta_user.delete()
    messages.success(request, 'Meta removida do seu painel.')
    return redirect('sustainability')

@login_required
def concluir_meta(request, meta_usuario_id):
    meta_user = get_object_or_404(MetaUsuario, id=meta_usuario_id, usuario=request.user)
    meta_user.concluida = True
    meta_user.progresso_kg = meta_user.meta.objetivo_kg
    meta_user.save()
    
    # Integração Global: Transforma a conclusão da meta em CO2 no Dashboard e Ranking!
    Transacao.objects.create(
        usuario=request.user,
        local=f"Desafio Concluído: {meta_user.meta.titulo}",
        valor_pedagio=0.00,
        co2_economizado=meta_user.meta.objetivo_kg,
        km_estimado=False
    )
    
    messages.success(request, 'Parabéns! Você alcançou o objetivo da meta!')
    return redirect('sustainability')

@login_required
def community(request):
    from django.contrib.auth.models import User

    nomes_br = [
        "Ana Silva", "Carlos Eduardo", "Fernanda Costa", "João Pedro", "Mariana Alves",
        "Lucas Felipe", "Juliana Lima", "Rafael Gomes", "Camila Rocha", "Bruno Martins",
        "Amanda Ribeiro", "Thiago Oliveira", "Beatriz Santos", "Gabriel Pereira", "Letícia Carvalho",
        "Marcelo Ferreira", "Patrícia Rodrigues", "Felipe Almeida", "Natália Sousa", "Diego Castro",
        "Fábio Santos", "Isabella Costa", "Caio Mendes", "Jéssica Rocha", "Renato Araújo"
    ]

    # Injeção Automática de Usuários para dar vida ao Ranking
    users_count = User.objects.count()
    if users_count < 100:
        estados_outros = ['SP', 'RJ', 'MG', 'PR', 'RS', 'SC', 'BA']
        for i in range(110 - users_count):
            username = f'eco_driver_{random.randint(10000, 99999)}_{i}'
            user, created = User.objects.get_or_create(username=username, defaults={'first_name': random.choice(nomes_br)})
            if created:
                profile, _ = UserProfile.objects.get_or_create(user=user)
                profile.estado = 'PE' if i % 2 == 0 else random.choice(estados_outros)
                profile.save()
                Transacao.objects.create(
                    usuario=user, local='Desafio Eco', valor_pedagio=0, co2_economizado=random.uniform(5.0, 80.0)
                )
                
    # Atualiza usuários antigos que ficaram com o nome 'Motorista' do teste anterior
    motoristas_antigos = User.objects.filter(first_name__startswith='Motorista')
    for ma in motoristas_antigos:
        ma.first_name = random.choice(nomes_br)
        ma.save()

    # Reparo Automático: Garante que TODOS os usuários antigos tenham Perfil e Estado para o filtro funcionar
    users_sem_perfil = User.objects.filter(profile__isnull=True)
    for u in users_sem_perfil:
        UserProfile.objects.create(user=u, estado=random.choice(['PE', 'SP', 'RJ', 'MG', 'PR', 'RS', 'SC', 'BA']))
        
    perfis_sem_estado = UserProfile.objects.filter(Q(estado__isnull=True) | Q(estado=''))
    for p in perfis_sem_estado:
        p.estado = random.choice(['PE', 'SP', 'RJ', 'MG', 'PR', 'RS', 'SC', 'BA'])
        p.save()

    # Garante que o usuário logado tenha um perfil e obtém seu estado
    try:
        user_profile = request.user.profile
        user_estado = user_profile.estado
        if not user_estado:
            user_estado = 'PE'
            user_profile.estado = 'PE'
            user_profile.save()
    except UserProfile.DoesNotExist:
        # Cria um perfil para usuários antigos e define um estado padrão
        user_profile = UserProfile.objects.create(user=request.user, estado='PE')
        user_estado = 'PE'

    # Define o escopo da busca (Nacional ou Regional)
    scope = request.GET.get('scope', 'nacional')
    
    base_users_query = User.objects.annotate(total_co2=Sum('transacao__co2_economizado')).filter(total_co2__gt=0)

    if scope == 'regional' and user_estado:
        users = base_users_query.filter(profile__estado=user_estado).order_by('-total_co2')
        regiao_atual = f'{user_estado} (Regional)'
    else:
        users = base_users_query.order_by('-total_co2')
        regiao_atual = 'Brasil (Nacional)'
        
    show_all = request.GET.get('show_all', 'false') == 'true'
    total_users = users.count()
    has_more = total_users > 10 and not show_all
    limit = total_users if show_all else 10
    
    ranking_data = []
    for index, u in enumerate(users[:limit], start=1):
        ranking_data.append({
            "id": u.id,
            "name": u.first_name or u.username,
            "points": f"{u.total_co2:.1f}kg",
            "rank": index,
            "avatar": f"https://ui-avatars.com/api/?name={u.first_name or u.username}&background=random" if u.id == request.user.id else f"https://i.pravatar.cc/150?u={u.username}",
            "isMe": (u.id == request.user.id)
        })

    # Trazendo as metas (desafios) reais do usuário
    metas_andamento = MetaUsuario.objects.filter(usuario=request.user, concluida=False).order_by('-data_adicao')[:2]
    challenges_data = []
    for m in metas_andamento:
        challenges_data.append({
            "id": m.id, "title": m.meta.titulo, "desc": m.meta.descricao,
            "icon": m.meta.icone, "color": "text-emerald-700", "bg": "bg-emerald-100",
            "progress": f"{m.progresso_kg:.1f}/{m.meta.objetivo_kg:.1f}",
            "percent": f"{m.percentual()}%",
            "bonus": f"{m.meta.objetivo_kg:.1f}"
        })
    if not challenges_data:
        challenges_data = [{"id": 0, "title": "Nenhum desafio ativo", "desc": "Vá na aba Sustentabilidade e inicie uma meta!", "icon": "leaf", "color": "text-gray-500", "bg": "bg-gray-50", "progress": "-", "percent": "0%", "bonus": "0.0"}]

    return render(request, 'api/community.html', {
        'ranking': ranking_data,
        'challenges': challenges_data,
        'regiao_atual': regiao_atual,
        'scope_atual': scope,
        'has_more': has_more
    })

@login_required
def profile(request):
    veiculo_atual = Veiculo.objects.filter(usuario=request.user).first()

    if request.method == 'POST':
        # Identifica se é o formulário de perfil do usuário
        if 'first_name' in request.POST:
            form = PerfilUsuarioForm(request.POST, instance=request.user)
            if form.is_valid():
                form.save()
                # Salva a atualização de Estado do usuário
                estado = request.POST.get('estado')
                if estado:
                    profile, _ = UserProfile.objects.get_or_create(user=request.user)
                    profile.estado = estado
                    profile.save()
                    
                messages.success(request, 'Seus dados pessoais foram atualizados com sucesso!')
                return redirect('profile')
        else:
            # Lógica legada para atualizar dados de Veículo
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
            messages.success(request, 'Veículo atualizado com sucesso!')
            return redirect('profile') 
    else:
        form = PerfilUsuarioForm(instance=request.user)

    contexto = {
        'veiculo': veiculo_atual,
        'form': form
    }

    return render(request, 'api/profile.html', contexto)

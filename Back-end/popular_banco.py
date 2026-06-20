import os
import django
import random
from decimal import Decimal
from datetime import timedelta
from django.utils import timezone

# Configura o ambiente do Django antes de qualquer importação
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.contrib.auth.models import User
from api.models import Veiculo, Transacao, RegistroEmissao, MetaSustentabilidade, MetaUsuario

def popular():
    print("Limpando dados antigos...")
    Transacao.objects.all().delete()
    RegistroEmissao.objects.all().delete()
    MetaUsuario.objects.all().delete()
    MetaSustentabilidade.objects.all().delete()

    # ==========================================
    # 1. CRIANDO USUÁRIO PRINCIPAL (Gabriel)
    # ==========================================
    print("Criando usuário principal Gabriel...")
    gabriel, _ = User.objects.get_or_create(username='gabriel_teste', defaults={'first_name': 'Gabriel', 'email': 'gabriel@cleantaggy.com'})
    gabriel.set_password('senha123')
    gabriel.save()

    veiculo_gabriel, _ = Veiculo.objects.get_or_create(
        usuario=gabriel,
        defaults={'marca': 'Volkswagen', 'ano': 2022, 'modelo': 'Polo', 'placa': 'ABC-1234', 'tipo_combustivel': 'GASOLINA', 'categoria': 'HATCH', 'rendimento_exato': 12.0}
    )

    locais = ['Pedágio Rodoanel Sul', 'Pedágio Imigrantes', 'Pedágio Anchieta', 'Pedágio Castello Branco', 'Pedágio Bandeirantes', 'Estacionamento Shopping', 'Estacionamento Aeroporto']

    print("Gerando 110 transações para o Gabriel (teste de paginação)...")
    for _ in range(110):
        data_t = timezone.now() - timedelta(days=random.randint(0, 30), hours=random.randint(0, 23), minutes=random.randint(0, 59))
        status_t = random.choice(['FATURADA', 'PENDENTE'])
        t = Transacao.objects.create(
            usuario=gabriel,
            local=random.choice(locais),
            valor_pedagio=Decimal(random.uniform(5.5, 38.0)).quantize(Decimal('0.00')),
            co2_economizado=Decimal(random.uniform(0.1, 1.2)).quantize(Decimal('0.00')),
            fator_co2=0.15,
            km_estimado=True,
            status=status_t
        )
        t.data = data_t
        t.save(update_fields=['data'])

        r = RegistroEmissao.objects.create(
            veiculo=veiculo_gabriel,
            distancia_percorrida=random.uniform(15.0, 120.0),
            co2_emitido_kg=random.uniform(1.0, 4.0),
            usou_fallback=False
        )
        r.data = data_t
        r.save(update_fields=['data'])

    # ==========================================
    # 2. CRIANDO 15 USUÁRIOS FAKES PRO RANKING
    # ==========================================
    print("Criando 15 usuários fictícios e suas transações...")
    nomes = ["Ana", "Carlos", "Maria", "João", "Fernanda", "Lucas", "Julia", "Pedro", "Beatriz", "Rafael", "Camila", "Bruno", "Letícia", "Felipe", "Sofia"]
    
    for nome in nomes:
        u, _ = User.objects.get_or_create(username=nome.lower(), defaults={'first_name': nome})
        u.set_password('senha123')
        u.save()

        for _ in range(random.randint(10, 25)):
            data_t = timezone.now() - timedelta(days=random.randint(0, 30), hours=random.randint(0, 23))
            status_t = random.choice(['FATURADA', 'PENDENTE'])
            t = Transacao.objects.create(
                usuario=u, local=random.choice(locais), valor_pedagio=Decimal(random.uniform(5.5, 38.0)).quantize(Decimal('0.00')),
                co2_economizado=Decimal(random.uniform(0.1, 1.8)).quantize(Decimal('0.00')), fator_co2=0.15, km_estimado=True, status=status_t
            )
            t.data = data_t; t.save(update_fields=['data'])

    # ==========================================
    # 3. CRIANDO CATÁLOGO DE METAS E ATRIBUINDO
    # ==========================================
    print("Criando Catálogo de Metas Sustentáveis...")
    metas_data = [
        {"titulo": "Pé de Pluma", "descricao": "Evite seus primeiros 2kg de CO2 com acelerações mais suaves.", "icone": "feather", "objetivo_kg": 2.0},
        {"titulo": "Janelas Abertas", "descricao": "Poupe 3kg de CO2 desligando o ar-condicionado em trechos urbanos.", "icone": "wind", "objetivo_kg": 3.0},
        {"titulo": "Fuga do Trânsito", "descricao": "Evite 5kg rodando em horários alternativos e fugindo do engarrafamento.", "icone": "clock", "objetivo_kg": 5.0},
        {"titulo": "Calibragem Perfeita", "descricao": "Economize 8kg mantendo a pressão dos pneus sempre ideal.", "icone": "circle-dashed", "objetivo_kg": 8.0},
        {"titulo": "Fluidez Taggy", "descricao": "Poupe 10kg passando direto por pedágios sem precisar parar ou arrancar.", "icone": "fast-forward", "objetivo_kg": 10.0},
        {"titulo": "Viajante Noturno", "descricao": "Economize 12kg de CO2 viajando em horários de menor fluxo.", "icone": "moon", "objetivo_kg": 12.0},
        {"titulo": "Fim de Semana Verde", "descricao": "Evite 15kg de CO2 em uma viagem de lazer eficiente.", "icone": "map", "objetivo_kg": 15.0},
        {"titulo": "Motor Afinadinho", "descricao": "Reduza 20kg de CO2 garantindo que filtros e velas estejam em dia.", "icone": "wrench", "objetivo_kg": 20.0},
        {"titulo": "Parceiro do Clima", "descricao": "Atinja a marca de 30kg de CO2 evitados na sua rotina.", "icone": "leaf", "objetivo_kg": 30.0},
        {"titulo": "Ecoviajante Frequente", "descricao": "Poupe 40kg acumulando viagens sustentáveis ao longo do mês.", "icone": "repeat", "objetivo_kg": 40.0},
        {"titulo": "Condutor Ouro", "descricao": "Conquiste 50kg de redução e seja um exemplo nas ruas.", "icone": "award", "objetivo_kg": 50.0},
        {"titulo": "Mestre da Inércia", "descricao": "Reduza 60kg de emissões otimizando a aceleração na estrada.", "icone": "trending-down", "objetivo_kg": 60.0},
        {"titulo": "Guardião do Ar Puro", "descricao": "Economize 75kg de CO2 e ajude a limpar nossa atmosfera.", "icone": "shield-check", "objetivo_kg": 75.0},
        {"titulo": "Lenda da Sustentabilidade", "descricao": "Alcance 100kg de CO2 evitados! O planeta agradece.", "icone": "crown", "objetivo_kg": 100.0},
        {"titulo": "Embaixador Taggy", "descricao": "Marca histórica: 150kg de CO2 poupados! Você é uma inspiração.", "icone": "globe", "objetivo_kg": 150.0},
    ]
    for m in metas_data:
        MetaSustentabilidade.objects.create(**m)

    meta1 = MetaSustentabilidade.objects.get(titulo="Motor Afinadinho")
    meta2 = MetaSustentabilidade.objects.get(titulo="Fluidez Taggy")
    MetaUsuario.objects.create(usuario=gabriel, meta=meta1, progresso_kg=14.2, concluida=False)
    MetaUsuario.objects.create(usuario=gabriel, meta=meta2, progresso_kg=10.0, concluida=True)

    print("\n✅ Massa de dados gerada com sucesso!\nFaça login com: usuário 'gabriel_teste' e senha 'senha123'.")

if __name__ == '__main__':
    popular()
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
        t = Transacao.objects.create(
            usuario=gabriel,
            local=random.choice(locais),
            valor_pedagio=Decimal(random.uniform(5.5, 38.0)).quantize(Decimal('0.00')),
            co2_economizado=Decimal(random.uniform(0.1, 1.2)).quantize(Decimal('0.00')),
            fator_co2=0.15,
            km_estimado=True
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
            t = Transacao.objects.create(
                usuario=u, local=random.choice(locais), valor_pedagio=Decimal(random.uniform(5.5, 38.0)).quantize(Decimal('0.00')),
                co2_economizado=Decimal(random.uniform(0.1, 1.8)).quantize(Decimal('0.00')), fator_co2=0.15, km_estimado=True
            )
            t.data = data_t; t.save(update_fields=['data'])

    # ==========================================
    # 3. CRIANDO CATÁLOGO DE METAS E ATRIBUINDO
    # ==========================================
    print("Criando Catálogo de Metas Sustentáveis...")
    metas_data = [
        {"titulo": "Iniciante Verde", "descricao": "Economize seus primeiros 5kg de CO2.", "icone": "leaf", "objetivo_kg": 5.0},
        {"titulo": "Semana Sustentável", "descricao": "Evite 10kg de CO2 em uma semana.", "icone": "calendar", "objetivo_kg": 10.0},
        {"titulo": "Motorista Consciente", "descricao": "Atinja 20kg de CO2 poupado.", "icone": "car", "objetivo_kg": 20.0},
        {"titulo": "Mestre da Redução", "descricao": "Reduza 50kg de CO2.", "icone": "award", "objetivo_kg": 50.0},
        {"titulo": "Viajante Ecológico", "descricao": "Evite 15kg de CO2 em viagens longas.", "icone": "map", "objetivo_kg": 15.0},
        {"titulo": "Ar Puro", "descricao": "Economize 8kg de CO2 melhorando a eficiência.", "icone": "wind", "objetivo_kg": 8.0},
        {"titulo": "Defensor do Clima", "descricao": "Atinja 30kg de CO2 poupado.", "icone": "shield-check", "objetivo_kg": 30.0},
        {"titulo": "Pé Leve", "descricao": "Reduza 12kg com acelerações suaves.", "icone": "gauge", "objetivo_kg": 12.0},
        {"titulo": "Eco-Milhas", "descricao": "Acumule 25kg de CO2 evitados em pedágios.", "icone": "milestone", "objetivo_kg": 25.0},
        {"titulo": "Guardião da Floresta", "descricao": "Alcance 40kg de CO2 evitado.", "icone": "tree-pine", "objetivo_kg": 40.0},
        {"titulo": "Atitude Sustentável", "descricao": "Poupe 7kg de CO2 no dia a dia.", "icone": "heart", "objetivo_kg": 7.0},
        {"titulo": "Mobilidade Limpa", "descricao": "Evite 18kg de CO2.", "icone": "zap", "objetivo_kg": 18.0},
        {"titulo": "Zero Fricção", "descricao": "Poupe 22kg de CO2 em pedágios sem parar.", "icone": "fast-forward", "objetivo_kg": 22.0},
        {"titulo": "Herói Verde", "descricao": "Alcance incríveis 100kg de CO2 poupado!", "icone": "crown", "objetivo_kg": 100.0},
        {"titulo": "Sintonia Eco", "descricao": "Evite 35kg de CO2 com manutenção em dia.", "icone": "settings", "objetivo_kg": 35.0},
    ]
    for m in metas_data:
        MetaSustentabilidade.objects.create(**m)

    meta1 = MetaSustentabilidade.objects.get(titulo="Iniciante Verde")
    meta2 = MetaSustentabilidade.objects.get(titulo="Semana Sustentável")
    MetaUsuario.objects.create(usuario=gabriel, meta=meta1, progresso_kg=3.5, concluida=False)
    MetaUsuario.objects.create(usuario=gabriel, meta=meta2, progresso_kg=10.0, concluida=True)

    print("\n✅ Massa de dados gerada com sucesso!\nFaça login com: usuário 'gabriel_teste' e senha 'senha123'.")

if __name__ == '__main__':
    popular()
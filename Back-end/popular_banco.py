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
from api.models import Veiculo, Transacao, RegistroEmissao

def popular():
    print("Limpando dados antigos...")
    Transacao.objects.all().delete()
    RegistroEmissao.objects.all().delete()

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

    print("Gerando pelo menos 30 transações para o Gabriel...")
    for _ in range(35):
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

    print("\n✅ Massa de dados gerada com sucesso!\nFaça login com: usuário 'gabriel_teste' e senha 'senha123'.")

if __name__ == '__main__':
    popular()
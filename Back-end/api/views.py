from django.http import JsonResponse
from .models import Transacao

def dashboard(request):
    transacoes = Transacao.objects.all()

    total_co2 = sum(
        transacao.co2_economizado
        for transacao in transacoes
    )

    total_pedagio = sum(
        transacao.valor_pedagio
        for transacao in transacoes
    )

    data = {
        "total_co2_economizado": float(total_co2),
        "total_pedagios": float(total_pedagio),
        "quantidade_transacoes": transacoes.count(),
    }

    return JsonResponse(data)

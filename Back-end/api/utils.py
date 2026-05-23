COEFICIENTES_GHG = {
    'GASOLINA': 1.614,
    'DIESEL': 2.238,
    'ETANOL': 0.000,
}

MEDIAS_INMETRO = {
    'HATCH': 13.5,
    'SEDAN': 10.0,
    'UTILITÁRIO': 7.5
}

def calcular_emissao_co2(combustivel, categoria_veiculo, distancia_km, rendimento_exato=None):
    
    combustivel_upper = combustivel.upper()
    categoria_upper = categoria_veiculo.upper()

    if rendimento_exato and float(rendimento_exato) > 0:
        rendimento = float(rendimento_exato)
    else:
        rendimento = MEDIAS_INMETRO.get(categoria_upper, 10.0)

    fator_emissao = COEFICIENTES_GHG.get(combustivel_upper, 1.614)

    co2_emitido = (fator_emissao / rendimento) * float(distancia_km)

    return round(co2_emitido, 3)
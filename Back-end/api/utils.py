COEFICIENTES_GHG = {
    'GASOLINA': 1.614,
    'DIESEL': 2.238,
    'ETANOL': 0.000,
}

MEDIAS_INMETRO = {
    'HATCH': 13.5,
    'SEDAN': 10.0,
    'UTILITARIO': 7.5
}

MAPEAMENTO_CATEGORIAS = {
    'ONIX': 'HATCH', 'ARGO': 'HATCH', 'MOBI': 'HATCH', 'UNO': 'HATCH',
    'POLO': 'HATCH', 'GOL': 'HATCH', 'FIT': 'HATCH', 'YARIS': 'HATCH', 'ETIOS': 'HATCH',
    'TRACKER': 'SEDAN', 'CRUZE': 'SEDAN', 'SPIN': 'SEDAN',
    'FASTBACK': 'SEDAN', 'PULSE': 'SEDAN',
    'NIVUS': 'SEDAN', 'T-CROSS': 'SEDAN', 'TAOS': 'SEDAN', 'VIRTUS': 'SEDAN',
    'CIVIC': 'SEDAN', 'HR-V': 'SEDAN', 'CITY': 'SEDAN',
    'COROLLA': 'SEDAN', 'COROLLA CROSS': 'SEDAN',
    'MONTANA': 'UTILITARIO', 'TORO': 'UTILITARIO', 'STRADA': 'UTILITARIO',
    'SAVEIRO': 'UTILITARIO', 'HILUX': 'UTILITARIO'
}

def obter_categoria_por_modelo(modelo):
    if not modelo:
        return 'HATCH'
    return MAPEAMENTO_CATEGORIAS.get(modelo.upper(), 'HATCH')

def calcular_emissao_co2(combustivel, categoria_veiculo, distancia_km, rendimento_exato=None):
    
    combustivel_upper = combustivel.upper() if combustivel else 'GASOLINA'
    categoria_upper = categoria_veiculo.upper() if categoria_veiculo else ''

    if rendimento_exato and float(rendimento_exato) > 0:
        rendimento = float(rendimento_exato)
    else:
        rendimento = MEDIAS_INMETRO.get(categoria_upper, 10.0)

    fator_emissao = COEFICIENTES_GHG.get(combustivel_upper, 1.614)

    co2_emitido = (fator_emissao / rendimento) * float(distancia_km)

    return round(co2_emitido, 3)
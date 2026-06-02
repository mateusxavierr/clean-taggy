def calcular_emissao_co2(distancia_km, rendimento, fator_emissao):
    """
    Metodologia de Cálculo de Emissões (GHG Protocol) - Tarefa 20
    
    Esta função aplica a metodologia científica padrão do Greenhouse Gas Protocol
    (GHG Protocol) para fontes móveis de combustão.
    
    Fórmula:
    Emissão (kg CO2) = (Distância percorrida / Rendimento do Veículo) * Fator de Emissão
    
    Args:
        distancia_km (float): Distância percorrida em quilômetros.
        rendimento (float): Rendimento do veículo (km/l).
        fator_emissao (float): Fator de emissão do combustível (kg CO2/l).
        
    Returns:
        float: Total de kg de CO2 emitidos. Retorna 0.0 em caso de erro no rendimento.
    """
    if rendimento <= 0:
        return 0.0
    
    litros_consumidos = distancia_km / rendimento
    return litros_consumidos * fator_emissao
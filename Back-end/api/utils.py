def calcular_emissao_co2(distancia_km, rendimento=None, fator_emissao=None, combustivel=None, categoria_veiculo=None, rendimento_exato=None):
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
        combustivel (str): Tipo de combustível do veículo.
        categoria_veiculo (str): Categoria do veículo (ex: HATCH, SEDAN).
        rendimento_exato (float): Rendimento exato do veículo (km/l).
        
    Returns:
        float: Total de kg de CO2 emitidos. Retorna 0.0 em caso de erro no rendimento.
    """
    # Definir fator de emissão padrão (GHG Protocol) com base no combustível
    if fator_emissao is None:
        fatores = {
            'GASOLINA': 2.31,
            'ETANOL': 1.50,
            'DIESEL': 2.68
        }
        fator_emissao = fatores.get(str(combustivel).upper(), 2.31)
        
    # Usar rendimento exato se disponível, senão usar o rendimento posicional ou fallback
    rendimento_usado = rendimento_exato if rendimento_exato is not None else rendimento
    
    if not rendimento_usado:
        # Metodologia de fallback para quando o usuário não informa o consumo
        fallbacks = {
            'HATCH': {'GASOLINA': 12.0, 'ETANOL': 8.5, 'DIESEL': 14.0},
            'SEDAN': {'GASOLINA': 10.0, 'ETANOL': 7.0, 'DIESEL': 12.0},
            'UTILITARIO': {'GASOLINA': 8.0, 'ETANOL': 6.0, 'DIESEL': 10.0},
        }
        cat = str(categoria_veiculo).upper() if categoria_veiculo else 'HATCH'
        comb = str(combustivel).upper() if combustivel else 'GASOLINA'
        rendimento_usado = fallbacks.get(cat, fallbacks['HATCH']).get(comb, 10.0)

    if rendimento_usado <= 0:
        return 0.0
    
    litros_consumidos = distancia_km / rendimento_usado
    return litros_consumidos * fator_emissao

def obter_categoria_por_modelo(modelo):
    if not modelo:
        return 'HATCH'
    modelo_lower = modelo.lower()
    if any(m in modelo_lower for m in ['suv', 'sedan', 'corolla', 'civic', 'compass', 'renegade', 'cruze', 'jetta']):
        return 'SEDAN'
    if any(m in modelo_lower for m in ['picape', 'hilux', 's10', 'ranger', 'amarok', 'toro', 'saveiro', 'strada']):
        return 'UTILITARIO'
    return 'HATCH'
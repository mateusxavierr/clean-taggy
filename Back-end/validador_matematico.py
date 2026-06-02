import sys

def simular_calculo_ghg(distancia_km, rendimento, fator_combustivel):
    """
    Simula o cálculo matemático baseado na Tarefa 08 (GHG Protocol).
    Fórmula: (Distância / Rendimento) * Fator de Emissão do Combustível
    """
    litros_consumidos = distancia_km / rendimento
    emissao_co2 = litros_consumidos * fator_combustivel
    return emissao_co2

def rodar_validacao():
    print("="*60)
    print(" TAREFA 19: RELATÓRIO DE VALIDAÇÃO DE INTEGRIDADE MATEMÁTICA")
    print("="*60)
    
    cenarios = [
        {"combustivel": "GASOLINA", "distancia": 100, "rendimento": 12.0, "fator": 2.31, "esperado": 19.25},
        {"combustivel": "ETANOL", "distancia": 150.5, "rendimento": 8.5, "fator": 1.50, "esperado": 26.558823529},
        {"combustivel": "DIESEL", "distancia": 50, "rendimento": 10.0, "fator": 2.68, "esperado": 13.40}
    ]
    
    erros = 0
    for idx, cenario in enumerate(cenarios, 1):
        resultado_calculado = simular_calculo_ghg(
            cenario["distancia"], 
            cenario["rendimento"], 
            cenario["fator"]
        )
        
        diferenca = abs(resultado_calculado - cenario["esperado"])
        passou = diferenca < 0.00001
        
        print(f"Cenário {idx}: {cenario['combustivel']} | {cenario['distancia']}km")
        print(f"  - Calculado: {resultado_calculado:.8f} kg CO2")
        print(f"  - Esperado:  {cenario['esperado']:.8f} kg CO2")
        print(f"  - Status:    {'✅ APROVADO' if passou else '❌ REPROVADO'}\n")
        
        if not passou:
            erros += 1
            
    print("-" * 60)
    if erros == 0:
        print("STATUS FINAL: ✅ SUCESSO! 0% de erro na lógica de cálculo (Precisão decimal validada).")
    else:
        print(f"STATUS FINAL: ❌ FALHA! Encontrado erro em {erros} cenário(s).")
        
if __name__ == "__main__":
    rodar_validacao()
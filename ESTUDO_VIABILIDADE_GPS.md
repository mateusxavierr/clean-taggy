# Estudo de Viabilidade Técnica: Geolocalização via GPS (Tarefa 21)

## 1. Objetivo
Avaliar a viabilidade técnica e financeira de integrar APIs de mapas (Google Maps e Mapbox) ao aplicativo Clean-Taggy para automatizar a identificação de praças de pedágio através da localização (GPS) do usuário, melhorando a precisão do cálculo de emissão de CO2 e reduzindo a fricção na experiência do usuário.

---

## 2. Abordagem Técnica
A identificação da praça de pedágio ocorrerá em 3 etapas:
1. **Captura no Device:** O app mobile captura as coordenadas geográficas (Latitude e Longitude) do usuário no momento da transação da Taggy.
2. **Comunicação:** As coordenadas são enviadas via payload para o backend (Django).
3. **Processamento (Matching):** O sistema cruza essas coordenadas com bases cartográficas para identificar se a localização corresponde a uma rodovia e/ou a uma praça de pedágio conhecida.

---

## 3. Análise das APIs e Estimativa de Custos

### 3.1. Google Maps Platform
O Google oferece a base de dados mais robusta do mercado. Para este cenário, utilizaríamos a **Geocoding API** (Reverse Geocoding) ou a **Places API** combinada com a **Roads API**.

- **Vantagens:** Altíssima precisão; dados de rodovias brasileiras muito atualizados.
- **Desvantagens:** Custo elevado em alta escala; políticas rígidas de cache de dados.
- **Custos Estimados:**
  - Crédito gratuito mensal: **US$ 200,00**
  - Geocoding API: **US$ 5,00** a cada 1.000 requisições (após o limite gratuito).
  - Places API: **US$ 17,00** a cada 1.000 requisições (após o limite gratuito).
  - *Viabilidade no limite grátis:* Cobre cerca de **40.000** transações/mês sem custo.

### 3.2. Mapbox
O Mapbox é amplamente utilizado como alternativa custo-efetiva ao Google, com grande flexibilidade de customização de mapas (útil para dashboards mobile). Utilizaríamos a **Mapbox Search API** (Reverse Geocoding).

- **Vantagens:** Desenvolvedor-friendly; limite gratuito generoso; custo significativamente menor.
- **Desvantagens:** Pode ter leve defasagem em rodovias rurais recém-inauguradas em comparação ao Google.
- **Custos Estimados:**
  - Limite gratuito: **100.000** requisições por mês.
  - Search/Geocoding API: **US$ 0,75** a cada 1.000 requisições (após o limite gratuito).
  - *Viabilidade no limite grátis:* Extremamente seguro para o início da operação (POC/MVP).

---

## 4. Alternativa Proposta: Geolocalização Interna (Custo Zero)
Como as praças de pedágio no Brasil são posições estáticas (não mudam de lugar), depender de requisições externas constantes a cada passagem de carro é um desperdício de recursos. 

**Solução Híbrida Recomendada:**
1. **Banco de Dados Espacial:** Migrar ou estender o banco para suportar dados espaciais (ex: `PostGIS` no PostgreSQL ou `SpatialExtensions` no MySQL).
2. **Mapeamento Prévio:** Obter as coordenadas (Lat/Lng) de todas as praças de pedágio operadas pela Taggy/Edenred e salvar no nosso banco de dados na tabela `Pedagio`.
3. **Cálculo de Proximidade Local (Raio de Tolerância):** Quando o celular enviar a posição (Ex: `Lat -23.55`, `Lng -46.63`), o próprio backend faz uma query espacial buscando qual pedágio está num **raio de 500 metros** daquela coordenada. (Fórmula de Haversine).

**Custos dessa abordagem:** **US$ 0,00** (Zero) em consumo de API externa.

---

## 5. Conclusão e Próximos Passos

**Veredito:** A geolocalização automática é **100% viável**. 

**Recomendação Arquitetural:**
- Não utilizar Google Maps/Mapbox para validar transações individuais em tempo real devido ao custo/escala.
- **Adotar a estratégia de "Geolocalização Interna" (Fórmula de Haversine)** no backend.
- Caso a praça não seja encontrada no raio predefinido (fallback), utilizar a **API do Mapbox** (devido aos 100k requests gratuitos) para realizar o *Reverse Geocoding* da rodovia, salvar esse novo ponto no banco interno e registrar o local para uso futuro.

**Riscos a Mitigar:** 
- Permissão de background location no app do usuário (Privacy Policies das stores).
- Consumo de bateria do smartphone se o polling de GPS for muito frequente. (Ideal é vincular a captura do GPS apenas ao momento que a antena do pedágio ler a Tag).
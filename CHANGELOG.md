# 🐛 Bug Tracker & Changelog

Este documento registra as principais correções de bugs (Bug Fixes) e melhorias implementadas durante o ciclo de desenvolvimento e testes do Clean Taggy.

## [1.0.0] - Incremento 3 (Reta Final)

### 🐛 Bugs Resolvidos (Bug Fixes)

- **[BUG-001] Filtro Regional da Comunidade inativo:** 
  - *Problema:* Usuários antigos no banco de dados não possuíam o campo `estado` vinculado ao `UserProfile`, fazendo com que o filtro não retornasse dados.
  - *Solução:* Implementado um script de reparo automático na view `community` para injetar estados em contas legadas, definindo 'PE' como padrão para novos perfis.

- **[BUG-002] Indicador de CO₂ Evitado "Este Mês" zerado:** 
  - *Problema:* Conflito de *Timezone* do MySQL em ambientes Windows ao utilizar o filtro nativo `data__month`, resultando em valores nulos.
  - *Solução:* Refatoração da query para utilizar `data__gte` buscando a partir do dia 1º do mês atual (`inicio_mes`), garantindo precisão matemática independente do Sistema Operacional.

- **[BUG-003] Histórico misturando Pedágios e Desafios:** 
  - *Problema:* As recompensas de conclusão de metas estavam sendo listadas como transações físicas de pedágio na aba de Histórico e "Última Passagem".
  - *Solução:* Adicionado o filtro `.exclude(local__startswith='Desafio')` nas views de `history` e `dashboard`, separando os bônus de gamificação das transações reais da Taggy.

- **[BUG-004] Links do Rodapé travados:** 
  - *Problema:* A navegação para as páginas institucionais não funcionava devido ao uso de âncoras vazias (`href="#"`) no frontend.
  - *Solução:* Substituição das âncoras pelas tags de roteamento dinâmico do Django (`{% url '...' %}`) no arquivo `base.html`.

- **[BUG-005] Erro 500 no Carregamento da Comunidade:** 
  - *Problema:* Falha de importação e erro de digitação (`USerProfile`) no schema do banco de dados causavam quebra total da página.
  - *Solução:* Correção da sintaxe da classe no `models.py` e inclusão correta da dependência no escopo do `views.py`.

---
*Documentação gerada e mantida pela equipe de desenvolvimento do Clean Taggy.*
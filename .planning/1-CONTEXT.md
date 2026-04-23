# Fase 1 — Contexto e Decisões

## Objetivo da fase

Entregar o MVP inicial do Dashboard de Investimentos com autenticação, registro de operações e dashboard por perfil.

## Referências canônicas

- `.planning/PROJECT.md` — visão, valor e restrições do produto
- `.planning/REQUIREMENTS.md` — requisitos essenciais e critérios de aceitação
- `.planning/STATE.md` — decisões de projeto e status da fase
- `.planning/ROADMAP.md` — escopo da fase 1 e limites do MVP

## Decisões bloqueadas

- Tecnologias principais
  - Frontend: latest stable Next.js com App Router, TypeScript e Tailwind CSS para layout.
  - Backend: latest stable Django (>=6.x) com Python 3.12/3.13.
  - Arquitetura: frontend Next.js separado do backend Django, comunicando-se via API REST.
  - Orquestração: usar Docker Compose para executar backend, frontend e banco de dados em containers durante desenvolvimento.
  - API: Django REST Framework para endpoints e `djangorestframework-simplejwt` para JWT.
  - Banco de dados: PostgreSQL em container Docker Compose para MVP, com volume persistente para não perder dados e migrations Django para facilitar migração futura.
  - Autenticação: JWT com Django backend e Next.js frontend.
  - Login: email + senha.
  - Sessões: autenticação baseada em token JWT armazenado inicialmente em cookie HTTP-only.
  - Fetching: usar SWR ou React Query no frontend para consumir a API.
  - Configuração: usar arquivos `.env` para settings sensíveis e separar ambiente de desenvolvimento/produção.
  - Localização/formatação: usar `pt-BR` para moeda e números, com biblioteca leve ou `Intl.NumberFormat` para formato de real e CPF.

- Papéis e acesso
  - Dois perfis: investidor individual e admin.
  - Admin MVP fica limitado a listar usuários.
  - O administrador não terá edição de transações no MVP; essa capacidade fica para fases posteriores.
  - Investidores individuais podem se cadastrar pelo fluxo público.
  - Admin será provisionado em um inventário inicial ou via superuser no Django.

- Modelo de dados de transação
  - Operações de compra/venda serão registradas com pelo menos os campos:
    - ticker
    - quantidade
    - preço
    - data da operação
    - tipo (compra ou venda)
    - observações

- Campos de cadastro de usuário
  - Email
  - Senha
  - Nome completo
  - Telefone
  - CPF ou documento

- Dashboard do investidor
  - Métrica principal do MVP: lucro total de todas as operações.
  - Deve mostrar um resumo de carteira com pelo menos:
    - total de lucro/prejuízo acumulado
    - número de operações
    - valor investido total (se aplicável)
  - Pode incluir uma visualização simples de evolução, mas o foco inicial é o indicador principal de lucro.

- Persistência de dados
  - Armazenar usuários, perfis e operações em PostgreSQL em container Docker Compose.
  - Estrutura de dados deve ser pensada para possível troca futura de DB sem mudar o desenho conceitual.

## Suposições

- O repositório atual está vazio de código de aplicação, então a fase 1 deve começar pela criação de uma app Django básica.
- Não há integração externa com corretoras ou APIs de bolsa no MVP.
- O MVP deve priorizar o fluxo funcional e a separação clara entre investidor e admin.

## Itens adiados

- Permissão de admin para editar/corrigir transações.
- Integração com corretoras, mercados ou dados de cotação externos.
- Dashboards avançados de performance e múltiplos gráficos.
- Painel administrativo completo além da listagem de usuários.

## Próximo passo para o planner

Construir o plano de implementação da fase 1 com:
- app Django 6
- autenticação e rotas protegidas
- modelo de transação definido
- dashboard do investidor com lucro total
- tela básica do admin para listar usuários
- usar o agente `@context7` como assistente de desenvolvimento e pesquisa técnica

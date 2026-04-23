# Fase 1 — Contexto de Implementação

## Objetivo da fase
Construir a base do MVP para o dashboard de investimentos: autenticação, cadastro/CRUD de investimentos, listagem e métricas básicas.

## Contexto prévio aplicado
- Usei `.planning/PROJECT.md`, `.planning/REQUIREMENTS.md`, `.planning/ROADMAP.md` e `.planning/STATE.md`.
- Não há arquivos de contexto de fases anteriores (`CONTEXT.md`) porque esta é a primeira fase.
- O repositório atual não contém código de frontend ou backend 

## Decisões de arquitetura
- Arquitetura: SPA frontend consumindo API JSON em nexjs.
- Backend: Django API.
- UI: aplicação web interativa em SPA.
- Persistência: SQLite local para dados do MVP com a possibilidade futura de modificar o banco.
- Orquestração: o ambiente local deve usar Docker Compose para backend e frontend.

## Autenticação
- Método: email e senha.
- Autorização: JWT token para API.
- Fluxo: usuário faz login, recebe token, SPA usa token para chamadas autenticadas.
- Sessão: token renovável ou expiração curta; o MVP não precisa de fluxo de refresh complexo.

## Dados e modelo de investimento
- Investimento obrigatório: nome, tipo, quantidade, valor aplicado, data de compra, tipo(compra ou venda).
- Campo opcional: valor atual estimado.
- Cálculo de lucro/prejuízo: derivado a partir do valor aplicado e do valor atual estimado quando fornecido.
- O MVP não requer integração de cotação de mercado; o valor atual é preenchido manualmente ou deixado para futuras fases.

## Escopo de administrador
- Incluir papel básico de administrador no modelo de usuário.
- Admin pode ser usado para gerenciar registros ou usuários numa etapa seguinte, mas não é um painel robusto no MVP.
- O foco inicial permanece no fluxo principal do investidor.

## Orientação para pesquisa e planejamento
- Pesquisar e escolher o framework Python para API.
- Definir o formato de dados do SQLite para usuários e investimentos.
- Projetar o fluxo SPA: login, dashboard de investimentos, formulário de CRUD e resumo financeiro.
- Configurar o ambiente de execução local com Docker Compose para backend e SPA.
- Manter a fase 1 enxuta: sem integrações externas e sem backend complexo de administração.

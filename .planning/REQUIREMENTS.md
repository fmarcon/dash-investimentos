# Requisitos do MVP

## Objetivo
Criar uma aplicação web para que investidores registrem e acompanhem seus investimentos com cálculo de retorno.

## Requisitos funcionais
- REQ-01: Autenticação de usuário
  - Usuário deve poder fazer login com email e senha.
  - O sistema deve manter sessão ativa enquanto o usuário estiver conectado.

- REQ-02: Cadastro e edição de investimento
  - Usuário deve poder criar um investimento com nome, tipo, valor aplicado, quantidade, data e corretora.
  - Usuário deve poder editar e excluir investimentos existentes.

- REQ-03: Listagem de investimentos
  - O sistema deve exibir a lista de investimentos cadastrados pelo usuário.
  - Cada item deve mostrar valor investido, valor atual estimado e lucro/prejuízo.

- REQ-04: Visão geral financeira
  - Exibir métricas principais como total investido, valor atual e resultado agregado.

## Critérios de aceitação
- Todos os campos obrigatórios são validados antes de salvar.
- O usuário consegue atualizar e excluir registros sem perder dados.
- A listagem reflete alterações imediatamente após criar, editar ou excluir.

## Escopo fora do MVP
- Integração com APIs de corretoras.
- Cálculo automático de preço de mercado em tempo real.
- Gestão avançada de usuários além do login básico.

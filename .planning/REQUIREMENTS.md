# Requisitos do Projeto

## Requisitos essenciais

1. Autenticação e gerenciamento de sessão [AUTH-01]
   - Usuários devem poder se cadastrar e fazer login.
   - O sistema deve suportar dois perfis: investidor individual e admin.

2. Usuário investidor [INV-01]
   - Deve poder cadastrar operações de compra e venda de ativos.
   - Deve visualizar histórico de transações.
   - Deve ver o valor total investido, saldo atual e lucro/prejuízo.
   - Deve ter uma tela inicial personalizada com resumo de carteira.

3. Usuário admin [ADM-01]
   - Deve poder visualizar lista de usuários.
   - Deve poder ajustar ou corrigir transações de investidores.
   - Deve ter acesso a uma tela administrativa básica.

4. Dashboard financeiro [DASH-01]
   - Deve mostrar evolução patrimonial ao longo do tempo.
   - Deve mostrar métricas de performance, como lucro/prejuízo total.
   - Deve exibir gráficos ou indicadores claros.

5. Persistência de dados [DATA-01]
   - Os dados de usuários e transações devem ser armazenados de forma durável.
   - A aplicação deve ler e gravar informações entre sessões.

## Critérios de aceitação

- A primeira entrega deve permitir o fluxo completo de cadastro, login e registro de transações.
- O dashboard deve ser diferente para investidor e admin.
- Um administrador deve conseguir inspecionar e corrigir dados de transações.
- O MVP não precisa de integração com corretoras ou Câmbio/B3.

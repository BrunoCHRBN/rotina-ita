# 03 --- System design

## 1. Arquitetura

MVP como monólito modular: - Next.js + TypeScript. - PostgreSQL. - ORM
com migrações versionadas (Prisma ou Drizzle; escolher um antes da
implementação). - Validação de entrada com schemas. - Provedor de IA
atrás de um adapter. - Testes unitários, integração e E2E.

Não introduzir microserviços, filas distribuídas ou Redis sem uma
necessidade demonstrada.

## 2. Camadas

### Presentation

Páginas, componentes, formulários, navegação e estado local de
interface.

### Application

Casos de uso, autorização, validação, transações e coordenação de
módulos.

### Domain

Entidades, políticas, motor de planejamento, regras de tarefa e sessão.
Deve ser testável sem Next.js, banco ou API de IA.

### Infrastructure

Repositórios, ORM, PostgreSQL, autenticação, logs, relógio e adapter do
provedor de IA.

## 3. Módulos

-   `routine`: disponibilidade, compromissos, preferências e limites.
-   `academics`: disciplinas, tópicos, metas e tarefas.
-   `planning`: geração, alocação, viabilidade e replanejamento.
-   `execution`: ciclo de vida de sessões e logs.
-   `reviews`: revisões e resultados.
-   `analytics`: agregações do histórico.
-   `ai`: contexto limitado, schemas, adapter e recomendações.
-   `design-system`: tokens, componentes e padrões visuais.
-   `shared`: autenticação, banco, validação, datas e utilitários.

## 4. Estrutura sugerida

``` text
src/
  app/
    hoje/
    semana/
    tarefas/
    revisoes/
    evolucao/
    rotina/
    configuracoes/
    api/
  modules/
    routine/
    academics/
    planning/
    execution/
    reviews/
    analytics/
    ai/
  design-system/
    tokens/
    components/
    patterns/
  shared/
    auth/
    database/
    validation/
    dates/
    logging/
prisma/
  schema.prisma
  migrations/
tests/
  unit/
  integration/
  e2e/
docs/
```

## 5. Contratos principais

### Planning service

Entrada: horizonte, regras de disponibilidade, compromissos, tarefas,
sessões existentes, preferências e política de autonomia.

Saída: - sessões propostas; - tarefas totalmente/ parcialmente
alocadas; - tarefas não alocadas e motivos; - conflitos detectados; -
alterações em relação ao plano atual; - métricas de capacidade; - versão
candidata.

### AI adapter

Entrada: contexto mínimo necessário e schema de saída esperado.

Saída: recomendação validada, com fatores e justificativa. Nunca recebe
credenciais de banco nem permissão para executar operações de domínio.

### Policy validator

Verifica: - schema; - autorização do usuário; - restrições rígidas; -
mudanças permitidas; - integridade das tarefas e sessões; - limites de
capacidade; - idempotência.

### Persistence

As mudanças de plano são persistidas em transação. Usar controle
otimista de versão ou outro mecanismo contra atualização concorrente.

## 6. Banco e datas

-   PostgreSQL como fonte de verdade.
-   IDs estáveis e chaves estrangeiras.
-   Fuso horário IANA por usuário.
-   Armazenar instantes com timezone e manter a regra local para
    compromissos recorrentes.
-   Separar regra recorrente da ocorrência concreta.
-   Indexar consultas por usuário, período e estado.
-   Impedir sobreposição de sessões confirmadas por validação
    transacional e, se adequado, restrição de exclusão no PostgreSQL.
-   Não depender exclusivamente de validação do frontend.

## 7. Segurança

-   Autenticação segura.
-   Autorização no servidor em toda operação.
-   Isolamento por usuário em todas as consultas e mutações.
-   Segredos apenas no servidor e em variáveis de ambiente.
-   Limitar o contexto enviado ao modelo de IA.
-   Não enviar dados pessoais desnecessários ao provedor.
-   Validar saída da IA antes de qualquer efeito.
-   Rate limit e limites de custo na integração de IA.
-   Não registrar tokens, segredos ou prompts contendo dados
    desnecessários.
-   Proteção CSRF conforme o modelo de autenticação.
-   Estratégia de backup e teste de restauração.

## 8. Observabilidade

Registrar eventos técnicos estruturados: -
planning_run_started/completed/failed; - plan_validation_failed; -
session_started/completed/interrupted; -
ai_recommendation_created/accepted/rejected; -
scheduling_conflict_detected.

Logs devem conter IDs de correlação e informações suficientes para
diagnóstico, sem registrar conteúdo pessoal desnecessário.

## 9. Estratégia de testes

-   Unitários: domínio e motor determinístico.
-   Integração: banco, transações, constraints e repositórios.
-   Contrato: schemas de entrada/saída da IA.
-   E2E: configuração, geração do plano, execução e replanejamento.
-   Testes de propriedade: nenhum plano validado possui sobreposição ou
    viola restrições.
-   Testes de falha: banco indisponível, IA indisponível, resposta
    malformada e concorrência.

## 10. Decisões ainda abertas na implementação

-   Escolher Prisma ou Drizzle; não usar ambos.
-   Escolher provedor de autenticação.
-   Escolher provedor de IA e modelo com base em custo, qualidade e
    saída estruturada.
-   Escolher hospedagem e estratégia de backup.
-   Definir política de retenção de logs.

Essas decisões não devem bloquear a especificação de domínio; devem ser
documentadas antes do respectivo módulo.

# Rotina ITA --- Especificação v1.0

**Data:** 17/10/2026\
**Status:** especificação-base aprovada para orientar a implementação\
**Produto:** aplicação web responsiva para organização da rotina de
estudos para o ITA

## Documentos

1.  `01-product-spec.md` --- escopo do produto, fluxos e regras
    funcionais.
2.  `02-planning-engine.md` --- restrições, priorização, alocação e
    replanejamento.
3.  `03-system-design.md` --- arquitetura, módulos, persistência,
    segurança e contratos.
4.  `04-design-system.md` --- identidade visual, tokens, componentes e
    critérios anti-AI-slop.
5.  `05-acceptance-tests.md` --- critérios de aceite e cenários de
    teste.
6.  `06-implementation-prompts.md` --- sequência de prompts para um
    agente de programação.
7.  `07-data-model.md` --- modelo relacional inicial e convenções.

## Decisões congeladas

-   Modelo híbrido: regras definidas pelo usuário + planejamento
    assistido por IA.
-   Plataforma web responsiva.
-   Direção visual editorial acadêmica.
-   Tema claro no MVP; modo escuro em versão posterior.
-   Agenda diária cronológica e calendário semanal em grade.
-   Autonomia automática somente dentro de regras explicitamente
    autorizadas.
-   Densidade visual equilibrada.
-   Motor determinístico como fonte de verdade para horários e
    restrições.
-   IA sem acesso direto ao banco de dados.
-   Monólito modular, sem microsserviços no MVP.

## Premissas

A aplicação começa como produto de uso pessoal, mas o modelo de dados
deve manter isolamento por usuário. A data-alvo do exame e a
disponibilidade são configuráveis; nenhuma data de prova é presumida
como fixa. O usuário cadastra sua disponibilidade e seus compromissos.

## Ordem de implementação

1.  Fundação, configuração, banco e autenticação.
2.  Design system e shell responsivo.
3.  Rotina, disponibilidade e compromissos.
4.  Tarefas e motor determinístico.
5.  Agenda diária e semanal.
6.  Execução, histórico e revisões.
7.  Replanejamento seguro.
8.  Integração com IA.
9.  Analytics, hardening e publicação.

# 01 --- Especificação de produto

## 1. Objetivo

Ajudar o usuário a responder diariamente: - O que devo estudar hoje? -
Quando devo estudar? - O que precisa ser revisado? - O que mudou em
relação ao plano original? - Como reorganizar tarefas atrasadas sem
criar uma carga irreal?

O MVP não inclui um banco próprio de questões, correção de provas, tutor
completo ou geração de conteúdo didático. Esses recursos podem ser
integrados futuramente, mas não são necessários para validar o
planejador.

## 2. Usuários e contexto

-   Usuário principal: estudante preparando-se para o ITA.
-   Contexto: rotina pessoal com horários de estudo, descanso e
    compromissos variáveis.
-   O usuário mantém controle das regras e pode revisar decisões do
    sistema.
-   A aplicação deve ser utilizável em desktop e celular.

## 3. Escopo P0 do MVP

### Perfil e objetivos

-   Configurar fuso horário IANA.
-   Definir data-alvo opcional.
-   Cadastrar disciplinas, tópicos e prioridades.
-   Definir metas semanais e limites diários/semanais.
-   Definir duração preferida de sessão e pausas.

### Rotina

-   Disponibilidade semanal recorrente.
-   Exceções para datas específicas.
-   Compromissos fixos com início e fim.
-   Períodos bloqueados e preferências de horário.
-   Validação de intervalos e conflitos.

### Tarefas

-   Criar, editar, priorizar, adiar e cancelar tarefa.
-   Definir disciplina, tópico, estimativa de esforço, prazo opcional e
    dependências.
-   Diferenciar tarefa de sessão: a tarefa é o trabalho; a sessão é uma
    alocação concreta de tempo.
-   Permitir que uma tarefa seja distribuída em mais de uma sessão.

### Agenda

-   Tela "Hoje" em formato cronológico.
-   Tela "Semana" em grade semanal.
-   Ações de iniciar, concluir, interromper, adiar e reagendar.
-   Exibição clara de tarefas não alocadas e motivo.
-   Comparação entre tempo planejado e realizado.

### Revisões

-   Criar revisão a partir de uma sessão ou tarefa concluída.
-   Configurar intervalos padrão e exceções.
-   Registrar resultado percebido, confiança e necessidade de nova
    revisão.
-   Evitar geração ilimitada de revisões sem capacidade disponível.

### Planejamento

-   Gerar plano semanal.
-   Alocar tarefas em janelas válidas.
-   Respeitar restrições rígidas.
-   Preservar sessões protegidas.
-   Detectar insuficiência de capacidade.
-   Registrar cada versão de planejamento.

### IA

-   Recomendar prioridades, duração e alternativas.
-   Explicar recomendações com base em dados disponíveis.
-   Validar a saída com schema.
-   Aplicar automaticamente apenas mudanças autorizadas por políticas
    explícitas.
-   Solicitar confirmação em qualquer caso fora da política autorizada.
-   Operar sem IA quando o provedor estiver indisponível.

### Histórico e analytics

-   Registrar duração real, resultado, dificuldade e confiança.
-   Mostrar horas planejadas versus realizadas.
-   Mostrar distribuição por disciplina e pendências.
-   Não declarar domínio de um tópico apenas porque uma sessão foi
    concluída.

## 4. Fora do escopo P0

-   Banco de questões do ITA.
-   Correção automatizada de provas.
-   Tutor socrático completo.
-   Sincronização com calendários externos.
-   Aplicativo nativo.
-   Notificações push.
-   Sistema de gamificação com streaks ou rankings.
-   Previsões de aprovação ou de nota sem base estatística validada.
-   Agentes autônomos com acesso irrestrito a dados ou ações.

## 5. Navegação

-   Hoje
-   Semana
-   Tarefas
-   Revisões
-   Evolução
-   Minha rotina
-   Configurações

A navegação pode ser ajustada durante prototipagem, mas os fluxos
essenciais devem continuar acessíveis em mobile.

## 6. Fluxos principais

### Primeiro uso

1.  Configurar fuso horário e preferências.
2.  Cadastrar disciplinas e tópicos iniciais.
3.  Definir limites de estudo.
4.  Informar disponibilidade semanal.
5.  Adicionar compromissos fixos.
6.  Criar tarefas.
7.  Gerar plano inicial.
8.  Revisar conflitos e tarefas não alocadas.
9.  Confirmar o plano.

### Executar uma sessão

1.  Abrir a sessão.
2.  Iniciar cronômetro opcional ou registrar manualmente.
3.  Concluir, interromper ou adiar.
4.  Informar tempo real e resultado.
5.  Atualizar tarefa e, se aplicável, criar revisão.
6.  Atualizar métricas sem alterar registros anteriores.

### Replanejar

1.  Identificar sessões/tarefas impactadas.
2.  Manter compromissos fixos e sessões protegidas.
3.  Recolocar tarefas flexíveis em janelas válidas.
4.  Mostrar o que mudou e por quê.
5.  Aplicar automaticamente somente dentro da política autorizada.
6.  Pedir decisão quando houver conflito, excesso de carga ou alteração
    protegida.

## 7. Requisitos não funcionais

-   Layout responsivo, teclado acessível e estados de foco visíveis.
-   Contraste WCAG AA para texto e controles essenciais.
-   Persistência confiável e transações em operações de replanejamento.
-   Isolamento dos dados por usuário.
-   Logs técnicos sem expor segredos ou conteúdo pessoal desnecessário.
-   Testes unitários do motor de planejamento.
-   Testes de integração para persistência e conflitos.
-   Testes E2E dos fluxos principais.
-   Estratégia de backup e restauração documentada.

## 8. Métricas do produto

-   Percentual de sessões planejadas concluídas.
-   Tempo planejado versus realizado.
-   Tarefas que ficaram sem alocação e seus motivos.
-   Número de replanejamentos por semana.
-   Percentual de sugestões de IA aceitas.
-   Frequência de conflitos detectados.
-   Revisões vencidas versus realizadas.

Não usar essas métricas como juízo moral ou como medida direta de
capacidade intelectual.

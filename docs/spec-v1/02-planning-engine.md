# 02 --- Motor determinístico de planejamento

## 1. Princípio central

O motor determinístico é a fonte de verdade para disponibilidade,
alocação e conflitos. A IA pode sugerir objetivos e preferências, mas
nunca pode sobrepor as restrições rígidas nem gravar diretamente no
banco.

## 2. Classes de elementos

### Compromisso fixo

Intervalo ocupado, imutável durante geração automática.

### Disponibilidade

Janela em que o usuário aceita estudar. É uma condição necessária, não
uma obrigação de preencher todos os minutos.

### Sessão protegida

Alocação que não pode ser deslocada automaticamente. Alteração exige
ação explícita do usuário.

### Tarefa flexível

Trabalho pendente que pode ser alocado em uma ou mais sessões.

### Revisão

Tarefa de revisão com data-alvo, prioridade e intervalo configurável.

### Tarefa opcional

Só recebe horário depois das tarefas prioritárias, respeitando a
capacidade disponível.

## 3. Restrições rígidas

O sistema jamais deve: - Alocar estudo fora de uma janela permitida. -
Sobrepor sessões, compromissos ou períodos bloqueados. - Ultrapassar
limites diários ou semanais configurados. - Violar pausas mínimas
configuradas entre sessões. - Mover compromissos fixos. - Mover sessão
protegida sem autorização. - Alterar ou apagar silenciosamente uma
sessão concluída. - Aplicar sugestão de IA que falhe na validação. -
Criar sessão duplicada para a mesma necessidade de tarefa. - Confirmar
um plano inviável como se estivesse completo.

## 4. Preferências flexíveis

Podem ser otimizadas dentro das restrições: - Distribuição entre
disciplinas. - Horários preferidos por disciplina. - Duração ideal de
sessão. - Alternância entre matérias exigentes. - Minimização de
alterações ao plano existente. - Preferência por sessões mais longas ou
mais curtas. - Distribuição das revisões dentro da janela permitida.

## 5. Priorização

A prioridade deve ser explicável. Evitar uma única pontuação opaca.

Ordem-base: 1. Restrições e sessões protegidas. 2. Tarefas com prazo
real e dependências críticas. 3. Revisões vencidas ou próximas da
data-alvo. 4. Tarefas ligadas às metas acadêmicas. 5. Preferências de
equilíbrio entre disciplinas. 6. Tarefas opcionais.

Dentro de uma categoria, pode-se usar pontuação configurável com: -
Urgência do prazo. - Importância declarada. - Tempo desde a última
revisão. - Dificuldade percebida. - Dependências. - Tempo estimado e
capacidade restante.

A pontuação e os fatores devem ser registrados ou explicáveis ao
usuário. Não inventar urgência se não houver prazo.

## 6. Algoritmo de alto nível

1.  Carregar regras, compromissos, tarefas e sessões existentes.
2.  Expandir regras recorrentes para o horizonte de planejamento.
3.  Normalizar instantes e fuso horário.
4.  Calcular janelas disponíveis subtraindo bloqueios e compromissos.
5.  Separar sessões fixas/protegidas das sessões flexíveis.
6.  Preparar a fila de tarefas por prioridade e dependências.
7.  Gerar candidatos de alocação que atendam à duração e às janelas.
8.  Alocar tarefas sem violar restrições.
9.  Aplicar otimizações de preferência sem piorar restrições rígidas.
10. Validar o plano completo.
11. Registrar tarefas alocadas, parcialmente alocadas e não alocadas.
12. Apresentar resumo e motivos.
13. Persistir nova versão em transação somente após a política de
    aprovação/autonomia permitir.

O algoritmo pode começar com heurísticas determinísticas (prioridade +
melhor janela disponível). Não é necessário introduzir solver complexo
no MVP. Manter a implementação substituível se os testes mostrarem
limitações.

## 7. Replanejamento

### Evento disparador

-   Sessão perdida ou interrompida.
-   Novo compromisso.
-   Mudança na disponibilidade.
-   Alteração da estimativa.
-   Revisão criada.
-   Solicitação manual.
-   Sugestão de IA aprovada.

### Procedimento

1.  Identificar o conjunto mínimo de tarefas afetadas.
2.  Preservar sessões concluídas, compromissos fixos e sessões
    protegidas.
3.  Liberar apenas alocações flexíveis que precisam mudar.
4.  Recalcular as janelas disponíveis.
5.  Tentar alocar tarefas prioritárias.
6.  Medir déficit de capacidade.
7.  Se houver déficit, não aumentar carga ou remover tarefa
    silenciosamente.
8.  Oferecer alternativas: postergar horizonte, reduzir tarefa opcional,
    dividir sessão, mudar prioridade ou pedir decisão.
9.  Registrar versão e diff do plano.
10. Aplicar transacionalmente e com proteção contra concorrência.

## 8. Regras para tarefas parcialmente alocadas

Uma tarefa pode ter: - esforço estimado total; - esforço alocado; -
esforço concluído; - esforço restante.

Invariante: esforço restante não pode ser negativo. Sessões não devem
contabilizar mais esforço concluído do que o restante da tarefa, salvo
ajuste explícito auditado.

## 9. Revisões espaçadas

-   Intervalos iniciais são configuráveis, não uma verdade universal.
-   Um exemplo inicial pode ser 1, 7 e 21 dias, mas o usuário pode
    ajustar.
-   O resultado da revisão influencia a próxima recomendação.
-   Uma revisão não deve ser criada repetidamente a cada replanejamento.
-   Usar chave idempotente ou relação explícita entre revisão e
    tópico/tarefa de origem.
-   Se não houver capacidade, registrar como não alocada e explicar o
    motivo.

## 10. Política de autonomia da IA

Autonomia configurável por tipo de ação, com lista permitida explícita.

Exemplo de ações potencialmente automáticas: - Reordenar tarefas
flexíveis ainda não iniciadas dentro da mesma janela semanal. -
Recalcular prioridades sugeridas sem alterar restrições. - Propor uma
nova duração sem aplicá-la automaticamente, salvo autorização
específica.

Ações que exigem confirmação por padrão: - Mover sessão protegida. -
Exceder limites de carga. - Alterar compromisso fixo. - Cancelar
tarefa. - Mudar a data-alvo global. - Descartar ou reduzir esforço
pendente. - Modificar regras de disponibilidade. - Replanejar para fora
do horizonte autorizado.

Toda ação automática deve ter trilha de auditoria e ser reversível
quando tecnicamente possível.

## 11. Casos de teste críticos

-   Disponibilidade vazia.
-   Capacidade menor que a carga.
-   Tarefas com dependências cíclicas.
-   Sessão cruzando meia-noite.
-   Mudança de fuso horário.
-   Dois pedidos simultâneos de replanejamento.
-   Sessão concluída no momento em que outro processo tenta movê-la.
-   Tarefa dividida em múltiplas sessões.
-   IA retorna JSON inválido ou recomenda horário proibido.
-   Provedor de IA indisponível.
-   Revisão duplicada.
-   Compromisso criado sobre uma sessão existente.

## 12. Definição de plano viável

Um plano é viável se todas as alocações confirmadas respeitam as
restrições rígidas. Um plano pode ser viável e incompleto: tarefas sem
horário devem aparecer em uma lista explícita com motivo, por exemplo,
"capacidade insuficiente" ou "nenhuma janela compatível".

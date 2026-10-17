# 05 --- Critérios de aceite e testes

## 1. Critérios de aceite do MVP

### Configuração

-   O usuário configura fuso horário, disponibilidade e limites.
-   Regras recorrentes e exceções são distintas.
-   Horários inválidos e intervalos conflitantes são rejeitados com
    mensagem compreensível.

### Planejamento

-   O motor gera sessões apenas em janelas válidas.
-   Nenhuma sessão confirmada se sobrepõe a compromisso ou outra sessão.
-   Limites diários e semanais são respeitados.
-   Sessões protegidas permanecem intactas.
-   Tarefas sem espaço são reportadas, não descartadas.
-   O resultado é determinístico para a mesma entrada e versão do
    algoritmo.

### Execução

-   Uma sessão pode ser iniciada, concluída, interrompida, adiada ou
    cancelada conforme transições válidas.
-   Sessões concluídas não são movidas automaticamente.
-   Tempo real e resultado ficam registrados.
-   Repetir uma requisição não duplica o log ou a sessão.

### Revisões

-   A conclusão pode originar uma revisão.
-   Replanejamento não duplica revisões.
-   Revisões sem capacidade permanecem visíveis como pendentes.

### IA

-   Saída inválida é rejeitada.
-   Recomendações passam por validação de política.
-   Nenhuma sugestão pode violar restrições rígidas.
-   Ações automáticas ocorrem somente quando autorizadas.
-   Falha de IA não impede uso do motor determinístico.
-   O usuário pode ver o motivo de uma mudança e desfazê-la quando
    aplicável.

### Design e acessibilidade

-   Agenda diária e semanal funcionam em desktop e mobile.
-   Não há overflow horizontal indevido em telas estreitas.
-   Componentes têm estados de foco e teclado.
-   Contraste dos tokens atende ao alvo definido.
-   Estados vazios, carregamento, erro e sucesso estão desenhados.
-   Sem dados fictícios apresentados como métricas reais.

### Segurança e persistência

-   Usuários não acessam dados de outros usuários.
-   Validações importantes ocorrem no servidor.
-   Replanejamento é transacional.
-   Segredos não são enviados ao cliente.
-   Backup e restauração são documentados.

## 2. Cenários unitários do motor

1.  Disponibilidade de 09:00--12:00 e tarefa de 90 minutos: alocar
    apenas dentro da janela.
2.  Janela de 60 minutos e tarefa indivisível de 90 minutos: retornar
    não alocada ou dividir somente se a política permitir.
3.  Compromisso 10:00--11:00: nenhuma sessão pode cruzar esse intervalo.
4.  Limite diário de 120 minutos: nunca confirmar 150 minutos.
5.  Duas tarefas no mesmo horário: resolver sem sobreposição.
6.  Sessão protegida: manter horário.
7.  Sessão concluída: preservar horário e log.
8.  Capacidade insuficiente: informar déficit e tarefas não alocadas.
9.  Tarefa com dependência: não alocar antes da dependência concluída
    quando a regra assim exigir.
10. Dependências cíclicas: rejeitar configuração e explicar o ciclo.
11. Replanejamento repetido: não criar tarefas ou revisões duplicadas.
12. Mudança de fuso: manter a semântica local de regras recorrentes.

## 3. Cenários de integração

-   Duas solicitações concorrentes não conseguem confirmar sessões
    sobrepostas.
-   Erro durante persistência reverte toda a alteração do plano.
-   Sessão concluída concorrentemente não é movida por um replanejamento
    antigo.
-   Controle de versão detecta plano desatualizado.
-   Repetição de operação idempotente não duplica efeitos.

## 4. Cenários de contrato de IA

-   JSON válido dentro do schema.
-   Campo obrigatório ausente.
-   Enum inválido.
-   Duração negativa ou excessiva.
-   Recomendação de horário fora da disponibilidade.
-   Tentativa de mover compromisso fixo.
-   Tentativa de aumentar limite semanal.
-   Resposta lenta, timeout ou indisponibilidade.
-   Conteúdo de prompt injection em texto de tarefa não altera políticas
    do sistema.
-   Justificativa sem evidência suficiente é apresentada como
    recomendação incerta, não fato.

## 5. Cenários E2E

### Fluxo A: primeiro planejamento

Criar rotina → cadastrar disciplinas → adicionar tarefas → gerar semana
→ revisar tarefas não alocadas → confirmar plano.

### Fluxo B: sessão concluída

Abrir Hoje → iniciar sessão → concluir → registrar tempo real →
verificar histórico e métricas.

### Fluxo C: sessão perdida

Marcar sessão como não realizada → solicitar replanejamento → verificar
preservação das restrições → confirmar mudanças permitidas.

### Fluxo D: indisponibilidade da IA

Simular falha do provedor → gerar plano determinístico → exibir aviso
sem bloquear o fluxo.

### Fluxo E: mobile

Abrir agenda em viewport estreito → navegar sessões → concluir tarefa →
acessar alternativa em lista para semana.

## 6. Definition of Done

Uma funcionalidade só está pronta quando: - critérios de aceite
implementados; - testes pertinentes passam; - validação ocorre no
servidor; - estados de interface foram tratados; - acessibilidade básica
foi verificada; - documentação foi atualizada; - não há dados mock
apresentados como reais fora de modo demonstrativo; - migrações e
mudanças de contrato são versionadas.

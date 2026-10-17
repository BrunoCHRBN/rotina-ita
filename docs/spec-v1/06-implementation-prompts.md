# 06 --- Sequência de prompts de implementação

## Instruções gerais para todos os prompts

Use o repositório existente se houver; não recrie a aplicação sem
inspecioná-la. Antes de editar, examine estrutura, dependências,
scripts, testes e estado do Git. Não sobrescreva alterações não
relacionadas.

Regras obrigatórias: - TypeScript estrito. - PostgreSQL como fonte de
verdade. - Monólito modular. - Motor de planejamento independente da
IA. - IA sem acesso direto ao banco. - Restrições rígidas sempre
validadas no servidor. - Não introduzir microsserviços sem
justificativa. - Não criar telas decorativas ou dados fictícios como se
fossem reais. - Executar lint, typecheck, testes e build aplicáveis. -
Informar arquivos alterados, decisões, comandos executados e
resultados. - Não afirmar que testes passaram sem executá-los. - Se
faltar uma decisão necessária, apresentar opções e escolher a menor
solução reversível.

## Prompt 0 --- Auditoria e plano de trabalho

Inspecione o repositório e compare-o com `README.md` e os documentos
desta especificação. Não implemente funcionalidades ainda. Informe: 1.
stack e arquitetura atuais; 2. dependências e comandos existentes; 3.
código reutilizável; 4. riscos, lacunas e conflitos; 5. plano
incremental com arquivos esperados; 6. decisões que precisam ser
resolvidas. Não sobrescreva trabalho existente. Proponha ADRs para
decisões arquiteturais relevantes.

Critério de saída: diagnóstico verificável e plano de execução.

## Prompt 1 --- Fundação e convenções

Implemente a fundação mínima: - configuração TypeScript estrita; -
estrutura modular; - lint, format e typecheck; - configuração de
ambiente validada; - logger seguro; - tratamento consistente de erros; -
documentação de setup local; - testes mínimos de infraestrutura. Escolha
apenas uma estratégia ORM e documente a decisão. Não implementar ainda o
motor completo.

Critérios: - instalação reproduzível; - build e verificações passam; -
segredos não ficam no repositório; - nenhum módulo depende circularmente
de outro.

## Prompt 2 --- Design system e shell responsivo

Implemente a identidade editorial acadêmica definida em
`04-design-system.md`: - tokens de cor, tipografia, espaçamento e
raio; - primitives acessíveis; - botões, campos, badges, diálogos,
feedback e estados vazios; - shell com navegação; - layouts base de Hoje
e Semana com dados claramente demonstrativos, se necessário; -
responsividade e foco por teclado. Não implementar gradientes,
glassmorphism ou dashboards decorativas. Os dados de demonstração devem
ser identificados e isolados.

Critérios: - tokens centralizados; - componentes reutilizáveis; -
contraste verificado; - layouts sem overflow indevido; - testes de
componentes essenciais.

## Prompt 3 --- Modelo de dados e rotina

Implemente as entidades e migrações para: - preferências do usuário; -
disponibilidade recorrente; - compromissos e exceções; - disciplinas e
tópicos; - tarefas; - sessões; - logs de execução; - revisões; - versões
e mudanças de planejamento. Ajuste os nomes conforme convenções do
projeto, mantendo relações e semântica documentadas.

Inclua validação de datas, fuso horário, ownership e índices. Não
confiar no frontend para integridade.

Critérios: - migrações aplicam e revertem conforme a estratégia do
projeto; - isolamento por usuário; - testes de repositório; -
constraints de integridade.

## Prompt 4 --- Motor determinístico v1

Implemente um módulo de domínio puro para: - expandir disponibilidade; -
subtrair compromissos; - gerar janelas; - priorizar tarefas por regras
explicáveis; - alocar sessões; - detectar inviabilidade; - retornar
tarefas não alocadas e motivos; - validar restrições rígidas. Não chamar
IA nesta fase.

Critérios: - testes unitários cobrindo todos os cenários de
`05-acceptance-tests.md`; - mesma entrada e versão produz resultado
determinístico; - nenhum plano inválido é retornado como viável; -
tarefas não alocadas nunca são descartadas silenciosamente.

## Prompt 5 --- Agenda diária e semanal

Conecte o domínio às telas: - Hoje em timeline cronológica; - Semana em
grade; - navegação por datas; - sessões e compromissos com distinção
semântica; - tarefas não alocadas; - estados vazios, erro e
carregamento; - ações de iniciar, concluir, adiar e reagendar. Use dados
persistidos. Remova mocks da aplicação funcional.

Critérios: - desktop e mobile; - acessibilidade por teclado; - testes
E2E dos fluxos de navegação; - nenhuma ação visualmente disponível sem
comportamento real.

## Prompt 6 --- Execução, histórico e revisões

Implemente ciclo de vida de sessão, registro de tempo real, resultado,
dificuldade e confiança. Crie revisões idempotentes a partir de eventos
definidos. Preserve logs e sessões concluídas.

Critérios: - transições inválidas são rejeitadas; - reenvio não duplica
logs; - revisão não duplica após replanejamento; - métricas derivam de
dados persistidos.

## Prompt 7 --- Replanejamento e auditoria

Implemente: - detecção de tarefas impactadas; - preservação de
compromissos fixos, sessões protegidas e concluídas; - diffs legíveis
entre planos; - versão otimista ou proteção equivalente contra
concorrência; - transação de persistência; - motivos para mudanças; -
desfazer quando seguro. Não integrar IA ainda; testar replanejamento
determinístico.

Critérios: - cenários concorrentes testados; - nenhuma alteração parcial
em caso de falha; - nenhuma tarefa perdida; - déficits de capacidade são
explícitos.

## Prompt 8 --- Integração com IA

Crie um adapter de provedor independente. Defina schemas de entrada e
saída, timeout, limites de custo, tratamento de erro e logs seguros. A
IA pode recomendar prioridades, duração e alternativas; não pode gravar
no banco.

Implemente política de autonomia por ação: - ações explicitamente
permitidas podem ser aplicadas automaticamente após validação; - ações
fora da allowlist exigem confirmação; - restrições rígidas nunca podem
ser flexibilizadas pela IA; - qualquer saída inválida é rejeitada.
Inclua testes com respostas malformadas, instruções hostis em conteúdo
de tarefa e indisponibilidade do provedor.

Critérios: - fluxo básico funciona sem IA; - nenhuma recomendação viola
políticas; - mudanças automáticas têm auditoria; - usuário entende o que
mudou e por quê.

## Prompt 9 --- Analytics e acabamento

Implemente métricas úteis e verificáveis: - planejado versus
realizado; - distribuição por disciplina; - sessões concluídas; -
tarefas não alocadas; - revisões vencidas. Finalize estados vazios,
responsividade, acessibilidade, performance, segurança, backup e
documentação de publicação.

Não invente previsão de aprovação ou métricas sem base. Faça auditoria
visual contra `04-design-system.md`.

Critérios: - suíte completa passa; - build de produção passa; - fluxos
críticos testados; - relatório final distingue resultados verificados de
limitações conhecidas.

## Formato obrigatório do relatório de cada etapa

1.  Resumo do que foi implementado.
2.  Decisões tomadas e ADRs.
3.  Arquivos criados/alterados.
4.  Migrações e mudanças de API.
5.  Testes executados e resultado real.
6.  Problemas restantes.
7.  Próximo passo recomendado.

Execute uma etapa por vez. Não avance automaticamente para a seguinte
sem revisar os resultados da etapa atual.

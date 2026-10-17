# 07 --- Modelo de dados inicial

Este é um modelo lógico inicial. Os nomes físicos e detalhes finais
devem ser confirmados ao escolher ORM e autenticação.

## Entidades e campos centrais

### users

-   `id`
-   `email` ou identificador do provedor de autenticação
-   `created_at`
-   `updated_at`

### tab_user_preferences

-   `id`
-   `user_id`
-   `timezone` (identificador IANA)
-   `daily_study_limit_minutes`
-   `weekly_study_limit_minutes`
-   `preferred_session_minutes`
-   `minimum_break_minutes`
-   `created_at`
-   `updated_at`

### tab_subjects

-   `id`
-   `user_id`
-   `name`
-   `color_token` (referência semântica, não cor arbitrária obrigatória)
-   `sort_order`
-   `is_archived`

### tab_study_topics

-   `id`
-   `user_id`
-   `subject_id`
-   `parent_topic_id` nullable
-   `name`
-   `self_assessed_mastery` nullable
-   `is_archived`

### tab_availability_rules

-   `id`
-   `user_id`
-   `weekday`
-   `start_local_time`
-   `end_local_time`
-   `effective_from` nullable
-   `effective_until` nullable
-   `is_active`

A regra recorrente usa horário local e fuso horário do usuário. Regras
que cruzam meia-noite devem ser normalizadas ou representadas
explicitamente.

### tab_calendar_events

-   `id`
-   `user_id`
-   `title`
-   `starts_at`
-   `ends_at`
-   `timezone`
-   `event_type`
-   `is_fixed`
-   `created_at`
-   `updated_at`

### tab_study_tasks

-   `id`
-   `user_id`
-   `subject_id`
-   `topic_id` nullable
-   `title`
-   `description` nullable
-   `priority`
-   `estimated_effort_minutes`
-   `completed_effort_minutes`
-   `due_at` nullable
-   `splittable`
-   `minimum_session_minutes` nullable
-   `status`
-   `created_at`
-   `updated_at`

### tab_task_dependencies

-   `task_id`
-   `depends_on_task_id`

A aplicação deve impedir dependências cíclicas.

### tab_study_sessions

-   `id`
-   `user_id`
-   `task_id`
-   `starts_at`
-   `ends_at`
-   `status`
-   `is_protected`
-   `plan_version`
-   `created_at`
-   `updated_at`

### tab_study_session_logs

-   `id`
-   `user_id`
-   `session_id`
-   `started_at` nullable
-   `ended_at` nullable
-   `actual_minutes`
-   `completion_result` nullable
-   `difficulty_rating` nullable
-   `confidence_rating` nullable
-   `notes` nullable
-   `created_at`

### tab_review_schedule

-   `id`
-   `user_id`
-   `source_task_id` nullable
-   `topic_id` nullable
-   `due_at`
-   `completed_at` nullable
-   `status`
-   `review_sequence`
-   `created_at`
-   `updated_at`

Deve existir uma regra de idempotência para não duplicar revisões da
mesma origem e sequência.

### tab_planning_runs

-   `id`
-   `user_id`
-   `horizon_start`
-   `horizon_end`
-   `algorithm_version`
-   `status`
-   `input_fingerprint`
-   `created_at`
-   `committed_at` nullable

### tab_planning_changes

-   `id`
-   `planning_run_id`
-   `entity_type`
-   `entity_id`
-   `change_type`
-   `before_snapshot` JSONB nullable
-   `after_snapshot` JSONB nullable
-   `reason_code`
-   `created_at`

### tab_ai_recommendations

-   `id`
-   `user_id`
-   `planning_run_id` nullable
-   `provider`
-   `model`
-   `recommendation_type`
-   `payload` JSONB
-   `validation_status`
-   `decision_status`
-   `created_at`
-   `decided_at` nullable

## Invariantes de domínio

-   `ends_at > starts_at`.
-   Durações e limites não podem ser negativos.
-   Esforço concluído não pode exceder o esforço total sem ajuste
    explícito auditado.
-   Uma sessão concluída não pode ser movida por replanejamento
    automático.
-   Usuário só acessa registros próprios.
-   Uma nova versão de plano não apaga a anterior.
-   Nenhuma recomendação de IA é aplicada sem validação.
-   Regras recorrentes e eventos concretos permanecem separados.
-   Datas de calendário são interpretadas no fuso IANA do usuário.
-   Evitar armazenar dados derivados que possam ser recalculados com
    confiabilidade, salvo necessidade de auditoria ou desempenho.

## Índices sugeridos

-   Por usuário e intervalo temporal para sessões.
-   Por usuário, status e prazo para tarefas.
-   Por usuário, data-alvo e estado para revisões.
-   Por usuário e período para compromissos.
-   Índices nas chaves estrangeiras.
-   Restrições únicas para idempotência de eventos e revisões quando
    aplicável.

## Observação

A lista é um ponto de partida, não um substituto para a migração
concreta. Antes de implementar, validar constraints de intervalo,
estratégia de exclusão de sobreposição e o desenho de autenticação no
PostgreSQL escolhido.

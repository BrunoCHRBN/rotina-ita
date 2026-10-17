# Rotina ITA — Auditoria Técnica Inicial e Plano de Implementação (Prompt 0)

**Data da Auditoria:** 17/10/2026  
**Workspace Auditado:** `/home/bruno-vsantos`  
**Especificação de Referência (v1.0):** [README.md](file:///home/bruno-vsantos/Downloads/rotina_ita_especificacao_v1/rotina_ita_spec_v1/README.md) e documentos `01` a `07` em `/home/bruno-vsantos/Downloads/rotina_ita_especificacao_v1/rotina_ita_spec_v1/`

---

## 1. Resumo Executivo

A auditoria do workspace local revelou que **a arquitetura alvo da Especificação v1.0 (monólito modular em Next.js + TypeScript + PostgreSQL + ORM + Adapter de IA) ainda não foi instanciada em um repositório próprio**. Em vez disso, o ambiente contém:

1. **Pacote de Especificação v1.0 recém-extraído** em `/home/bruno-vsantos/Downloads/rotina_ita_especificacao_v1/rotina_ita_spec_v1/` ([01-product-spec.md](file:///home/bruno-vsantos/Downloads/rotina_ita_especificacao_v1/rotina_ita_spec_v1/01-product-spec.md) a [07-data-model.md](file:///home/bruno-vsantos/Downloads/rotina_ita_especificacao_v1/rotina_ita_spec_v1/07-data-model.md) e [design-tokens.css](file:///home/bruno-vsantos/Downloads/rotina_ita_especificacao_v1/rotina_ita_spec_v1/design-tokens.css)).
2. **Protótipo funcional ativo "Rotina ITA — Organizador de Estudos" (v0/SPA)** em [index.html](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/index.html) (2.610 linhas, HTML5 + Tailwind Play CDN + Vanilla JS ES6+ + `localStorage` sob a chave `rotina-ita-v1`), acompanhado de documentação de diagnóstico visual ([melhorias-ui.md](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/docs/melhorias-ui.md), [plano-refatoracao.md](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/docs/plano-refatoracao.md)) e scripts de verificação baseados em CDP e testes por mutação (`verificacao/`).
3. **Backups reais de dados do usuário** exportados do protótipo SPA em `/home/bruno-vsantos/Downloads/` ([rotina-ita-2026-10-08.json](file:///home/bruno-vsantos/Downloads/rotina-ita-2026-10-08.json), [rotina-ita-2026-10-10.json](file:///home/bruno-vsantos/Downloads/rotina-ita-2026-10-10.json), [rotina-ita-2026-10-13.json](file:///home/bruno-vsantos/Downloads/rotina-ita-2026-10-13.json)).
4. **Protótipos e projetos correlatos de estudo para o ITA** em diretórios separados:
   - [ITAPlanner.jsx](file:///home/bruno-vsantos/antigravity/optimistic-pythagoras/ITAPlanner.jsx) e [index.html](file:///home/bruno-vsantos/antigravity/optimistic-pythagoras/index.html) (protótipo React single-file).
   - [index.html](file:///home/bruno-vsantos/antigravity/wise-pasteur/index.html) e [test-srs.js](file:///home/bruno-vsantos/antigravity/wise-pasteur/test-srs.js) (protótipo com cálculo de repetição espaçada SM-2).
   - [index.html](file:///home/bruno-vsantos/ita-forge-hub/index.html) (`/home/bruno-vsantos/ita-forge-hub`, caderno de provas e diagnóstico acadêmico ITA, com estética editorial clara em `Source Serif 4` + `Inter`).

**Conclusão central:** Existe código de domínio e catálogo reutilizável valioso nos protótipos (especialmente o seed de disciplinas/tópicos do edital ITA, normalização/importação de backup JSON v2 e cálculo base de SRS), mas a aplicação precisa de sua **Fundação Técnica (Etapa 1)** para estabelecer o projeto Next.js + TypeScript + PostgreSQL, o Design System Editorial Acadêmico em marfim/terracota ([design-tokens.css](file:///home/bruno-vsantos/Downloads/rotina_ita_especificacao_v1/rotina_ita_spec_v1/design-tokens.css)) e o motor determinístico de alocação em janelas horárias.

---

## 2. Stack e Estrutura Verificadas (Fase A)

### 2.1. Ferramentas e Runtimes Disponíveis no Ambiente Local

| Ferramenta | Versão / Estado Verificado | Observação |
|---|---|---|
| SO | Linux (`x86_64`) | Ambiente local do usuário (`/home/bruno-vsantos`) |
| Node.js | `v26.8.2` | Disponível no `PATH` |
| npm / npx | `12.0.2` | Disponível no `PATH` |
| pnpm | `12.3.4` | Disponível via Node.js |
| Python | `3.14.7` | Disponível no `PATH` |
| Git | `2.55.0` | Disponível no `PATH` |
| Docker | `29.8.0` (build `88096ef005`) | Daemon ativo (containers `homeassistant` up, `mongo` exited) |
| SQLite3 | `3.53.4` | Disponível no `PATH` |
| PostgreSQL (`psql` / `systemd`) | `psql` ausente no `PATH`; serviço `postgresql` `inactive` | Exigirá container Docker PostgreSQL ou instalação local antes da Etapa 3 |

### 2.2. Inventário de Diretórios e Artefatos Relacionados ao Projeto

#### A. Especificação Oficial v1.0
- **Caminho:** `/home/bruno-vsantos/Downloads/rotina_ita_especificacao_v1/rotina_ita_spec_v1/`
- **Arquivos:**
  - [README.md](file:///home/bruno-vsantos/Downloads/rotina_ita_especificacao_v1/rotina_ita_spec_v1/README.md) — Decisões congeladas, premissas e ordem de implementação.
  - [01-product-spec.md](file:///home/bruno-vsantos/Downloads/rotina_ita_especificacao_v1/rotina_ita_spec_v1/01-product-spec.md) — Escopo P0, fora de escopo, navegação (7 seções) e fluxos principais.
  - [02-planning-engine.md](file:///home/bruno-vsantos/Downloads/rotina_ita_especificacao_v1/rotina_ita_spec_v1/02-planning-engine.md) — Classes de elementos, 10 restrições rígidas, priorização explicável, algoritmo de 13 passos, replanejamento e política de autonomia de IA.
  - [03-system-design.md](file:///home/bruno-vsantos/Downloads/rotina_ita_especificacao_v1/rotina_ita_spec_v1/03-system-design.md) — Arquitetura em 4 camadas (`Presentation`, `Application`, `Domain`, `Infrastructure`) e 9 módulos (`routine`, `academics`, `planning`, `execution`, `reviews`, `analytics`, `ai`, `design-system`, `shared`).
  - [04-design-system.md](file:///home/bruno-vsantos/Downloads/rotina_ita_especificacao_v1/rotina_ita_spec_v1/04-design-system.md) — Direção editorial acadêmica, tokens semânticos claros (`#F7F5F0` canvas, `#A84635` terracota), tipografia (`Source Serif 4` + `Inter`), geometria 4px e regras anti-AI-slop.
  - [05-acceptance-tests.md](file:///home/bruno-vsantos/Downloads/rotina_ita_especificacao_v1/rotina_ita_spec_v1/05-acceptance-tests.md) — Critérios de aceite, 12 cenários unitários do motor, integração, contrato de IA, 5 fluxos E2E e Definition of Done.
  - [06-implementation-prompts.md](file:///home/bruno-vsantos/Downloads/rotina_ita_especificacao_v1/rotina_ita_spec_v1/06-implementation-prompts.md) — Sequência de Prompts 0 a 9.
  - [07-data-model.md](file:///home/bruno-vsantos/Downloads/rotina_ita_especificacao_v1/rotina_ita_spec_v1/07-data-model.md) — 14 tabelas relacionais iniciais e invariantes de domínio.
  - [design-tokens.css](file:///home/bruno-vsantos/Downloads/rotina_ita_especificacao_v1/rotina_ita_spec_v1/design-tokens.css) — Folha de tokens CSS v1.0 (`--rita-*`).

#### B. Protótipo Atual "Rotina ITA — Organizador de Estudos" (SPA Monolítico)
- **Caminho:** `/home/bruno-vsantos/WorkBuddy AI/2026-10-07-23-46-19/`
- **Stack atual:** HTML5 estático + CSS customizado + Tailwind Play CDN (`https://cdn.tailwindcss.com`) + Google Fonts (`Literata`) + Vanilla JS ES6+ inline.
- **Gerenciador de pacotes / Build:** Inexistente (`package.json` ausente).
- **Persistência:** `localStorage` no navegador sob a chave `rotina-ita-v1` (schema `version: 2`), com exportação/importação manual de arquivo JSON (`rotina-ita-YYYY-MM-DD.json`).
- **Autenticação e Autorização:** Inexistentes.
- **Organização interna de [index.html](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/index.html) (2.610 linhas):**
  - Linhas `24–466`: Folha de estilos com tokens `--c-*`, `--fs-*`, `--lh-*`, `--sp-*` ("Caderno Pautado", tema escuro `#0B0F19` por padrão e tema claro `html.claro` `#F6F7FA`).
  - Linhas `522–591`: Constantes (`SUBJECTS`, `DAYS`, `STATUS`, `PRIORITY`, `TYPES`, `SEED` com 56 tópicos do edital ITA em 6 matérias).
  - Linhas `592–680`: Utilitários de data/hora ([`iso`](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/index.html#L603-L605), [`mondayOf`](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/index.html#L606-L611), [`weekRange`](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/index.html#L613-L618), [`fmtMinutes`](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/index.html#L629-L635)) e escape XSS ([`esc`](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/index.html#L599-L601)).
  - Linhas `685–796`: Estado e persistência ([`defaultState`](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/index.html#L685-L709), [`normalize`](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/index.html#L712-L778), [`load`](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/index.html#L780-L789), [`save`](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/index.html#L790-L793)).
  - Linhas `818–850`: Consultas derivadas ([`plannedMinutesBySubject`](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/index.html#L835-L840), [`suggestedMinutesBySubject`](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/index.html#L841-L850)).
  - Linhas `934–1078`: Mapa de 26 ícones SVG inline (`ICONES`), [`paint`](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/index.html#L972-L996), preservação de foco ([`capturarFoco`](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/index.html#L1045-L1055), [`restaurarFoco`](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/index.html#L1057-L1068)) e [`render`](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/index.html#L1070-L1078).
  - Linhas `1258–1856`: 5 abas ([`viewHoje`](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/index.html#L1258-L1353), [`viewSemana`](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/index.html#L1386-L1516), [`viewConteudos`](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/index.html#L1521-L1575), [`viewProgresso`](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/index.html#L1601-L1773), [`viewAjustes`](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/index.html#L1778-L1856)).
  - Linhas `1868–2115`: Modais de ação e backup ([`dataDeSessao`](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/index.html#L1868-L1871), [`pareceBackup`](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/index.html#L2073-L2076), [`mesclarBackup`](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/index.html#L2082-L2094)).
- **Documentação e Scripts de Verificação do Protótipo:**
  - [docs/melhorias-ui.md](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/docs/melhorias-ui.md) e [docs/plano-refatoracao.md](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/docs/plano-refatoracao.md).
  - `verificacao/`: [av.sh](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/verificacao/av.sh), [sonda.js](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/verificacao/sonda.js), [compara.py](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/verificacao/compara.py), [mutacoes.md](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/verificacao/mutacoes.md).

#### C. Outros Protótipos e Repositórios ITA Encontrados no Workspace
1. **`/home/bruno-vsantos/antigravity/optimistic-pythagoras/`**:
   - Contém [ITAPlanner.jsx](file:///home/bruno-vsantos/antigravity/optimistic-pythagoras/ITAPlanner.jsx) (81 KB, componente React com edital verticalizado ITA 2026, cronômetro Pomodoro e grade semanal) e [index.html](file:///home/bruno-vsantos/antigravity/optimistic-pythagoras/index.html) (638 KB).
2. **`/home/bruno-vsantos/antigravity/wise-pasteur/`**:
   - Contém [index.html](file:///home/bruno-vsantos/antigravity/wise-pasteur/index.html) (148 KB, "ITA 2026 | Sistema Integrado de Preparação & SRS") e [test-srs.js](file:///home/bruno-vsantos/antigravity/wise-pasteur/test-srs.js) (125 linhas, função [`calculateSRS`](file:///home/bruno-vsantos/antigravity/wise-pasteur/test-srs.js#L2-L63) com suíte de testes unitários via `console.assert`).
3. **`/home/bruno-vsantos/ita-forge-hub/`**:
   - Repositório Git ativo (`https://github.com/BrunoCHRBN/ita-forge-hub.git`) voltado a banco de questões e provas comentadas do ITA ([index.html](file:///home/bruno-vsantos/ita-forge-hub/index.html), `data/questions.json`, scripts Python em `scripts/`). Possui estética acadêmica clara com `Source Serif 4` e `Inter`, mas escopo funcional distinto (Fora do Escopo P0 segundo [01-product-spec.md](file:///home/bruno-vsantos/Downloads/rotina_ita_especificacao_v1/rotina_ita_spec_v1/01-product-spec.md#L94-L105)).
4. **`/home/bruno-vsantos/WorkBuddy AI/2026-10-02-17-24-45/ita-estudos/`**:
   - Aplicação local CLI/acervo de questões (`bin/ita`, `bin/ita-app`), fora do escopo do planejador web v1.0.

---

## 3. Estado do Git e do Ambiente (Fase B)

| Diretório | É repositório Git? | Branch Atual | Remoto (`origin`) | Estado / Arquivos Não Rastreados |
|---|---|---|---|---|
| `/home/bruno-vsantos` (raiz do workspace) | **Não** | — | — | Diretório `HOME` do usuário |
| `/home/bruno-vsantos/Downloads/rotina_ita_especificacao_v1` | **Não** | — | — | Especificação v1.0 extraída do `.zip` |
| `/home/bruno-vsantos/WorkBuddy AI/2026-10-07-23-46-19` | **Não** | — | — | Protótipo SPA "Rotina ITA" sem versionamento Git próprio |
| `/home/bruno-vsantos/antigravity/optimistic-pythagoras` | **Sim** | `master` (1 commit `a873bc2`) | Nenhum remoto | `?? ITAPlanner.jsx`, `?? index.html` (não rastreados) |
| `/home/bruno-vsantos/antigravity/wise-pasteur` | **Sim** | `master` (1 commit `b034446`) | Nenhum remoto | `?? index.html`, `?? test-srs.js` (não rastreados) |
| `/home/bruno-vsantos/antigravity/fearless-hubble` | **Sim** | `master` (1 commit `34df2c6`) | Nenhum remoto | Working tree limpa (vazia) |
| `/home/bruno-vsantos/ita-forge-hub` | **Sim** | `master...origin/master` (`90f2614`) | `https://github.com/BrunoCHRBN/ita-forge-hub.git` | Working tree limpa |

### Verificação de Segredos e Credenciais
- Nenhum arquivo `.env`, `.env.local`, `.pem` ou `.key` foi encontrado em `/home/bruno-vsantos/Downloads/rotina_ita_especificacao_v1`, `/home/bruno-vsantos/WorkBuddy AI/2026-10-07-23-46-19`, `/home/bruno-vsantos/antigravity/*` ou `/home/bruno-vsantos/ita-forge-hub`.
- **Atenção crítica de segurança de ambiente:** Como a sessão foi aberta na raiz `/home/bruno-vsantos` (`$HOME`), existem diretórios sensíveis do sistema operacional do usuário na mesma árvore (`.ssh/`, `.gnupg/`, `.npmrc`, `.config/`). O novo projeto **jamais** deve inicializar Git diretamente em `/home/bruno-vsantos`; deve ser criado em um subdiretório dedicado e isolado (ex.: `/home/bruno-vsantos/Projetos/rotina-ita` ou `/home/bruno-vsantos/rotina-ita`).

---

## 4. Resultado das Validações Técnicas (Fase C)

Como ainda não há `package.json`, TypeScript, ESLint ou Next.js configurados para o projeto v1.0, foram executadas todas as validações estáticas e funcionais disponíveis nos artefatos existentes de forma estritamente somente leitura:

### 4.1. Validações Executadas

1. **Verificador de regressão de ícones e estado do protótipo Rotina ITA ([compara.py](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/verificacao/compara.py)):**
   - **Comando:**
     ```bash
     python3 "/home/bruno-vsantos/WorkBuddy AI/2026-10-07-23-46-19/verificacao/compara.py" \
       "/home/bruno-vsantos/WorkBuddy AI/2026-10-07-23-46-19/verificacao/controle-pre-fase1.json" \
       "/home/bruno-vsantos/WorkBuddy AI/2026-10-07-23-46-19/verificacao/controle-pos-fase1-final.json"
     ```
   - **Resultado:** `PASSA` (Código de saída `0`). 271 ícones comparados nas 5 abas e 4 modais + 15 sintéticos byte a byte iguais ao controle; estado persistido intacto (`56/0/0`).

2. **Checagem de sintaxe JavaScript dos blocos `<script>` inline de [index.html](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/index.html) e scripts de `verificacao/`:**
   - **Comando:** Extração em memória via Python + `node --input-type=commonjs --check` e `node --check verificacao/*.js`.
   - **Resultado:** Código de saída `0` para os 3 blocos `<script>` inline (8, 6 e 2.093 linhas) e para [sonda.js](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/verificacao/sonda.js), [colhe.js](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/verificacao/colhe.js) e [colhe_todos.js](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/verificacao/colhe_todos.js). Soma MD5 do `index.html` preservada em `7b0573054987d9d0207f6b2cc6178b08`.

3. **Suíte de testes unitários de SRS ([test-srs.js](file:///home/bruno-vsantos/antigravity/wise-pasteur/test-srs.js)):**
   - **Comando:** `node "/home/bruno-vsantos/antigravity/wise-pasteur/test-srs.js"`
   - **Resultado:** `All SRS unit tests passed successfully!` (Código de saída `0`, 5 grupos de cenários exercitados).

### 4.2. Validações Não Executadas e Impedimentos

- **`npm run lint`, `npm run typecheck`, `npm run test`, `npm run build` (Next.js/TypeScript):** Não executados porque o repositório Next.js/TypeScript ainda não foi criado (`package.json` e `tsconfig.json` ausentes).
- **Sonda live via navegador CDP ([av.sh](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/verificacao/av.sh) + [sonda.js](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/verificacao/sonda.js)):** Não executada ao vivo porque [av.sh](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/verificacao/av.sh#L23) cria arquivo temporário em `/tmp/ui_err.XXXXXX` e exige instância ativa do navegador CDP e servidor HTTP local.
- **Testes de integração com PostgreSQL:** Não executados porque o banco PostgreSQL e o schema ORM ainda não existem e o serviço `postgresql` está inativo.

---

## 5. Matriz de Conformidade com a Especificação v1.0 (Fase D)

Avaliação rigorosa confrontando o estado real do código ([WorkBuddy AI/2026-10-07-23-46-19/index.html](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/index.html) e demais protótipos) contra os 12 requisitos da Especificação v1.0:

| # | Requisito da Especificação v1.0 | Classificação | Evidência Verificada |
|---|---|---|---|
| 1 | **Separação entre apresentação, aplicação, domínio e infraestrutura** | **AUSENTE** | No protótipo [index.html](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/index.html), estado (`S`), persistência (`localStorage`), regras de negócio e templates HTML (`innerHTML`) coexistem em um único `<script>` global de 2.093 linhas. Não há camadas `Presentation`, `Application`, `Domain` e `Infrastructure` nem estrutura `src/modules/*` ([03-system-design.md](file:///home/bruno-vsantos/Downloads/rotina_ita_especificacao_v1/rotina_ita_spec_v1/03-system-design.md#L12-L86)). |
| 2 | **Módulos de rotina, disciplinas, tópicos, tarefas, planejamento, execução, revisões, métricas e IA** | **IMPLEMENTADO PARCIALMENTE** | O protótipo [index.html](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/index.html) implementa em código monolítico: disciplinas e tópicos com seed do ITA (`SUBJECTS`, `SEED`, [`viewConteudos`](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/index.html#L1521-L1575)), atividades semanais ([`viewSemana`](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/index.html#L1386-L1516)), registro manual de sessões ([`completeModal`](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/index.html#L1873-L1897), [`unplannedModal`](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/index.html#L1899-L1917)) e métricas básicas ([`viewProgresso`](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/index.html#L1601-L1773)). Estão **ausentes** no protótipo principal: módulo de revisões espaçadas, módulo de disponibilidade/compromissos por janela horária, motor de planejamento por horário e módulo de IA. |
| 3 | **Motor determinístico de planejamento** | **AUSENTE** | O protótipo possui apenas uma divisão proporcional de minutos por prioridade de matéria ([`suggestedMinutesBySubject`](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/index.html#L841-L850) e [`blocosDe`](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/index.html#L1977-L1983)) que cria atividades "sem dia fixo" (`day: null`). Não existe expansão de disponibilidade, subtração de compromissos, cálculo de janelas (`starts_at`/`ends_at`), tratamento de dependências entre tarefas nem versionamento de `planning_runs` ([02-planning-engine.md](file:///home/bruno-vsantos/Downloads/rotina_ita_especificacao_v1/rotina_ita_spec_v1/02-planning-engine.md#L75-L95)). |
| 4 | **Disponibilidade semanal e compromissos fixos** | **AUSENTE** | O protótipo armazena apenas um escalar `weeklyAvailabilityHours: 35` em [`defaultState`](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/index.html#L696). Não existem regras de disponibilidade por dia da semana com `start_local_time`/`end_local_time`, exceções de datas nem compromissos fixos (`tab_calendar_events`). |
| 5 | **Proibição de conflitos de horários e violações de limites configurados** | **AUSENTE** | Como as atividades têm apenas `day: 0..6 | null` e `plannedMinutes` (sem `starts_at`/`ends_at`), não há detecção de sobreposição de horário. Além disso, quando `planned > avail`, o sistema apenas exibe um aviso amarelo e afirma explicitamente: *"Nada é bloqueado"* ([index.html](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/index.html#L1402), [index.html](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/index.html#L1804)), contrariando a restrição rígida de [02-planning-engine.md](file:///home/bruno-vsantos/Downloads/rotina_ita_especificacao_v1/rotina_ita_spec_v1/02-planning-engine.md#L39-L48). |
| 6 | **Proteção de sessões concluídas, fixas ou explicitamente protegidas** | **IMPLEMENTADO PARCIALMENTE** | O protótipo separa `plannedMinutes` (plano na atividade) de `sessions.minutes` (realizado no histórico, ligado por `activityId`) e preserva o histórico ao editar/remover atividades ou tópicos ([index.html](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/index.html#L2183-L2192), [index.html](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/index.html#L2291-L2298)). Contudo, não existem o atributo `is_protected`, o bloqueio de movimentação em replanejamento automático nem transações no servidor. |
| 7 | **Replanejamento rastreável e justificável** | **AUSENTE** | Existe apenas um botão manual `"Trazer para esta semana"` (`data-act="carry-all"`, [index.html](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/index.html#L2302-L2313)) que sobrescreve `a.weekKey = weekKeyOf(); a.day = null` nas atividades abertas de semanas passadas, sem cálculo de janelas, sem `tab_planning_runs`, sem `tab_planning_changes` (`before_snapshot`/`after_snapshot`/`reason_code`) e sem diff de plano. |
| 8 | **Política de autorização para ações da IA** | **AUSENTE** | O próprio protótipo declara na interface: *"Esta aplicação não usa IA, não faz conexões externas"* ([index.html](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/index.html#L1853)). Não há AI Adapter, validação de schema nem Policy Validator/allowlist de autonomia ([02-planning-engine.md](file:///home/bruno-vsantos/Downloads/rotina_ita_especificacao_v1/rotina_ita_spec_v1/02-planning-engine.md#L146-L163)). |
| 9 | **Persistência e integridade dos dados** | **IMPLEMENTADO PARCIALMENTE** | Existe persistência local funcional via `localStorage` com normalização defensiva ([`normalize`](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/index.html#L712-L778)) e validação/mesclagem segura de backups JSON ([`pareceBackup`](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/index.html#L2073-L2076), [`mesclarBackup`](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/index.html#L2082-L2094)). Porém, **está ausente toda a camada de persistência da especificação v1.0**: PostgreSQL, ORM com migrações versionadas, chaves estrangeiras, transações ACID, controle de concorrência otimista e isolamento multiusuário (`user_id`). |
| 10 | **Design system acadêmico editorial** | **IMPLEMENTADO PARCIALMENTE** | O protótipo [index.html](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/index.html) já segue princípios editoriais anti-slop (réguas estruturais em vez de cards, números tabulares, sem glassmorphism), mas **diverge das decisões congeladas da v1.0**: (a) usa tema escuro (`#0B0F19`) como padrão em vez de tema claro exclusivo no MVP; (b) usa papel frio `#F6F7FA` sem acento em vez de fundo marfim `#F7F5F0` e acento terracota `#A84635`; (c) usa apenas a fonte `Literata` em vez de `Source Serif 4` (títulos) + `Inter` (corpo/UI) definidos em [04-design-system.md](file:///home/bruno-vsantos/Downloads/rotina_ita_especificacao_v1/rotina_ita_spec_v1/04-design-system.md) e [design-tokens.css](file:///home/bruno-vsantos/Downloads/rotina_ita_especificacao_v1/rotina_ita_spec_v1/design-tokens.css); (d) exibe "Semana" como lista de 7 linhas em vez de grade semanal por dia e horário. |
| 11 | **Responsividade e acessibilidade** | **IMPLEMENTADO PARCIALMENTE** | No protótipo [index.html](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/index.html), foram implementados e medidos (conforme [melhorias-ui.md](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/docs/melhorias-ui.md)): foco visível, restauração de foco após re-render ([`capturarFoco`](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/index.html#L1045-L1055)/[`restaurarFoco`](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/index.html#L1057-L1068)), trap de `Tab` e `Escape` em modais ([index.html](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/index.html#L2576-L2599)), `aria-live="polite"` para avisos, `prefers-reduced-motion` e ausência de overflow horizontal. Faltam os componentes e telas da v1.0 (timeline cronológica diária, grade semanal horária com alternativa acessível em lista no mobile e validação dos novos tokens `--rita-*`). |
| 12 | **Testabilidade, observabilidade e segurança** | **IMPLEMENTADO PARCIALMENTE** | **Segurança:** Escape HTML ([`esc`](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/index.html#L599-L601)) verificado contra XSS no protótipo; porém não há autenticação, autorização server-side, proteção CSRF ou isolamento por `user_id`. **Testabilidade:** Existem probes CDP ([sonda.js](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/verificacao/sonda.js), [compara.py](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/verificacao/compara.py)) e teste isolado de SRS ([test-srs.js](file:///home/bruno-vsantos/antigravity/wise-pasteur/test-srs.js)), mas as funções do protótipo estão presas em `<script>` inline e não há suíte automatizada unitária/integração/E2E na arquitetura alvo. **Observabilidade:** Ausente (não há logger estruturado de eventos de domínio com IDs de correlação). |

---

## 6. Problemas e Riscos Classificados por Severidade (Fase E)

### Severidade Crítica (Bloqueadores de Arquitetura e Segurança)

1. **[CRÍTICO] Ausência de diretório/repositório Git isolado para o projeto v1.0:**
   - O workspace atual está aberto em `/home/bruno-vsantos` (`$HOME`), enquanto a especificação está em `Downloads/` e o protótipo em `WorkBuddy AI/2026-10-07-23-46-19/`. Inicializar Git ou instalar dependências na raiz do usuário exporia dados pessoais e chaves privadas.
2. **[CRÍTICO] Gap arquitetural entre o protótipo SPA (`localStorage`) e a Especificação v1.0 (Next.js + PostgreSQL):**
   - O protótipo atual não possui backend, banco de dados PostgreSQL, ORM, autenticação nem separação em camadas (`Presentation`, `Application`, `Domain`, `Infrastructure`).
3. **[CRÍTICO] Ausência de modelo temporal com horários (`starts_at`/`ends_at`) e fuso IANA:**
   - No protótipo, atividades só possuem `day` (`0..6` ou `null`) e duração em minutos, sem horário de início/fim, sem fuso horário IANA, sem janelas de disponibilidade e sem compromissos fixos. Isso impede a existência do motor determinístico de alocação e da agenda cronológica/grade semanal.
4. **[CRÍTICO] Serviço PostgreSQL inativo e cliente `psql` ausente no host:**
   - `systemctl is-active postgresql` retornou `inactive` e `psql` não está instalado. Como o Docker (`v29.8.0`) está ativo e funcional, o risco é facilmente mitigado provendo um `docker-compose.yml` com PostgreSQL 16+ para desenvolvimento e testes.

### Severidade Alta (Dívida Técnica, Design e Integridade)

5. **[ALTO] Divergência de Identidade Visual entre o protótipo ("Caderno Pautado" escuro) e o Design System v1.0 ("Editorial Acadêmico" marfim/terracota):**
   - O protótipo usa fundo navy `#0B0F19` por padrão, fonte `Literata` única e proíbe cor de acento (`--c-page`, `--c-ink`), enquanto a especificação v1.0 congela tema claro no MVP (`--rita-color-canvas: #F7F5F0`), títulos em `Source Serif 4`, corpo em `Inter` e acento em terracota (`--rita-color-accent: #A84635`).
6. **[ALTO] Dependência de runtime externo no protótipo (Tailwind Play CDN + Google Fonts):**
   - Conforme documentado em [plano-refatoracao.md](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/docs/plano-refatoracao.md#L25-L49), o protótipo baixa ~397 KB do compilador JIT do Tailwind em runtime e degrada o layout silenciosamente quando offline. Na aplicação Next.js v1.0, o CSS e as fontes (`next/font/local` ou self-hosted) devem ser processados em build time.
7. **[ALTO] Preservação e migração dos dados reais já cadastrados pelo usuário:**
   - Existem backups JSON reais do usuário em `/home/bruno-vsantos/Downloads/rotina-ita-2026-10-13.json` (versão 2, com tópicos, configurações e prioridades). A nova aplicação deve fornecer um importador compatível com o formato `version: 2` do protótipo para não perder dados reais.

### Severidade Média / Baixa (Testabilidade e Escopo)

8. **[MÉDIO] Lógica pura acoplada a arquivo HTML monolítico nos protótipos:**
   - Funções úteis como [`normalize`](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/index.html#L712-L778), [`pareceBackup`](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/index.html#L2073-L2076), [`mesclarBackup`](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/index.html#L2082-L2094) e [`calculateSRS`](file:///home/bruno-vsantos/antigravity/wise-pasteur/test-srs.js#L2-L63) precisam ser extraídas e adaptadas para módulos TypeScript puros em `src/modules/` com testes unitários automatizados.
9. **[BAIXO] Dispersão de múltiplos protótipos ITA no computador:**
   - Existem 5 diretórios distintos com experimentos ITA (`WorkBuddy AI/2026-10-07-23-46-19`, `antigravity/optimistic-pythagoras`, `antigravity/wise-pasteur`, `ita-forge-hub`, `ita-estudos`). Nenhum deles deve ser apagado (Regra 5), mas o novo repositório v1.0 deve ser a única fonte oficial do produto **Rotina ITA**.

---

## 7. Decisões Pendentes e Propostas de ADRs (Fase E)

Conforme [03-system-design.md](file:///home/bruno-vsantos/Downloads/rotina_ita_especificacao_v1/rotina_ita_spec_v1/03-system-design.md#L168-L179) e [06-implementation-prompts.md](file:///home/bruno-vsantos/Downloads/rotina_ita_especificacao_v1/rotina_ita_spec_v1/06-implementation-prompts.md#L17-L30), seguem as decisões abertas que precisam de validação, acompanhadas da **menor solução reversível recomendada (ADR)**:

### Decisões que Precisam ser Resolvidas Agora (Pré-Etapa 1)

1. **Localização do Repositório Oficial do Projeto v1.0:**
   - *Opções:* (a) Criar `/home/bruno-vsantos/rotina-ita` (ou `/home/bruno-vsantos/Projetos/rotina-ita`) como repositório Git limpo, copiando a especificação v1.0 para `docs/spec/` e preservando o protótipo `WorkBuddy AI/2026-10-07-23-46-19` intocado; ou (b) Inicializar o projeto dentro de `/home/bruno-vsantos/WorkBuddy AI/2026-10-07-23-46-19/`.
   - *Recomendação (ADR-001):* **Opção (a) — Criar `/home/bruno-vsantos/rotina-ita`** (ou `/home/bruno-vsantos/Projetos/rotina-ita`), mantendo os documentos de especificação versionados em `docs/` e preservando 100% do protótipo anterior intacto para referência e migração de backups.

2. **Escolha do ORM e Estratégia de Migrações ([03-system-design.md](file:///home/bruno-vsantos/Downloads/rotina_ita_especificacao_v1/rotina_ita_spec_v1/03-system-design.md#L170)):**
   - *Opções:* **Drizzle ORM** (`drizzle-orm` + `drizzle-kit`) vs. **Prisma ORM**.
   - *Recomendação (ADR-002):* **Drizzle ORM** (ou Prisma, caso prefira). Drizzle oferece tipagem TypeScript estrita sem geração pesada de binários Rust, SQL transparente para constraints avançadas do PostgreSQL (como índices parciais e `EXCLUDE USING gist` para impedir sobreposição de sessões) e excelente integração com transações. *(Se preferir Prisma conforme o exemplo de árvore em `03-system-design.md`, a escolha é igualmente suportada).*

3. **Infraestrutura Local de Banco de Dados PostgreSQL:**
   - *Opções:* Container Docker via `docker-compose.yml` (`postgres:16-alpine`) vs. instalação nativa no EndeavourOS/Arch.
   - *Recomendação (ADR-003):* **`docker-compose.yml` com `postgres:16-alpine`** (Docker já está instalado e rodando na versão `29.8.0`), garantindo ambiente reproduzível sem alterar pacotes globais do sistema.

4. **Modelo de Autenticação no MVP ([03-system-design.md](file:///home/bruno-vsantos/Downloads/rotina_ita_especificacao_v1/rotina_ita_spec_v1/03-system-design.md#L171)):**
   - *Opções:* (a) Sessão local autenticada (Auth.js / NextAuth com Credentials ou sessão assinada HTTP-only + suporte a perfil padrão local autenticado, exigindo `user_id` em todas as queries); (b) OAuth externo.
   - *Recomendação (ADR-004):* **Autenticação baseada em sessão HTTP-only com suporte a credenciais locais (sem depender de provedor externo para rodar offline/localmente)**, mantendo `user_id` obrigatório em 100% das tabelas, repositórios e casos de uso.

### Decisões que Podem ser Adiadas sem Prejudicar o MVP Inicial

- **Escolha do provedor/modelo de IA comercial (Gemini / OpenAI / Anthropic / Ollama local):** Pode ser adiada até a **Etapa 8**, pois o módulo `ai` ficará atrás de uma interface `AIProviderAdapter` com modo fallback determinístico obrigatório quando desligado ou indisponível.
- **Hospedagem em nuvem e automação externa de backups:** Pode ser adiada até a **Etapa 9** (no MVP local, script documentado de `pg_dump`/`pg_restore` + exportação/importação JSON por usuário atendem ao requisito).
- **Tema escuro v1.0:** Explicitamente adiado pela especificação ([04-design-system.md](file:///home/bruno-vsantos/Downloads/rotina_ita_especificacao_v1/rotina_ita_spec_v1/04-design-system.md#L178-L183)); basta usar exclusivamente os tokens semânticos `--rita-*`.

---

## 8. Código e Ativos Reutilizáveis Identificados

1. **Tokens e Especificação v1.0 (`/home/bruno-vsantos/Downloads/rotina_ita_especificacao_v1/rotina_ita_spec_v1/`):**
   - [design-tokens.css](file:///home/bruno-vsantos/Downloads/rotina_ita_especificacao_v1/rotina_ita_spec_v1/design-tokens.css) pronto para ser incorporado diretamente em `src/design-system/tokens/design-tokens.css`.
2. **Catálogo Inicial do Edital ITA (`SEED` e `SUBJECTS` em [index.html](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/index.html#L542-L590)):**
   - As 6 disciplinas (`Matemática`, `Física`, `Química`, `Português`, `Inglês`, `Redação`) e os 56 tópicos base já curados podem servir como seed opcional de primeiro acesso (`first-run onboarding`) para o módulo `academics`.
3. **Importador/Compatibilidade de Backups JSON v2 ([`pareceBackup`](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/index.html#L2073-L2076), [`normalize`](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/index.html#L712-L778)):**
   - Permite migrar os backups reais do usuário (`Downloads/rotina-ita-2026-10-13.json`) para o banco PostgreSQL.
4. **Padrões de Acessibilidade de Diálogo e Foco ([index.html](file:///home/bruno-vsantos/WorkBuddy%20AI/2026-10-07-23-46-19/index.html#L2576-L2599)):**
   - Lógica de trap de foco, fechamento com `Escape`, retorno de foco ao elemento disparador e região viva `aria-live="polite"`.

---

## 9. Plano de Implementação Priorizado (Fase F)

O plano segue estritamente a sequência incremental de 9 etapas da especificação ([06-implementation-prompts.md](file:///home/bruno-vsantos/Downloads/rotina_ita_especificacao_v1/rotina_ita_spec_v1/06-implementation-prompts.md)), adaptado ao estado real auditado.

### Etapa 1 — Fundação Técnica e Convenções (Prompt 1)
- **Objetivo:** Inicializar o repositório do monólito modular em Next.js (App Router) + TypeScript estrito, configurar banco PostgreSQL local via Docker Compose, ORM com migrações versionadas, validação de variáveis de ambiente com Zod, logger estruturado seguro, tratamento padronizado de erros e suíte de testes (Vitest + Playwright).
- **Arquivos/Módulos Envolvidos:**
  - `package.json`, `tsconfig.json`, `next.config.ts`, `eslint.config.mjs`, `vitest.config.ts`, `playwright.config.ts`, `docker-compose.yml`, `.env.example`, `.gitignore`.
  - `docs/adr/0001-stack-and-orm.md`, `docs/spec/*` (cópia versionada da especificação v1.0).
  - `src/shared/env/`, `src/shared/logging/`, `src/shared/errors/`, `src/shared/database/`, `src/shared/dates/`, `src/shared/auth/`.
- **Dependências:** Aprovação desta auditoria e das ADRs 001 a 004.
- **Critérios de Aceitação:**
  - `tsconfig.json` com `"strict": true`, `"noUncheckedIndexedAccess": true`.
  - `npm run lint`, `npm run typecheck`, `npm run test` e `npm run build` executam e passam sem erros.
  - Nenhum segredo versionado; `.env.example` documentado.
- **Testes Obrigatórios:** Testes unitários de validação de env (`src/shared/env`), logger estruturado (garantindo redaction de campos sensíveis) e utilitários de fuso horário IANA (`src/shared/dates`).
- **Riscos e Pré-requisitos:** Garantir que as portas do PostgreSQL no `docker-compose.yml` (ex.: `5432` ou `5433`) não conflitem com outros serviços locais.

### Etapa 2 — Design System Editorial Acadêmico e Estrutura Responsiva (Prompt 2)
- **Objetivo:** Implementar a direção visual de [04-design-system.md](file:///home/bruno-vsantos/Downloads/rotina_ita_especificacao_v1/rotina_ita_spec_v1/04-design-system.md) com os tokens de [design-tokens.css](file:///home/bruno-vsantos/Downloads/rotina_ita_especificacao_v1/rotina_ita_spec_v1/design-tokens.css) (fundo marfim `#F7F5F0`, tinta `#222522`, títulos `Source Serif 4`, corpo `Inter`, acento terracota `#A84635`), primitives acessíveis e o App Shell responsivo com as 7 rotas de navegação (`Hoje`, `Semana`, `Tarefas`, `Revisões`, `Evolução`, `Minha rotina`, `Configurações`).
- **Arquivos/Módulos Envolvidos:**
  - `src/design-system/tokens/design-tokens.css`
  - `src/design-system/components/` (`Button`, `Input`, `Select`, `Textarea`, `Switch`, `Checkbox`, `Dialog`, `Badge`, `EmptyState`, `Skeleton`, `AlertBanner`, `PageHeader`, `SectionRule`)
  - `src/design-system/patterns/` (`AppShell`, `SidebarNav`, `MobileNav`, `DailyTimelineView`, `WeeklyGridView`)
  - `src/app/layout.tsx`, `src/app/hoje/page.tsx`, `src/app/semana/page.tsx`, `src/app/tarefas/page.tsx`, `src/app/revisoes/page.tsx`, `src/app/evolucao/page.tsx`, `src/app/rotina/page.tsx`, `src/app/configuracoes/page.tsx`.
- **Dependências:** Etapa 1 concluída.
- **Critérios de Aceitação:**
  - 100% das cores referenciando tokens `--rita-*`; zero gradientes decorativos, zero glassmorphism, zero emojis como ícones.
  - Fontes com fallback local sem bloqueio de renderização offline.
  - Contraste WCAG AA verificado e ausência de overflow horizontal em desktop (`1280px`) e mobile (`390px`/`360px`).
  - Dados demonstrativos explícitos e isolados.
- **Testes Obrigatórios:** Testes de componentes (estados `default`, `focus-visible`, `disabled`, `loading`, `error`, `empty`) e verificação de layout responsivo.
- **Riscos e Pré-requisitos:** Não carregar vícios do tema escuro do protótipo antigo; o MVP v1.0 é estritamente claro com paleta marfim/terracota.

### Etapa 3 — Modelo de Dados, Persistência e Configuração da Rotina (Prompt 3)
- **Objetivo:** Implementar o schema relacional completo de [07-data-model.md](file:///home/bruno-vsantos/Downloads/rotina_ita_especificacao_v1/rotina_ita_spec_v1/07-data-model.md) no PostgreSQL com migrações versionadas, constraints de integridade (`ends_at > starts_at`, durações não negativas, chave idempotente de revisões, isolamento por `user_id`) e os módulos `routine` e `academics` (preferências, fuso IANA, disponibilidade recorrente, compromissos fixos/exceções, disciplinas e tópicos com seed opcional do ITA).
- **Arquivos/Módulos Envolvidos:**
  - Schema ORM e migrações (`prisma/` ou `src/shared/database/schema.ts` + `migrations/`).
  - `src/modules/routine/` (`domain/`, `application/`, `infrastructure/`, `presentation/`).
  - `src/modules/academics/` (`domain/`, `application/`, `infrastructure/`, `presentation/`, incluindo seed das disciplinas ITA).
  - `src/app/rotina/`, `src/app/configuracoes/`, `src/app/api/routine/`, `src/app/api/academics/`.
- **Dependências:** Etapas 1 e 2 concluídas; container PostgreSQL ativo.
- **Critérios de Aceitação:**
  - As 14 entidades (`users`, `tab_user_preferences`, `tab_subjects`, `tab_study_topics`, `tab_availability_rules`, `tab_calendar_events`, `tab_study_tasks`, `tab_task_dependencies`, `tab_study_sessions`, `tab_study_session_logs`, `tab_review_schedule`, `tab_planning_runs`, `tab_planning_changes`, `tab_ai_recommendations`) criadas e migradas.
  - Rejeição no servidor de intervalos inválidos (`ends_at <= starts_at`), limites negativos e conflitos entre compromissos fixos.
  - Isolamento por `user_id` garantido em todas as queries e mutações.
- **Testes Obrigatórios:** Testes de integração de repositório no PostgreSQL validando constraints, fuso horário IANA, regras que cruzam meia-noite e isolamento entre dois usuários distintos.
- **Riscos e Pré-requisitos:** Normalização cuidadosa de horários locais (`start_local_time`/`end_local_time`) em relação a instantes `TIMESTAMPTZ` no fuso IANA do usuário.

### Etapa 4 — Motor Determinístico de Planejamento e Testes de Invariantes (Prompt 4)
- **Objetivo:** Implementar o módulo `src/modules/planning/domain/` como código de domínio puro (sem depender de Next.js, banco ou IA) executando o algoritmo determinístico de 13 passos ([02-planning-engine.md](file:///home/bruno-vsantos/Downloads/rotina_ita_especificacao_v1/rotina_ita_spec_v1/02-planning-engine.md#L75-L95)) e o CRUD de tarefas (`tab_study_tasks` + `tab_task_dependencies`).
- **Arquivos/Módulos Envolvidos:**
  - `src/modules/planning/domain/` (`window-calculator.ts`, `task-prioritizer.ts`, `dependency-graph.ts`, `session-allocator.ts`, `plan-validator.ts`, `planning-engine.ts`).
  - `src/modules/academics/application/task-service.ts`.
  - `tests/unit/planning/`.
- **Dependências:** Etapa 3 concluída.
- **Critérios de Aceitação:**
  - Expansão de disponibilidade semanal e subtração de compromissos/bloqueios e pausas mínimas (`minimum_break_minutes`).
  - Detecção de ciclos de dependência (DAG check) com explicação do ciclo.
  - Priorização explicável em 6 níveis ([02-planning-engine.md](file:///home/bruno-vsantos/Downloads/rotina_ita_especificacao_v1/rotina_ita_spec_v1/02-planning-engine.md#L62-L73)) com registro dos fatores.
  - Divisão de tarefas divisíveis (`splittable: true`) respeitando `minimum_session_minutes` e manutenção de tarefas indivisíveis.
  - Retorno explícito de tarefas não alocadas com código de motivo (`INSUFFICIENT_CAPACITY`, `NO_COMPATIBLE_WINDOW`, `UNMET_DEPENDENCY`, `DAILY_LIMIT_REACHED`, `WEEKLY_LIMIT_REACHED`).
  - Validador final garantindo as 10 restrições rígidas.
- **Testes Obrigatórios:** Todos os **12 cenários unitários obrigatórios** de [05-acceptance-tests.md](file:///home/bruno-vsantos/Downloads/rotina_ita_especificacao_v1/rotina_ita_spec_v1/05-acceptance-tests.md#L63-L80) + teste de propriedade (nenhum plano validado possui sobreposição ou viola limites) + determinismo (`mesma entrada + algorithm_version => saída idêntica`).
- **Riscos e Pré-requisitos:** Tratamento correto de sessões que cruzam meia-noite e mudanças de horário/fuso.

### Etapa 5 — Agenda Diária ("Hoje") e Grade Semanal ("Semana") (Prompt 5)
- **Objetivo:** Conectar o motor de planejamento e a persistência às telas `Hoje` (timeline cronológica), `Semana` (grade horária por dia com alternativa acessível em lista para mobile) e `Tarefas`, removendo quaisquer dados demonstrativos do fluxo principal.
- **Arquivos/Módulos Envolvidos:**
  - `src/modules/planning/application/` (`generate-weekly-plan.ts`, `confirm-plan.ts`).
  - `src/modules/planning/presentation/` (`DailyTimeline.tsx`, `WeeklyScheduleGrid.tsx`, `WeeklyMobileList.tsx`, `UnallocatedTasksPanel.tsx`, `SessionBlock.tsx`, `CalendarEventBlock.tsx`).
  - `src/app/hoje/page.tsx`, `src/app/semana/page.tsx`, `src/app/tarefas/page.tsx`.
- **Dependências:** Etapas 2, 3 e 4 concluídas.
- **Critérios de Aceitação:**
  - Distinção semântica visual e programática (não apenas por cor) entre sessão flexível, sessão protegida, sessão concluída e compromisso fixo.
  - Exibição clara de tarefas não alocadas e seus motivos tanto em `Hoje` quanto em `Semana`.
  - Alternativa em lista para telas estreitas em `Semana`.
  - Ações reais de iniciar, concluir, interromper, adiar, proteger/desproteger e reagendar.
- **Testes Obrigatórios:** Testes E2E do **Fluxo A (primeiro planejamento)** e **Fluxo E (mobile)** de [05-acceptance-tests.md](file:///home/bruno-vsantos/Downloads/rotina_ita_especificacao_v1/rotina_ita_spec_v1/05-acceptance-tests.md#L106-L132).
- **Riscos e Pré-requisitos:** Garantir que a grade semanal não gere overflow horizontal em viewports de `360px–390px`.

### Etapa 6 — Execução das Sessões, Histórico e Revisões Espaçadas (Prompt 6)
- **Objetivo:** Implementar a máquina de estados de execução de sessão (`PLANNED -> IN_PROGRESS -> COMPLETED | INTERRUPTED | POSTPONED | CANCELED`), cronômetro opcional + registro manual (`tab_study_session_logs`), contabilidade de esforço (`completed_effort_minutes` vs. `estimated_effort_minutes`) e agendamento idempotente de revisões (`tab_review_schedule`).
- **Arquivos/Módulos Envolvidos:**
  - `src/modules/execution/` (`domain/session-lifecycle.ts`, `application/record-session-log.ts`, `presentation/SessionExecutionModal.tsx`).
  - `src/modules/reviews/` (`domain/review-scheduler.ts`, `application/review-service.ts`, `presentation/ReviewsList.tsx`).
  - `src/app/revisoes/page.tsx`.
- **Dependências:** Etapa 5 concluída.
- **Critérios de Aceitação:**
  - Transições de estado inválidas rejeitadas no servidor.
  - Sessões concluídas tornam-se imutáveis para o replanejamento automático.
  - Invariante de esforço respeitada: esforço restante nunca negativo; excesso exige ajuste explícito auditado.
  - Geração idempotente de revisões (chave única `(user_id, source_task_id, review_sequence)`) com intervalos configuráveis (padrão inicial sugerido `1, 7, 21` dias ajustável pelo usuário e influenciado por dificuldade/confiança).
- **Testes Obrigatórios:** Testes unitários e de integração de idempotência de log/revisão e E2E do **Fluxo B (sessão concluída)**.
- **Riscos e Pré-requisitos:** Impedir que cliques duplos ou reenvios de rede dupliquem logs de sessão ou revisões.

### Etapa 7 — Replanejamento Seguro e Auditoria de Alterações (Prompt 7)
- **Objetivo:** Implementar o replanejamento determinístico incremental disparado por eventos (sessão perdida/interrompida, novo compromisso, mudança de disponibilidade, revisão criada, pedido manual), gerando versão candidata (`tab_planning_runs`), diff legível (`tab_planning_changes`), opções de resolução de déficit de capacidade e persistência transacional com controle otimista de concorrência (`plan_version`).
- **Arquivos/Módulos Envolvidos:**
  - `src/modules/planning/domain/replanning-engine.ts`, `src/modules/planning/domain/plan-diff.ts`.
  - `src/modules/planning/application/replan-use-case.ts`, `src/modules/planning/application/undo-plan-use-case.ts`.
  - `src/modules/planning/presentation/ReplanDiffDialog.tsx`.
- **Dependências:** Etapas 4, 5 e 6 concluídas.
- **Critérios de Aceitação:**
  - Preservação absoluta de sessões concluídas, compromissos fixos e sessões protegidas.
  - Cálculo do conjunto mínimo de sessões flexíveis impactadas.
  - Exibição do diff ("antes vs. depois" + `reason_code`) e alternativas explícitas quando houver déficit de capacidade.
  - Persistência atômica em transação com detecção de conflito concorrente (`plan_version` otimista) e reversão segura (undo).
- **Testes Obrigatórios:** Todos os **5 cenários de integração** de [05-acceptance-tests.md](file:///home/bruno-vsantos/Downloads/rotina_ita_especificacao_v1/rotina_ita_spec_v1/05-acceptance-tests.md#L81-L90) (concorrência, rollback em erro de persistência, sessão concluída concorrentemente, plano desatualizado, idempotência) e E2E do **Fluxo C (sessão perdida)**.
- **Riscos e Pré-requisitos:** Uso de isolamento transacional adequado e constraints no PostgreSQL para impedir que duas requisições simultâneas gravem sessões sobrepostas.

### Etapa 8 — Adaptador de IA e Políticas de Autorização (Prompt 8)
- **Objetivo:** Implementar o módulo `src/modules/ai/` com adapter desacoplado de provedor, contratos estritos validados por schema (Zod), Policy Validator (`allowlist` configurável por tipo de ação), proteção contra prompt injection, controle de timeout/rate-limit/custo e degradação graciosa quando a IA estiver indisponível ou desativada.
- **Arquivos/Módulos Envolvidos:**
  - `src/modules/ai/domain/` (`ai-policy-validator.ts`, `ai-schemas.ts`).
  - `src/modules/ai/infrastructure/` (`ai-provider.interface.ts`, `gemini-adapter.ts`, `noop-adapter.ts`).
  - `src/modules/ai/application/` (`request-ai-recommendation.ts`, `apply-ai-recommendation.ts`).
  - `src/modules/ai/presentation/` (`AiRecommendationPanel.tsx`, `AutonomyPolicySettings.tsx`).
- **Dependências:** Etapa 7 concluída.
- **Critérios de Aceitação:**
  - A IA nunca acessa o banco nem modifica entidades diretamente; toda sugestão passa pelo `PolicyValidator` e pelo motor determinístico.
  - Ações fora da allowlist do usuário (ex.: mover sessão protegida, alterar compromisso fixo, exceder limites, cancelar tarefa) exigem confirmação explícita.
  - Qualquer sugestão da IA que viole uma das 10 restrições rígidas é rejeitada com status registrado em `tab_ai_recommendations`.
  - Quando o provedor falha ou está desligado, o planejador determinístico opera 100% normalmente.
- **Testes Obrigatórios:** Todos os **10 cenários de contrato de IA** de [05-acceptance-tests.md](file:///home/bruno-vsantos/Downloads/rotina_ita_especificacao_v1/rotina_ita_spec_v1/05-acceptance-tests.md#L91-L105) (JSON malformado, enum inválido, duração negativa, horário fora da janela, tentativa de mover compromisso fixo, timeout/indisponibilidade, prompt injection em título/descrição de tarefa) e E2E do **Fluxo D (indisponibilidade da IA)**.
- **Riscos e Pré-requisitos:** Sanitizar e delimitar claramente os campos de texto do usuário antes de compor o contexto mínimo enviado ao provedor.

### Etapa 9 — Métricas, Acessibilidade, Backup e Refinamento Final (Prompt 9)
- **Objetivo:** Implementar o módulo `analytics` e a tela `Evolução` com as 7 métricas de produto ([01-product-spec.md](file:///home/bruno-vsantos/Downloads/rotina_ita_especificacao_v1/rotina_ita_spec_v1/01-product-spec.md#L164-L175)), utilitário de migração/importação de backups JSON do protótipo v0, documentação de backup/restauração do PostgreSQL e auditoria final de acessibilidade WCAG AA e anti-AI-slop.
- **Arquivos/Módulos Envolvidos:**
  - `src/modules/analytics/` (`domain/`, `application/`, `presentation/`).
  - `src/app/evolucao/page.tsx`.
  - `scripts/backup-db.sh`, `scripts/restore-db.sh`, `docs/operations-and-backup.md`.
- **Dependências:** Etapas 1 a 8 concluídas.
- **Critérios de Aceitação:**
  - Exibição real de: % de sessões concluídas, horas planejadas vs. realizadas, distribuição por disciplina, tarefas não alocadas e motivos, replanejamentos por semana, % de sugestões de IA aceitas, conflitos detectados e revisões vencidas vs. realizadas.
  - Zero afirmações de "domínio definitivo" por mera conclusão de uma sessão e zero previsões de aprovação sem base estatística.
  - Suíte completa (unitários, integração, contrato IA, E2E desktop/mobile) e build de produção (`npm run build`) aprovados.
- **Testes Obrigatórios:** Testes de agregação de métricas sobre dados persistidos, auditoria automatizada de acessibilidade (teclado, foco, contraste) e teste de backup/restauração.
- **Riscos e Pré-requisitos:** Garantir que nenhuma tela residual contenha mocks fora de modo demonstrativo explícito.

---

## 10. Critérios para Considerar a Fundação Técnica Pronta (Gate da Etapa 1)

A Fundação Técnica (Etapa 1) só poderá ser declarada pronta quando **todos** os itens abaixo forem comprovados por execução real de comandos:

1. Repositório isolado criado e inicializado com Git (`main`), `.gitignore` estrito e cópia dos documentos da especificação v1.0 em `docs/spec/`.
2. `tsconfig.json` configurado com `strict: true`, `noImplicitAny: true`, `strictNullChecks: true` e `noUncheckedIndexedAccess: true`.
3. Estrutura de diretórios modular criada (`src/app`, `src/modules/{routine,academics,planning,execution,reviews,analytics,ai}`, `src/design-system/{tokens,components,patterns}`, `src/shared/{auth,database,validation,dates,logging,errors}`, `tests/{unit,integration,e2e}`).
4. `docker-compose.yml` funcional para PostgreSQL local + ORM configurado (comandos de migração configurados e documentados).
5. Validador de variáveis de ambiente (`src/shared/env`) testado para falhar rapidamente com mensagem clara se variáveis obrigatórias estiverem ausentes.
6. Logger técnico estruturado (`src/shared/logging`) com suporte a `correlationId` e filtro contra vazamento de segredos/tokens.
7. Comandos `npm run lint`, `npm run typecheck`, `npm run test` e `npm run build` executando com código de saída `0`.

---

## 11. Checklist Pré-Publicação no GitHub

Antes de qualquer futuro `git push` (quando autorizado pelo usuário após as etapas de implementação):

- [ ] Repositório Git inicializado **exclusivamente** na pasta do projeto (nunca em `/home/bruno-vsantos`).
- [ ] Verificação `git status --ignored` e `git diff` confirmando que nenhum arquivo `.env`, `.env.local`, dump de banco de dados pessoal (`rotina-ita-*.json`), chave SSH ou token consta na árvore de commits.
- [ ] `.env.example` completo e contendo apenas placeholders seguros.
- [ ] `npm run lint`, `npm run typecheck`, `npm run test` (unitários + integração + contrato IA) e `npm run test:e2e` executados e aprovados.
- [ ] `npm run build` de produção concluído sem erros ou warnings críticos.
- [ ] Verificação de conformidade com [04-design-system.md](file:///home/bruno-vsantos/Downloads/rotina_ita_especificacao_v1/rotina_ita_spec_v1/04-design-system.md) (tokens `--rita-*`, contraste WCAG AA, navegação completa por teclado, sem overflow horizontal em `360px`/`390px`/`1280px`, checklist anti-AI-slop).
- [ ] Documentação atualizada (`README.md`, `docs/adr/`, instruções de setup local, migrações e rotina de backup/restauração).

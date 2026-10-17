# Melhorias de UI — Rotina ITA

Diagnóstico medido, não opinado. Cada número abaixo foi lido do DOM renderizado num
navegador real (agent-browser 0.39, via CDP), com o layout **assentado** antes de medir
(2 `requestAnimationFrame` + 300 ms — a CDN do Tailwind injeta as classes *depois* do
`render()`, e medir antes disso dá falso positivo). Cinco abas × dois temas.

As hipóteses que **não** se sustentaram estão listadas no fim, com o número que as derrubou.
Elas importam tanto quanto os defeitos: são justamente os lugares onde se esperaria um
problema e não há.

---

## A tese

A camada de tokens cobre **cor e tipografia** — e é exatamente aí que a aplicação está
limpa: contraste de texto passa em 478 medições sem uma única reprovação, a paleta de
matérias se sustenta (o pior par ΔE00 é 12,32, número que eu recalculei e bate com o que
está escrito no próprio arquivo), e a escala tipográfica é coerente (8 corpos, 2 pesos).

As duas dimensões que **criam** a sensação de caderno pautado — **o espaço** e **a régua** —
são as duas que não têm token, não têm escala e não têm disciplina. O resultado é que o
caderno lê como uma lista larga, esparsa e de borda macia, e não como uma página pautada.

O diagnóstico inteiro cabe nessa frase: **o que foi tokenizado ficou bom; o que ficou solto
virou o problema.**

---

## P1 — O ledger não tem medida (o achado mais forte)

A prosa é disciplinada: `.measure` fixa o teto de leitura em **62ch = 406,5 px**, aplicado a
13 blocos de texto nas cinco abas. Tudo o mais — linhas de ledger, tabelas, réguas de seção,
estados vazios — corre os **960 px** inteiros da coluna.

Consequência medida: **o rótulo e o valor da mesma linha ficam a ~850 px de distância.**

| aba | linhas | mediana | máximo | pior caso |
|---|---|---|---|---|
| Hoje | 3 | 856,5 px | 858,1 px | "3" → "Ver Progresso" |
| Semana | 13 | 847,6 px | 864,4 px | "Física" → "5h 46m" |
| Progresso | 9 | 864,3 px | **896,3 px** | "Meta" → "25h" |
| Ajustes | 2 | 805,3 px | 805,3 px | "Tema da interface" → "claro" |

Ler "Meta ... 25h" custa **896 px de varredura ocular** — mais que o dobro da medida de
leitura que a própria aplicação definiu para o texto. Não é um erro de contraste nem de
tamanho: é a ausência de uma coluna. A aplicação tem **duas noções contraditórias de "a
largura de uma linha"** e nenhuma delas governa a outra.

Evidência: `capturas/08-progresso-vao-escuro.png` — "Meta" encosta na margem esquerda,
"25h" na direita, e nada entre os dois.

**Proposta.** Introduzir um segundo token de medida para o material tabular — algo como
`--measure-wide: 72ch` (~560–600 px) — e aplicá-lo ao bloco do ledger e das tabelas,
mantendo `--measure` para a prosa. O objetivo não é estreitar por estreitar: é que o par
rótulo/valor caia dentro de **uma saccade** (≈ 400–600 px), e que a régua de seção termine
na mesma coluna que o conteúdo que ela encabeça. Um caderno tem uma largura de página; hoje
esta aplicação tem duas, e a errada venceu.

---

## P2 — A régua não carrega a estrutura

A tese do arquivo é explícita (linha 35): *"A RÉGUA carrega a estrutura"*. E a linha 57
registra a intenção: *"réguas: agora são o elemento estrutural, não um sussurro"*.

Medido, no tema escuro, contra o papel (`#0B0F19`):

| elemento | cor | contraste |
|---|---|---|
| `.row` — separador do ledger (56 linhas em Conteúdos) | `--c-rule-soft` `#1F2735` | **1,28:1** |
| `.sec-head::after` — fio do cabeçalho de seção | `--c-rule` `#2A3244` | **1,49:1** |
| `.leaf` — borda da superfície que flutua | `--c-rule` | **1,49:1** |
| `.rule` — fio solto | `--c-rule` | **1,49:1** |
| `.track` — trilho da barra de progresso | `--c-track` `#2C3547` | **1,56:1** |

No tema claro é **pior**: `.row` **1,12:1**, `.sec-head::after` **1,27:1**, `.track` **1,26:1**.

A régua é, hoje, o elemento menos visível da tela. Quem separa as linhas é o espaço em
branco, não o fio — ou seja, a estrutura que a tese atribui à régua está sendo entregue por
outro elemento, e o "caderno pautado" aparece como uma lista.

**E a própria aplicação já sabe disso.** Linhas 61–66, sobre o interruptor desligado:

> *"Com `--c-rule` o contorno dava 1,49:1 sobre a página: o interruptor desligado não se
> distinguia do papel e parecia um controle inativo. A fronteira do controle precisa de 3:1
> (1.4.11)."*

Foi por isso que `--c-sw-off: #5A6376` (**3,17:1**) existe. O arquivo estabeleceu o
princípio — *um traço que carrega significado precisa de 3:1* — e o aplicou ao interruptor.
**A régua ficou com o valor que o próprio arquivo chama de baixo demais para se distinguir
do papel.** É o mesmo argumento, não aplicado ao elemento que a tese nomeia como estrutural.

**Proposta.** Subir os tokens de régua, mantendo a hierarquia entre eles (o separador de
linha continua mais discreto que o fio de seção):

| token | hoje (escuro) | 2:1 | 3:1 |
|---|---|---|---|
| `--c-rule` | `#2A3244` (1,49:1) | `#404651` | `#58606E` |
| `--c-rule-soft` | `#1F2735` (1,28:1) | `#3E4651` | `#56606E` |
| `--c-track` | `#2C3547` (1,56:1) | `#3F4650` | `#57606E` |

| token | hoje (claro) | 2:1 | 3:1 |
|---|---|---|---|
| `--c-rule` | `#D8DDE6` (1,27:1) | `#B0B1B5` | `#8E8F92` |
| `--c-rule-soft` | `#E7EAF0` (1,12:1) | `#B0B1B4` | `#8F9091` |
| `--c-track` | `#D8DEE9` (1,26:1) | `#AFB2B5` | `#8E8F93` |

Não recomendo 3:1 para o separador de linha — 56 fios a 3:1 viram grade de planilha e
matam a leveza. Recomendo **~2:1 para o separador** (deixa de ser sussurro, continua sendo
fio) e **3:1 para o fio de seção e a borda da superfície** (que delimitam, e delimitam
significado). Medir o resultado nos dois temas depois de trocar.

---

## P3 — A entrelinha vaza na camada de componente

A camada de tokens declara **uma entrelinha por corpo** (1.0 / 1.15 / 1.25 / 1.1 / 1.62 /
1.5 / 1.45 / 1.45). O que o DOM renderiza são **12 entrelinhas distintas para 8 corpos**.

A causa é que quatro componentes **redeclaram** `line-height` por cima do token:

| componente | declara | efeito |
|---|---|---|
| `.t-col` | `line-height: 1.3` | cabeçalho de coluna de tabela |
| `.t-field` | `line-height: 1.3` | rótulo de campo |
| `.btn` | `line-height: 1.4` | e `.btn-sm` herda 1.4 num corpo **menor** |
| `.word` | não declara nada | herda o que estiver em volta |

Resultado direto: **12 px renderiza com quatro entrelinhas diferentes — 15,6 / 16,8 / 17,4 /
18 px.** Mesmo corpo, quatro ritmos, justamente no material tabular que define a estética do
caderno. O olho não nomeia isso, mas sente: as linhas de tabela não respiram juntas.

**Proposta.** Escolher uma das duas e seguir até o fim:

- **(a)** remover as declarações locais e deixar o token de corpo governar — mais simples,
  mas muda a densidade das tabelas;
- **(b)** declarar a entrelinha como token por corpo (`--lh-hint`, `--lh-field`, `--lh-btn`)
  e fazer os componentes **referenciarem** o token em vez de cravarem o número.

A (b) é a que preserva a intenção de densidade e fecha o vazamento. O critério de aceite é
objetivo: **um corpo, uma entrelinha.** Medir os 12 pares e reduzir a 8.

---

## P4 — O espaço não tem camada de token

O bloco de tokens declara cor (`--c-*`), tipografia (`--fs-*`, `--lh-*`) e medida
(`--measure`). **Zero tokens de espaço.** Todo o ritmo vertical vive em classes utilitárias
do Tailwind, com três valores fora da escala escritos à mão dentro de componentes.

Medido: **16 valores distintos** de espaço vertical —
`2, 3, 4, 5, 6, 7, 8, 10, 12, 14, 16, 20, 24, 28, 32, 36 px`.

A maior parte segue o passo de 2 px do Tailwind. Os três fora da escala são da camada
própria: `3px` (`.sec-head` row-gap), `5px` (`.nav-btn` padding), `7px` (`.btn` gap e
padding). E o ritmo de seção usa **três valores diferentes para a mesma função**:
`36px` (`mt-9`, 11×), `28px` (`main` `mt-7`) e `32px` (uma seção com `mb-8`).

Isso não é "bagunça" — é a ausência de uma escala declarada. Sem ela, P1 e P3 não têm como
ser cobrados: não existe o valor contra o qual conferir.

**Proposta.** Declarar a escala de espaço na camada de tokens (`--sp-1 … --sp-6`, algo como
2/4/8/12/16/24/36) e substituir os três valores fora da escala. Ganho imediato: o ritmo de
seção passa a ter um valor só, e a revisão de P1 fica verificável.

---

## P5 — Alvos no piso (polimento, não defeito)

| controle | tamanho | ocorrências |
|---|---|---|
| `.sw` (interruptor) | 34 × **19 px** | 6 |
| `select.inp-quiet` (status do tópico) | 85 × **22 px** | 56 |
| `select.inp-quiet.w-24` (prioridade) | 96 × **22 px** | 6 |
| `.word` (link-botão) | — × **23 px** | 9 |
| `.btn-icon.is-sm` (ação da linha) | **26 × 26 px** | 176 |

**Isto passa em WCAG 2.5.8.** Medi a exceção de espaçamento: a menor distância de um alvo
abaixo de 24 px ao alvo mais próximo é **24,8 px**, contra os 12 px que a norma exige — o
círculo de 24 px de diâmetro centrado em cada alvo não cruza nenhum outro. Zero colisões em
75 alvos medidos.

Mas todos ficam **abaixo dos 44 px** de alvo tátil, e a aplicação tem layout de celular
(`nav` é `fixed inset-x-0 bottom-0` no mobile). No toque, os dois controles mais usados —
o interruptor e o select de status — são os dois menores da tela.

**Proposta.** Não redesenhar nada. Só subir o piso: `.sw` para 24 px de altura e
`.inp-quiet` com `min-height: 24px`. O `.btn-icon.is-sm` a 26 px já está no limite aceitável
para ponteiro; no mobile, subir o padding do alvo sem mexer no glifo.

---

## Verificado e limpo (hipóteses que caíram)

Registrado porque "não achei problema" também é resultado — e porque são os lugares onde se
esperaria achar:

- **Contraste de texto: 478 medições** (5 abas × 2 temas, cada elemento com texto próprio,
  contra o fundo efetivo composto) — **0 reprovações.** Pior caso: 4,85:1 no escuro
  (`.measure` 11 px) e 5,07:1 no claro (`.t-hint` 11 px), ambos acima dos 4,5:1 exigidos.
- **Paleta de matérias: verificada de forma independente.** Recalculei o ΔE00 (CIEDE2000)
  de todos os 15 pares nas três variantes: pior par = **12,32** em `deep`, 13,84 em `color`,
  19,26 em `light` — sempre Matemática × Português. Bate exatamente com o número escrito no
  comentário do arquivo (linha 452). Os pontos medem 5,53–11,47:1 contra o fundo.
- **Altura das linhas do ledger é regular:** 43 px em 50 linhas, 42 px em 6 — e as 6 são
  exatamente as primeiras de cada grupo, onde `.row:first-child` remove o `border-top`. Não
  é tremor de subpixel, é a regra funcionando.
- **Mobile 390 × 844: sem overflow horizontal em nenhuma das cinco abas.**
- **A medida de leitura está dentro da faixa:** `62ch` resolve para 406 px e as linhas cheias
  carregam **68–75 caracteres** (média 71,3), dentro da faixa confortável de 60–75. Ressalva
  de nomenclatura: `ch` vale 6,556 px (deriva do `0` intrínseco da Literata a 11 px) enquanto
  o `0` renderizado mede 8,74 px, porque a aplicação usa numerais tabulares — então o token
  chamado `62ch` entrega 68–75 caracteres. O valor está certo; o **nome** mente.

---

## Ordem sugerida

1. **P1** — a coluna. É o que mais muda a leitura e o que mais aparece na tela.
2. **P2** — as réguas. Barato (três valores) e é a tese do projeto.
3. **P4** — a escala de espaço. Sem ela, P1 e P3 não têm contra o quê ser cobrados.
4. **P3** — a entrelinha. Fecha depois que a escala existe.
5. **P5** — o piso dos alvos. Polimento; não bloqueia nada.

P1 e P2 são independentes e podem andar juntos. P3 depende de P4 para ser verificável.

---
---

# Execução

Os cinco pontos foram implementados **na ordem acima** e medidos um a um. Onde a execução
divergiu da proposta, a divergência está registrada com o número que a decidiu — a proposta era
uma hipótese medida, não um contrato.

Cada par antes/depois abaixo vem do **mesmo instrumento**, rodado no mesmo enquadramento
(1280 × 900, layout assentado). Isso importa: dois harnesses que medem "o vão" com seletores
diferentes dão números diferentes, e misturar os dois numa tabela é comparar réguas distintas.

---

## P1 — a coluna, executado

**Divergência da proposta.** A proposta pedia um segundo token de medida (`--measure-wide: 72ch`)
aplicado **só ao ledger**, mantendo `--measure` para a prosa. O que foi implementado é um token
de **página** — `--page: 42rem` — aplicado a tudo (cabeçalho, índice, texto, réguas).

O motivo veio de uma varredura, não de uma preferência: o vão cai **linearmente** com a largura,
porque o valor é alinhado à direita. Varri 960 → 536 px de conteúdo e escolhi o degrau em que o
pior caso entra numa saccade:

| `max-w` | conteúdo | mediana | **máx** | veredito |
|---|---|---|---|---|
| 1024 (antes) | 960 | 849,1 | **896,3** | longe |
| 900 | 836 | 725,1 | 772,3 | longe |
| 820 | 756 | 645,1 | 692,3 | limite |
| 768 | 704 | 593,1 | 640,3 | limite |
| 720 | 656 | 545,1 | 592,3 | OK |
| **672 (escolhido)** | **608** | **497,1** | **544,3** | **OK** |
| 640 | 576 | 465,1 | 512,3 | OK |
| 600 | 536 | 425,1 | 472,3 | OK |

Escolher só o ledger estreitaria as linhas e deixaria as réguas de seção correndo até a margem
da **janela** — o fio terminaria fora da coluna que ele encabeça. Um caderno tem uma largura de
página. Cabeçalho, índice e texto estreitam juntos, e a régua corre até essa margem.

**Resultado medido** (`vao.js`, mesmo instrumento nas duas pontas):

| aba | antes (mediana / máx) | depois (mediana / máx) | ganho no máx |
|---|---|---|---|
| Hoje | 856,5 / 858,1 | 504,5 / 506,1 | −352 |
| Semana | 847,6 / 864,4 | 495,6 / 512,4 | −352 |
| Progresso | 864,3 / **896,3** | 512,3 / **544,3** | **−352** |
| Ajustes | 805,3 (n = 2) | 453,3 (n = 2) | −352 |

O pior caso da aplicação — *"Meta" → "25h"* — caiu de **896 px para 544 px**. A prosa continua
com os seus 406 px: a medida de leitura não foi tocada, foi **acompanhada**.

Overflow horizontal verificado em 1280 / 1024 / 768 / 390 / 360: **zero em todas as cinco abas**.
A 768 o conteúdo já mede 608 px e a 390 mede 350 px — `--page` é teto, não largura fixa.

Evidência: `capturas/08-progresso-vao-escuro.png` (antes) contra
`capturas/11-progresso-depois-escuro.png` (depois).

---

## P2 — a régua, executado

| elemento | escuro antes | escuro depois | claro antes | claro depois |
|---|---|---|---|---|
| fio de seção (`.sec-head::after`) | 1,49:1 | **3,00:1** | 1,27:1 | **3,00:1** |
| separador do ledger (`.row`) | 1,28:1 | **2,01:1** | 1,12:1 | **2,00:1** |
| trilho da barra (`.track`) | 1,56:1 | **1,99:1** | 1,26:1 | **2,01:1** |
| borda da superfície (`.leaf`) | 1,49:1 | **3,00:1** | — | **3,00:1** |

A hierarquia entre os dois foi mantida **de propósito**: **3:1 para o que DELIMITA** (o fio de
seção, a borda da superfície que flutua) e **~2:1 para o que apenas SEPARA** (as 56 linhas do
ledger). 56 fios a 3:1 viram grade de planilha e matam a leveza que o caderno persegue. O
separador deixou de ser sussurro e continua sendo fio; o fio de seção passou a delimitar.

**Divergência da proposta — e um erro meu que ela continha.** A tabela de valores claros que
escrevi no diagnóstico (`#8E8F92`, `#B0B1B5`) estava **errada**, por dois defeitos somados:

1. a busca binária que usei estava **invertida** para papel claro, e devolvia `#FFFFFF` para
   qualquer alvo;
2. ao consertar, escalei a cor em **espaço sRGB** em vez de **linear**. Escalar em sRGB
   dessatura: as réguas claras viravam cinza-frio, alheio ao papel azulado (`#F6F7FA`), e
   `#8E8F92` entregava **1,268:1** para um alvo de 1,4:1.

O que foi implementado (`#8C9096` e `#AFB1B6`) foi derivado escalando em **espaço linear**, o que
**preserva o matiz** do papel. O mesmo vale no escuro: a proposta sugeria `#58606E` (cinza
neutro); o que ficou é `#515F7E`, que mantém o azul do papel. O erro foi pego pela
inconsistência interna — a curva não era monótona —, não por eu ter desconfiado da tabela.

---

## P4 — o espaço, executado

Escala declarada: `--sp-1 … --sp-6` = **4 / 8 / 12 / 16 / 24 / 36 px**. A regra escrita no
arquivo é *todo espaço é múltiplo de 2 px*.

| | antes | depois |
|---|---|---|
| valores distintos | **16** | **12** |
| fora do passo de 2 px | `3`, `5`, `7` (e `13` na horizontal) | **nenhum** |
| ritmo de seção | 36 / 28 / 32 (três valores) | **36** (um valor) |

O `32px` desapareceu e o `36px` virou o passo único entre seções (19 → 20 ocorrências). O `3px`
do `.sec-head`, o `5px` do `.nav-btn` e o `7px` do `.btn`/`.inp` foram absorvidos pelos degraus.

**Ressalva honesta — e a distinção que a resolve.** Sobrou **um** valor de 28 px: o padding vertical
do cartão de estado vazio (`div.leaf.px-6.py-7`, 5 ocorrências, uma por aba). Medido: **nenhum passo
de seção usa 28 px.** A distinção é a que o próprio arquivo declara — a escala `--sp-*` governa o
**ritmo** (o que separa blocos), não o **respiro interno de um controle**; e 28 px é um meio-degrau
legítimo da grade de 2 px do Tailwind, que é a regra dura (*todo espaço é múltiplo de 2 px*).
Resultado: o **ritmo de seção ficou 100 % token-conformante** (só 36 px), e o que resta fora da
escala está na camada de componente, onde a regra dura é a que vale.

O gate verifica a **regra dura** (nenhum valor fora do passo de 2 px), não a conformidade à escala —
e isso é deliberado: separar "ritmo" de "respiro de componente" por medição não é possível com um
seletor só, então cobrar a escala seria uma asserção que eu não conseguiria provar.

---

## P3 — a entrelinha, executado

Escolhi a opção **(b)** do diagnóstico: token por corpo, com os componentes **referenciando** o
token em vez de cravar o número. Preserva a densidade pretendida das tabelas e fecha o vazamento.
A regra ficou escrita no arquivo: **nenhum componente crava `line-height`.**

| | antes | depois |
|---|---|---|
| corpos | 8 | 8 |
| entrelinhas distintas | **12** | **8** |
| corpos com mais de uma entrelinha | 4 | **0** |

Tabela final — um corpo, uma entrelinha:

```
11 px → 1,45 (×50)     15 px → 1,62 (×98)     26 px → 1,15 (×2)
12 px → 1,45 (×20)     18 px → 1,25 (×22)     40 px → 1,00 (×1)
13 px → 1,50 (×39)     22 px → 1,10 (×7)
```

Os `12 px` renderizavam com **quatro** entrelinhas (15,6 / 16,8 / 17,4 / 18 px); agora renderizam
com uma. E o efeito colateral foi contido: o `.word` caiu de 23 px para 22,4 px, o que o deixaria
abaixo do piso de alvo — recebeu `min-height: 24px` em vez de eu afrouxar a regra.

**Ritmo do ledger inalterado**, que era o risco real desta passagem: 43 px em 50 linhas e 42 px
em 6, exatamente como antes (as 6 são as primeiras de cada grupo, onde `.row:first-child` remove
o `border-top`). Conferido a olho em Semana: cabeçalho e colunas continuam alinhados.

---

## P5 — o piso dos alvos, executado

| controle | antes | depois |
|---|---|---|
| `.sw` (interruptor) | 34 × **19** | **40 × 24** |
| `select.inp-quiet` | — × **22** (62×) | — × **24** |
| `.word` (link-botão) | — × **23** | — × **24** |
| `.btn-sm` | 27,4 | 29,9 |
| `.btn-icon.is-sm` | 26 × 26 | 26 × 26 (inalterado) |

**Abaixo de 24 px: nenhum.** A exceção de espaçamento da 2.5.8 continua valendo depois da troca
(a menor distância entre alvos é 24,8 px, contra os 12 px exigidos).

**Divergência da proposta.** A proposta dizia "só subir o `.sw` para 24 px de altura". Subir só a
altura **achataria** o botão: 22 px de caixa útil para um botão de 13 px deixaria 4 px de folga.
A geometria foi reescalada inteira — caixa útil 38 × 22, botão 18, folga 2, curso 16.

Também foi corrigida uma cor que tinha ficado para trás: a seta do `select.inp-quiet` no tema
claro era `#767D8B` — **exatamente a cor que o próprio arquivo já havia rejeitado** para
`--c-ink3` por dar 3,86:1. Ficou esquecida quando a tinta foi corrigida. Agora acompanha a tinta
terciária (`#636A78`), com um comentário avisando que são as duas únicas cópias.

---

## Validação por mutação

Regra do projeto: **teste que passa com o defeito reintroduzido não vale nada.** Reintroduzi cada
defeito no arquivo, confirmei que a mutação **de fato caiu** (o padrão aparece 1×), rodei o gate,
e restaurei conferindo o md5.

| mutação | defeito reintroduzido | medido depois da mutação | gate |
|---|---|---|---|
| M1 | `--page: 42rem` → `64rem` | vão máx **544,3 → 896,3**; página 672 → 1024 | **FALHA** |
| M2 | `--c-rule` escuro → `#2A3244` | fio de seção **3,00 → 1,49** | **FALHA** |
| M3 | `.btn` crava `line-height: 1.4` | `12 px` ganha 2ª entrelinha; ratios **7 → 8** | **FALHA** |
| M4 | `.sec-head` crava `gap: 3px` | `div.sec-head @3px` fora do passo | **FALHA** |
| M5 | `.sw` volta a `height: 19px` | interruptor **24 → 19**; 6 alvos abaixo de 24 | **FALHA** |

**5 de 5 pegas.** Em todas, o *valor medido mudou* — não me contentei com o veredito. Ao fim,
o arquivo voltou ao md5 exato do baseline e o gate voltou a **PASSA** nos cinco pontos.

O gate é um arquivo só (`gate.js`), que decide sozinho o veredito de cada P. Foi escrito assim de
propósito: se o gate decide, a mutação é um veredito, não uma interpretação minha do número.

---

## Regressão (o que não podia quebrar)

| verificação | resultado |
|---|---|
| Contraste de texto — 478 medições (5 abas × 2 temas) | **0 reprovações** |
| Pior caso de contraste | 4,85:1 escuro / 5,07:1 claro — **idêntico ao de antes** |
| Overflow horizontal — 1280 / 1024 / 768 / 390 / 360 × 5 abas | **0** |
| Ritmo do ledger — 43 px ×50, 42 px ×6 | **inalterado** |
| Alvos abaixo de 24 px | **0** |
| Tema ao fim de cada harness | restaurado (ver ressalva abaixo) |

**Ressalva de instrumento.** O harness de contraste original trocava o tema e **não devolvia** —
e o tema persiste em `localStorage`, então a medição seguinte rodava no tema errado. Pior: eu
descobri isso **olhando um PNG**, não por um número. Corrigido em duas frentes: o harness de
contraste agora restaura o tema antes de retornar, e o gate **pina o tema na entrada** e informa
o tema no fim. Um instrumento que altera o objeto que mede e não desfaz a alteração não é um
instrumento.

---

## Limpeza final (depois da validação)

Duas coisas que eu havia registrado como "de fora" e que são pequenas o bastante para fechar junto:

1. **`.dashed` removido.** Era o único CSS morto do arquivo: definido como
   `border: 1px dashed var(--c-rule)` e com **zero referências** em markup e em JS. Removido, e o
   lugar ficou com uma nota dizendo o que havia ali — se um dia precisar de um contorno tracejado,
   ele volta junto com o uso.
2. **O offset do topo da página virou um passo da escala.** Era `mt-6 md:mt-7` (24 px no celular,
   28 px no desktop — dois valores para a mesma função, e um deles fora da escala). Ficou `mt-6`:
   24 px nos dois, igual a `--sp-5`. Medido depois: `marginTop = 24px` nas cinco abas.

**Re-certificação no build limpo** (md5 `8959d8d92d2c2748eb057403950df32f`): `node --check` nos três
blocos inline OK (o maior com 2026 linhas) · gate **PASSA** nos cinco pontos · contraste **478
medições, 0 reprovadas** (pior 4,85 / 5,07, inalterado) · overflow **0** em 1280 e 390.

---

## Achado por olhar, não por medir: o aviso cobre o título no celular

Este não veio de nenhum harness — veio de **olhar a captura**. O aviso ("Tema escuro ativo.") aparece
em cima do título *Rotina ITA*. Medido, porque "parece que cobre" não é resposta:

| viewport | aviso | cabeçalho | sobreposição com o **título** | elementos interativos cobertos |
|---|---|---|---|---|
| 1280 | 141 × 39,4 em 16→55,4 | 48→78,5 | **não** (largura 0 — o aviso está centrado, o título à esquerda) | **nenhum** |
| 390 | 141 × 39,4 em 16→55,4 | 32→98,9 | **sim: 28,7 × 23,4 px** | **nenhum** |

Três conclusões, e a terceira é a que importa:

1. No desktop **não há sobreposição** com o título — o que a captura sugere é proximidade, não colisão.
2. No celular há: o cabeçalho empilha e começa em 32 px, então o aviso (que começa em 16 px) alcança
   o título. São 28,7 × 23,4 px por ~2,7 s.
3. **Nenhum elemento interativo é coberto, nos dois viewports.** O `#toast-root` é
   `pointer-events-none` e o item do aviso é `pointer-events-auto` — mas ele não cobre botão nenhum,
   então não engole clique. O defeito clássico ("o aviso fixo que come o clique") **não** se aplica.

**Não corrigido, de propósito.** O arquivo declara que a superfície é para o que flutua, e um aviso
que flutua sobre conteúdo é o comportamento pretendido; mover o aviso para baixo só transferiria a
sobreposição para o `nav` ou para o primeiro bloco. Fica registrado com o número, para a decisão ser
de quem olha o produto — não minha.

---

## O que ficou de fora (e por quê)

- **`.leaf`: o harness de régua lê o *preenchimento*, não a *borda*.** Ele reporta 1,09:1 para a
  superfície — que é o papel da superfície contra o papel da página, um número real, mas não o
  que a linha da tabela de P2 quer dizer. A **borda**, medida à parte, dá **3,00:1** nos dois
  temas. Fica a nota porque a confusão é fácil de repetir.
- **Ainda em aberto, do diagnóstico funcional anterior:** planejar semanas futuras; busca/filtro
  em Conteúdos (56 tópicos); desfazer para exclusão e reset; e `pendingConfirm` sendo um global
  único (dois modais de confirmação não podem coexistir).
- **Resolvidos nesta passagem:** `.dashed` (CSS morto, removido — ver *Limpeza final*) e o
  comentário obsoleto da lista de `activities`, que documentava `minutes` quando o campo é
  `plannedMinutes` desde a separação plano/realizado (agora na linha 705, não 614 — o número
  antigo era de antes destas edições).

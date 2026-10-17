# Plano de refatoração — visual e estruturação de telas

Diagnóstico medido antes de propor. Todos os números vieram do código e de um
navegador real (`agent-browser` 0.39, via CDP) sobre
`index.html` md5 `6d958a3fcd316d3c74d5342dd7c197f6`.

---

## O que foi medido

### O arquivo

| | valor |
|---|---|
| linhas totais | **2549** |
| bytes | 132.377 (129,3 KB) |
| folha própria (`<style>`, linhas 25–469) | 444 linhas, **24,8 KB**, 103 regras |
| shell do documento (480–516) | 38 linhas |
| app JS (517–2547) | 2030 linhas, **16 seções numeradas**, **75 funções** |
| render() | 8 linhas — despachador fino |
| views | 5 funções puras que devolvem string (`viewHoje`…`viewAjustes`) |
| eventos | delegação única (seção 15) |

### As dependências externas

| dependência | o que baixa | o que o app usa | bytes → resultado |
|---|---|---|---|
| Tailwind **Play CDN** | compilador JIT inteiro | **200** utilitárias literais + 17 dinâmicas (29 com prefixo responsivo) | **397,7 KB → 8,0 KB** de CSS |
| Lucide **UMD** | 2.129 ícones | **15** (medido no DOM renderizado) | **435,9 KB → ~6,8 KB** de SVG |
| Google Fonts (Literata) | CSS + 5 arquivos servidos, **2 baixados** | 1 família, serifada, variável | ~4,8 KB de CSS + **218 KB** decodificados |

**Total do payload: ~1186 KB, dos quais ~1056 KB (89 %) são runtime de terceiro.**

### O comportamento offline (medido, com os CDNs apontados a uma porta morta)

| | online (controle) | offline |
|---|---|---|
| `window.tailwind` | `object` | `undefined` |
| `window.lucide` | `object` | `undefined` |
| `<svg>` no documento | 8 | **0** |
| `.row` `display` | `flex` | **`block`** |
| `.page` `padding-left` | `32px` | **`0px`** |
| `.row` `padding-top` | `12px` | **`0px`** |
| `t-h1` `font-family` | Literata, Georgia | Literata, Georgia (o **arquivo** da Literata não carrega) |

E `file:///…index.html` **funciona** — protocolo `file:`, 8 abas, 785 caracteres
de conteúdo renderizados. A aplicação continua utilizável, mas visualmente
degrada **sem nenhum erro na tela**.

---

## A tese

**O arquivo não é o problema.** 16 seções numeradas, 75 funções, `render()` com
8 linhas, views puras que devolvem string, delegação única de eventos, e uma
camada de componentes que já existe (`INP`, `BTN_PRI`, `BTN_GHOST`,
`BTN_DANGER`, `BTN_ICON` mapeiam para classes reais em `<style>`).

**O problema é o runtime.** O aplicativo gasta 397,7 KB para gerar 8,0 KB de
CSS e 435,9 KB para desenhar 15 ícones. Some a isso a ausência de rede:
degrada em silêncio.

**E o visual é bicameral.** 24,8 KB de tokens e 103 regras mandam de um lado;
do outro, 200 nomes de utilitária e 26 `style=""` inline são emitidos de dentro
de strings de template em JavaScript. Uma mudança de aparência é editada num
template, onde classe utilitária e estilo inline se misturam — e o CSS
efetivamente renderizado não pode ser auditado estaticamente, porque é gerado
em runtime por um servidor de terceiro.

A refatoração que vale a pena é a que **fecha a runtime e unifica o visual**.
Não é a que reescreve o arquivo.

---

## O que NÃO vale a pena (e por quê)

1. **Reescrever o `index.html` do zero.** O que está lá funciona e está
   organizado. Um rewrite trocaria 75 funções testáveis por 75 funções novas,
   com o mesmo visual, para zero ganho funcional. Risco puro.
2. **Migrar para React/Vue/Svelte.** Cinco telas, estado em memória, um
   `localStorage`. Um framework traria build, bundle e uma cadeia de ferramentas
   para uma aplicação que hoje abre com duplo clique.
3. **Trocar o sistema visual.** "Caderno pautado" está medido, aplicado e
   validado por mutação neste repositório (ver `melhorias-ui.md`). A tese
   (uma cor só, a das matérias; a régua carrega a estrutura; uma serifada) não
   é o alvo — o alvo é *como ela chega à tela*.
4. **ES modules em `<script type="module">`.** `file://` funciona hoje, e
   módulos são bloqueados por CORS em `file://`. Qualquer divisão em arquivos
   precisa de um passo de build que **re-inline** tudo no `index.html`. Sem
   isso, "modularizar" quebra a propriedade de entregável único.

---

## Os achados que mandam no plano

**F1 — 89 % do payload é alheio.** 1,05 MB de runtime de terceiro contra 129 KB
de aplicação.

**F2 — Offline degrada em silêncio.** Sem rede: layout colapsa (`.row` de
`flex` para `block`, padding da página a zero) e os ícones somem. Nenhuma
mensagem. Para um organizador de estudos que a pessoa abre para estudar — muitas
vezes sem rede — isso é o defeito mais sério da lista, e não apareceu em
nenhuma varredura de contraste ou overflow porque todas mediram com rede.

**F3 — O escape está correto, verificado empiricamente.** Injetei um tópico
chamado `<img src=x onerror="…">` e observações `<script>…</script>` direto no
`localStorage`, recarreguei e **olhei o DOM**: nenhum `onerror` executou
(`window.__XSS_TOPICO` e `window.__XSS_NOTAS` ambos `false`), `<img>` real
**0**, `<script>` **0**, e o nome hostil aparece como **texto**
(`innerHTML` com `&lt;img src=x`, sem `<img` cru), nas abas Hoje, Conteúdos e
Progresso. Escape **não** é dívida; não entra no plano.

**F4 — A lógica pura hoje não é testável fora do browser.** `normalize`,
`pareceBackup`, `mesclarBackup`, `weekKeyOf`, `fmtMinutes`,
`suggestedMinutesBySubject`, `clamp`, `pct` e mais umas poucas são funções puras
dentro de um `<script>` inline de 2.030 linhas. Não dá para importá-las em Node
— então as regras mais críticas do app (o que faz um backup ser um backup, o que
uma sessão com data futura deve recusar) só são exercitáveis com navegador. O
projeto já validou essas correções por mutação, mas cada rodada custa um ciclo
inteiro de browser.

**F5 — A camada de componentes já começou.** `INP`, `BTN_PRI`, `BTN_GHOST`,
`BTN_DANGER`, `BTN_ICON` já são constantes que mapeiam para classes reais.
Falta estender o padrão às 200 utilitárias restantes.

---

## As fases

Cada uma tem um **critério de aceite medido** e é **validada por mutação** antes
de seguir. A ordem não é arbitrária: F2 (offline) e F1 (payload) são as que
corrigem o que um usuário sente, e são também as mais baratas.

### Fase 0 — Recriar a guarda (pré-requisito, não é opcional) — **PARCIALMENTE EXECUTADA**

O gate desta sessão morreu com o `/tmp/ui` (a pasta é descartável e foi limpa
entre sessões). Ele precisa voltar a viver **no repositório**, não em `/tmp`:
`gate.js` + o driver de mutação, rodando as cinco asserções de P1–P5 mais as
três novas que este plano introduz. Enquanto ele vive em `/tmp`, toda rodada de
mutação começa por reescrever o instrumento.

- **Feito:** o instrumento vive em `verificacao/` — `av.sh` (wrapper do
  `agent-browser eval` que trata resposta vazia como erro, não como zero),
  `dec.py` (duplo-decode do JSON do CLI), `colhe.js`/`colhe_todos.js`
  (colheita dos SVGs), `sonda.js` + `compara.py` (o gate antes/depois desta
  fase). Uma rodada de mutação de 5 defeitos… ficou em 4/4 nesta fase — todas
  pegadas, todas com md5 restaurado (ver `verificacao/mutacoes.md`).
- **Falta:** reversionar o `gate.js` geral com as asserções P1–P5 da sessão
  anterior (render das 5 abas, ícones, escaping, tema, persistência), hoje
  ainda só existindo no histórico da conversa.

### Fase 1 — Substituir o Lucide por caminhos inline — **EXECUTADA (2026-10-10)**

**O quê:** extrair os SVGs usados como strings inline e trocar
`lucide.createIcons()` por um injetor local. Medido no DOM renderizado: **26
nomes** (15 nas abas com os dados semeados + 11 que só aparecem em modais ou
estados que estes dados não alcançam) — os 26 foram mapeados, porque call site
que existe não pode depender de estado sorteado.

**Como:** o SVG renderizado de cada ícone foi **colhido da própria
biblioteca** (`verificacao/colhe_todos.js` injeta os 26 `<i data-lucide>` num
contêiner fora da tela, chama o `createIcons()` do UMD e grava o
`outerHTML`): 10.843 bytes de markup, nenhum byte digitado de memória. O
merge de atributos também foi medido, não suposto — a biblioteca anexa a
classe do placeholder **depois** de `lucide lucide-<nome>`, copia `style`,
sobrepõe `stroke-width` e derruba `aria-hidden` quando o placeholder tem
`aria-label`. O injetor replica os quatro; a query é só `i[data-lucide]`
porque o `<svg>` resultado carrega `data-lucide`.

**Ganho:** −435,9 KB de download; +10,8 KB no arquivo.

- **Aceite (medido):** `window.lucide` deixou de existir (`typeof` =
  `undefined`; 0 tags `<script>` apontando lucide); os 271 `<svg>` das 5 abas
  e dos 4 modais que abrimos são idênticos ao controle atributo por atributo,
  em ordem, markup interno, geometria (rect) e estilo computado; 15
  `outerHTML` sintéticos — as formas de placeholder do código mais os 5 nomes
  que os dados não alcançam — **byte a byte** iguais; zero `<i>` órfão;
  estado persistido intacto (56 tópicos / 0 / 0).
- **Mutação:** 4/4 pegas — ícone fora do mapa, merge de classe quebrado
  (geometria 18→24 denuncia), cópia de `style` quebrada (**só a seção
  sintética pega** — com 0 atividades o check verde nunca renderiza no DOM) e
  query genérica `[data-lucide]` (classe acumulada a cada re-paint).
  Detalhe em `verificacao/mutacoes.md`.
- **Efeito colateral bom, medido:** em `file://`, com os CDNs inacessíveis,
  os ícones continuam renderizando (8 `<svg>` na aba Hoje, 0 órfãos) — deixaram
  de ter dependência de rede. O Tailwind segue dependendo (é a Fase 2).

### Fase 2 — Pré-gerar o CSS do Tailwind

**O quê:** capturar os 8,0 KB que o Play CDN gera (120 regras, 148 seletores,
incluindo o preflight) e colá-los num `<style>` local; remover o `<script>` do
CDN. As 200 utilitárias ficam como estão, nas strings de template — esta fase
só troca de **onde o CSS vem**.

**Como:** o CDN injeta exatamente um `<style>` no `head` (medido: 2 estilos
online, 1 offline). Ele é legível por `document.styleSheets`. Copiar esse
texto substitui o compilador pelo seu produto.

**Verificado, e isso facilita:** o bloco `tailwind.config` (linhas 14–22) só
estende `fontFamily.sans` com a pilha da Literata — e a app **não usa
`font-sans` em nenhum lugar** (0 ocorrências). A família é declarada no próprio
`body`, na linha 197–198, dentro da folha de tokens. Ou seja: **o bloco de
configuração é configuração morta** e pode ir embora junto com o CDN, sem
perder nada. A extração é literalmente "copiar o CSS gerado".

**Ganho:** −397,7 KB; e some a **corrida de JIT** — o fato que já custou duas
medições erradas neste repositório (medir antes de o Tailwind injetar as classes
lê um layout que não é o entregue, e acusou 18 estouros que não existiam).
Passa a ser possível auditar o CSS renderizado com `grep`.

**Risco:** baixo. A única serventia do config seria `font-sans`, que não é usada.

- **Aceite:** `<svg>` e layout idênticos ao controle em 1280/390; zero
  diferença em `scrollWidth`; o CSS gerado pelo CDN não é mais necessário.
- **Mutação:** apagar uma regra do CSS extraído e exigir que a varredura de
  overflow a denuncie.

### Fase 3 — Trazer a Literata para casa

**O quê:** a tese é *uma* serifada. Duas opções medidas:

- **(a) Self-host com subset:** a app usa um conjunto de glifos pequeno e
  conhecido (nada de CJK). Subsetado para latim básico, a Literata cai para
  uma fração dos 218 KB. Mantém a tipografia escolhida.
- **(b) Serifada do sistema:** `Georgia, 'Times New Roman', serif` — zero
  bytes, zero rede, e a app já declara exatamente isso como *fallback*.

**Minha opinião: (a), com (b) como degrade.** A Literata foi escolhida por três
razões funcionais escritas no próprio arquivo; trocá-la por Georgia muda o
produto. Mas o valor exato do subset **não foi medido** — depende de quais
glifos e quais pesos a app realmente usa, e isso precisa de uma medição antes
de eu prometer um número.

- **Aceite:** offline, `t-h1` renderiza com a Literata (ou o degrade admitido),
  e a varredura de contraste segue em 0 reprovações nos dois temas.
- **Mutação:** remover o `@font-face` e conferir que a sonda de fonte denuncia.

### Fase 4 — A camada de componentes (o refactor "visual" de verdade)

**O quê:** transformar as 200 utilitárias literais em classes nomeadas em
`<style>`, do mesmo jeito que `BTN_PRI` já faz. Não é um redesign: é dar nome
ao que já existe, para que a aparência seja **auditável** e more num lugar só.

Isto é a fase que resolve o "visual bicameral", e é a única com risco real de
regressão visual. Por isso vem **depois** das três que são mecânicas: quando o
runtime estiver fechado e o gate verde, a mudança fica medida em cima de uma
base estável.

- **Aceite:** cada view emite classes nomeadas; `<style>` cresce; zero
  utilitária literal restante em `class=""`; as 18 larguras de overflow
  (110 a 100 % + 70 a 200 %) seguem em zero; contraste segue 478/0.
- **Mutação:** trocar o valor de um token de componente e exigir que a
  varredura de overflow/contraste denuncie.

### Fase 5 — `src/` com build que re-inline

**O quê:** dividir os 2.030 linhas em módulos (`logica/`, `telas/`, `estado/`,
`estilo/`) e um script de build que produza **um** `index.html` — porque
`file://` funciona hoje e `<script type="module">` quebraria isso.

O ganho não é organizacional, é **testável**: as ~12 funções puras passam a ser
importáveis em Node com `node:test`, e as regras críticas (`pareceBackup`,
`mesclarBackup`, `normalize`, `dataDeSessao`) ganham suíte que roda em
milissegundos, sem browser.

- **Aceite:** `node --test` verde nas funções puras; o `index.html` gerado tem
  MD5 diferente mas **comportamento idêntico** — verificado pelas mesmas 18
  larguras de overflow; abre por `file://`.
- **Mutação:** introduzir um defeito numa função pura e exigir que o teste de
  unidade falhe.

---

## Ordem

**0 → 1 → 2 → 3 → 4 → 5.**

- **1 e 2 antes de 4**, embora 4 seja o "refactor visual" propriamente dito:
  são mecânicas, ganham 833 KB e somam com a corrida de JIT. Fazê-las depois
  significaria medir regressão visual em cima de um runtime instável.
- **3 é independente** das outras e pode ir a qualquer momento depois de 2.
- **4 é a fase que mais muda a aparência**, então precisa do gate completo e
  das 18 larguras de overflow verdes.
- **5 por último**, porque só compensa quando as fronteiras dos módulos estão
  estáveis — senão o build é reescrito a cada fase.

**Uma ressalva sobre a Fase 5:** hoje, com 2.030 linhas e 16 seções numeradas,
o custo de build pode não pagar o ganho. Meu conselho é fazer 1–4, medir, e só
então decidir se 5 vale. Se valer, o teste é simples: as funções puras são
testáveis sem browser?

---

## Fora do escopo destas fases

- **Funcionalidades novas** (planejar semanas futuras, busca em Conteúdos,
  desfazer exclusão/reset, `pendingConfirm` global). São débito funcional de
  outra natureza; misturá-las com refactor visual é como não fazer nenhum dos
  dois.
- **A tese visual.** Não se mexe.
- **O aviso que cobre o título no celular** (28,7 × 23,4 px a 390, já medido em
  `melhorias-ui.md`). Decisão de produto, não de arquitetura.

---

## Como saber que deu certo

Uma única métrica, medida antes e depois de cada fase:

| | hoje | depois da Fase 1 (medido) | alvo |
|---|---|---|---|
| payload total | ~1186 KB | **~750 KB** (1186 − 435,9 do Lucide) | ~137 KB só com as fases 1–2; ~160 KB com a 3 (o subset **não foi medido**) |
| bytes de terceiros | ~1056 KB (89 %) | **~620 KB** (Tailwind 397,7 + fontes 218 + …) | **0** |
| dependências de rede | 3 | **2** (Tailwind + fontes) | **0** |
| funciona offline | não (degrada em silêncio) | parcial: **ícones sim**, layout/folha ainda não | **sim** |
| abre por `file://` | sim | **sim, com ícones** (verificado) | **sim** (obrigatório) |
| overflow (18 larguras) | 0 | 0 (mesma sonda, mesma fixture) | 0 |
| contraste (478 medições) | 0 reprovações | 0 reprovações | 0 reprovações |
| escape de dados do usuário | correto (medido) | correto (mesma fixture, mesma sonda) | correto |

Os 8,0 KB de CSS extraído **entram** no `index.html` na fase 2 — o arquivo vai de
129,3 KB para ~137 KB. Não some, troca de dono.

O número que resume o plano: **1056 KB (89 %) é runtime de terceiro.** A
aplicação em si são 129 KB — agora 141,8 KB (129,3 + os 10,8 KB do mapa de
ícones e o injetor, −0,2 KB de script e regra removidos), que é o preço de
tirar 435,9 KB da rede.


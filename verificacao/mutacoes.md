# Fase 1 — verificação por mutação

Cada mutação foi aplicada ao `index.html` já com a Fase 1, medida pela MESMA
sonda (`sonda.js`) e julgada pelo MESMO comparador (`compara.py`) contra o
controle de antes (`controle-pre-fase1.json`). Toda mutação foi revertida e o
md5 devolvido a `7b0573054987d9d0207f6b2cc6178b08` (verificado depois de cada
revert).

| # | mutação | veredito | como a sonda achou |
|---|---------|----------|--------------------|
| M1 | `'settings'` removido do mapa ICONES | **FALHA (36)** | `<i data-lucide> ÓRFÃO: settings` nas 5 abas e nos 4 modais; total de `<svg>` 271 → 262; contagem por nome divergente em todos os contextos |
| M2 | merge de classe desligado (`+ ' ' + a.value` removido) | **FALHA** | atributo `class` sem as classes do call-site e geometria `h: 24` onde o controle tem `h: 18` — os ícones do nav cresceriam 18×18 → 24×24 |
| M3 | cópia de `style` desligada | **FALHA (2)** | **invisível no DOM**: com 0 atividades, o `<i>` que carrega `style` (o check verde da aba Hoje) nunca renderiza — os 271 ícones do DOM passam. Quem pegou foi só a seção
sintética: `outerHTML` do `check` sem `style="color:var(--c-ok)"`. Uma sonda
só de DOM teria dado PASSA. |
| M4 | query do injetor alargada para `[data-lucide]` | **FALHA (5)** | classe ACUMULADA a cada re-paint: `class="lucide lucide-book-open lucide lucide-book-open h-[18px] w-[18px]"` nos ícones da aba por baixo do modal (o `paint()` do modal re-processou os `<svg>` já substituídos) + segunda passada sintética divergente |

Leituras que isto sustenta:

1. **A asserção de órfão não é decorativa** — M1 prova que um ícone faltando
   no mapa aparece nomeado, em todos os contextos, e não como "sumiu um svg".
2. **A asserção de geometria não é decorativa** — M2 prova que o comparador
   comparar rect, não só atributo: o dano visual (ícone 33 % maior) teria
   passado batido por uma comparação só de nomes.
3. **A seção sintética do probe existe por M3** — estados que os dados atuais
   não alcançam (0 atividades, 0 tópicos arquivados) são injetados como
   placeholder de verdade e renderizados pelo próprio `paint()` do app. Sem
   ela, a quebra da cópia de `style` seria invisível.
4. **A query `i[data-lucide]` não é estilo, é contrato** — M4 mostra que a
   query genérica corrompe o documento em silêncio (crescimento monótono da
   classe), e que a segunda passada sintética é o que a denuncia mais cedo.

Rodada final depois de todos os reverts: **PASSA** —
271 ícones idênticos ao controle em 5 abas + 4 modais, 15 `outerHTML`
sintéticos byte a byte iguais (inclusive os 5 nomes que nunca renderizam nos
dados semeados), zero `<i>` órfão, estado persistido intacto (56/0/0).

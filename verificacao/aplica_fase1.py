#!/usr/bin/env python3
"""aplica_fase1.py — aplica a Fase 1 (lucide UMD -> mapa ICONES inline).

Três substituições exatas, uma por região, cada uma verificada por
contagem de ocorrências antes de agir:
  1. o corpo de paint() (que chamava lucide.createIcons) dá lugar ao mapa
     ICONES + ao injetor local;
  2. a tag <script> do UMD lucide@1.52.0 sai do <head>;
  3. a regra morta i[data-lucide] (e seu comentário velho) sai do <style>.
Nada mais é tocado. A verificação final confronta o resultado com o baseline:
o arquivo novo tem de ser exatamente o baseline com essas três regiões
trocadas.
"""
import sys

ARQ = '../index.html'
BASELINE = '.baseline-pre-fase1.html'
FRAG = 'icones.frag.js'

NOVO_PINT = '''/* Ícones como SVG inline, um mapa por nome. Cada entrada é o outerHTML que a
   própria lucide@1.52.0 produzia — colhido por renderização em
   verificacao/colheita_completa.json, não digitado de memória. Troca os
   435,9 KB do UMD por 10,8 KB de mapa, com a marcação idêntica à do
   controle, atributo por atributo: width/height 24 ficam (quem dimensiona
   é a classe do call-site, como sempre foi). */
'''

NOVO_PAINT2 = '''
/* Substitui os <i data-lucide> pelo SVG do mapa repetindo o merge que o
   createIcons() fazia: os atributos do placeholder são copiados por cima
   dos defaults, a classe é ANEXADA depois de `lucide lucide-<nome>` e um
   placeholder com aria-label não leva aria-hidden. Um call site depende
   disso — o check verde da aba Hoje passa style="color:var(--c-ok)" e a
   classe do nav passava h-[18px] w-[18px].
   A query é só <i>: o <svg> resultado carrega data-lucide, e uma query
   genérica por [data-lucide] re-processaria o próprio substituto a cada
   render, acumulando classe. Ícone fora do mapa não é apagado em silêncio —
   fica como <i> órfão e o nome aparece no console. */
function paint() {
  const faltando = [];
  document.querySelectorAll('i[data-lucide]').forEach(el => {
    const nome = el.getAttribute('data-lucide');
    const html = ICONES[nome];
    if (!html) { faltando.push(nome); return; }
    const tpl = document.createElement('template');
    tpl.innerHTML = html;
    const svg = tpl.content.firstElementChild;
    if (!svg) { faltando.push(nome); return; }
    [...el.attributes].forEach(a => {
      if (a.name === 'data-lucide') return;
      if (a.name === 'class') {
        svg.setAttribute('class', svg.getAttribute('class') + ' ' + a.value);
      } else {
        svg.setAttribute(a.name, a.value);
      }
    });
    if (el.hasAttribute('aria-label') || el.hasAttribute('aria-labelledby')) {
      svg.removeAttribute('aria-hidden');
    }
    el.replaceWith(svg);
  });
  if (faltando.length) console.warn('Ícone ausente do mapa ICONES:', faltando.join(', '));
}
'''

def troca_uma(txt, de, para, rotulo):
    n = txt.count(de)
    if n != 1:
        print(f'ABORTADO: "{rotulo}" aparece {n}x (esperava 1)', file=sys.stderr)
        sys.exit(1)
    return txt.replace(de, para, 1)

def main():
    txt = open(ARQ, encoding='utf-8').read()
    frag = open(FRAG, encoding='utf-8').read().rstrip('\n')  # const ICONES = {...};

    # --- 1. paint() + mapa ---
    velho_paint = """/* No Lucide v1, createIcons() exige o objeto de ícones — sem isso ele lança erro. */
function paint() {
  const L = window.lucide;
  if (!L || typeof L.createIcons !== 'function') return;
  try { L.createIcons({ icons: L.icons || {} }); }
  catch (err) { console.warn('Lucide indisponível, seguindo sem ícones.', err); }
}"""
    txt = troca_uma(txt, velho_paint,
                    NOVO_PINT + frag + NOVO_PAINT2, 'bloco paint() velho')

    # --- 2. tag do UMD ---
    txt = troca_uma(txt,
        '<script src="https://unpkg.com/lucide@1.52.0/dist/umd/lucide.min.js"></script>\n',
        '', 'tag <script> do lucide')

    # --- 3. regra morta do CSS ---
    txt = troca_uma(txt,
        "  /* só vale antes da substituição pelo SVG (o <i> vira <svg class=\"h-* w-*\">) */\n"
        "  i[data-lucide] { width: 1em; height: 1em; stroke-width: 1.75; }\n",
        '', 'regra morta i[data-lucide]')

    # --- verificação: só essas três regiões mudaram ---
    base = open(BASELINE, encoding='utf-8').read()
    # remonta o baseline a partir do novo, desfazendo as três trocas
    reconta = txt
    # 1
    bloco_novo = NOVO_PINT + frag + NOVO_PAINT2
    if reconta.count(bloco_novo) != 1:
        print('ABORTADO: bloco novo não encontrado 1x para reconstrução', file=sys.stderr)
        sys.exit(1)
    reconta = reconta.replace(bloco_novo, velho_paint, 1)
    # 2 e 3: reinsere o script (vinha logo antes do <style>) e a regra CSS
    # (vinha logo antes do .no-scrollbar), nas âncoras verificadas por contagem
    ancora = '</script>\n\n<style>\n'
    if reconta.count(ancora) != 1:
        print(f'ABORTADO: âncora </script>+<style> aparece {reconta.count(ancora)}x', file=sys.stderr)
        sys.exit(1)
    reconta = reconta.replace(ancora,
        '</script>\n<script src="https://unpkg.com/lucide@1.52.0/dist/umd/lucide.min.js"></script>\n\n<style>\n', 1)
    ancora_css = '  .no-scrollbar::-webkit-scrollbar { display: none; }\n'
    if reconta.count(ancora_css) != 1:
        print(f'ABORTADO: âncora .no-scrollbar aparece {reconta.count(ancora_css)}x', file=sys.stderr)
        sys.exit(1)
    reconta = reconta.replace(ancora_css,
        "  /* só vale antes da substituição pelo SVG (o <i> vira <svg class=\"h-* w-*\">) */\n"
        "  i[data-lucide] { width: 1em; height: 1em; stroke-width: 1.75; }\n" + ancora_css, 1)
    if reconta != base:
        print('ABORTADO: a reconstrução não devolve o baseline byte a byte', file=sys.stderr)
        # Diagnóstico: primeira diferença
        for i, (x, y) in enumerate(zip(base, reconta)):
            if x != y:
                print(f'  primeira diferença no offset {i}:', file=sys.stderr)
                print(f'  baseline: {base[max(0,i-60):i+60]!r}', file=sys.stderr)
                print(f'  recons  : {reconta[max(0,i-60):i+60]!r}', file=sys.stderr)
                break
        sys.exit(1)

    open(ARQ, 'w', encoding='utf-8').write(txt)
    print(f'index.html reescrito: {len(base)} -> {len(txt)} bytes ({len(txt)-len(base):+d})')
    print('reconstrução contra o baseline: idêntica (só as 3 regiões mudaram)')

if __name__ == '__main__':
    main()

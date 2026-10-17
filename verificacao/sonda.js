/* sonda.js — UMA sonda, usada IDÊNTICA antes e depois da Fase 1.
 *
 * Tira uma fotografia do documento: as 5 abas, os modais que abrem de verdade
 * e uma secao sintetica que mede o MERGE de atributos do lugar que substitui
 * os <i data-lucide> — chamando o proprio paint() do app.
 *
 * Antes: paint() = lucide.createIcons(). Depois: paint() = injetor local.
 * A fotografia dos dois mundos é comparada por compara.py. O que pode mudar
 * de um mundo para o outro está declarado lá (window.lucide, tag <script>);
 * todo o resto tem de ser igual.
 *
 * Regras que esta sonda obedece (aprendidas na marra):
 *  - IIFE sempre: o `agent-browser eval` compartilha UM escopo persistente.
 *  - numero que pode dar -0 sai com `+ 0` — o CDP serializa -0 como
 *    `unserializableValue` e a asserção morre sem detalhe.
 *  - espera de animação: o modal entra com anim-sheet; sem freio, o rect é
 *    medido no meio da animação. O freio é injetado e REMOVIDO, e roda igual
 *    nos dois mundos.
 *  - nada de save(): todos os cliques são de abrir/fechar modal. O estado
 *    persistido é lido no início e no fim para provar que não mudou.
 */
(() => {
  const R = {};

  let lsAntes = null;
  try { lsAntes = JSON.parse(localStorage.getItem('rotina-ita-v1') || 'null'); } catch (e) {}

  /* ---------------- documento ---------------- */
  R.doc = {
    lucide: typeof window.lucide,
    scriptsLucide: [...document.scripts].filter(s => /lucide/i.test(s.src)).length,
    tema: document.documentElement.className,
    lsTopicos: lsAntes && Array.isArray(lsAntes.topics) ? lsAntes.topics.length : null,
    lsAtividades: lsAntes && Array.isArray(lsAntes.activities) ? lsAntes.activities.length : null,
    lsSessoes: lsAntes && Array.isArray(lsAntes.sessions) ? lsAntes.sessions.length : null,
  };

  /* ---------------- fotografia de um estado do documento ----------------
     Para cada <svg>: nome, mapa de atributos, ORDEM dos atributos, markup
     interno, geometria (rect) e estilos computados que mudam aparência.
     Junto: quantos <i data-lucide> sobraram ORFAOS (placeholder não substituído). */
  const medir = () => {
    const svgs = [...document.querySelectorAll('svg')].map(s => {
      const r = s.getBoundingClientRect();
      const cs = getComputedStyle(s);
      return {
        nome: s.getAttribute('data-lucide'),
        attrs: Object.fromEntries([...s.attributes].map(a => [a.name, a.value])),
        ordem: [...s.attributes].map(a => a.name).join(','),
        inner: s.innerHTML,
        w: Math.round(r.width * 100) / 100 + 0,
        h: Math.round(r.height * 100) / 100 + 0,
        sw: cs.strokeWidth, disp: cs.display, cor: cs.color, fill: cs.fill,
      };
    });
    const orfaos = [...document.querySelectorAll('i[data-lucide]')];
    const contagem = {};
    for (const s of svgs) contagem[s.nome] = (contagem[s.nome] || 0) + 1;
    return {
      totalSvg: svgs.length,
      orfaos: orfaos.length,
      nomesOrfaos: orfaos.map(e => e.getAttribute('data-lucide')),
      contagem,
      svgs,
    };
  };

  const clicar = (sel) => { const el = document.querySelector(sel); if (!el) return false; el.click(); return true; };
  const abaAtiva = () => { const b = document.querySelector('[data-tab][aria-current]'); return b ? b.getAttribute('data-tab') : null; };

  /* ---------------- abas ---------------- */
  R.abas = {};
  for (const id of ['hoje', 'semana', 'conteudos', 'progresso', 'ajustes']) {
    const ok = clicar(`[data-tab="${id}"]`);
    const reg = { clicou: ok, abaAtiva: abaAtiva() };
    if (ok) reg.snap = medir();
    R.abas[id] = reg;
  }

  /* ---------------- modais ----------------
     Abre pelo caminho real do usuário (clique), fotografa, fecha pelo X.
     confirmModal é alcançado por deletar atividade (ou, se não houver, pelo
     Zerar aplicação de Ajustes) — em nenhum dos casos o estado é gravado,
     porque a confirmação é um segundo clique que esta sonda não dá. */
  R.modais = {};
  const freio = document.createElement('style');
  freio.textContent = '*,*::before,*::after{animation:none !important;transition:none !important}';
  document.head.appendChild(freio);

  const abrirModal = (chave, alvo) => {
    const el = typeof alvo === 'string' ? document.querySelector(alvo) : alvo;
    const ok = !!el;
    if (ok) el.click();
    const root = document.querySelector('#modal-root');
    const visivel = !!(root && !root.classList.contains('hidden'));
    const reg = { clicou: ok, visivel };
    if (visivel) {
      const t = root.querySelector('#modal-titulo');
      reg.titulo = t ? t.textContent.trim() : null;
      reg.snap = medir();
      const x = root.querySelector('[data-act="close-modal"]');
      if (x) x.click();
      reg.fechou = document.querySelector('#modal-root').classList.contains('hidden');
    } else {
      reg.titulo = null;
    }
    R.modais[chave] = reg;
  };

  clicar('[data-tab="hoje"]');
  abrirModal('nao-planejado', '[data-act="unplanned"]');

  const concluir = [...document.querySelectorAll('[data-act="complete"]')]
    .find(b => (b.getAttribute('title') || '').indexOf('Concluir') === 0)
    || document.querySelector('[data-act="complete"]');
  if (concluir) abrirModal('concluir', concluir);
  else R.modais.concluir = { clicou: false, motivo: 'nenhum botao complete no documento' };

  if (document.querySelector('[data-act="del-activity"]')) {
    abrirModal('confirmar-exclusao-atividade', '[data-act="del-activity"]');
  } else {
    clicar('[data-tab="ajustes"]');
    abrirModal('confirmar-zere', '[data-act="reset"]');
  }

  clicar('[data-tab="semana"]');
  abrirModal('nova-atividade', '[data-act="new-activity"]');
  abrirModal('sugestao', '[data-act="apply-suggestion"]');

  freio.remove();

  /* ---------------- sintético: o merge de atributos ----------------
     Todas as formas de placeholder que existem no código, mais os nomes que
     os dados atuais não alcançam (com 0 atividades, `check`/`save` não
     renderizam; sem tópico arquivado, `rotate-ccw` e os chevrons também não).
     Assim os 26 nomes do mapa são cobertos aqui ou nas abas — e a comparacao
     before/after prova o glyph de cada um contra a própria biblioteca.
       forma 1: sem classe nenhuma     — o X do modal (linha 893)
       forma 2: classe + style inline   — o check verde da aba Hoje (1127)
       forma 3: classe só               — ícones de navegação (950)
       forma 4: classe + atributos extras — forma que NENHUM call site usa
       forma 5+: as classes reais de cada ícone que só apareceria em outro estado */
  const FORMAS = [
    '<i data-lucide="x"></i>',
    '<i data-lucide="check" class="h-2.5 w-2.5" style="color:var(--c-ok)"></i>',
    '<i data-lucide="calendar-check" class="h-[18px] w-[18px]"></i>',
    '<i data-lucide="sun" class="h-5 w-5 ink3" title="tit" stroke-width="3" data-extra="z" aria-label="rotulo"></i>',
    '<i data-lucide="check" class="h-4 w-4"></i>',
    '<i data-lucide="save" class="h-4 w-4"></i>',
    '<i data-lucide="rotate-ccw" class="h-3.5 w-3.5"></i>',
    '<i data-lucide="chevron-right" class="h-3 w-3"></i>',
    '<i data-lucide="chevron-down" class="h-3 w-3"></i>',
    '<i data-lucide="archive" class="h-3.5 w-3.5"></i>',
    '<i data-lucide="sigma"></i>',
    '<i data-lucide="atom"></i>',
    '<i data-lucide="flask-conical"></i>',
    '<i data-lucide="languages"></i>',
    '<i data-lucide="pen-line"></i>',
  ];
  const box = document.createElement('div');
  box.style.cssText = 'position:absolute;left:-9999px;top:0';
  box.innerHTML = FORMAS.join('');
  document.body.appendChild(box);
  paint();
  const colher = () => [...box.querySelectorAll('svg')].map(s => s.outerHTML);
  R.sintetico = { passe1: colher() };
  paint();
  R.sintetico.passe2 = colher();
  R.sintetico.restouI = box.querySelectorAll('i[data-lucide]').length;
  box.remove();

  /* ---------------- estado no fim ----------------
     Mesmas contagens do início: prova que a sonda não gravou nada. */
  let lsDepois = null;
  try { lsDepois = JSON.parse(localStorage.getItem('rotina-ita-v1') || 'null'); } catch (e) {}
  R.docFim = {
    lsTopicos: lsDepois && Array.isArray(lsDepois.topics) ? lsDepois.topics.length : null,
    lsAtividades: lsDepois && Array.isArray(lsDepois.activities) ? lsDepois.activities.length : null,
    lsSessoes: lsDepois && Array.isArray(lsDepois.sessions) ? lsDepois.sessions.length : null,
    modalAberto: !document.querySelector('#modal-root').classList.contains('hidden'),
  };

  return JSON.stringify(R);
})()

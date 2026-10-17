(async () => {
  // Colhe o SVG EXATO que o Lucide produz, em todos os estados.
  // Copiar do proprio resultado e a unica forma de reproduzir o visual sem adivinhar.
  const settle = async () => {
    await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
    await new Promise(r => setTimeout(r, 420));
  };
  const achados = {};
  const colher = () => {
    for (const svg of document.querySelectorAll('svg')) {
      const cls = (svg.getAttribute('class') || '');
      const m = cls.match(/(?:^|\s)lucide-(?:lucide-)?([a-z0-9-]+)(?:\s|$)/) || cls.match(/lucide-([a-z0-9-]+)/);
      if (!m) continue;
      const nome = m[1];
      if (achados[nome]) continue;
      const cs = getComputedStyle(svg);
      achados[nome] = {
        outerHTML: svg.outerHTML,
        attrs: [...svg.attributes].map(a => `${a.name}="${a.value}"`),
        strokeWidth: cs.strokeWidth,
        width: cs.width,
        height: cs.height,
        display: cs.display,
        cor: cs.color,
        fill: cs.fill
      };
    }
  };
  for (const t of ['hoje', 'semana', 'conteudos', 'progresso', 'ajustes']) {
    const b = document.querySelector(`[data-act="tab"][data-tab="${t}"]`);
    if (!b) continue;
    b.click(); await settle(); colher();
  }
  return JSON.stringify({
    n: Object.keys(achados).length,
    nomes: Object.keys(achados).sort(),
    icones: achados
  });
})()

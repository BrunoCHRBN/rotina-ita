(async () => {
  // Colhe o SVG AUTENTICO de TODOS os icones que o app pode pedir, inclusive os
  // que o estado semeado atual nao alcanca (archive, chevron-*, rotate-ccw,
  // check, save, x) e os 6 de SUBJECTS.
  //
  // Metodo: injeta um <i data-lucide="NOME"> para cada nome num container
  // temporario, chama o createIcons() da PROPRIA biblioteca, e colhe o <svg>
  // resultante. Nao muta o estado do app (nenhum save()), e o markup vem da
  // mesma biblioteca que hoje o app usa — entao copiar isso reproduz o visual
  // sem adivinhar atributo nenhum.
  const settle = async () => {
    await new Promise(r => requestAnimationFrame(() => requestAnimationFrame(r)));
    await new Promise(r => setTimeout(r, 300));
  };
  await settle();

  const NOMES = [
    // nav + estados vazios + acoes de linha
    'calendar-check', 'calendar-days', 'book-open', 'chart-column', 'settings',
    'sun', 'history', 'calendar-x',
    // botoes de acao
    'check', 'save', 'x', 'plus', 'pencil', 'trash-2', 'list-plus',
    'download', 'upload', 'archive', 'rotate-ccw', 'chevron-down', 'chevron-right',
    // SUBJECTS (declarados no dados; renderizados em lugar nenhum hoje)
    'sigma', 'atom', 'flask-conical', 'languages', 'pen-line'
  ];

  const box = document.createElement('div');
  box.id = '__colheita';
  box.style.cssText = 'position:absolute;left:-9999px;top:0';
  box.innerHTML = NOMES.map(n => `<i data-lucide="${n}"></i>`).join('');
  document.body.appendChild(box);
  await settle();

  const L = window.lucide;
  if (!L || typeof L.createIcons !== 'function') {
    box.remove();
    return JSON.stringify({ erro: 'lucide indisponivel', temLucide: !!L });
  }
  try { L.createIcons({ icons: L.icons || {} }); } catch (e) {
    box.remove();
    return JSON.stringify({ erro: 'createIcons falhou: ' + e.message });
  }
  await settle();

  const fora = {};
  for (const nome of NOMES) {
    const svg = box.querySelector(`svg.lucide-${nome}`) || box.querySelector(`[class*="lucide-${nome}"]`);
    const i = box.querySelector(`[data-lucide="${nome}"]`);
    if (!svg && !i) { fora[nome] = null; continue; }
    if (!svg) { fora[nome] = { soPlaceholder: i.outerHTML }; continue; }
    fora[nome] = {
      html: svg.outerHTML,
      attrs: Object.fromEntries([...svg.attributes].map(a => [a.name, a.value])),
      filhos: svg.children.length,
      bytes: svg.outerHTML.length
    };
  }
  box.remove();

  const valor = NOMES.filter(n => fora[n] && fora[n].html);
  return JSON.stringify({
    total: NOMES.length,
    colhidos: valor.length,
    faltando: NOMES.filter(n => !fora[n] || !fora[n].html),
    bytesTotal: valor.reduce((s, n) => s + fora[n].bytes, 0),
    icones: fora
  });
})()

#!/usr/bin/env python3
"""compara.py — compara duas fotografias da sonda.js e emite o veredito.

  ./compara.py <antes.json> <depois.json>

O que PODE mudar entre os dois mundos está declarado e é exigido:
  - doc.lucide: 'object' -> 'undefined'   (o UMD sai do documento)
  - doc.scriptsLucide: 1 -> 0
Todo o resto tem de ser idêntico, ícone por ícone, atributo por atributo:
  - 5 abas e os modais: mesmo total de <svg>, ZERO <i> órfão, mesma
    contagem por nome, e para cada ícone o mesmo mapa de atributos, a
    mesma ORDEM de atributos, o mesmo markup interno e a mesma geometria
    (rect) e estilo computado;
  - secao sintetica: o outerHTML colhido tem de ser BYTE A BYTE igual —
    é a comparação mais estrita possível do merge de atributos.
O estado persistido (localStorage) tem de estar intacto nos dois.
"""
import json
import sys

CAMPOS_ICONE = ['attrs', 'ordem', 'inner', 'w', 'h', 'sw', 'disp', 'cor', 'fill']

def canon(ic):
    return json.dumps({k: ic.get(k) for k in CAMPOS_ICONE}, sort_keys=True, ensure_ascii=False)

def diff_icone(a, b):
    """devolve lista de diferenças legíveis entre dois ícones"""
    d = []
    for k in ['attrs', 'ordem', 'inner', 'w', 'h', 'sw', 'disp', 'cor', 'fill']:
        va, vb = a.get(k), b.get(k)
        if va != vb:
            if k == 'attrs' and isinstance(va, dict) and isinstance(vb, dict):
                for chave in sorted(set(va) | set(vb)):
                    if va.get(chave) != vb.get(chave):
                        d.append(f'{k}.{chave}: {va.get(chave)!r} -> {vb.get(chave)!r}')
            else:
                d.append(f'{k}: {va!r} -> {vb!r}')
    return d

def comparar_contexto(rotulo, reg_a, reg_b, falhas, avisos):
    if reg_a is None or reg_b is None:
        falhas.append(f'{rotulo}: registro ausente')
        return
    for campo in ['clicou', 'visivel', 'titulo', 'fechou']:
        if reg_a.get(campo) != reg_b.get(campo):
            falhas.append(f'{rotulo}: {campo} mudou: {reg_a.get(campo)!r} -> {reg_b.get(campo)!r}')
    sa, sb = reg_a.get('snap'), reg_b.get('snap')
    if not sa or not sb:
        return
    if sa.get('totalSvg') != sb.get('totalSvg'):
        falhas.append(f'{rotulo}: total de <svg> mudou: {sa.get("totalSvg")} -> {sb.get("totalSvg")}')
    if sa.get('contagem') != sb.get('contagem'):
        falhas.append(f'{rotulo}: contagem por nome mudou: {sa.get("contagem")} -> {sb.get("contagem")}')
    if sb.get('orfaos'):
        nomes = ','.join(sorted(set(sb.get('nomesOrfaos') or [])))
        falhas.append(f'{rotulo}: {sb["orfaos"]} <i data-lucide> ORFÃO(S) ficaram sem substituto: {nomes}')
    # comparação multiconjunto: mesma coleção de ícones, em qualquer ordem
    ca = sorted(canon(i) for i in sa['svgs'])
    cb = sorted(canon(i) for i in sb['svgs'])
    if ca == cb:
        return
    # houve diferença — acha os ícones responsáveis e descreve
    from collections import Counter
    nao_acertas = []
    sobra_a, sobra_b = list(ca), list(cb)
    for x in list(sobra_a):
        if x in sobra_b:
            sobra_a.remove(x); sobra_b.remove(x)
    for x in sobra_a[:6]:
        nao_acertas.append('  controle: ' + x[:400])
    for x in sobra_b[:6]:
        nao_acertas.append('  rodada  : ' + x[:400])
    falhas.append(f'{rotulo}: {len(sobra_a)} ícone(s) diferentes do controle, {len(sobra_b)} na rodada\n' + '\n'.join(nao_acertas))

def main():
    if len(sys.argv) != 3:
        print('uso: compara.py <antes.json> <depois.json>', file=sys.stderr)
        sys.exit(2)
    a = json.load(open(sys.argv[1], encoding='utf-8'))
    b = json.load(open(sys.argv[2], encoding='utf-8'))
    falhas, avisos, passes = [], [], []

    # ---- mudanças exigidas (a Fase 1 tem de produzir estas) ----
    if a['doc']['lucide'] != 'object' or b['doc']['lucide'] != 'undefined':
        falhas.append(f'doc.lucide deveria ir de object para undefined: {a["doc"]["lucide"]!r} -> {b["doc"]["lucide"]!r}')
    else:
        passes.append('window.lucide deixou de existir')
    if a['doc']['scriptsLucide'] != 1 or b['doc']['scriptsLucide'] != 0:
        falhas.append(f'script do lucide deveria sair do documento: {a["doc"]["scriptsLucide"]} -> {b["doc"]["scriptsLucide"]}')
    else:
        passes.append('tag <script> do lucide removida')

    # ---- o que não pode mudar ----
    if a['doc']['tema'] != b['doc']['tema']:
        falhas.append(f'tema mudou: {a["doc"]["tema"]!r} -> {b["doc"]["tema"]!r}')
    for chave in ['lsTopicos', 'lsAtividades', 'lsSessoes']:
        if a['doc'][chave] != b['docFim'][chave] or a['doc'][chave] != b['doc'][chave]:
            falhas.append(f'estado persistido mudou em {chave}: {a["doc"][chave]} -> {b["doc"][chave]} -> {b["docFim"][chave]}')
    if b['docFim'].get('modalAberto'):
        falhas.append('sonda deixou modal aberto no fim')

    for aba in ['hoje', 'semana', 'conteudos', 'progresso', 'ajustes']:
        comparar_contexto(f'aba {aba}', a['abas'].get(aba), b['abas'].get(aba), falhas, avisos)
    for m in sorted(set(a['modais']) | set(b['modais'])):
        comparar_contexto(f'modal {m}', a['modais'].get(m), b['modais'].get(m), falhas, avisos)
    sa, sb = a.get('sintetico', {}), b.get('sintetico', {})
    if sa.get('passe1') != sb.get('passe1'):
        # descreve a primeira diferença
        pa, pb = sa.get('passe1', []), sb.get('passe1', [])
        if len(pa) != len(pb):
            falhas.append(f'sintetico: {len(pa)} svgs no controle, {len(pb)} na rodada')
        else:
            for i, (x, y) in enumerate(zip(pa, pb)):
                if x != y:
                    falhas.append(f'sintetico: outerHTML do ícone {i} difere\n  controle: {x[:300]}\n  rodada  : {y[:300]}')
                    break
    else:
        passes.append(f'sintetico: {len(sa.get("passe1", []))} outerHTML byte a byte iguais ao controle')
    if sb.get('restouI'):
        falhas.append(f'sintetico: {sb["restouI"]} placeholder(s) não substituído(s)')
    if sa.get('passe2') != sb.get('passe2') or sb.get('passe1') != sb.get('passe2'):
        # o controle provou: re-processar ícone já substituído é no-op
        # (passe1 == passe2, byte a byte). Se a rodada acumular classe na
        # segunda passada, a query do injetor está genérica demais — regressão.
        falhas.append('sintetico: segunda passada difere (re-processar ícone já substituído acumula atributo)')
    else:
        passes.append('sintetico: segunda passada também idêntica (re-processar é no-op)')

    # ---- totais ----
    tot_a = sum(len(r.get('snap', {}).get('svgs', [])) for r in a['abas'].values()) \
          + sum(len(r.get('snap', {}).get('svgs', [])) for r in a['modais'].values())
    tot_b = sum(len(r.get('snap', {}).get('svgs', [])) for r in b['abas'].values()) \
          + sum(len(r.get('snap', {}).get('svgs', [])) for r in b['modais'].values())

    print(f'ícones comparados: {tot_a} (controle) vs {tot_b} (rodada), mais {len(sb.get("passe1", []))} sintéticos')
    for p in passes:
        print(f'PASS {p}')
    for av in avisos:
        print(f'AVISO {av}')
    for f in falhas:
        print(f'FAIL {f}')
    print(f'\nveredito: {"PASSA" if not falhas else "FALHA (" + str(len(falhas)) + ")"}')
    sys.exit(0 if not falhas else 1)

if __name__ == '__main__':
    main()

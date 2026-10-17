#!/usr/bin/env python3
"""gera_icones.py — gera o mapa ICONES para o index.html a partir da colheita.

A colheita (verificacao/colheita_completa.json) é o outerHTML que a PRÓPRIA
biblioteca lucide@1.52.0 produziu ao renderizar cada ícone num contêiner
fora da tela. Nada aqui é digitado de memória: o gerador só re-empacota.

 dupla verificacao antes de emitir:
  1. cada html não contém crase nem aspas simples (iriam quebrar a string JS)
  2. nenhum html contém a sequência `</script` (fecharia o <script> inline
     no meio do mapa e derrubaria o app inteiro, em silêncio)

saída: verificacao/icones.frag.js — um objeto literal JS, uma chave por linha.
"""
import json
import sys

COLHEITA = 'colheita_completa.json'
SAIDA = 'icones.frag.js'

def main():
    dados = json.load(open(COLHEITA, encoding='utf-8'))
    icones = dados['icones']
    if dados.get('faltando'):
        print('COLHEITA INCOMPLETA, abortando:', dados['faltando'], file=sys.stderr)
        sys.exit(1)

    linhas = []
    total = 0
    for nome, info in icones.items():
        html = info['html']
        assert "'" not in html, f'{nome}: html contém aspas simples'
        assert '</script' not in html.lower(), f'{nome}: html contém </script'
        assert '`' not in html, f'{nome}: html contém crase'
        assert '${' not in html, f'{nome}: html contém sequencia de template'
        linhas.append(f"  '{nome}': '{html}',")
        total += len(html)

    with open(SAIDA, 'w', encoding='utf-8') as f:
        f.write('const ICONES = {\n')
        f.write('\n'.join(linhas))
        f.write('\n};\n')

    print(f'icones gerados : {len(linhas)}')
    print(f'bytes de SVG   : {total} ({total/1024:.1f} KB)')
    print(f'arquivo        : {SAIDA}')
    # assinatura para rastreabilidade: hash do mapa emitido
    import hashlib
    h = hashlib.md5('\n'.join(linhas).encode('utf-8')).hexdigest()
    print(f'md5 das linhas: {h}')

if __name__ == '__main__':
    main()

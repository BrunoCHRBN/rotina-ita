#!/usr/bin/env bash
# av.sh — rode um probe JS no browser e imprima o JSON decodificado.
#
#   ./av.sh <arquivo.js>        # devolve o JSON na saida padrao
#
# Repete 3x porque o `agent-browser eval` as vezes volta VAZIO — e saida vazia
# NAO e resultado negativo: e instrumento mudo. Se repetir 3x e continuar vazio,
# imprime um erro explicito com o stderr, em vez de um JSON vazio que passaria
# por "0 achados".
#
# Versione AQUI, nao em /tmp: a pasta /tmp deste ambiente e limpa entre comandos
# e entre sessoes, e perder o instrumento no meio de uma medicao custa mais que
# versiona-lo.
export PATH="$HOME/.npm-global/bin:$PATH"
ALVO="$1"
if [ -z "$ALVO" ]; then echo '{"erro":"uso: ./av.sh <arquivo.js>"}'; exit 2; fi
if [ ! -f "$ALVO" ]; then echo "{\"erro\":\"arquivo nao existe: $ALVO\"}"; exit 2; fi
# aceita caminho relativo ao diretorio do script tambem
case "$ALVO" in /*) ;; *) ALVO="$(cd "$(dirname "$0")" && pwd)/$ALVO";; esac
if [ ! -f "$ALVO" ]; then echo "{\"erro\":\"arquivo nao existe: $ALVO\"}"; exit 2; fi

JS="$(cat "$ALVO")"
ERR="$(mktemp /tmp/ui_err.XXXXXX)"
for i in 1 2 3; do
  RAW="$(agent-browser eval "$JS" 2>"$ERR")"
  if [ -n "$RAW" ]; then
    OUT="$(printf '%s' "$RAW" | python3 "$(cd "$(dirname "$0")" && pwd)/dec.py" 2>/dev/null)"
    if [ -n "$OUT" ]; then printf '%s\n' "$OUT"; rm -f "$ERR"; exit 0; fi
    printf '{"erro":"resposta nao decodificavel","bruto":"%s"}\n' "$(printf '%s' "$RAW" | head -c 200)"
    rm -f "$ERR"; exit 0
  fi
  sleep 0.5
done
printf '{"erro":"eval devolveu VAZIO 3x","stderr":"%s"}\n' "$(head -c 300 "$ERR" | tr -d '\n' | tr '"' "'")"
rm -f "$ERR"

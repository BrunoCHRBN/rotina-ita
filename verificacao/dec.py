"""dec.py — decodifica a saida do `agent-browser eval`.

Dois problemas que ele resolve:

1. **JSON duplo-codificado.** O CLI devolve uma *string* que contem JSON, ou
   seja `"{\\"chave\\": ...}"`. `json.loads` uma vez devolve outra string; o
   `dec.py` tenta a segunda vez sozinho. Sem isso, um regex `\\{.*\\}` acha um
   `\\` interno e estoura com "Expecting property name".

2. **Saida vazia.** Se nao houver JSON nenhum, imprime um erro explicito — nunca
   um JSON vazio. Um `{}` ou nada passaria por "0 achados", que e a pior mentira
   que um instrumento pode contar.
"""
import sys, json, re

raw = sys.stdin.read().strip()


def tenta(txt):
    try:
        d = json.loads(txt)
    except Exception:
        return None
    if isinstance(d, str):          # duplo-codificado
        try:
            d = json.loads(d)
        except Exception:
            return None
    return d


d = tenta(raw)
if d is None:
    m = re.search(r"\{.*\}", raw, re.S)
    if m:
        d = tenta(m.group(0))
if d is None:
    print(json.dumps({"erro": "sem json decodificavel", "bruto": raw[:200]}, ensure_ascii=False))
    raise SystemExit(1)
print(json.dumps(d, ensure_ascii=False, indent=1))

#!/usr/bin/env python3
"""
Refresca los datos en bruto desde las APIs y regenera la web.

Descarga:
  - AREDL:       https://api.aredl.net/v2/api/aredl/levels
  - Pointercrate: https://pointercrate.com/api/v2/demons/listed/?limit=100&after=N  (paginado)

Guarda:
  - datos-brutos/aredl_raw.json
  - datos-brutos/pc_raw.json

y luego ejecuta build_data.py para reconstruir datos-niveles.json, el CSV y index.html.

Uso:  python3 actualizar_datos_brutos.py
"""
import json
import os
import subprocess
import sys
import time
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
BRUTOS = os.path.join(HERE, "datos-brutos")
CABECERAS = {"User-Agent": "Mozilla/5.0 (compatible; demonlist-grupo/1.0)"}


def traer(url):
    req = urllib.request.Request(url, headers=CABECERAS)
    with urllib.request.urlopen(req, timeout=40) as r:
        return json.load(r)


def main():
    os.makedirs(BRUTOS, exist_ok=True)

    print("→ Descargando AREDL…")
    aredl = traer("https://api.aredl.net/v2/api/aredl/levels")
    with open(os.path.join(BRUTOS, "aredl_raw.json"), "w", encoding="utf-8") as f:
        json.dump(aredl, f, ensure_ascii=False)
    print(f"  {len(aredl)} niveles")

    print("→ Descargando Pointercrate (paginado)…")
    pc, after, pagina = [], 0, 0
    while pagina < 60:
        d = traer(f"https://pointercrate.com/api/v2/demons/listed/?limit=100&after={after}")
        if not isinstance(d, list) or not d:
            break
        pc += d
        pagina += 1
        if len(d) < 100:
            break
        after = d[-1]["position"] + 1
        time.sleep(0.35)  # sé amable con su API
    with open(os.path.join(BRUTOS, "pc_raw.json"), "w", encoding="utf-8") as f:
        json.dump(pc, f, ensure_ascii=False)
    print(f"  {len(pc)} posiciones")

    print("→ Reconstruyendo la web…")
    subprocess.run([sys.executable, os.path.join(HERE, "build_data.py")], check=True, cwd=HERE)


if __name__ == "__main__":
    main()

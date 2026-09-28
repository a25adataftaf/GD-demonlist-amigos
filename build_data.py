#!/usr/bin/env python3
"""
Construye los datos y la web de la Demonlist del grupo a partir de:
  - AREDL API:      https://api.aredl.net/v2/api/aredl/levels
  - Pointercrate:   https://pointercrate.com/api/v2/demons/listed/?limit=100&after=N

Entradas (en ./datos-brutos/):
  - aredl_raw.json   respuesta de la API de AREDL
  - pc_raw.json      todas las páginas de Pointercrate juntas

Salidas (en la raíz del repo):
  - datos-niveles.json            dataset compacto
  - lista-aredl-pointercrate.csv  listado para Excel/Sheets
  - index.html                    la web (plantilla + datos incrustados)

Uso:
  python3 build_data.py                 # genera index.html
  python3 build_data.py otra.html       # genera con otro nombre de salida

Para refrescar los datos en bruto desde las APIs (necesita internet):
  python3 actualizar_datos_brutos.py
"""
import csv
import datetime
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BRUTOS = os.path.join(HERE, "datos-brutos")
SALIDA_WEB = sys.argv[1] if len(sys.argv) > 1 else "index.html"


def cargar(nombre):
    with open(os.path.join(BRUTOS, nombre), encoding="utf-8") as f:
        return json.load(f)


def video_id(url):
    m = re.search(r"(?:v=|youtu\.be/|embed/)([A-Za-z0-9_-]{11})", url or "")
    return m.group(1) if m else ""


def main():
    aredl = cargar("aredl_raw.json")
    pc = cargar("pc_raw.json")
    pc_por_lid = {d["level_id"]: d for d in pc if d.get("level_id")}

    niveles = []
    for l in sorted(aredl, key=lambda x: x["position"]):
        p = pc_por_lid.get(l["level_id"], {})
        niveles.append([
            l["id"],                                                    # 0 clave única AREDL (uuid)
            l["name"],                                                  # 1 nombre
            l["position"],                                              # 2 posición AREDL
            l["points"],                                                # 3 puntos oficiales AREDL
            1 if l["status"] == "MainList" else 0,                      # 4 1=MainList, 0=Legacy
            1 if l.get("two_player") else 0,                            # 5 2 jugadores
            p.get("position", 0),                                       # 6 posición Pointercrate (0 = no está)
            p.get("requirement", 0),                                    # 7 % mínimo para récord parcial en PC
            int(l["gddl_tier"]) if l.get("gddl_tier") is not None else 0,     # 8 tier GDDL
            round(l["edel_enjoyment"]) if l.get("edel_enjoyment") is not None else -1,  # 9 disfrute EDEL
            l.get("tags") or [],                                        # 10 etiquetas
            0,                                                          # 11 solo-Pointercrate (sin puntos AREDL)
            l["level_id"],                                              # 12 ID del nivel en GD
            video_id(p.get("video", "")),                               # 13 vídeo de YouTube
            (p.get("verifier") or {}).get("name", ""),                  # 14 verificador
            (p.get("publisher") or {}).get("name", ""),                 # 15 publisher
            p.get("id", 0),                                             # 16 id de ficha en Pointercrate
        ])

    lids_aredl = {l["level_id"] for l in aredl}
    solo_pc = [d for d in pc if d["level_id"] not in lids_aredl]
    for d in sorted(solo_pc, key=lambda x: x["position"]):
        niveles.append([
            "pc-" + str(d["level_id"]), d["name"], 0, 0, 0, 0,
            d["position"], d.get("requirement", 0), 0, -1, [], 1, d["level_id"],
            video_id(d.get("video", "")),
            (d.get("verifier") or {}).get("name", ""),
            (d.get("publisher") or {}).get("name", ""),
            d.get("id", 0),
        ])

    puntos_total = sum(n[3] for n in niveles)
    dataset = {
        "generado": datetime.date.today().isoformat(),
        "fuente_aredl": "https://api.aredl.net/v2/api/aredl/levels",
        "fuente_pointercrate": "https://pointercrate.com/api/v2/demons/listed/",
        "total_niveles": len(niveles),
        "con_puntos": sum(1 for n in niveles if n[3] > 0),
        "legacy": sum(1 for n in niveles if n[4] == 0 and n[11] == 0),
        "en_pointercrate": sum(1 for n in niveles if n[6] > 0),
        "solo_pointercrate": len(solo_pc),
        "puntos_totales": puntos_total,
        "niveles": niveles,
    }

    with open(os.path.join(HERE, "datos-niveles.json"), "w", encoding="utf-8") as f:
        json.dump(dataset, f, ensure_ascii=False, separators=(",", ":"))

    # --- CSV para curiosear en Excel/Sheets ---
    with open(os.path.join(HERE, "lista-aredl-pointercrate.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["pos_aredl", "nivel", "puntos_aredl", "en_pointercrate", "pc_min_pct", "estado",
                    "id_gd", "tier_gddl", "disfrute_edel", "2p", "etiquetas"])
        for n in niveles:
            estado_txt = "solo Pointercrate" if n[11] else ("Legacy" if n[4] == 0 else "Main List")
            w.writerow([n[2] or "", n[1], n[3], n[6] or "", n[7] or "", estado_txt, n[12],
                        n[8] or "", n[9] if n[9] >= 0 else "", "sí" if n[5] else "", ", ".join(n[10])])

    # --- web: plantilla + datos incrustados ---
    with open(os.path.join(HERE, "app_template.html"), encoding="utf-8") as f:
        html = f.read()
    datos_js = json.dumps(dataset, ensure_ascii=False, separators=(",", ":")).replace("<", "\\u003c")
    html = html.replace("/*__DATOS__*/null", datos_js)
    destino = os.path.join(HERE, SALIDA_WEB)
    with open(destino, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"Niveles: {len(niveles)} (con puntos: {dataset['con_puntos']} | legacy: {dataset['legacy']} | "
          f"en Pointercrate: {dataset['en_pointercrate']} | solo-PC: {len(solo_pc)})")
    print(f"Puntos totales de la lista: {puntos_total:,}")
    print(f"Generado: datos-niveles.json, lista-aredl-pointercrate.csv y {SALIDA_WEB} "
          f"({os.path.getsize(destino)/1024:.0f} KB)")


if __name__ == "__main__":
    main()

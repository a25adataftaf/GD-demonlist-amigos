# 🏆 Demonlist del grupo — réplica de Pointercrate

Web privada para picarnos entre colegas: clonamos la página de la
**[Demonlist de Pointercrate](https://pointercrate.com/demonlist/)** (paneles con la miniatura del vídeo,
verificador, publisher y el % de récord parcial) y le añadimos nuestro marcador, con los
**puntos oficiales de la AREDL**.

🌐 **Online:** https://a25adataftaf.github.io/GD-demonlist-amigos/

👉 **También se abre con doble clic en `index.html`** (no necesita servidor, ni instalar nada, ni internet
para funcionar: los datos van incrustados).

---

## 📂 Qué hay en el repo

| Archivo | Qué es |
|---|---|
| **`index.html`** | ⭐ La web entera (plantilla + datos incrustados). Es lo que se abre y lo que se publica. |
| `app_template.html` | Plantilla de la web (textos, estilos y lógica). Aquí se edita el diseño. |
| `build_data.py` | Reconstruye `index.html`, `datos-niveles.json` y el CSV a partir de los datos en bruto. |
| `actualizar_datos_brutos.py` | Descarga otra vez las listas de AREDL y Pointercrate y regenera todo. |
| `datos-niveles.json` | Dataset: 1.679 niveles con posición y puntos AREDL, posición Pointercrate, % requerido, verificador, publisher, vídeo, tier GDDL, disfrute EDEL y etiquetas. |
| `lista-aredl-pointercrate.csv` | La lista completa en CSV (`;`) para Excel / Google Sheets. |
| `datos-brutos/` | Respuestas tal cual de las APIs (para poder regenerar todo sin internet). |
| `.github/workflows/pages.yml` | Publica la web en **GitHub Pages** automáticamente al hacer push. |

## 🧭 La web, por dentro

- **Demonlist** — los niveles tal y como aparecen en Pointercrate (miniatura del vídeo que enlaza a YouTube,
  `#posición – nombre`, *verified by… · published by…*, puntos AREDL y tags). Debajo de cada nivel, los
  botones con las iniciales de cada jugador: un clic marca, otro desmarca.
  - Cuatro listas: **Pointercrate Demonlist** (sus 707 niveles), **AREDL completa** (1.621),
    **Lo que nos falta** y **Lo que hemos pasado**.
  - Filtros: buscador, orden (PC / AREDL / puntos / GDDL / disfrute), top 150, legacy, 2P, con vídeo,
    “le falta a…” / “lo ha pasado…” por jugador y filtro por etiqueta.
- **Clasificación** — podio, tabla (puntos, peso, niveles, récord, dificultad media, diferencia con el líder),
  estadísticas del grupo y **piques** (el nivel que solo tiene uno / el que se le resiste a uno y ya tienen todos).
- **Jugadores** — añadir, renombrar y borrar; exportar/importar el progreso como texto
  (para pasar las marcas por WhatsApp; al importar se puede *fusionar*).
- **Reglas** — cómo puntuamos, qué cuenta como récord y de dónde salen los datos.

Arriba, un **marcador fijo** con las puntuaciones en vivo mientras navegas la lista.

## 🎯 Puntuación

Puntos oficiales de la AREDL (no lineales): el **#1 (Society)** vale **5.000 pts** y el último nivel
puntuado, **10 pts**. En total, **1.159.358 puntos** repartidos entre **1.588 niveles**.

- `LEGACY` → 0 puntos (retirados de la lista), pero se pueden marcar igual.
- Los 58 niveles que están en Pointercrate y aún no en la AREDL aparecen con 0 puntos y la etiqueta *solo AREDL*.
- En la AREDL un récord cuenta solo con el **100%**; en Pointercrate el top 75 admite parciales
  (la web indica desde qué % — aquí marcamos niveles completados).

## 🚀 Publicado

Repo: <https://github.com/a25adataftaf/GD-demonlist-amigos> · Web: <https://a25adataftaf.github.io/GD-demonlist-amigos/>

El remoto `origin` ya está configurado y la web se publica **sola en cada push** a `main`
(Settings → Pages → Source: GitHub Actions, ya activado).

Para subir cambios:

```bash
git add -A
git commit -m "lo que hayas cambiado"
git push
```

Si algún día quieres publicar desde otro repositorio, basta con cambiar el remoto:

```bash
git remote set-url origin https://github.com/TU-USUARIO/TU-REPO.git
git push -u origin main
```

## 🔄 Actualizar los datos

```bash
python3 actualizar_datos_brutos.py   # vuelve a descargar AREDL + Pointercrate y regenera index.html
```

Solo necesitas `python3` (sin librerías externas). También se puede refrescar desde la propia web,
en la pestaña *Jugadores* → *Descargar de nuevo* (eso sí, con internet y fuera de vistas previas integradas).

## ℹ️ Fuentes

- AREDL: `https://api.aredl.net/v2/api/aredl/levels` — 1.679 niveles (datos del 28/09/2026).
- Pointercrate: `https://pointercrate.com/api/v2/demons/listed/` — 702 posiciones (su top 150 coincide con el de la AREDL).

## ⚠️ Notas

- Las marcas se guardan por **ID del nivel**, así que aguantan las actualizaciones de las listas
  (aunque las posiciones, y por tanto los puntos, pueden cambiar cuando las listas se mueven).
- El progreso se guarda en el navegador (localStorage). Si abres la web dentro de una vista previa
  integrada puede estar bloqueado: la web te avisa y puedes copiar el ranking para no perderlo.
- Réplica hecha por y para el grupo, sin relación con Pointercrate ni con la AREDL.

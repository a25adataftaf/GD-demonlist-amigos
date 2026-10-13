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
| `datos-niveles.json` | Snapshot para abrir sin conexión: niveles, puntos AREDL, posiciones Pointercrate, % requerido, verificador, publisher, vídeo, tier GDDL, disfrute EDEL y etiquetas. El #1, GRIEF, se verificó el 13/10/2026; el resto conserva el snapshot base del 28/09/2026 hasta sincronizar. |
| `lista-aredl-pointercrate.csv` | El snapshot en CSV (`;`) para Excel / Google Sheets. |
| `datos-brutos/` | Último respaldo descargado de las APIs; para reconstruir el top vigente, primero ejecuta `actualizar_datos_brutos.py`. |
| `.github/workflows/pages.yml` | Publica la web en **GitHub Pages** automáticamente al hacer push. |

## 🧭 La web, por dentro

- **Demonlist** — los niveles tal y como aparecen en Pointercrate (miniatura del vídeo que enlaza a YouTube,
  `#posición – nombre`, *verified by… · published by…*, puntos AREDL y tags). Debajo de cada nivel, los
  botones con las iniciales de cada jugador: un clic marca, otro desmarca.
  - Cuatro listas: **Pointercrate Demonlist**, **AREDL completa**, **Lo que nos falta** y **Lo que hemos pasado**. Los datos se sincronizan al abrir la web cuando hay conexión; si no, se usa el snapshot incrustado.
  - Filtros: buscador, orden (PC / AREDL / puntos / GDDL / disfrute), top 150, legacy, 2P, con vídeo,
    “le falta a…” / “lo ha pasado…” por jugador y filtro por etiqueta.
- **Clasificación** — podio, tabla (puntos, peso, niveles, récord, dificultad media, diferencia con el líder),
  estadísticas del grupo y **piques** (el nivel que solo tiene uno / el que se le resiste a uno y ya tienen todos).
- **Jugadores** — añadir, renombrar y borrar; exportar/importar el progreso como texto
  (para pasar las marcas por WhatsApp; al importar se puede *fusionar*).
- **Reglas** — cómo puntuamos, qué cuenta como récord y de dónde salen los datos.

Arriba, un **marcador fijo** con las puntuaciones en vivo mientras navegas la lista.

## 🎯 Puntuación

Puntos oficiales de la AREDL (no lineales): el **#1 actual, GRIEF**, vale **5.000 pts**. La suma y las posiciones se recalculan al sincronizar con la API, así que pueden variar cuando se mueve la lista (el snapshot de GRIEF se verificó el 13/10/2026).

- `LEGACY` → 0 puntos (retirados de la lista), pero se pueden marcar igual.
- Los niveles que están en Pointercrate y aún no en la AREDL aparecen con 0 puntos y la etiqueta *solo Pointercrate*.
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

Solo necesitas `python3` (sin librerías externas). La web también intenta sincronizar AREDL y Pointercrate al abrirse, y permite forzar la descarga en *Jugadores* → *Descargar de nuevo*. Si la conexión o CORS bloquea las APIs, conserva el snapshot y sigue funcionando sin conexión.

## ℹ️ Fuentes

- AREDL: `https://api.aredl.net/v2/api/aredl/levels` — la web consulta la lista vigente; el snapshot del top se verificó el 13/10/2026.
- Pointercrate: `https://pointercrate.com/api/v2/demons/listed/` — la web consulta la Demonlist completa y usa sus posiciones para ordenar el top.

## ⚠️ Notas

- Las marcas se guardan por **ID del nivel**, así que aguantan las actualizaciones de las listas
  (aunque las posiciones, y por tanto los puntos, pueden cambiar cuando las listas se mueven).
- El progreso se guarda en el navegador (localStorage). Si abres la web dentro de una vista previa
  integrada puede estar bloqueado: la web te avisa y puedes copiar el ranking para no perderlo.
- Réplica hecha por y para el grupo, sin relación con Pointercrate ni con la AREDL.

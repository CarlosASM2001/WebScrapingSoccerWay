# Dataset Card - Liga FUTVE Results (2002-2003 a 2025)

## 1) Resumen

Este dataset contiene resultados historicos de la primera division de futbol de Venezuela (Liga FUTVE), extraidos desde Soccerway y guardados en formato CSV.

Objetivo principal: analisis de resultados y modelado de la variable objetivo `result` (H, D, A).

- H: victoria local
- D: empate
- A: victoria visitante

## 2) Cobertura

- Competicion: Liga FUTVE (formatos historicos incluidos: Apertura, Clausura, fases y playoffs segun temporada)
- Temporadas: 2002-2003 hasta 2025
- Numero de archivos por temporada: 24 CSV (uno por temporada)
- Rango temporal en UTC: `2002-08-04T20:30:00+00:00` a `2025-12-06T22:00:00+00:00`

## 3) Fuente de datos

- Fuente primaria: Soccerway
- Dominio observado en `source_url`: `ve.soccerway.com`
- Naturaleza de recoleccion: web scraping de paginas de resultados

## 4) Metodo de recoleccion

La extraccion se realiza desde el bloque de script embebido en la pagina de resultados (`cjs.initialFeeds['results']`) y, cuando aplica, mediante paginacion de feeds internos para completar todos los eventos de una temporada.

Salida por temporada:

- `data/raw/futve_<season>_results.csv`

Salida consolidada (script incluido):

- `data/processed/futve_consolidated_results.csv`

Script de consolidacion:

- `consolidate_csv.py`

## 5) Estructura de datos (schema)

Columnas del CSV:

1. `season` (string): temporada (ejemplo: `2005-2006`, `2025`)
2. `competition` (string): nombre de competicion (`Liga FUTVE`)
3. `phase` (string): fase/torneo (ejemplo: `Apertura`, `Clausura`, `Primera fase`)
4. `round` (string): jornada/ronda (ejemplo: `Jornada 1`, `Round 18`)
5. `match_id` (string): identificador unico de partido en fuente
6. `match_date_utc` (datetime ISO 8601): fecha/hora en UTC
7. `match_date_local` (datetime ISO 8601): fecha/hora local
8. `home_team` (string): equipo local
9. `away_team` (string): equipo visitante
10. `home_score` (integer): goles local
11. `away_score` (integer): goles visitante
12. `result` (string): `H`, `D`, `A`
13. `source_url` (string): URL origen de temporada

## 6) Estadisticas descriptivas (corte actual)

Resumen global de todas las temporadas:

- Filas totales: **6550**
- Temporadas: **24**
- Equipos unicos (home/away combinados): **42**
- Distribucion de `result`:
  - H: **2979**
  - D: **1935**
  - A: **1636**
- Valores faltantes en `round`: **614**

Fases mas frecuentes:

- Apertura: 2542
- Clausura: 2504
- VENEZUELA: Liga FUTVE: 450
- Primera fase: 306
- VENEZUELA: Primera Division: 190

## 7) Calidad y validaciones realizadas

Validaciones observadas sobre el set historico:

- Cabecera consistente en todos los CSV.
- Sin duplicados por `match_id` en el conjunto total evaluado.
- `result` presente en formato categorico esperado (`H`, `D`, `A`).

## 8) Limitaciones conocidas

1. **Nomenclatura de fases heterogenea**: `phase` mezcla etiquetas limpias y etiquetas de fuente (ej. `Apertura` vs `VENEZUELA: Primera Division`).
2. **Rondas faltantes**: algunas filas no contienen `round`.
3. **Cambios de formato de liga** por temporada pueden afectar comparabilidad directa.
4. Dependencia de estructura de fuente web (potencial rotura futura del scraper).

## 9) Recomendaciones de uso

- Normalizar `phase` antes de modelar.
- Estandarizar nombres de equipos (alias historicos).
- Usar particion temporal para ML (train temporadas antiguas, test temporadas recientes).
- Mantener `home_score` y `away_score` para validacion, incluso si el objetivo es solo `result`.

## 10) Uso responsable, legal y etico

- Uso recomendado para fines educativos/investigacion.
- Respetar terminos de uso y `robots.txt` del sitio fuente.
- Evitar scraping agresivo (usar rate limiting y reintentos controlados).

## 11) Versionado sugerido

- Versionar por fecha de extraccion (ej: `vYYYY.MM.DD`)
- Incluir changelog con:
  - temporadas nuevas
  - correcciones de parseo
  - cambios de esquema

## 12) Como generar el consolidado

Comando:

```bash
python3 consolidate_csv.py
```

Comando con rutas personalizadas:

```bash
python3 consolidate_csv.py --input-glob "data/raw/futve_*_results.csv" --output "data/processed/futve_consolidated_results.csv"
```


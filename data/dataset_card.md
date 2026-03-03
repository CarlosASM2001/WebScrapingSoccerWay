# Dataset Card – Liga FUTVE Results (2002–2003 to 2025)

## 1) Summary

This dataset contains historical results from Venezuela’s top-division football league (Liga FUTVE), scraped from Soccerway and stored in CSV format.

Primary objective: results analysis and modeling the target variable `result` (H, D, A).

- H: home win  
- D: draw  
- A: away win  

## 2) Coverage

- Competition: Liga FUTVE (historical formats included: Apertura, Clausura, phases and playoffs depending on the season)
- Seasons: 2002–2003 through 2025
- Files per season: 24 CSVs (one per season)
- Time range in UTC: `2002-08-04T20:30:00+00:00` to `2025-12-06T22:00:00+00:00`

## 3) Data Source

- Primary source: Soccerway
- Domain observed in `source_url`: `ve.soccerway.com`
- Collection method: web scraping of results pages

## 4) Collection Method

Extraction is performed from the embedded script block on the results page (`cjs.initialFeeds['results']`) and, when applicable, through pagination of internal feeds to retrieve all events for a season.

Per-season output:

- `data/raw/futve_<season>_results.csv`

Consolidated output (script included):

- `data/processed/futve_consolidated_results.csv`

Consolidation script:

- `consolidate_csv.py`

## 5) Data Structure (Schema)

CSV columns:

1. `season` (string): season (e.g., `2005-2006`, `2025`)
2. `competition` (string): competition name (`Liga FUTVE`)
3. `phase` (string): phase/tournament (e.g., `Apertura`, `Clausura`, `First stage`)
4. `round` (string): matchday/round (e.g., `Matchday 1`, `Round 18`)
5. `match_id` (string): unique match identifier from the source
6. `match_date_utc` (ISO 8601 datetime): date/time in UTC
7. `match_date_local` (ISO 8601 datetime): local date/time
8. `home_team` (string): home team
9. `away_team` (string): away team
10. `home_score` (integer): home goals
11. `away_score` (integer): away goals
12. `result` (string): `H`, `D`, `A`
13. `source_url` (string): season source URL

## 6) Descriptive Statistics (Current Snapshot)

Overall summary across all seasons:

- Total rows: **6,550**
- Seasons: **24**
- Unique teams (home/away combined): **42**
- `result` distribution:
  - H: **2,979**
  - D: **1,935**
  - A: **1,636**
- Missing values in `round`: **614**

Most frequent phases:

- Apertura: 2,542  
- Clausura: 2,504  
- VENEZUELA: Liga FUTVE: 450  
- First stage: 306  
- VENEZUELA: First Division: 190  

## 7) Data Quality and Validations

Observed validations on the historical set:

- Consistent header across all CSVs.
- No duplicates by `match_id` in the evaluated full dataset.
- `result` present in the expected categorical format (`H`, `D`, `A`).

## 8) Known Limitations

1. **Heterogeneous phase naming**: `phase` mixes clean labels and source labels (e.g., `Apertura` vs `VENEZUELA: First Division`).
2. **Missing rounds**: some rows do not include `round`.
3. **League format changes** by season may affect direct comparability.
4. Dependency on the source website structure (potential future scraper breakage).

## 9) Usage Recommendations

- Normalize `phase` before modeling.
- Standardize team names (historical aliases).
- Use time-based splitting for ML (train on older seasons, test on more recent seasons).
- Keep `home_score` and `away_score` for validation, even if the target is only `result`.

## 10) Responsible, Legal, and Ethical Use

- Recommended for educational/research purposes.
- Respect the source site’s terms of use and `robots.txt`.
- Avoid aggressive scraping (use rate limiting and controlled retries).

## 11) Suggested Versioning

- Version by extraction date (e.g., `vYYYY.MM.DD`)
- Include a changelog with:
  - new seasons
  - parsing fixes
  - schema changes

## 12) How to Generate the Consolidated File

Command:

```bash
python3 consolidate_csv.py
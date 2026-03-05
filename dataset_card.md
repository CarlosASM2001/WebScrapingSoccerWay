# Liga FUTVE Match Results Dataset (2002-2003 to 2025)

Kaggle-ready dataset card for historical Venezuelan first-division match results.

---

## Suggested Kaggle metadata

- **Title:** Liga FUTVE Match Results (2002-2003 to 2025)
- **Subtitle:** Historical match-level results for Venezuelan first division
- **License (recommended):** CC BY 4.0
- **Tags (recommended):** football, soccer, sports analytics, time series, classification

---

## Context

This dataset contains historical match results for Venezuela's top football division (Liga FUTVE), extracted from Soccerway and stored in CSV format.

The main modeling target is:

- `result = H` (home win)
- `result = D` (draw)
- `result = A` (away win)

Typical use cases:

- match outcome prediction (H/D/A)
- trend analysis by season/phase
- team performance analysis
- feature engineering for time-based ML pipelines

---

## Coverage

- **Competition:** Liga FUTVE (including historical formats such as Apertura, Clausura, phase groups, playoffs)
- **Seasons covered:** 2002-2003 through 2025
- **Season files:** 24 CSV files (one per season)
- **Observed UTC range:** `2002-08-04T20:30:00+00:00` to `2025-12-06T22:00:00+00:00`
- **Source domain in `source_url`:** `ve.soccerway.com`

---

## Content

### Files

- Per-season files: `data/raw/futve_<season>_results.csv`
- Consolidated output (generated): `data/processed/futve_consolidated_results.csv`
- Consolidation script: `consolidate_csv.py`

### Columns

1. `season` (string) - season label (e.g., `2005-2006`, `2025`)
2. `competition` (string) - competition name (`Liga FUTVE`)
3. `phase` (string) - tournament phase (e.g., `Apertura`, `Clausura`, `Primera fase`)
4. `round` (string) - round/matchday (e.g., `Jornada 1`, `Round 18`)
5. `match_id` (string) - source match identifier
6. `match_date_utc` (ISO 8601 datetime) - kickoff datetime in UTC
7. `match_date_local` (ISO 8601 datetime) - local kickoff datetime
8. `home_team` (string) - home team
9. `away_team` (string) - away team
10. `home_score` (integer) - home goals
11. `away_score` (integer) - away goals
12. `result` (string) - categorical outcome (`H`, `D`, `A`)
13. `source_url` (string) - source season URL

---

## Data Collection Process

Data is collected via web scraping from Soccerway result pages.

At extraction time, match records are parsed from embedded script feed blocks (e.g., `cjs.initialFeeds['results']`) and, when needed, completed through paginated internal feed requests to capture all events in a season.

---

## Data Quality Summary (current cut)

Global summary across all seasons:

- **Rows:** 6550
- **Seasons:** 24
- **Unique teams (home+away combined):** 42
- **Outcome distribution (`result`):**
  - H: 2979
  - D: 1935
  - A: 1636
- **Missing values in `round`:** 614

Observed quality checks:

- consistent header across season CSV files
- no duplicate `match_id` in the evaluated global set
- categorical target `result` consistently encoded as `H/D/A`

---

## Known Limitations

1. **Heterogeneous `phase` labels:** some values are normalized labels (`Apertura`) while others are source-style labels (e.g., `VENEZUELA: Primera División`).
2. **Missing `round` values:** part of the rows has empty round information.
3. **Competition format changes by season:** direct cross-season comparisons may require normalization.
4. **Source dependency:** scraper stability depends on external website structure.

---

## Recommended Preprocessing

- normalize `phase` into a curated taxonomy (e.g., Apertura/Clausura/Playoffs/Other)
- standardize team names and aliases
- use time-aware train/test splits (older seasons for training, newer for testing)
- keep `home_score` and `away_score` for validation and feature engineering even when predicting only `result`

---

## Consolidation

Generate a single consolidated CSV from all season files:

```bash
python3 consolidate_csv.py
```

Custom paths:

```bash
python3 consolidate_csv.py --input-glob "data/raw/futve_*_results.csv" --output "data/processed/futve_consolidated_results.csv"
```

---

## Acknowledgements

- Data source: Soccerway
- This dataset is intended for educational/research purposes.

---

## Inspiration

- Build a robust baseline for Liga FUTVE match outcome prediction (`H/D/A`)
- Study long-term evolution of home advantage and draw rates
- Create reproducible football analytics workflows for Venezuelan football


import csv
from pathlib import Path

DEFAULT_INPUT_GLOBAL = 'data/raw/futve_*_results.csv'
DEFAULT_OUTPUT_GLOBAL = 'data/processed/futve_consolidate_results.csv'

def load_rows(csv_path:Path) -> tuple[list[str],list[dict[str,str]]]:

    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)

        rows = list(reader)

        return reader.fieldnames,rows



def main():
    expected_headers: list[str] | None = None
    consolidated_rows: list[dict[str, str]] = []
    seen_keys: set[tuple[str, str]] = set()
    duplicates_skipped = 0

    input_files = sorted(Path().glob(DEFAULT_INPUT_GLOBAL))
    output_path = Path(DEFAULT_OUTPUT_GLOBAL)

    for csv_path in input_files:

        headers,rows = load_rows(csv_path)

        if expected_headers is None:
            expected_headers = headers

        for row in rows:
            key = (row.get("season",""), row.get("match_id",""))
            if key in seen_keys:
                duplicates_skipped += 1
                continue
            seen_keys.add(key)
            consolidated_rows.append(row)

    consolidated_rows.sort(
        key=lambda row: (
            row.get("match_date_utc", ""),
            row.get("season", ""),
            row.get("match_id", ""),
        )
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=expected_headers)
        writer.writeheader()
        writer.writerows(consolidated_rows)

    print(f"Temporadas leidas: {len(input_files)}")
    print(f"Partidos consolidados: {len(consolidated_rows)}")
    print(f"Duplicados omitidos: {duplicates_skipped}")
    print(f"CSV consolidado: {output_path}")

if __name__ == "__main__":
    main()
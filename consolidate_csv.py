import argparse
import csv
from pathlib import Path

DEFAULT_INPUT_GLOB = "data/raw/futve_*_results.csv"
DEFAULT_OUTPUT_PATH = "data/processed/futve_consolidated_results.csv"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Consolida todos los CSV de temporadas FUTVE en un solo archivo."
    )
    parser.add_argument(
        "--input-glob",
        default=DEFAULT_INPUT_GLOB,
        help=f"Patron glob de entrada (default: {DEFAULT_INPUT_GLOB})",
    )
    parser.add_argument(
        "--output",
        default=DEFAULT_OUTPUT_PATH,
        help=f"Ruta del CSV consolidado (default: {DEFAULT_OUTPUT_PATH})",
    )
    return parser.parse_args()


def load_rows(csv_path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames is None:
            raise ValueError(f"El archivo no tiene cabecera CSV: {csv_path}")
        rows = list(reader)
        return reader.fieldnames, rows


def main() -> None:
    args = parse_args()
    output_path = Path(args.output)

    input_files = sorted(Path().glob(args.input_glob))
    input_files = [path for path in input_files if path.resolve() != output_path.resolve()]

    if not input_files:
        raise FileNotFoundError(
            f"No se encontraron archivos con el patron: {args.input_glob}"
        )

    expected_headers: list[str] | None = None
    consolidated_rows: list[dict[str, str]] = []
    seen_keys: set[tuple[str, str]] = set()
    duplicates_skipped = 0

    for csv_path in input_files:
        headers, rows = load_rows(csv_path)
        if expected_headers is None:
            expected_headers = headers
        elif headers != expected_headers:
            raise ValueError(
                f"Cabeceras incompatibles en {csv_path}. "
                f"Esperado: {expected_headers} | Encontrado: {headers}"
            )

        for row in rows:
            key = (row.get("season", ""), row.get("match_id", ""))
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

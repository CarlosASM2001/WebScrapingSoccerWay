import csv
import json
import re
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlparse

import requests

RESULTS_PAGE_URL = "https://ve.soccerway.com/venezuela/liga-futve/resultados/"
SUMMARY_PAGE_URL = "https://us.soccerway.com/venezuela/liga-futve/"
SEASON_LABEL = "2026"
COMPETITION_LABEL = "Liga FUTVE"
OUTPUT_CSV_PATH = Path("data/raw/futve_2026_results.csv")
RAW_HTML_PATH = Path("data/raw/html/futve_2026_results_page.html")
USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
)


def extract_window_environment(html: str) -> dict:
    match = re.search(r"window\.environment\s*=\s*(\{.*?\});", html, re.S)
    if not match:
        raise ValueError("No se pudo encontrar window.environment en la página.")
    return json.loads(match.group(1))


def resolve_environment(results_html: str) -> dict:
    try:
        return extract_window_environment(results_html)
    except ValueError:
        summary_response = requests.get(
            SUMMARY_PAGE_URL,
            timeout=30,
            headers={"User-Agent": USER_AGENT},
        )
        summary_response.raise_for_status()
        return extract_window_environment(summary_response.text)


def extract_initial_results_feed(html: str) -> tuple[str, int, int]:
    pattern = (
        r"cjs\.initialFeeds\['results'\]\s*=\s*\{\s*"
        r"data:\s*`(.*?)`,\s*"
        r"allEventsCount:\s*(\d+),\s*"
        r"seasonId:\s*(\d+)\s*,?"
    )
    match = re.search(pattern, html, re.S)
    if not match:
        raise ValueError("No se pudo encontrar el feed inicial de resultados.")
    feed_data = match.group(1)
    all_events_count = int(match.group(2))
    season_id = int(match.group(3))
    return feed_data, all_events_count, season_id


def extract_timezone_hour(html: str) -> int:
    match = re.search(r"default_tz\s*=\s*(-?\d+)\s*;", html)
    if not match:
        raise ValueError("No se pudo encontrar default_tz en la página.")
    return int(match.group(1))


def parse_feed_events(feed_text: str) -> list[dict]:
    events = []
    current_phase = ""

    for segment in feed_text.split("¬~"):
        if not segment.strip():
            continue

        segment_data = {}
        for item in segment.split("¬"):
            if "÷" not in item:
                continue
            key, value = item.split("÷", 1)
            segment_data[key] = value

        if "ZA" in segment_data:
            raw_phase = segment_data["ZA"]
            if " - " in raw_phase:
                current_phase = raw_phase.split(" - ", 1)[1].strip()
            else:
                current_phase = raw_phase.strip()

        if "AA" in segment_data:
            segment_data["_phase"] = current_phase
            events.append(segment_data)

    return events


def parse_basic_feed_meta(feed_text: str) -> tuple[int, str]:
    for segment in feed_text.split("¬~"):
        if not segment.strip():
            continue
        data = {}
        for item in segment.split("¬"):
            if "÷" not in item:
                continue
            key, value = item.split("÷", 1)
            data[key] = value
        if "ZB" in data and "ZEE" in data:
            return int(data["ZB"]), data["ZEE"]
    raise ValueError("No se pudieron extraer country_id y tournament_id del feed.")


def build_tournament_results_feed_name(
    sport_id: int,
    country_id: int,
    tournament_id: str,
    season_id: int,
    data_part: int,
    timezone_hour: int,
    language_web: str,
    project_type_id: int,
) -> str:
    return (
        f"tr_{sport_id}_{country_id}_{tournament_id}_{season_id}_{data_part}_"
        f"{timezone_hour}_{language_web}_{project_type_id}"
    )


def compute_result(home_score: int | None, away_score: int | None) -> str:
    if home_score is None or away_score is None:
        return ""
    if home_score > away_score:
        return "H"
    if home_score < away_score:
        return "A"
    return "D"


def to_int(value: str | None) -> int | None:
    if value is None:
        return None
    value = value.strip()
    if value == "":
        return None
    try:
        return int(value)
    except ValueError:
        return None


def write_csv(events_by_id: dict[str, dict], timezone_hour: int) -> None:
    tz = timezone(timedelta(hours=timezone_hour))
    rows = []

    for event in events_by_id.values():
        timestamp = to_int(event.get("AD"))
        if timestamp is None:
            continue

        utc_dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
        local_dt = utc_dt.astimezone(tz)

        home_score = to_int(event.get("AG"))
        away_score = to_int(event.get("AH"))

        rows.append(
            {
                "season": SEASON_LABEL,
                "competition": COMPETITION_LABEL,
                "phase": event.get("_phase", ""),
                "round": event.get("ER", ""),
                "match_id": event.get("AA", ""),
                "match_date_utc": utc_dt.isoformat(),
                "match_date_local": local_dt.isoformat(),
                "home_team": event.get("AE", ""),
                "away_team": event.get("AF", ""),
                "home_score": home_score if home_score is not None else "",
                "away_score": away_score if away_score is not None else "",
                "result": compute_result(home_score, away_score),
                "source_url": RESULTS_PAGE_URL,
            }
        )

    rows.sort(key=lambda row: row["match_date_utc"])

    OUTPUT_CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
    with OUTPUT_CSV_PATH.open("w", encoding="utf-8", newline="") as csv_file:
        writer = csv.DictWriter(
            csv_file,
            fieldnames=[
                "season",
                "competition",
                "phase",
                "round",
                "match_id",
                "match_date_utc",
                "match_date_local",
                "home_team",
                "away_team",
                "home_score",
                "away_score",
                "result",
                "source_url",
            ],
        )
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    response = requests.get(
        RESULTS_PAGE_URL,
        timeout=30,
        headers={"User-Agent": USER_AGENT},
    )
    response.raise_for_status()
    html = response.text

    RAW_HTML_PATH.parent.mkdir(parents=True, exist_ok=True)
    RAW_HTML_PATH.write_text(html, encoding="utf-8")

    environment = resolve_environment(html)
    app_config = environment["config"]["app"]
    sport_id = int(environment["sport_id"])
    feed_sign = app_config["feed_sign"]
    language_web = app_config["lang"]["web"]
    project_type_id = int(app_config["project_type"]["id"])
    timezone_hour = extract_timezone_hour(html)

    initial_feed, all_events_count, season_id = extract_initial_results_feed(html)
    country_id, tournament_id = parse_basic_feed_meta(initial_feed)

    events_by_id = {}
    for event in parse_feed_events(initial_feed):
        events_by_id[event["AA"]] = event

    parsed_url = urlparse(RESULTS_PAGE_URL)
    origin = f"{parsed_url.scheme}://{parsed_url.netloc}"

    # Soccerway entrega una parte inicial y luego páginas extra en /x/feed/tr_...
    for data_part in range(1, 50):
        if len(events_by_id) >= all_events_count:
            break

        feed_name = build_tournament_results_feed_name(
            sport_id=sport_id,
            country_id=country_id,
            tournament_id=tournament_id,
            season_id=season_id,
            data_part=data_part,
            timezone_hour=timezone_hour,
            language_web=language_web,
            project_type_id=project_type_id,
        )
        feed_url = f"{origin}/x/feed/{feed_name}"
        feed_response = requests.get(
            feed_url,
            timeout=30,
            headers={
                "User-Agent": USER_AGENT,
                "Referer": RESULTS_PAGE_URL,
                "x-fsign": feed_sign,
            },
        )
        feed_response.raise_for_status()
        feed_text = feed_response.text
        if not feed_text.strip():
            break

        new_events = parse_feed_events(feed_text)
        added = 0
        for event in new_events:
            if event["AA"] not in events_by_id:
                added += 1
            events_by_id[event["AA"]] = event

        if added == 0:
            break

    write_csv(events_by_id, timezone_hour)

    print(f"Partidos esperados: {all_events_count}")
    print(f"Partidos extraidos: {len(events_by_id)}")
    print(f"CSV generado en: {OUTPUT_CSV_PATH}")
    print(f"HTML crudo guardado en: {RAW_HTML_PATH}")

    if len(events_by_id) != all_events_count:
        raise RuntimeError(
            f"Extraccion incompleta: se esperaban {all_events_count} "
            f"partidos y se obtuvieron {len(events_by_id)}."
        )


if __name__ == "__main__":
    main()
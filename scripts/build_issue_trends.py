from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.analyzers.issue_trend_analyzer import analyze_issue_trends


DEFAULT_CLASSIFIED_SOURCE = ROOT / "data" / "processed" / "issue_classified_sample.json"
DEFAULT_RAW_SOURCE = ROOT / "data" / "raw" / "cycc_question_video_metadata.csv"
DEFAULT_HOTSPOTS_SOURCE = ROOT / "dashboard" / "data" / "hotspots.json"
DEFAULT_OUTPUT = ROOT / "dashboard" / "data" / "issue_trends.json"


def load_json_list(path: Path) -> list[dict]:
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, list) else []


def load_csv_records(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as csv_file:
        return list(csv.DictReader(csv_file))


def write_json(path: Path, data: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        json.dumps(data, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )


def build_issue_trends(
    classified_source: Path = DEFAULT_CLASSIFIED_SOURCE,
    raw_source: Path = DEFAULT_RAW_SOURCE,
    hotspots_source: Path = DEFAULT_HOTSPOTS_SOURCE,
    output: Path = DEFAULT_OUTPUT,
) -> list[dict]:
    classified_records = load_json_list(classified_source)
    raw_records = load_csv_records(raw_source)
    hotspots = load_json_list(hotspots_source)

    trends = analyze_issue_trends(
        classified_records=classified_records,
        raw_records=raw_records,
        hotspots=hotspots,
    )
    write_json(output, trends)
    return trends


def main() -> None:
    parser = argparse.ArgumentParser(description="Build dashboard issue trend prototype data.")
    parser.add_argument("--classified-source", type=Path, default=DEFAULT_CLASSIFIED_SOURCE)
    parser.add_argument("--raw-source", type=Path, default=DEFAULT_RAW_SOURCE)
    parser.add_argument("--hotspots-source", type=Path, default=DEFAULT_HOTSPOTS_SOURCE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()

    trends = build_issue_trends(
        classified_source=args.classified_source,
        raw_source=args.raw_source,
        hotspots_source=args.hotspots_source,
        output=args.output,
    )
    print(f"Wrote {len(trends)} issue trend records to {args.output}")


if __name__ == "__main__":
    main()

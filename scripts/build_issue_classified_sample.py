from __future__ import annotations

import argparse
import csv
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.classifiers.issue_classifier import classify_record

DEFAULT_SOURCE = ROOT / "data" / "raw" / "cycc_question_video_metadata.csv"
DEFAULT_OUTPUT = ROOT / "data" / "processed" / "issue_classified_sample.json"
DEFAULT_LIMIT = 10


def load_records(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing source CSV: {path}")
    with path.open("r", encoding="utf-8-sig", newline="") as csv_file:
        return list(csv.DictReader(csv_file))


def build_issue_classified_sample(
    source: Path = DEFAULT_SOURCE,
    output: Path = DEFAULT_OUTPUT,
    limit: int = DEFAULT_LIMIT,
) -> list[dict]:
    records = load_records(source)
    classified = [classify_record(record) for record in records[:limit]]
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(classified, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return classified


def main() -> None:
    parser = argparse.ArgumentParser(description="Build a classified issue sample from CYCC question video metadata.")
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--limit", type=int, default=DEFAULT_LIMIT)
    args = parser.parse_args()

    classified = build_issue_classified_sample(args.source, args.output, args.limit)
    print(f"Wrote {len(classified)} classified issue records to {args.output}")


if __name__ == "__main__":
    main()

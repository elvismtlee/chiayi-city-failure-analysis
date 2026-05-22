from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.parse_cycc_minutes_sample import parse_all_fixtures


OUTPUT_PATH = ROOT / "dashboard" / "data" / "cycc_minutes_review_queue.json"

SENSITIVE_FIELDS = {"phone", "email", "address", "national_id", "id_number", "full_address"}

REQUIRED_FIELDS = [
    "queue_id", "source_id", "meeting_name", "meeting_date", "councilor_name",
    "department", "agenda_item", "issue_keywords", "source_url", "raw_text_excerpt",
    "raw_hash", "parser_status", "review_status", "review_priority",
    "needs_manual_review", "recommended_action", "notes",
]

NOTES = (
    "fixture-only parser prototype output; this record has not been manually reviewed "
    "and must not be used as an official analysis result."
)


def text_excerpt(value: str, max_chars: int = 120) -> str:
    text = " ".join(str(value or "").split())
    if len(text) <= max_chars:
        return text
    return text[: max_chars - 1].rstrip() + "…"


def review_priority(record: dict[str, Any]) -> str:
    if not str(record.get("meeting_date", "")).strip():
        return "needs_metadata_review"
    if not str(record.get("councilor_name", "")).strip():
        return "needs_metadata_review"
    return "normal"


def build_queue_item(record: dict[str, Any]) -> dict[str, Any]:
    raw_hash = str(record.get("raw_hash", ""))
    item = {
        "queue_id": f"cycc-minutes-{raw_hash[:12]}",
        "source_id": str(record.get("source_id", "")),
        "meeting_name": str(record.get("meeting_name", "")),
        "meeting_date": str(record.get("meeting_date", "")),
        "councilor_name": str(record.get("councilor_name", "")),
        "department": str(record.get("department", "")),
        "agenda_item": str(record.get("agenda_item", "")),
        "issue_keywords": list(record.get("issue_keywords") or []),
        "source_url": str(record.get("source_url", "")),
        "raw_text_excerpt": text_excerpt(str(record.get("raw_text", ""))),
        "raw_hash": raw_hash,
        "parser_status": "parsed_from_fixture",
        "review_status": "unreviewed",
        "review_priority": review_priority(record),
        "needs_manual_review": True,
        "recommended_action": "manual_minutes_review",
        "notes": NOTES,
    }
    validate_queue_item(item)
    return item


def validate_queue_item(item: dict[str, Any]) -> None:
    missing = [field for field in REQUIRED_FIELDS if field not in item]
    if missing:
        raise ValueError(f"Missing required queue fields: {missing}")
    leaked = SENSITIVE_FIELDS.intersection(str(key).lower() for key in item.keys())
    if leaked:
        raise ValueError(f"Sensitive fields are not allowed: {sorted(leaked)}")
    if item["parser_status"] != "parsed_from_fixture":
        raise ValueError("parser_status must remain parsed_from_fixture")
    if item["review_status"] != "unreviewed":
        raise ValueError("review_status must remain unreviewed")
    if item["needs_manual_review"] is not True:
        raise ValueError("needs_manual_review must be true")
    if len(item["raw_text_excerpt"]) > 120:
        raise ValueError("raw_text_excerpt must be at most 120 characters")


def build_queue() -> list[dict[str, Any]]:
    return [build_queue_item(record) for record in parse_all_fixtures()]


def write_queue(output_path: Path = OUTPUT_PATH) -> list[dict[str, Any]]:
    queue = build_queue()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(queue, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return queue


def main() -> None:
    queue = write_queue()
    print(f"Wrote {len(queue)} CYCC minutes review candidates to {OUTPUT_PATH}")


if __name__ == "__main__":
    main()

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = ROOT / "dashboard" / "data" / "cycc_minutes_review_queue.json"
OUTPUT_PATH = ROOT / "data" / "processed" / "cycc_minutes_reviewed_sample.json"
DASHBOARD_OUTPUT_PATH = ROOT / "dashboard" / "data" / "cycc_minutes_reviewed_sample.json"

REVIEWED_AT = "2026-05-22"
REVIEWER = "campaign_ops"
PUBLIC_USE_STATUS = "internal_reviewed_sample"
PUBLIC_USE_NOTES = "sample data, not official conclusion; requires manual policy review before public use."

SENSITIVE_FIELDS = {"phone", "email", "address", "full_address", "national_id", "id_number"}

REQUIRED_FIELDS = [
    "reviewed_id",
    "source_queue_id",
    "source_id",
    "meeting_name",
    "meeting_date",
    "councilor_name",
    "department",
    "agenda_item",
    "issue_keywords",
    "source_url",
    "raw_text_excerpt",
    "raw_hash",
    "parser_status",
    "review_status",
    "reviewed_at",
    "reviewer",
    "review_notes",
    "source_context",
    "public_use_status",
    "public_use_notes",
]


def load_queue(input_path: Path = INPUT_PATH) -> list[dict[str, Any]]:
    return json.loads(input_path.read_text(encoding="utf-8"))


def reviewed_id(raw_hash: str) -> str:
    return f"cycc-reviewed-{raw_hash[:12]}"


def is_fixture_sample(item: dict[str, Any]) -> bool:
    return item.get("parser_status") == "parsed_from_fixture" and str(item.get("queue_id", "")).startswith("cycc-minutes-")


def build_reviewed_item(item: dict[str, Any]) -> dict[str, Any]:
    raw_hash = str(item["raw_hash"])
    reviewed_item = {
        "reviewed_id": reviewed_id(raw_hash),
        "source_queue_id": item["queue_id"],
        "source_id": item["source_id"],
        "meeting_name": item["meeting_name"],
        "meeting_date": item["meeting_date"],
        "councilor_name": item["councilor_name"],
        "department": item["department"],
        "agenda_item": item["agenda_item"],
        "issue_keywords": list(item.get("issue_keywords") or []),
        "source_url": item["source_url"],
        "raw_text_excerpt": item["raw_text_excerpt"],
        "raw_hash": raw_hash,
        "parser_status": item["parser_status"],
        "review_status": "reviewed",
        "reviewed_at": REVIEWED_AT,
        "reviewer": REVIEWER,
        "review_notes": "Sample manual review confirms fixture fields are internally consistent; not an official conclusion.",
        "source_context": f"Fixture-only public sample derived from {item['source_url']}; not a formal CYCC dataset.",
        "public_use_status": PUBLIC_USE_STATUS,
        "public_use_notes": PUBLIC_USE_NOTES,
    }
    validate_reviewed_item(reviewed_item)
    return reviewed_item


def validate_reviewed_item(item: dict[str, Any]) -> None:
    missing = [field for field in REQUIRED_FIELDS if field not in item]
    if missing:
        raise ValueError(f"Missing reviewed sample fields: {', '.join(missing)}")

    sensitive = {key.lower() for key in item} & SENSITIVE_FIELDS
    if sensitive:
        raise ValueError(f"Sensitive fields are not allowed: {', '.join(sorted(sensitive))}")

    if item["review_status"] != "reviewed":
        raise ValueError("Reviewed sample rows must use review_status=reviewed.")
    if item["public_use_status"] != PUBLIC_USE_STATUS:
        raise ValueError("Reviewed sample rows must remain internal_reviewed_sample.")

    notes = item["public_use_notes"].lower()
    if "sample" not in notes or "not official" not in notes:
        raise ValueError("public_use_notes must disclose sample data and not official conclusion.")

    if not isinstance(item["issue_keywords"], list):
        raise ValueError("issue_keywords must be a list.")


def build_reviewed_sample(records: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    source_records = records if records is not None else load_queue()
    return [build_reviewed_item(item) for item in source_records if is_fixture_sample(item)]


def write_reviewed_sample(
    output_path: Path = OUTPUT_PATH,
    dashboard_output_path: Path | None = DASHBOARD_OUTPUT_PATH,
) -> list[dict[str, Any]]:
    sample = build_reviewed_sample()
    serialized = json.dumps(sample, ensure_ascii=False, indent=2) + "\n"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(serialized, encoding="utf-8")
    if dashboard_output_path is not None:
        dashboard_output_path.parent.mkdir(parents=True, exist_ok=True)
        dashboard_output_path.write_text(serialized, encoding="utf-8")
    return sample


if __name__ == "__main__":
    rows = write_reviewed_sample()
    print(f"Wrote {len(rows)} reviewed sample rows to {OUTPUT_PATH.relative_to(ROOT)}")
    print(f"Wrote {len(rows)} reviewed sample rows to {DASHBOARD_OUTPUT_PATH.relative_to(ROOT)}")

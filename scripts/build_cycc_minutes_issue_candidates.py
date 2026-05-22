from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = ROOT / "data" / "processed" / "cycc_minutes_reviewed_sample.json"
OUTPUT_PATH = ROOT / "dashboard" / "data" / "cycc_minutes_issue_candidates.json"

SENSITIVE_FIELDS = {"phone", "email", "address", "full_address", "national_id", "id_number"}
BANNED_TERMS = ["民調", "支持度調查"]

REQUIRED_FIELDS = [
    "candidate_id",
    "reviewed_id",
    "meeting_date",
    "department",
    "issue_title",
    "issue_keywords",
    "issue_summary",
    "source_url",
    "source_context",
    "review_status",
    "public_use_status",
    "confidence_level",
    "recommended_follow_up",
    "notes",
]


def load_reviewed_sample(input_path: Path = INPUT_PATH) -> list[dict[str, Any]]:
    return json.loads(input_path.read_text(encoding="utf-8"))


def candidate_id(reviewed_id: str) -> str:
    return f"cycc-issue-{reviewed_id[-12:]}"


def short_summary(excerpt: str) -> str:
    text = " ".join(str(excerpt).split())
    return f"依 reviewed sample 摘要：{text[:120]}"


def build_issue_candidate(item: dict[str, Any]) -> dict[str, Any]:
    reviewed_id = str(item["reviewed_id"])
    candidate = {
        "candidate_id": candidate_id(reviewed_id),
        "reviewed_id": reviewed_id,
        "meeting_date": item["meeting_date"],
        "department": item["department"],
        "issue_title": item["agenda_item"],
        "issue_keywords": list(item.get("issue_keywords") or []),
        "issue_summary": short_summary(item.get("raw_text_excerpt", "")),
        "source_url": item["source_url"],
        "source_context": item["source_context"],
        "review_status": item["review_status"],
        "public_use_status": item["public_use_status"],
        "confidence_level": "sample_only",
        "recommended_follow_up": "manual_policy_review",
        "notes": "derived from reviewed sample, not official public conclusion; requires manual policy review.",
    }
    validate_issue_candidate(candidate)
    return candidate


def validate_issue_candidate(item: dict[str, Any]) -> None:
    missing = [field for field in REQUIRED_FIELDS if field not in item]
    if missing:
        raise ValueError(f"Missing issue candidate fields: {', '.join(missing)}")

    sensitive = {key.lower() for key in item} & SENSITIVE_FIELDS
    if sensitive:
        raise ValueError(f"Sensitive fields are not allowed: {', '.join(sorted(sensitive))}")

    if item["confidence_level"] != "sample_only":
        raise ValueError("Issue candidates must remain sample_only.")
    if item["recommended_follow_up"] != "manual_policy_review":
        raise ValueError("Issue candidates must require manual_policy_review.")
    if not isinstance(item["issue_keywords"], list):
        raise ValueError("issue_keywords must be a list.")

    serialized = json.dumps(item, ensure_ascii=False)
    if any(term in serialized for term in BANNED_TERMS):
        raise ValueError("Issue candidates must not use polling or support survey wording.")

    notes = item["notes"].lower()
    if "sample" not in notes and "not official" not in notes:
        raise ValueError("notes must disclose sample or not official status.")


def build_issue_candidates(records: list[dict[str, Any]] | None = None) -> list[dict[str, Any]]:
    source_records = records if records is not None else load_reviewed_sample()
    return [build_issue_candidate(item) for item in source_records if item.get("public_use_status") == "internal_reviewed_sample"]


def write_issue_candidates(output_path: Path = OUTPUT_PATH) -> list[dict[str, Any]]:
    candidates = build_issue_candidates()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(candidates, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return candidates


if __name__ == "__main__":
    rows = write_issue_candidates()
    print(f"Wrote {len(rows)} issue candidates to {OUTPUT_PATH.relative_to(ROOT)}")

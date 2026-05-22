from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
INPUT_PATH = ROOT / "dashboard" / "data" / "cycc_minutes_issue_candidates.json"
OUTPUT_PATH = ROOT / "dashboard" / "data" / "weekly_summary_draft.json"

SUMMARY_ID = "weekly-summary-sample-2026-05-22"
WEEK_START = "2026-05-18"
WEEK_END = "2026-05-24"
GENERATED_AT = "2026-05-22"
PUBLIC_USE_STATUS = "internal_weekly_draft"
NOTES = "internal draft; not official conclusion; requires human review before public use."
SENSITIVE_FIELDS = {"phone", "email", "address", "full_address", "national_id", "id_number"}

REQUIRED_FIELDS = [
    "summary_id",
    "week_start",
    "week_end",
    "generated_at",
    "source_files",
    "total_candidates",
    "department_summary",
    "keyword_summary",
    "top_issues",
    "needs_review",
    "suggested_policy_topics",
    "public_use_status",
    "notes",
]


def load_candidates(input_path: Path = INPUT_PATH) -> list[dict[str, Any]]:
    return json.loads(input_path.read_text(encoding="utf-8"))


def count_summary(values: list[str]) -> list[dict[str, Any]]:
    counts = Counter(value for value in values if value)
    return [{"name": name, "count": count} for name, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))]


def build_top_issues(candidates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            "source_candidate_id": item["candidate_id"],
            "issue_title": item["issue_title"],
            "department": item["department"],
            "issue_keywords": list(item.get("issue_keywords") or []),
            "source_url": item["source_url"],
            "review_status": item["review_status"],
            "confidence_level": item["confidence_level"],
            "summary": item["issue_summary"],
        }
        for item in candidates
    ]


def build_weekly_summary(candidates: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    source_candidates = candidates if candidates is not None else load_candidates()
    keywords = [keyword for item in source_candidates for keyword in (item.get("issue_keywords") or [])]
    summary = {
        "summary_id": SUMMARY_ID,
        "week_start": WEEK_START,
        "week_end": WEEK_END,
        "generated_at": GENERATED_AT,
        "source_files": ["dashboard/data/cycc_minutes_issue_candidates.json"],
        "total_candidates": len(source_candidates),
        "department_summary": count_summary([item.get("department", "") for item in source_candidates]),
        "keyword_summary": count_summary(keywords),
        "top_issues": build_top_issues(source_candidates),
        "needs_review": [
            {
                "source_candidate_id": item["candidate_id"],
                "issue_title": item["issue_title"],
                "review_reason": "需要人工確認來源、上下文與政策可用性。",
                "recommended_next_step": "manual_policy_review",
            }
            for item in source_candidates
        ],
        "suggested_policy_topics": [
            {
                "source_candidate_id": item["candidate_id"],
                "topic_title": f"初步政策討論：{item['issue_title']}",
                "keywords": list(item.get("issue_keywords") or []),
                "rationale": "由 issue candidate 的標題與關鍵字整理，僅供內部政策審核前參考。",
                "review_status": "needs_policy_review",
            }
            for item in source_candidates
        ],
        "public_use_status": PUBLIC_USE_STATUS,
        "notes": NOTES,
    }
    validate_summary(summary)
    return summary


def validate_summary(summary: dict[str, Any]) -> None:
    missing = [field for field in REQUIRED_FIELDS if field not in summary]
    if missing:
        raise ValueError(f"Missing weekly summary fields: {', '.join(missing)}")
    sensitive = {key.lower() for key in summary} & SENSITIVE_FIELDS
    if sensitive:
        raise ValueError(f"Sensitive fields are not allowed: {', '.join(sorted(sensitive))}")
    if summary["public_use_status"] != PUBLIC_USE_STATUS:
        raise ValueError("Weekly summary must remain internal_weekly_draft.")
    notes = summary["notes"].lower()
    if "internal draft" not in notes and "not official" not in notes:
        raise ValueError("notes must disclose internal draft or not official status.")


def write_weekly_summary(output_path: Path = OUTPUT_PATH) -> dict[str, Any]:
    summary = build_weekly_summary()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return summary


if __name__ == "__main__":
    summary = write_weekly_summary()
    print(f"Wrote weekly summary draft {summary['summary_id']} to {OUTPUT_PATH.relative_to(ROOT)}")

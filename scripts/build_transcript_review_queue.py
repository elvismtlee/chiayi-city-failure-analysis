from __future__ import annotations

import csv
import json
import re
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RAW_METADATA_CSV = ROOT / "data" / "raw" / "cycc_question_video_metadata.csv"
OUTPUT_JSON = ROOT / "dashboard" / "data" / "transcript_review_queue.json"

SENSITIVE_KEYS = {
    "phone",
    "mobile",
    "email",
    "national_id",
    "id_number",
    "address",
    "full_address",
}

REQUIRED_SOURCE_FIELDS = [
    "source_id",
    "councilor_name",
    "council_term",
    "session_name",
    "video_title",
    "video_url",
    "meeting_date",
    "topic_guess",
    "crawled_at",
    "raw_hash",
]


def read_metadata(path: Path = RAW_METADATA_CSV) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        missing = [field for field in REQUIRED_SOURCE_FIELDS if field not in (reader.fieldnames or [])]
        if missing:
            raise ValueError(f"Missing required metadata fields: {missing}")
        return [dict(row) for row in reader]


def detect_video_platform(url: str) -> str:
    if "youtube.com" in url or "youtu.be" in url:
        return "youtube"
    if url:
        return "unknown_video_url"
    return "missing_url"


def extract_video_id(url: str) -> str:
    if not url:
        return ""
    patterns = [
        r"youtube\.com/embed/([A-Za-z0-9_-]+)",
        r"youtube\.com/watch\?v=([A-Za-z0-9_-]+)",
        r"youtu\.be/([A-Za-z0-9_-]+)",
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return ""


def transcript_priority(row: dict[str, str]) -> str:
    if not row.get("video_url"):
        return "needs_metadata_review"
    if not row.get("councilor_name") or not row.get("meeting_date"):
        return "medium"
    return "normal"


def needs_metadata_review(row: dict[str, str]) -> bool:
    return not bool(row.get("councilor_name")) or not bool(row.get("meeting_date"))


def queue_id(row: dict[str, str], index: int) -> str:
    raw_hash = row.get("raw_hash") or f"row-{index + 1}"
    return f"cycc-transcript-{raw_hash[:12]}"


def sanitize_item(item: dict[str, Any]) -> dict[str, Any]:
    blocked = {str(key).lower() for key in item.keys()} & SENSITIVE_KEYS
    if blocked:
        raise ValueError(f"Transcript queue item contains sensitive fields: {sorted(blocked)}")
    return item


def build_queue(rows: list[dict[str, str]] | None = None) -> list[dict[str, Any]]:
    rows = read_metadata() if rows is None else rows
    queue: list[dict[str, Any]] = []

    for index, row in enumerate(rows):
        video_url = row.get("video_url", "").strip()
        item = {
            "queue_id": queue_id(row, index),
            "source_id": row.get("source_id", "CYCC_QUESTION_VIDEO"),
            "councilor_name": row.get("councilor_name", ""),
            "council_term": row.get("council_term", ""),
            "session_name": row.get("session_name", ""),
            "video_title": row.get("video_title", ""),
            "video_url": video_url,
            "video_platform": detect_video_platform(video_url),
            "video_id": extract_video_id(video_url),
            "meeting_date": row.get("meeting_date", ""),
            "topic_guess": row.get("topic_guess", ""),
            "raw_hash": row.get("raw_hash", ""),
            "transcript_status": "not_started",
            "review_status": "unreviewed",
            "priority": transcript_priority(row),
            "needs_metadata_review": needs_metadata_review(row),
            "recommended_action": "manual_transcript_or_asr_review",
            "notes": "此清單只建立待轉錄佇列，不下載影音、不呼叫 Whisper、不加入 API key；轉錄結果需人工 review 後才能進入正式分析。",
        }
        queue.append(sanitize_item(item))

    priority_order = {"needs_metadata_review": 0, "medium": 1, "normal": 2}
    return sorted(queue, key=lambda item: (priority_order.get(item["priority"], 9), item["queue_id"]))


def write_queue(output_path: Path = OUTPUT_JSON) -> list[dict[str, Any]]:
    queue = build_queue()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(queue, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return queue


if __name__ == "__main__":
    queue = write_queue()
    print(f"Wrote {OUTPUT_JSON.relative_to(ROOT)} with {len(queue)} transcript candidates")

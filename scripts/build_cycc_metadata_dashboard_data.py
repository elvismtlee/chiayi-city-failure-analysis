from __future__ import annotations

import csv
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RAW_DIR = ROOT / "data" / "raw"
DASHBOARD_DATA_DIR = ROOT / "dashboard" / "data"
MINUTES_CSV = RAW_DIR / "cycc_minutes_metadata.csv"
VIDEOS_CSV = RAW_DIR / "cycc_question_video_metadata.csv"
REPORT_PATH = DASHBOARD_DATA_DIR / "cycc_public_records_crawl_report.json"
MINUTES_OUTPUT = DASHBOARD_DATA_DIR / "cycc_minutes_metadata.json"
VIDEOS_OUTPUT = DASHBOARD_DATA_DIR / "cycc_question_video_metadata.json"
TAIPEI_TZ = timezone(timedelta(hours=8))


def now_taipei() -> str:
    return datetime.now(TAIPEI_TZ).isoformat(timespec="seconds")


def to_taipei_iso(value: str) -> str:
    if not value:
        return now_taipei()
    parsed = datetime.fromisoformat(value)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(TAIPEI_TZ).isoformat(timespec="seconds")


def read_csv_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        return [dict(row) for row in reader]


def read_json(path: Path, fallback: Any) -> Any:
    if not path.exists() or path.stat().st_size == 0:
        return fallback
    return json.loads(path.read_text(encoding="utf-8"))


def clean_text(value: str | None) -> str:
    return (value or "").strip()


def as_int(value: str | None) -> int | None:
    text = clean_text(value)
    if not text:
        return None
    return int(text) if text.isdigit() else None


def build_minutes_payload(rows: list[dict[str, str]], latest_crawl_at: str) -> dict[str, Any]:
    items: list[dict[str, Any]] = []
    for index, row in enumerate(rows, start=1):
        detail_url = clean_text(row.get("detail_url")) or clean_text(row.get("file_url"))
        items.append(
            {
                "record_id": f"cycc-minutes-{index:03d}",
                "source_type": "minutes",
                "title": clean_text(row.get("title")) or "待補標題",
                "date": clean_text(row.get("updated_at")),
                "source_url": detail_url,
                "detail_url": detail_url,
                "view_count": as_int(row.get("views")),
                "record_count": None,
                "review_status": "manual_review_required",
                "department": clean_text(row.get("department")),
                "notes": "internal metadata / manual review required / manual publishing only",
            }
        )

    return {
        "generated_at": now_taipei(),
        "latest_crawl_at": latest_crawl_at,
        "source_name": "嘉義市議會公開資料",
        "source_type": "minutes",
        "total_count": len(items),
        "public_use_status": "internal_metadata_table",
        "manual_review_required": True,
        "no_auto_publish": True,
        "metadata_only": True,
        "notes": [
            "Internal metadata only.",
            "Manual review required before public citation.",
            "Do not use as a public-facing final statement without human verification.",
        ],
        "items": items,
    }


def build_video_payload(rows: list[dict[str, str]], latest_crawl_at: str) -> dict[str, Any]:
    items: list[dict[str, Any]] = []
    for index, row in enumerate(rows, start=1):
        video_url = clean_text(row.get("video_url"))
        title = clean_text(row.get("video_title"))
        councilor_name = clean_text(row.get("councilor_name"))
        session_name = clean_text(row.get("session_name"))
        display_title = title or "待補標題"
        if councilor_name:
            display_title = f"{display_title} / {councilor_name}"
        items.append(
            {
                "record_id": f"cycc-video-{index:03d}",
                "source_type": "question_videos",
                "title": display_title,
                "date": clean_text(row.get("meeting_date")),
                "source_url": video_url,
                "detail_url": video_url,
                "view_count": None,
                "record_count": None,
                "review_status": "manual_review_required",
                "councilor_name": councilor_name,
                "session_name": session_name,
                "topic_guess": clean_text(row.get("topic_guess")),
                "notes": "internal metadata / manual review required / manual publishing only",
            }
        )

    return {
        "generated_at": now_taipei(),
        "latest_crawl_at": latest_crawl_at,
        "source_name": "嘉義市議會公開資料",
        "source_type": "question_videos",
        "total_count": len(items),
        "public_use_status": "internal_metadata_table",
        "manual_review_required": True,
        "no_auto_publish": True,
        "metadata_only": True,
        "notes": [
            "Internal metadata only.",
            "Manual review required before public citation.",
            "Do not use as a public-facing final statement without human verification.",
        ],
        "items": items,
    }


def build_dashboard_metadata() -> tuple[dict[str, Any], dict[str, Any]]:
    report = read_json(REPORT_PATH, {})
    latest_crawl_at = to_taipei_iso(report.get("crawled_at", ""))
    minutes_rows = read_csv_rows(MINUTES_CSV)
    video_rows = read_csv_rows(VIDEOS_CSV)
    return (
        build_minutes_payload(minutes_rows, latest_crawl_at),
        build_video_payload(video_rows, latest_crawl_at),
    )


def write_dashboard_metadata() -> tuple[dict[str, Any], dict[str, Any]]:
    DASHBOARD_DATA_DIR.mkdir(parents=True, exist_ok=True)
    minutes_payload, video_payload = build_dashboard_metadata()
    MINUTES_OUTPUT.write_text(json.dumps(minutes_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    VIDEOS_OUTPUT.write_text(json.dumps(video_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return minutes_payload, video_payload


if __name__ == "__main__":
    minutes_payload, video_payload = write_dashboard_metadata()
    print(
        "Wrote dashboard metadata files with "
        f"{minutes_payload['total_count']} minutes records and {video_payload['total_count']} video records"
    )

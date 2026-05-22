from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "dashboard" / "data"
INPUT_PATH = DATA_DIR / "social_post_drafts.json"
OUTPUT_PATH = DATA_DIR / "content_schedule.json"
TAIPEI_TZ = timezone(timedelta(hours=8))


def now_taipei() -> str:
    return datetime.now(TAIPEI_TZ).isoformat(timespec="seconds")


def read_json(path: Path, fallback: Any) -> Any:
    if not path.exists() or path.stat().st_size == 0:
        return fallback
    return json.loads(path.read_text(encoding="utf-8"))


def build_content_schedule(records: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    source = records if records is not None else read_json(INPUT_PATH, [])
    items: list[dict[str, Any]] = []
    for index, draft in enumerate(source[:5], start=1):
        items.append(
            {
                "schedule_id": f"schedule-{index:03d}",
                "date": "待排程",
                "channel": draft.get("channel", "manual"),
                "title": draft.get("headline") or draft.get("issue_title") or "待命名素材",
                "status": "draft",
                "review_required": True,
                "source_issue": draft.get("issue_title", "待補"),
                "source_id": draft.get("post_id", "待補"),
                "notes": "internal schedule draft / needs human review / manual publishing only",
            }
        )
    return {
        "generated_at": now_taipei(),
        "public_use_status": "internal_content_schedule",
        "notes": [
            "Internal schedule draft only.",
            "No automatic publishing.",
            "Human review is required before public use.",
        ],
        "items": items,
    }


def write_content_schedule(output_path: Path = OUTPUT_PATH) -> dict[str, Any]:
    result = build_content_schedule()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    result = write_content_schedule()
    print(f"Wrote {len(result['items'])} content schedule items to {OUTPUT_PATH.relative_to(ROOT)}")

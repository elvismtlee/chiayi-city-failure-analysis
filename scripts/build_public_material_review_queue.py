from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "dashboard" / "data"
SOCIAL_PATH = DATA_DIR / "social_post_drafts.json"
VIDEO_PATH = DATA_DIR / "short_video_script_drafts.json"
OUTPUT_PATH = DATA_DIR / "public_material_review_queue.json"
TAIPEI_TZ = timezone(timedelta(hours=8))


def now_taipei() -> str:
    return datetime.now(TAIPEI_TZ).isoformat(timespec="seconds")


def read_json(path: Path, fallback: Any) -> Any:
    if not path.exists() or path.stat().st_size == 0:
        return fallback
    return json.loads(path.read_text(encoding="utf-8"))


def build_public_material_review_queue(
    social_records: list[dict[str, Any]] | None = None,
    video_records: list[dict[str, Any]] | None = None,
) -> dict[str, Any]:
    social_source = social_records if social_records is not None else read_json(SOCIAL_PATH, [])
    video_source = video_records if video_records is not None else read_json(VIDEO_PATH, [])
    items: list[dict[str, Any]] = []

    for index, item in enumerate(social_source[:3], start=1):
        items.append(
            {
                "review_id": f"public-review-social-{index:03d}",
                "item_type": "social_post",
                "title": item.get("headline") or item.get("issue_title") or "待命名社群草稿",
                "risk_level": "medium",
                "review_status": "needs_review",
                "evidence_status": "needs_source_check",
                "source_id": item.get("post_id", "待補"),
                "required_action": "人工確認來源、語氣、法遵與平台適用性。",
                "notes": "未通過人工審核，不可公開使用。",
            }
        )

    for index, item in enumerate(video_source[:2], start=1):
        items.append(
            {
                "review_id": f"public-review-video-{index:03d}",
                "item_type": "short_video_script",
                "title": item.get("title") or item.get("issue_title") or "待命名短影音腳本",
                "risk_level": "medium",
                "review_status": "needs_review",
                "evidence_status": "needs_source_check",
                "source_id": item.get("script_id", "待補"),
                "required_action": "人工確認旁白、畫面、來源與是否適合拍攝。",
                "notes": "未通過人工審核，不可公開使用。",
            }
        )

    return {
        "generated_at": now_taipei(),
        "public_use_status": "internal_public_review_queue",
        "notes": [
            "Internal public material review queue only.",
            "Materials are not approved until human review is complete.",
            "Manual publishing only.",
        ],
        "items": items,
    }


def write_public_material_review_queue(output_path: Path = OUTPUT_PATH) -> dict[str, Any]:
    result = build_public_material_review_queue()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    result = write_public_material_review_queue()
    print(f"Wrote {len(result['items'])} public review items to {OUTPUT_PATH.relative_to(ROOT)}")

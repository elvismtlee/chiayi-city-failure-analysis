from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "dashboard" / "data"
REVIEW_PATH = DATA_DIR / "public_material_review_queue.json"
OUTPUT_PATH = DATA_DIR / "approved_materials_sample.json"
TAIPEI_TZ = timezone(timedelta(hours=8))


def now_taipei() -> str:
    return datetime.now(TAIPEI_TZ).isoformat(timespec="seconds")


def read_json(path: Path, fallback: Any) -> Any:
    if not path.exists() or path.stat().st_size == 0:
        return fallback
    return json.loads(path.read_text(encoding="utf-8"))


def build_approved_materials_sample(review_queue: dict[str, Any] | None = None) -> dict[str, Any]:
    source = review_queue if review_queue is not None else read_json(REVIEW_PATH, {"items": []})
    queue_items = source.get("items", []) if isinstance(source, dict) else []
    approved_items = [item for item in queue_items if item.get("review_status") == "approved"]
    materials = [
        {
            "material_id": f"approved-{index:03d}",
            "item_type": item.get("item_type", "material"),
            "title": item.get("title", "待命名素材"),
            "approved_at": now_taipei(),
            "approved_by": "manual_reviewer",
            "source_files": ["dashboard/data/public_material_review_queue.json"],
            "public_use_notes": "Approved sample only; final publishing remains manual.",
        }
        for index, item in enumerate(approved_items, start=1)
    ]
    return {
        "generated_at": now_taipei(),
        "public_use_status": "internal_approved_materials_sample",
        "notes": [
            "Approved materials sample only.",
            "Manual publishing only.",
            "Keep evidence and review notes before public use.",
        ],
        "items": materials,
    }


def write_approved_materials_sample(output_path: Path = OUTPUT_PATH) -> dict[str, Any]:
    result = build_approved_materials_sample()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    result = write_approved_materials_sample()
    print(f"Wrote {len(result['items'])} approved material samples to {OUTPUT_PATH.relative_to(ROOT)}")

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "dashboard" / "data"
OUTPUT_PATH = DATA_DIR / "daily_execution_list.json"
TAIPEI_TZ = timezone(timedelta(hours=8))

DEFAULT_TASKS = [
    {
        "priority": "P1",
        "task": "檢查 health check 與 command center warnings",
        "estimated_minutes": 10,
        "status": "todo",
        "related_dashboard": "health-check.html",
        "notes": "先確認本地資料檔與頁面狀態，再進入審核。",
    },
    {
        "priority": "P1",
        "task": "審核 public review queue 中的待審素材",
        "estimated_minutes": 30,
        "status": "todo",
        "related_dashboard": "public-review.html",
        "notes": "未通過人工審核前不可公開使用。",
    },
    {
        "priority": "P2",
        "task": "整理隔日可手動發布的 approved materials",
        "estimated_minutes": 20,
        "status": "todo",
        "related_dashboard": "approved-materials.html",
        "notes": "approved 仍代表人工手動發布，不代表自動發布。",
    },
]


def now_taipei() -> str:
    return datetime.now(TAIPEI_TZ).isoformat(timespec="seconds")


def build_daily_execution_list(tasks: list[dict[str, Any]] | None = None) -> dict[str, Any]:
    return {
        "generated_at": now_taipei(),
        "public_use_status": "internal_daily_execution",
        "notes": [
            "Internal daily execution list only.",
            "No automatic publishing.",
            "No external platform API calls.",
        ],
        "items": tasks if tasks is not None else DEFAULT_TASKS,
    }


def write_daily_execution_list(output_path: Path = OUTPUT_PATH) -> dict[str, Any]:
    result = build_daily_execution_list()
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    result = write_daily_execution_list()
    print(f"Wrote {len(result['items'])} daily execution items to {OUTPUT_PATH.relative_to(ROOT)}")

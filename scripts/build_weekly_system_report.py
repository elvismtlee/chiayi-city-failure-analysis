from __future__ import annotations

import json
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "dashboard" / "data"
OUTPUT_FILE = DATA_DIR / "weekly_system_report.json"

SOURCE_FILES = [
    "dashboard/data/command_center_overview.json",
    "dashboard/data/dashboard_health_check.json",
    "dashboard/data/public_material_review_queue.json",
    "dashboard/data/approved_materials_sample.json",
]


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def read_json(root: Path, relative: str) -> tuple[Any | None, str | None]:
    path = root / relative
    if not path.exists():
        return None, "missing"
    if path.stat().st_size == 0:
        return None, "empty"
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except json.JSONDecodeError:
        return None, "invalid_json"


def count_records(data: Any) -> int:
    if isinstance(data, list):
        return len(data)
    if isinstance(data, dict):
        for key in ("items", "records", "materials", "queue"):
            value = data.get(key)
            if isinstance(value, list):
                return len(value)
        return 1 if data else 0
    return 0


def week_range(today: date | None = None) -> tuple[str, str]:
    current = today or date.today()
    start = current - timedelta(days=current.weekday())
    end = start + timedelta(days=6)
    return start.isoformat(), end.isoformat()


def build_weekly_report(root: Path = ROOT) -> dict[str, Any]:
    warnings: list[str] = []
    source_files: list[str] = []
    loaded: dict[str, Any] = {}

    for relative in SOURCE_FILES:
        source_files.append(relative)
        data, issue = read_json(root, relative)
        if issue:
            warnings.append(f"{issue.replace('_', ' ').title()}: {relative}")
        else:
            loaded[relative] = data

    overview = loaded.get("dashboard/data/command_center_overview.json", {})
    health = loaded.get("dashboard/data/dashboard_health_check.json", {})
    review_queue = loaded.get("dashboard/data/public_material_review_queue.json")
    approved_materials = loaded.get("dashboard/data/approved_materials_sample.json")

    pipeline_items = overview.get("pipeline_status", []) if isinstance(overview, dict) else []
    pipeline_summary = {
        "available": sum(1 for item in pipeline_items if item.get("status") == "available"),
        "missing": sum(1 for item in pipeline_items if item.get("status") == "missing"),
        "empty": sum(1 for item in pipeline_items if item.get("status") == "empty"),
        "total": len(pipeline_items),
    }
    review_backlog_summary = overview.get("review_backlog", {}) if isinstance(overview, dict) else {}
    completed_outputs = {
        "approved_materials_count": count_records(approved_materials),
        "public_review_queue_count": count_records(review_queue),
    }

    health_status = health.get("status") if isinstance(health, dict) else None
    if not loaded:
        system_status = "incomplete"
    elif warnings or health_status == "needs_attention" or pipeline_summary["missing"]:
        system_status = "needs_attention"
    else:
        system_status = "ok"

    recommended_next_actions = [
        "Resolve missing or empty dashboard inputs.",
        "Review public material queue manually before public use.",
        "Confirm approved materials retain approval notes.",
        "Prepare manual publishing only after final human review.",
    ]

    start, end = week_range()
    return {
        "report_id": f"weekly-system-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "week_start": start,
        "week_end": end,
        "generated_at": now_iso(),
        "source_files": source_files,
        "system_status": system_status,
        "pipeline_summary": pipeline_summary,
        "review_backlog_summary": review_backlog_summary,
        "completed_outputs": completed_outputs,
        "warnings": warnings,
        "recommended_next_actions": recommended_next_actions,
        "public_use_status": "internal_weekly_system_report",
        "notes": [
            "internal dashboard / needs human review / manual publishing only",
            "Internal weekly system report only.",
            "Not public campaign material.",
            "Needs human review and manual publishing only.",
        ],
    }


def main() -> dict[str, Any]:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    report = build_weekly_report(ROOT)
    OUTPUT_FILE.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    return report


if __name__ == "__main__":
    main()

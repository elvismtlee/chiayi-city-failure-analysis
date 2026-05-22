from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "dashboard" / "data"
OUTPUT_FILE = DATA_DIR / "command_center_overview.json"
TAIPEI_TZ = timezone(timedelta(hours=8))

PIPELINE_SOURCES = [
    ("minutes review", "cycc_minutes_review_queue.json", "Review queued meeting records."),
    ("reviewed minutes sample", "cycc_minutes_reviewed_sample.json", "Use reviewed samples to improve extraction rules."),
    ("issue candidates", "cycc_minutes_issue_candidates.json", "Review and approve issue candidates."),
    ("weekly summary", "weekly_summary_draft.json", "Human review before publishing."),
    ("policy drafts", "policy_draft_candidates.json", "Review policy language and evidence."),
    ("social drafts", "social_post_drafts.json", "Manual review and manual publishing only."),
    ("video scripts", "short_video_script_drafts.json", "Human review before filming."),
    ("filming checklists", "filming_checklists.json", "Confirm location, message, and safety details."),
    ("content schedule", "content_schedule.json", "Confirm schedule before manual publishing."),
    ("daily execution list", "daily_execution_list.json", "Use as internal daily work list."),
    ("public review queue", "public_material_review_queue.json", "Human approval required before public use."),
    ("approved materials", "approved_materials_sample.json", "Keep approval notes with each output."),
]


def now_iso() -> str:
    return datetime.now(TAIPEI_TZ).isoformat(timespec="seconds")


def read_json(path: Path) -> tuple[Any | None, str | None]:
    if not path.exists():
        return None, "missing"
    if path.stat().st_size == 0:
        return None, "empty"
    try:
        return json.loads(path.read_text(encoding="utf-8")), None
    except json.JSONDecodeError:
        return None, "invalid_json"


def count_records(data: Any) -> int:
    if data is None:
        return 0
    if isinstance(data, list):
        return len(data)
    if isinstance(data, dict):
        for key in ("items", "records", "drafts", "materials", "queue", "actions", "candidates"):
            value = data.get(key)
            if isinstance(value, list):
                return len(value)
        return 1 if data else 0
    return 0


def build_overview(root: Path = ROOT) -> dict[str, Any]:
    data_dir = root / "dashboard" / "data"
    warnings: list[str] = []
    source_files: list[str] = []
    pipeline_status: list[dict[str, Any]] = []
    key_counts: dict[str, int] = {}

    for name, filename, next_step in PIPELINE_SOURCES:
        path = data_dir / filename
        source_files.append(str(path.relative_to(root)).replace("\\", "/"))
        data, issue = read_json(path)
        record_count = count_records(data)

        if issue == "missing":
            status = "missing"
            warnings.append(f"Missing source file: dashboard/data/{filename}")
        elif issue == "empty":
            status = "empty"
            warnings.append(f"Empty source file: dashboard/data/{filename}")
        elif issue == "invalid_json":
            status = "empty"
            warnings.append(f"Invalid JSON source file: dashboard/data/{filename}")
        else:
            status = "available"

        pipeline_status.append(
            {
                "name": name,
                "status": status,
                "record_count": record_count,
                "source_file": f"dashboard/data/{filename}",
                "next_step": next_step,
            }
        )
        key_counts[name.replace(" ", "_")] = record_count

    review_backlog = {
        name: key_counts.get(label.replace(" ", "_"), 0)
        for name, label in {
            "minutes_review": "minutes review",
            "issue_candidates": "issue candidates",
            "public_review": "public review queue",
        }.items()
    }

    next_actions = [
        "Review missing upstream files before relying on the overview.",
        "Confirm public review queue items with a human reviewer.",
        "Move only reviewed materials into approved materials.",
        "Use manual publishing only after final human approval.",
    ]

    return {
        "overview_id": f"command-center-{datetime.now(TAIPEI_TZ).strftime('%Y%m%d%H%M%S')}",
        "generated_at": now_iso(),
        "source_files": source_files,
        "pipeline_status": pipeline_status,
        "key_counts": key_counts,
        "review_backlog": review_backlog,
        "next_actions": next_actions,
        "warnings": warnings,
        "public_use_status": "internal_command_center",
        "notes": [
            "internal dashboard / needs human review / manual publishing only",
            "Internal dashboard only.",
            "Needs human review before any public use.",
            "Manual publishing only; no automatic posting or platform API calls.",
            "This command center is not official public data.",
        ],
    }


def main() -> dict[str, Any]:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    overview = build_overview(ROOT)
    OUTPUT_FILE.write_text(json.dumps(overview, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return overview


if __name__ == "__main__":
    main()

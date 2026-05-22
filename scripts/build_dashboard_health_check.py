from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "dashboard" / "data"
OUTPUT_FILE = DATA_DIR / "dashboard_health_check.json"

IMPORTANT_JSON = [
    "dashboard/data/cycc_minutes_review_queue.json",
    "dashboard/data/cycc_minutes_reviewed_sample.json",
    "dashboard/data/cycc_minutes_issue_candidates.json",
    "dashboard/data/weekly_summary_draft.json",
    "dashboard/data/policy_draft_candidates.json",
    "dashboard/data/social_post_drafts.json",
    "dashboard/data/short_video_script_drafts.json",
    "dashboard/data/filming_checklists.json",
    "dashboard/data/content_schedule.json",
    "dashboard/data/daily_execution_list.json",
    "dashboard/data/public_material_review_queue.json",
    "dashboard/data/approved_materials_sample.json",
    "dashboard/data/command_center_overview.json",
    "dashboard/data/dashboard_health_check.json",
    "dashboard/data/weekly_system_report.json",
    "dashboard/data/site_map.json",
]

IMPORTANT_PAGES = [
    "dashboard/minutes-review.html",
    "dashboard/minutes-issues.html",
    "dashboard/weekly-summary.html",
    "dashboard/policy-drafts.html",
    "dashboard/social-drafts.html",
    "dashboard/video-scripts.html",
    "dashboard/filming-checklists.html",
    "dashboard/content-schedule.html",
    "dashboard/daily-execution.html",
    "dashboard/public-review.html",
    "dashboard/approved-materials.html",
    "dashboard/command-center.html",
    "dashboard/health-check.html",
    "dashboard/weekly-system-report.html",
]

IMPORTANT_JS = [
    "dashboard/shared-nav.js",
    "dashboard/command-center.js",
    "dashboard/health-check.js",
    "dashboard/weekly-system-report.js",
]

NAV_LABELS = ["總控台", "健康檢查", "每週系統報告"]


def now_iso() -> str:
    return datetime.now(timezone.utc).astimezone().isoformat(timespec="seconds")


def parse_json(path: Path) -> bool:
    json.loads(path.read_text(encoding="utf-8"))
    return True


def check_file(root: Path, relative: str, invalid_json_files: list[str]) -> dict[str, Any]:
    path = root / relative
    exists = path.exists()
    is_empty = exists and path.stat().st_size == 0
    is_valid_json = None
    if exists and not is_empty and path.suffix == ".json":
        try:
            is_valid_json = parse_json(path)
        except json.JSONDecodeError:
            is_valid_json = False
            invalid_json_files.append(relative)
    return {
        "file": relative,
        "exists": exists,
        "empty": is_empty,
        "valid_json": is_valid_json,
    }


def build_health_check(root: Path = ROOT) -> dict[str, Any]:
    checked_targets = IMPORTANT_JSON + IMPORTANT_PAGES + IMPORTANT_JS
    invalid_json_files: list[str] = []
    checked_files = [check_file(root, target, invalid_json_files) for target in checked_targets]
    missing_files = [item["file"] for item in checked_files if not item["exists"]]
    empty_files = [item["file"] for item in checked_files if item["empty"]]

    page_checks = [
        {
            "page": page,
            "exists": (root / page).exists(),
            "empty": (root / page).exists() and (root / page).stat().st_size == 0,
        }
        for page in IMPORTANT_PAGES
    ]

    site_map_path = root / "dashboard" / "data" / "site_map.json"
    shared_nav_path = root / "dashboard" / "shared-nav.js"
    site_map_text = site_map_path.read_text(encoding="utf-8") if site_map_path.exists() else ""
    shared_nav_text = shared_nav_path.read_text(encoding="utf-8") if shared_nav_path.exists() else ""
    nav_checks = [
        {
            "name": label,
            "in_site_map": label in site_map_text,
            "in_shared_nav": label in shared_nav_text,
        }
        for label in NAV_LABELS
    ]

    warnings = []
    warnings.extend(f"Missing file: {path}" for path in missing_files)
    warnings.extend(f"Empty file: {path}" for path in empty_files)
    warnings.extend(f"Invalid JSON file: {path}" for path in invalid_json_files)
    warnings.extend(
        f"Navigation entry missing: {item['name']}"
        for item in nav_checks
        if not item["in_site_map"] or not item["in_shared_nav"]
    )

    status = "ok" if not warnings else "needs_attention"
    return {
        "check_id": f"dashboard-health-{datetime.now().strftime('%Y%m%d%H%M%S')}",
        "generated_at": now_iso(),
        "checked_files": checked_files,
        "missing_files": missing_files,
        "empty_files": empty_files,
        "invalid_json_files": invalid_json_files,
        "page_checks": page_checks,
        "nav_checks": nav_checks,
        "warnings": warnings,
        "status": status,
        "public_use_status": "internal_health_check",
        "notes": [
            "internal dashboard / needs human review / manual publishing only",
            "Internal dashboard health check only.",
            "Checks local files only and does not call external APIs.",
            "This does not mean content has completed human review.",
        ],
    }


def main() -> dict[str, Any]:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    result = build_health_check(ROOT)
    OUTPUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    return result


if __name__ == "__main__":
    main()

from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "dashboard" / "data"
OUTPUT_FILE = DATA_DIR / "dashboard_health_check.json"
TAIPEI_TZ = timezone(timedelta(hours=8))

IMPORTANT_JSON = [
    "dashboard/data/open_data_url_inventory.json",
    "dashboard/data/open_data_url_review_queue.json",
    "dashboard/data/open_data_readiness_report.json",
    "dashboard/data/open_data_top10_review_tasks.json",
    "dashboard/data/open_data_crawler_spec_drafts.json",
    "dashboard/data/open_data_human_review_workbook.json",
    "dashboard/data/open_data_engineering_review_checklist.json",
    "dashboard/data/open_data_review_session_planner.json",
    "dashboard/data/open_data_review_evidence_pack.json",
    "dashboard/data/open_data_manual_review_result_template.json",
    "dashboard/data/open_data_manual_review_sop.json",
    "dashboard/data/open_data_manual_review_execution_packets.json",
    "dashboard/data/open_data_manual_review_result_patch_drafts.json",
    "dashboard/data/open_data_day1_sample_manual_review_results.json",
    "dashboard/data/open_data_day1_manual_review_form_draft.json",
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
    "dashboard/open-data-inventory.html",
    "dashboard/open-data-review.html",
    "dashboard/open-data-readiness.html",
    "dashboard/open-data-top10-tasks.html",
    "dashboard/open-data-crawler-specs.html",
    "dashboard/open-data-human-review.html",
    "dashboard/open-data-engineering-review.html",
    "dashboard/open-data-review-sessions.html",
    "dashboard/open-data-review-evidence.html",
    "dashboard/open-data-manual-review-results.html",
    "dashboard/open-data-manual-review-sop.html",
    "dashboard/open-data-manual-review-packets.html",
    "dashboard/open-data-manual-review-patches.html",
    "dashboard/open-data-day1-sample-results.html",
    "dashboard/open-data-day1-review-form.html",
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
    "dashboard/site-pages.js",
    "dashboard/command-center.js",
    "dashboard/health-check.js",
    "dashboard/weekly-system-report.js",
    "dashboard/content-schedule.js",
    "dashboard/daily-execution.js",
    "dashboard/public-review.js",
    "dashboard/approved-materials.js",
]

IMPORTANT_DOCS = [
    "docs/open_data_manual_review_packets/day_1_packet.md",
    "docs/open_data_manual_review_packets/day_2_packet.md",
    "docs/open_data_manual_review_packets/day_3_packet.md",
    "docs/open_data_manual_review_patch_drafts/day_1_patch_drafts.md",
    "docs/open_data_manual_review_patch_drafts/day_2_patch_drafts.md",
    "docs/open_data_manual_review_patch_drafts/day_3_patch_drafts.md",
    "docs/open_data_day1_sample_results/day_1_sample_manual_review_results.md",
    "docs/open_data_day1_manual_review_forms/day_1_manual_review_form_draft.md",
]

NAV_LABELS = [
    "開放資料盤點",
    "官方資料審核",
    "Readiness評分",
    "Top10審核任務",
    "Crawler規格草稿",
    "人工審核工作簿",
    "工程審查清單",
    "人工審核執行",
    "審核證據包",
    "審核結果輸入",
    "人工審核 SOP",
    "人工審核工作包",
    "回填 Patch 草稿",
    "Day1填寫範例",
    "Day1審核表單",
    "內容排程",
    "每日執行",
    "公開審核",
    "已核准素材",
    "總控台",
    "健康檢查",
    "每週系統報告",
]


def now_iso() -> str:
    return datetime.now(TAIPEI_TZ).isoformat(timespec="seconds")


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
    checked_targets = IMPORTANT_JSON + IMPORTANT_PAGES + IMPORTANT_JS + IMPORTANT_DOCS
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

    data_status_checks = []
    open_data_inventory_path = root / "dashboard" / "data" / "open_data_url_inventory.json"
    if open_data_inventory_path.exists() and open_data_inventory_path.stat().st_size > 0:
        try:
            open_data_inventory = json.loads(open_data_inventory_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            open_data_inventory = {}
        data_status_checks.append(
            {
                "name": "open_data_url_inventory",
                "path": "dashboard/data/open_data_url_inventory.json",
                "expected_public_use_status": "internal_url_inventory",
                "actual_public_use_status": open_data_inventory.get("public_use_status"),
                "ok": open_data_inventory.get("public_use_status") == "internal_url_inventory",
            }
        )
    open_data_review_path = root / "dashboard" / "data" / "open_data_url_review_queue.json"
    if open_data_review_path.exists() and open_data_review_path.stat().st_size > 0:
        try:
            open_data_review_queue = json.loads(open_data_review_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            open_data_review_queue = {}
        data_status_checks.append(
            {
                "name": "open_data_url_review_queue",
                "path": "dashboard/data/open_data_url_review_queue.json",
                "expected_public_use_status": "internal_url_review_queue",
                "actual_public_use_status": open_data_review_queue.get("public_use_status"),
                "ok": open_data_review_queue.get("public_use_status") == "internal_url_review_queue",
            }
        )
    open_data_readiness_path = root / "dashboard" / "data" / "open_data_readiness_report.json"
    if open_data_readiness_path.exists() and open_data_readiness_path.stat().st_size > 0:
        try:
            open_data_readiness_report = json.loads(open_data_readiness_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            open_data_readiness_report = {}
        data_status_checks.append(
            {
                "name": "open_data_readiness_report",
                "path": "dashboard/data/open_data_readiness_report.json",
                "expected_public_use_status": "internal_readiness_report",
                "actual_public_use_status": open_data_readiness_report.get("public_use_status"),
                "ok": open_data_readiness_report.get("public_use_status") == "internal_readiness_report",
            }
        )
    open_data_top10_path = root / "dashboard" / "data" / "open_data_top10_review_tasks.json"
    if open_data_top10_path.exists() and open_data_top10_path.stat().st_size > 0:
        try:
            open_data_top10_tasks = json.loads(open_data_top10_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            open_data_top10_tasks = {}
        data_status_checks.append(
            {
                "name": "open_data_top10_review_tasks",
                "path": "dashboard/data/open_data_top10_review_tasks.json",
                "expected_public_use_status": "internal_top10_review_tasks",
                "actual_public_use_status": open_data_top10_tasks.get("public_use_status"),
                "ok": open_data_top10_tasks.get("public_use_status") == "internal_top10_review_tasks",
            }
        )
    open_data_crawler_specs_path = root / "dashboard" / "data" / "open_data_crawler_spec_drafts.json"
    if open_data_crawler_specs_path.exists() and open_data_crawler_specs_path.stat().st_size > 0:
        try:
            open_data_crawler_specs = json.loads(open_data_crawler_specs_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            open_data_crawler_specs = {}
        data_status_checks.append(
            {
                "name": "open_data_crawler_spec_drafts",
                "path": "dashboard/data/open_data_crawler_spec_drafts.json",
                "expected_public_use_status": "internal_crawler_spec_drafts",
                "actual_public_use_status": open_data_crawler_specs.get("public_use_status"),
                "ok": open_data_crawler_specs.get("public_use_status") == "internal_crawler_spec_drafts",
            }
        )
    open_data_human_review_path = root / "dashboard" / "data" / "open_data_human_review_workbook.json"
    if open_data_human_review_path.exists() and open_data_human_review_path.stat().st_size > 0:
        try:
            open_data_human_review = json.loads(open_data_human_review_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            open_data_human_review = {}
        data_status_checks.append(
            {
                "name": "open_data_human_review_workbook",
                "path": "dashboard/data/open_data_human_review_workbook.json",
                "expected_public_use_status": "internal_human_review_workbook",
                "actual_public_use_status": open_data_human_review.get("public_use_status"),
                "ok": open_data_human_review.get("public_use_status") == "internal_human_review_workbook",
            }
        )
    open_data_engineering_review_path = root / "dashboard" / "data" / "open_data_engineering_review_checklist.json"
    if open_data_engineering_review_path.exists() and open_data_engineering_review_path.stat().st_size > 0:
        try:
            open_data_engineering_review = json.loads(open_data_engineering_review_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            open_data_engineering_review = {}
        data_status_checks.append(
            {
                "name": "open_data_engineering_review_checklist",
                "path": "dashboard/data/open_data_engineering_review_checklist.json",
                "expected_public_use_status": "internal_engineering_review_checklist",
                "actual_public_use_status": open_data_engineering_review.get("public_use_status"),
                "ok": open_data_engineering_review.get("public_use_status") == "internal_engineering_review_checklist",
            }
        )
    open_data_review_sessions_path = root / "dashboard" / "data" / "open_data_review_session_planner.json"
    if open_data_review_sessions_path.exists() and open_data_review_sessions_path.stat().st_size > 0:
        try:
            open_data_review_sessions = json.loads(open_data_review_sessions_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            open_data_review_sessions = {}
        data_status_checks.append(
            {
                "name": "open_data_review_session_planner",
                "path": "dashboard/data/open_data_review_session_planner.json",
                "expected_public_use_status": "internal_review_session_planner",
                "actual_public_use_status": open_data_review_sessions.get("public_use_status"),
                "ok": open_data_review_sessions.get("public_use_status") == "internal_review_session_planner",
            }
        )
    open_data_review_evidence_path = root / "dashboard" / "data" / "open_data_review_evidence_pack.json"
    if open_data_review_evidence_path.exists() and open_data_review_evidence_path.stat().st_size > 0:
        try:
            open_data_review_evidence = json.loads(open_data_review_evidence_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            open_data_review_evidence = {}
        data_status_checks.append(
            {
                "name": "open_data_review_evidence_pack",
                "path": "dashboard/data/open_data_review_evidence_pack.json",
                "expected_public_use_status": "internal_review_evidence_pack",
                "actual_public_use_status": open_data_review_evidence.get("public_use_status"),
                "ok": open_data_review_evidence.get("public_use_status") == "internal_review_evidence_pack",
            }
        )
    open_data_manual_review_result_path = root / "dashboard" / "data" / "open_data_manual_review_result_template.json"
    if open_data_manual_review_result_path.exists() and open_data_manual_review_result_path.stat().st_size > 0:
        try:
            open_data_manual_review_result = json.loads(open_data_manual_review_result_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            open_data_manual_review_result = {}
        data_status_checks.append(
            {
                "name": "open_data_manual_review_result_template",
                "path": "dashboard/data/open_data_manual_review_result_template.json",
                "expected_public_use_status": "internal_manual_review_result_template",
                "actual_public_use_status": open_data_manual_review_result.get("public_use_status"),
                "ok": open_data_manual_review_result.get("public_use_status") == "internal_manual_review_result_template",
            }
        )
    open_data_manual_review_sop_path = root / "dashboard" / "data" / "open_data_manual_review_sop.json"
    if open_data_manual_review_sop_path.exists() and open_data_manual_review_sop_path.stat().st_size > 0:
        try:
            open_data_manual_review_sop = json.loads(open_data_manual_review_sop_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            open_data_manual_review_sop = {}
        data_status_checks.append(
            {
                "name": "open_data_manual_review_sop",
                "path": "dashboard/data/open_data_manual_review_sop.json",
                "expected_public_use_status": "internal_manual_review_sop",
                "actual_public_use_status": open_data_manual_review_sop.get("public_use_status"),
                "ok": open_data_manual_review_sop.get("public_use_status") == "internal_manual_review_sop",
            }
        )
    open_data_manual_review_packets_path = root / "dashboard" / "data" / "open_data_manual_review_execution_packets.json"
    if open_data_manual_review_packets_path.exists() and open_data_manual_review_packets_path.stat().st_size > 0:
        try:
            open_data_manual_review_packets = json.loads(open_data_manual_review_packets_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            open_data_manual_review_packets = {}
        data_status_checks.append(
            {
                "name": "open_data_manual_review_execution_packets",
                "path": "dashboard/data/open_data_manual_review_execution_packets.json",
                "expected_public_use_status": "internal_manual_review_execution_packets",
                "actual_public_use_status": open_data_manual_review_packets.get("public_use_status"),
                "ok": open_data_manual_review_packets.get("public_use_status") == "internal_manual_review_execution_packets",
            }
        )
    open_data_manual_review_patch_drafts_path = root / "dashboard" / "data" / "open_data_manual_review_result_patch_drafts.json"
    if open_data_manual_review_patch_drafts_path.exists() and open_data_manual_review_patch_drafts_path.stat().st_size > 0:
        try:
            open_data_manual_review_patch_drafts = json.loads(open_data_manual_review_patch_drafts_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            open_data_manual_review_patch_drafts = {}
        data_status_checks.append(
            {
                "name": "open_data_manual_review_result_patch_drafts",
                "path": "dashboard/data/open_data_manual_review_result_patch_drafts.json",
                "expected_public_use_status": "internal_manual_review_result_patch_drafts",
                "actual_public_use_status": open_data_manual_review_patch_drafts.get("public_use_status"),
                "ok": open_data_manual_review_patch_drafts.get("public_use_status") == "internal_manual_review_result_patch_drafts",
            }
        )
    open_data_day1_sample_results_path = root / "dashboard" / "data" / "open_data_day1_sample_manual_review_results.json"
    if open_data_day1_sample_results_path.exists() and open_data_day1_sample_results_path.stat().st_size > 0:
        try:
            open_data_day1_sample_results = json.loads(open_data_day1_sample_results_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            open_data_day1_sample_results = {}
        data_status_checks.append(
            {
                "name": "open_data_day1_sample_manual_review_results",
                "path": "dashboard/data/open_data_day1_sample_manual_review_results.json",
                "expected_public_use_status": "internal_day1_sample_manual_review_results",
                "actual_public_use_status": open_data_day1_sample_results.get("public_use_status"),
                "ok": open_data_day1_sample_results.get("public_use_status") == "internal_day1_sample_manual_review_results",
            }
        )
    open_data_day1_review_form_path = root / "dashboard" / "data" / "open_data_day1_manual_review_form_draft.json"
    if open_data_day1_review_form_path.exists() and open_data_day1_review_form_path.stat().st_size > 0:
        try:
            open_data_day1_review_form = json.loads(open_data_day1_review_form_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            open_data_day1_review_form = {}
        data_status_checks.append(
            {
                "name": "open_data_day1_manual_review_form_draft",
                "path": "dashboard/data/open_data_day1_manual_review_form_draft.json",
                "expected_public_use_status": "internal_day1_manual_review_form_draft",
                "actual_public_use_status": open_data_day1_review_form.get("public_use_status"),
                "ok": open_data_day1_review_form.get("public_use_status") == "internal_day1_manual_review_form_draft",
            }
        )

    warnings = []
    warnings.extend(f"Missing file: {path}" for path in missing_files)
    warnings.extend(f"Empty file: {path}" for path in empty_files)
    warnings.extend(f"Invalid JSON file: {path}" for path in invalid_json_files)
    warnings.extend(
        f"Navigation entry missing: {item['name']}"
        for item in nav_checks
        if not item["in_site_map"] or not item["in_shared_nav"]
    )
    warnings.extend(
        f"Unexpected public_use_status: {item['path']}"
        for item in data_status_checks
        if not item["ok"]
    )

    status = "ok" if not warnings else "needs_attention"
    return {
        "check_id": f"dashboard-health-{datetime.now(TAIPEI_TZ).strftime('%Y%m%d%H%M%S')}",
        "generated_at": now_iso(),
        "checked_files": checked_files,
        "missing_files": missing_files,
        "empty_files": empty_files,
        "invalid_json_files": invalid_json_files,
        "page_checks": page_checks,
        "nav_checks": nav_checks,
        "data_status_checks": data_status_checks,
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
    OUTPUT_FILE.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


if __name__ == "__main__":
    main()

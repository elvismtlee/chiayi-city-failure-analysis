from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = ROOT / "dashboard" / "data" / "open_data_review_session_planner.json"
OUTPUT_PATH = ROOT / "dashboard" / "data" / "open_data_review_evidence_pack.json"
TAIPEI_TZ = timezone(timedelta(hours=8))

REQUIRED_EVIDENCE_ITEMS = [
    "source_url",
    "page_title_or_dataset_title",
    "official_owner",
    "official_domain_or_platform",
    "license_or_terms_summary",
    "available_format",
    "update_cadence_observed",
    "personal_data_risk_observed",
    "private_complaint_risk_observed",
    "reviewer_notes",
    "reviewed_at",
]

EVIDENCE_FILE_PLACEHOLDERS = [
    "source_page_screenshot_placeholder",
    "license_terms_screenshot_placeholder",
    "format_or_download_link_note",
    "risk_review_note",
    "reviewer_summary_note",
]

ACCEPTANCE_CRITERIA = [
    "已人工開啟 source_url",
    "已記錄來源頁標題或 dataset title",
    "已確認官方來源",
    "已記錄授權或條款摘要",
    "已確認可用格式",
    "已確認個資風險",
    "已確認私人陳情全文風險",
    "已填寫 reviewer summary",
    "crawler_execution_allowed 仍為 false",
]


def now_iso() -> str:
    return datetime.now(TAIPEI_TZ).isoformat(timespec="seconds")


def load_source(path: Path = SOURCE_PATH) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_sessions(payload: dict) -> list[dict]:
    session_tasks = payload.get("session_tasks", [])
    if not isinstance(session_tasks, list):
        raise ValueError("Review session planner must contain a session_tasks list")
    if int(payload.get("total_count", 0)) != len(session_tasks):
        raise ValueError("Review session planner total_count does not match session_tasks length")
    if int(payload.get("source_checklist_count", 0)) != len(session_tasks):
        raise ValueError("Review session planner source_checklist_count does not match session_tasks length")
    if len(session_tasks) != 10:
        raise ValueError("Review session planner should currently contain 10 records")
    return session_tasks


def official_domain_or_platform(source_url: str) -> str:
    if "data.gov.tw" in source_url:
        return "data.gov.tw"
    if "chiayi.gov.tw" in source_url:
        return "chiayi.gov.tw"
    return "official_platform_to_confirm"


def reviewer_summary_template() -> str:
    return "\n".join(
        [
            "- 本筆來源是否為官方來源：",
            "- 授權或條款摘要：",
            "- 可用格式：",
            "- 更新頻率觀察：",
            "- 是否含個資：",
            "- 是否含私人陳情全文：",
            "- 是否需要 follow-up：",
            "- 審核者備註：",
        ]
    )


def evidence_blockers(task: dict) -> list[str]:
    blockers = ["尚未開始人工蒐集證據，不能更新 workbook 或 engineering checklist"]
    if str(task.get("topic_group", "")) == "complaints_service":
        blockers.append("complaints_service 需額外人工檢查私人陳情與個資風險")
    return blockers


def safety_notes(task: dict) -> str:
    notes = [
        "no live crawler",
        "no personal data",
        "no private complaint full text",
        "no auto publish",
        "review evidence pack draft only",
    ]
    if str(task.get("topic_group", "")) == "complaints_service":
        notes.append("complaints_service requires extra privacy review")
    return " / ".join(notes)


def build_evidence_pack(index: int, task: dict) -> dict:
    return {
        "evidence_pack_id": f"open-data-evidence-pack-{index + 1:02d}",
        "session_task_id": task["session_task_id"],
        "checklist_id": task["checklist_id"],
        "review_id": task["review_id"],
        "spec_id": task["spec_id"],
        "task_id": task["task_id"],
        "inventory_id": task["inventory_id"],
        "title": task["title"],
        "topic_group": task["topic_group"],
        "source_owner": task["source_owner"],
        "source_url": task["source_url"],
        "review_day": task["review_day"],
        "review_batch": task["review_batch"],
        "evidence_status": "not_started",
        "required_evidence_items": list(REQUIRED_EVIDENCE_ITEMS),
        "evidence_file_placeholders": list(EVIDENCE_FILE_PLACEHOLDERS),
        "source_identity_evidence": {
            "source_url_to_open": task["source_url"],
            "expected_source_owner": task["source_owner"],
            "expected_topic_group": task["topic_group"],
            "official_source_check": "not_checked",
        },
        "license_evidence": {
            "expected_license_status": "待人工核對原始來源授權",
            "license_terms_check": "not_checked",
            "license_summary": "",
        },
        "format_evidence": {
            "expected_fetch_method": task["proposed_fetch_method"],
            "expected_parser_type": task["proposed_parser_type"],
            "format_check": "not_checked",
            "format_notes": "",
        },
        "update_cadence_evidence": {
            "expected_review_day": task["review_day"],
            "update_cadence_check": "not_checked",
            "update_cadence_notes": "",
        },
        "personal_data_evidence": {
            "personal_data_check": "not_checked",
            "risk_notes": "",
        },
        "private_complaint_evidence": {
            "private_complaint_check": "not_checked",
            "risk_notes": "",
        },
        "reviewer_notes_required": True,
        "reviewer_summary_template": reviewer_summary_template(),
        "acceptance_criteria": list(ACCEPTANCE_CRITERIA),
        "evidence_blockers": evidence_blockers(task),
        "next_action": "collect_source_identity_evidence",
        "crawler_execution_allowed": False,
        "engineering_review_allowed": False,
        "human_approval_required": True,
        "no_live_crawler": True,
        "manual_review_required": True,
        "no_auto_publish": True,
        "no_personal_data": True,
        "safety_notes": safety_notes(task),
    }


def build_open_data_review_evidence_pack(
    source_path: Path = SOURCE_PATH,
    output_path: Path = OUTPUT_PATH,
) -> dict:
    payload = load_source(source_path)
    session_tasks = validate_sessions(payload)
    evidence_packs = [build_evidence_pack(index, task) for index, task in enumerate(session_tasks)]

    if any(item["crawler_execution_allowed"] for item in evidence_packs):
        raise ValueError("Evidence pack must never enable crawler execution")
    if any(item["engineering_review_allowed"] for item in evidence_packs):
        raise ValueError("Evidence pack must not enable engineering review")
    if any(item["evidence_status"] == "approved_for_crawling" for item in evidence_packs):
        raise ValueError("approved_for_crawling is not allowed")
    if any(item.get("live_crawler") for item in evidence_packs):
        raise ValueError("live_crawler is not allowed")
    if any(len(item["required_evidence_items"]) < 10 for item in evidence_packs):
        raise ValueError("Each evidence pack must contain at least 10 required evidence items")
    if any(len(item["evidence_file_placeholders"]) < 5 for item in evidence_packs):
        raise ValueError("Each evidence pack must contain at least 5 evidence file placeholders")
    if any(len(item["acceptance_criteria"]) < 8 for item in evidence_packs):
        raise ValueError("Each evidence pack must contain at least 8 acceptance criteria")

    review_days = Counter(item["review_day"] for item in evidence_packs)
    review_batches = Counter(item["review_batch"] for item in evidence_packs)
    topic_groups = Counter(item["topic_group"] for item in evidence_packs)
    evidence_status_counts = Counter(item["evidence_status"] for item in evidence_packs)
    engineering_review_allowed_count = sum(1 for item in evidence_packs if item["engineering_review_allowed"])

    result = {
        "generated_at": now_iso(),
        "public_use_status": "internal_review_evidence_pack",
        "source_session_count": len(session_tasks),
        "total_count": len(evidence_packs),
        "review_days": dict(sorted(review_days.items())),
        "review_batches": dict(sorted(review_batches.items())),
        "topic_groups": dict(sorted(topic_groups.items())),
        "evidence_status_counts": dict(sorted(evidence_status_counts.items())),
        "crawler_execution_allowed": False,
        "engineering_review_allowed_count": engineering_review_allowed_count,
        "no_live_crawler": True,
        "manual_review_required": True,
        "no_auto_publish": True,
        "no_personal_data": True,
        "evidence_packs": evidence_packs,
    }

    if result["total_count"] != 10:
        raise ValueError("Review evidence pack should currently contain 10 records")
    if result["source_session_count"] != 10:
        raise ValueError("Review evidence pack should currently come from 10 session tasks")
    if result["engineering_review_allowed_count"] != 0:
        raise ValueError("Review evidence pack must keep engineering_review_allowed_count at 0")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> dict:
    return build_open_data_review_evidence_pack()


if __name__ == "__main__":
    main()

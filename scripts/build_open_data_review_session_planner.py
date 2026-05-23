from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = ROOT / "dashboard" / "data" / "open_data_engineering_review_checklist.json"
OUTPUT_PATH = ROOT / "dashboard" / "data" / "open_data_review_session_planner.json"
TAIPEI_TZ = timezone(timedelta(hours=8))

DAY_ONE_LIMIT = 3
DAY_TWO_LIMIT = 7

BASE_ACTION_ITEMS = [
    "開啟 source_url",
    "截圖或記錄來源頁標題",
    "確認是否為官方來源",
    "確認授權或使用條款",
    "確認可下載或可閱讀格式",
    "檢查是否含個資",
    "檢查是否含私人陳情全文",
    "填寫 reviewer notes",
    "不執行 crawler",
]

BASE_EVIDENCE_FIELDS = [
    "source_url",
    "page_title_or_dataset_title",
    "official_owner",
    "license_or_terms_summary",
    "available_format",
    "update_cadence_observed",
    "personal_data_risk_observed",
    "private_complaint_risk_observed",
    "reviewer_notes",
    "reviewed_at",
]

BASE_COMPLETION_CRITERIA = [
    "source_url 已人工開啟",
    "官方來源已人工確認",
    "授權或條款已人工記錄",
    "格式已人工確認",
    "個資風險已人工確認",
    "私人陳情全文風險已人工確認",
    "reviewer_notes 已完成",
    "crawler_execution_allowed 仍為 false",
]


def now_iso() -> str:
    return datetime.now(TAIPEI_TZ).isoformat(timespec="seconds")


def load_source(path: Path = SOURCE_PATH) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_checklists(payload: dict) -> list[dict]:
    checklists = payload.get("checklists", [])
    if not isinstance(checklists, list):
        raise ValueError("Engineering review checklist must contain a checklists list")
    if int(payload.get("total_count", 0)) != len(checklists):
        raise ValueError("Engineering review checklist total_count does not match checklists length")
    if int(payload.get("source_workbook_count", 0)) != len(checklists):
        raise ValueError("Engineering review checklist source_workbook_count does not match checklists length")
    if len(checklists) != 10:
        raise ValueError("Engineering review checklist should currently contain 10 records")
    return checklists


def review_day_and_batch(index: int) -> tuple[str, str]:
    if index < DAY_ONE_LIMIT:
        return "day_1", "batch_1_high_priority"
    if index < DAY_TWO_LIMIT:
        return "day_2", "batch_2_standard"
    return "day_3", "batch_3_follow_up"


def estimated_minutes(topic_group: str) -> int:
    mapping = {
        "social_welfare": 30,
        "public_works_environment": 30,
        "traffic_parking": 25,
        "culture_events": 20,
        "complaints_service": 40,
    }
    return mapping.get(topic_group, 25)


def session_blockers(item: dict) -> list[str]:
    blockers = ["原始 engineering review checklist 尚未解除人工審核 gate"]
    if str(item.get("topic_group", "")) == "complaints_service":
        blockers.append("complaints_service 需加強私人陳情與個資風險人工檢查")
    return blockers


def reviewer_notes_template(item: dict) -> str:
    return (
        f"請記錄 {item['title']} 的官方來源確認、授權條款摘要、格式觀察、"
        "個資風險與私人陳情全文風險，並註記後續是否需要人工 follow-up。"
    )


def safety_notes(item: dict) -> str:
    notes = [
        "no live crawler",
        "no personal data",
        "no private complaint full text",
        "no auto publish",
        "manual review session planner only",
    ]
    if str(item.get("topic_group", "")) == "complaints_service":
        notes.append("complaints_service requires extra human privacy review")
    return " / ".join(notes)


def build_session_task(index: int, item: dict) -> dict:
    review_day, review_batch = review_day_and_batch(index)
    topic_group = str(item.get("topic_group", ""))
    return {
        "session_task_id": f"open-data-review-session-{index + 1:02d}",
        "checklist_id": item["checklist_id"],
        "review_id": item["review_id"],
        "spec_id": item["spec_id"],
        "task_id": item["task_id"],
        "inventory_id": item["inventory_id"],
        "title": item["title"],
        "topic_group": topic_group,
        "source_owner": item["source_owner"],
        "source_url": item["source_url"],
        "proposed_fetch_method": item["proposed_fetch_method"],
        "proposed_parser_type": item["proposed_parser_type"],
        "review_day": review_day,
        "review_batch": review_batch,
        "estimated_minutes": estimated_minutes(topic_group),
        "session_status": "not_started",
        "source_open_check": "not_checked",
        "official_source_check": "not_checked",
        "license_terms_check": "not_checked",
        "format_check": "not_checked",
        "personal_data_check": "not_checked",
        "private_complaint_check": "not_checked",
        "engineering_gate_check": "locked",
        "reviewer_action_items": list(BASE_ACTION_ITEMS),
        "evidence_to_record": list(BASE_EVIDENCE_FIELDS),
        "reviewer_notes_template": reviewer_notes_template(item),
        "completion_criteria": list(BASE_COMPLETION_CRITERIA),
        "next_action_after_session": "record_source_evidence",
        "session_blockers": session_blockers(item),
        "safety_notes": safety_notes(item),
        "crawler_execution_allowed": False,
        "engineering_review_allowed": False,
        "human_approval_required": True,
        "no_live_crawler": True,
        "manual_review_required": True,
        "no_auto_publish": True,
        "no_personal_data": True,
    }


def build_open_data_review_session_planner(
    source_path: Path = SOURCE_PATH,
    output_path: Path = OUTPUT_PATH,
) -> dict:
    payload = load_source(source_path)
    checklists = validate_checklists(payload)
    session_tasks = [build_session_task(index, item) for index, item in enumerate(checklists)]

    if any(item["crawler_execution_allowed"] for item in session_tasks):
        raise ValueError("Session planner must never enable crawler execution")
    if any(item["engineering_review_allowed"] for item in session_tasks):
        raise ValueError("Session planner must not enable engineering review")
    if any(item["session_status"] == "approved_for_crawling" for item in session_tasks):
        raise ValueError("approved_for_crawling is not allowed")
    if any(item["proposed_fetch_method"] == "live_crawler" for item in session_tasks):
        raise ValueError("live_crawler is not allowed")
    if any(len(item["reviewer_action_items"]) < 8 for item in session_tasks):
        raise ValueError("Each session task must contain at least 8 reviewer action items")
    if any(len(item["evidence_to_record"]) < 8 for item in session_tasks):
        raise ValueError("Each session task must contain at least 8 evidence fields")
    if any(len(item["completion_criteria"]) < 7 for item in session_tasks):
        raise ValueError("Each session task must contain at least 7 completion criteria")

    topic_groups = Counter(item["topic_group"] for item in session_tasks)
    review_days = Counter(item["review_day"] for item in session_tasks)
    review_batches = Counter(item["review_batch"] for item in session_tasks)
    session_status_counts = Counter(item["session_status"] for item in session_tasks)
    total_estimated_minutes = sum(int(item["estimated_minutes"]) for item in session_tasks)
    engineering_review_allowed_count = sum(1 for item in session_tasks if item["engineering_review_allowed"])

    result = {
        "generated_at": now_iso(),
        "public_use_status": "internal_review_session_planner",
        "source_checklist_count": len(checklists),
        "total_count": len(session_tasks),
        "review_days": dict(sorted(review_days.items())),
        "review_batches": dict(sorted(review_batches.items())),
        "topic_groups": dict(sorted(topic_groups.items())),
        "session_status_counts": dict(sorted(session_status_counts.items())),
        "total_estimated_minutes": total_estimated_minutes,
        "crawler_execution_allowed": False,
        "engineering_review_allowed_count": engineering_review_allowed_count,
        "no_live_crawler": True,
        "manual_review_required": True,
        "no_auto_publish": True,
        "no_personal_data": True,
        "session_tasks": session_tasks,
    }

    if result["total_count"] != 10:
        raise ValueError("Review session planner should currently contain 10 records")
    if result["source_checklist_count"] != 10:
        raise ValueError("Review session planner should currently come from 10 engineering checklist records")
    if result["engineering_review_allowed_count"] != 0:
        raise ValueError("Review session planner must keep engineering_review_allowed_count at 0")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> dict:
    return build_open_data_review_session_planner()


if __name__ == "__main__":
    main()

from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = ROOT / "dashboard" / "data" / "open_data_manual_review_result_template.json"
OUTPUT_PATH = ROOT / "dashboard" / "data" / "open_data_manual_review_sop.json"
TAIPEI_TZ = timezone(timedelta(hours=8))
RESULT_TEMPLATE_FILE = "dashboard/data/open_data_manual_review_result_template.json"

TOPIC_MINUTES = {
    "traffic_parking": 25,
    "social_welfare": 30,
    "culture_events": 20,
    "public_works_environment": 30,
    "complaints_service": 40,
}

PRE_REVIEW_CHECKLIST = [
    "確認只做人工審核，不執行 crawler",
    "確認不下載私人陳情全文",
    "確認不收集姓名、電話、email、地址等個資",
    "準備人工截圖或文字紀錄工具",
    "開啟 dashboard/open-data-review-evidence.html",
    "開啟 dashboard/open-data-manual-review-results.html",
]

PER_SOURCE_REVIEW_STEPS = [
    "開啟 source_url",
    "記錄來源頁標題或 dataset title",
    "確認是否為官方來源",
    "確認 source_owner 是否一致",
    "確認授權或使用條款",
    "確認資料格式",
    "確認更新頻率",
    "檢查是否含個資",
    "檢查是否含私人陳情全文",
    "不執行 crawler",
    "不自動發布",
]

EVIDENCE_RECORDING_STEPS = [
    "記錄 source_url",
    "記錄 page_title_or_dataset_title",
    "記錄 official_owner",
    "記錄 license_or_terms_summary",
    "記錄 available_format",
    "記錄 update_cadence_observed",
    "記錄 personal_data_risk_observed",
    "記錄 private_complaint_risk_observed",
    "記錄 reviewed_at",
    "記錄 reviewer_notes",
]

RESULT_TEMPLATE_FILL_STEPS = [
    "更新 source_opened_result",
    "更新 official_source_result",
    "更新 license_terms_result",
    "更新 format_result",
    "更新 update_cadence_result",
    "更新 personal_data_result",
    "更新 private_complaint_result",
    "填寫 evidence_summary",
    "填寫 reviewer_notes",
    "選擇 reviewer_decision",
    "保持 crawler_execution_allowed false",
    "保持 engineering_review_allowed false",
]

SAFETY_CHECKLIST = [
    "no live crawler",
    "no personal data",
    "no private complaint full text",
    "no auto publish",
    "no automated email",
    "manual review only",
    "crawler_execution_allowed remains false",
    "engineering_review_allowed remains false",
]

COMPLETION_CHECKLIST = [
    "已人工開啟 source_url",
    "已記錄來源頁標題或 dataset title",
    "已人工確認官方來源",
    "已人工記錄授權或條款摘要",
    "已人工確認可用格式",
    "已人工確認更新頻率",
    "已人工確認個資風險",
    "已人工確認私人陳情全文風險",
    "已填寫 reviewer_notes",
    "crawler_execution_allowed 仍為 false",
    "engineering_review_allowed 仍為 false",
]

HANDOFF_NEXT_ACTIONS = [
    "update_human_review_workbook_later",
    "update_engineering_checklist_later",
    "prepare_manual_review_summary_later",
    "block_item_if_risk_found",
    "request_follow_up_if_license_unclear",
]


def now_iso() -> str:
    return datetime.now(TAIPEI_TZ).isoformat(timespec="seconds")


def load_source(path: Path = SOURCE_PATH) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_source(payload: dict) -> list[dict]:
    results = payload.get("results", [])
    if not isinstance(results, list):
        raise ValueError("Manual review result template must contain a results list")
    if int(payload.get("total_count", 0)) != len(results):
        raise ValueError("Manual review result template total_count mismatch")
    if int(payload.get("source_evidence_pack_count", 0)) != len(results):
        raise ValueError("Manual review result template source_evidence_pack_count mismatch")
    if len(results) != 10:
        raise ValueError("Manual review result template should currently contain 10 records")
    return results


def estimate_minutes(topic_group: str) -> int:
    return TOPIC_MINUTES.get(topic_group, 25)


def build_batch_item(result: dict) -> dict:
    return {
        "result_id": result["result_id"],
        "title": result["title"],
        "topic_group": result["topic_group"],
        "source_owner": result["source_owner"],
        "source_url": result["source_url"],
        "review_batch": result["review_batch"],
        "recommended_next_action": result["recommended_next_action"],
        "result_status": result["result_status"],
        "reviewer_decision": result["reviewer_decision"],
        "crawler_execution_allowed": False,
        "engineering_review_allowed": False,
        "estimated_minutes": estimate_minutes(result["topic_group"]),
    }


def build_sop(results: list[dict]) -> dict:
    grouped: dict[str, list[dict]] = {}
    for result in results:
        grouped.setdefault(result["review_day"], []).append(result)

    daily_batches = []
    for review_day in ["day_1", "day_2", "day_3"]:
        day_items = [build_batch_item(item) for item in grouped.get(review_day, [])]
        daily_batches.append(
            {
                "review_day": review_day,
                "task_count": len(day_items),
                "estimated_minutes_total": sum(item["estimated_minutes"] for item in day_items),
                "items": day_items,
            }
        )

    return {
        "sop_id": "open-data-manual-review-sop-001",
        "sop_title": "官方資料第一批人工審核 SOP",
        "review_scope": "第一批 10 筆官方資料來源人工審核流程",
        "source_result_template_file": RESULT_TEMPLATE_FILE,
        "total_tasks": len(results),
        "review_days": {
            "day_1": len(grouped.get("day_1", [])),
            "day_2": len(grouped.get("day_2", [])),
            "day_3": len(grouped.get("day_3", [])),
        },
        "daily_batches": daily_batches,
        "step_groups": [
            "before_review",
            "source_identity_review",
            "license_terms_review",
            "format_review",
            "risk_review",
            "evidence_recording",
            "result_template_update",
            "completion_handoff",
        ],
        "pre_review_checklist": list(PRE_REVIEW_CHECKLIST),
        "per_source_review_steps": list(PER_SOURCE_REVIEW_STEPS),
        "evidence_recording_steps": list(EVIDENCE_RECORDING_STEPS),
        "result_template_fill_steps": list(RESULT_TEMPLATE_FILL_STEPS),
        "safety_checklist": list(SAFETY_CHECKLIST),
        "completion_checklist": list(COMPLETION_CHECKLIST),
        "handoff_next_actions": list(HANDOFF_NEXT_ACTIONS),
        "crawler_execution_allowed": False,
        "engineering_review_allowed": False,
        "notes": "manual review only / no live crawler / no auto publish / no personal data",
    }


def build_open_data_manual_review_sop(
    source_path: Path = SOURCE_PATH,
    output_path: Path = OUTPUT_PATH,
) -> dict:
    payload = load_source(source_path)
    results = validate_source(payload)
    sop = build_sop(results)

    review_days = Counter(item["review_day"] for item in results)
    review_batches = Counter(item["review_batch"] for item in results)
    topic_groups = Counter(item["topic_group"] for item in results)
    estimated_total_minutes = sum(estimate_minutes(item["topic_group"]) for item in results)

    result = {
        "generated_at": now_iso(),
        "public_use_status": "internal_manual_review_sop",
        "source_result_template_count": len(results),
        "total_tasks": len(results),
        "review_days": dict(sorted(review_days.items())),
        "review_batches": dict(sorted(review_batches.items())),
        "topic_groups": dict(sorted(topic_groups.items())),
        "estimated_total_minutes": estimated_total_minutes,
        "crawler_execution_allowed": False,
        "engineering_review_allowed_count": 0,
        "no_live_crawler": True,
        "manual_review_required": True,
        "no_auto_publish": True,
        "no_personal_data": True,
        "sop": sop,
    }

    if result["total_tasks"] != 10:
        raise ValueError("Manual review SOP should currently contain 10 tasks")
    if result["source_result_template_count"] != 10:
        raise ValueError("Manual review SOP should currently come from 10 result templates")
    if result["review_days"].get("day_1") != 3:
        raise ValueError("Manual review SOP day_1 should contain 3 tasks")
    if result["review_days"].get("day_2") != 4:
        raise ValueError("Manual review SOP day_2 should contain 4 tasks")
    if result["review_days"].get("day_3") != 3:
        raise ValueError("Manual review SOP day_3 should contain 3 tasks")
    if result["engineering_review_allowed_count"] != 0:
        raise ValueError("Manual review SOP must keep engineering_review_allowed_count at 0")
    if len(sop["safety_checklist"]) < 8:
        raise ValueError("Manual review SOP safety_checklist must contain at least 8 items")
    if len(sop["per_source_review_steps"]) < 10:
        raise ValueError("Manual review SOP per_source_review_steps must contain at least 10 items")
    if len(sop["result_template_fill_steps"]) < 10:
        raise ValueError("Manual review SOP result_template_fill_steps must contain at least 10 items")
    serialized = json.dumps(result, ensure_ascii=False)
    if '"approved_for_crawling"' in serialized:
        raise ValueError("approved_for_crawling is not allowed")
    if '"live_crawler"' in serialized:
        raise ValueError("live_crawler is not allowed")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> dict:
    return build_open_data_manual_review_sop()


if __name__ == "__main__":
    main()

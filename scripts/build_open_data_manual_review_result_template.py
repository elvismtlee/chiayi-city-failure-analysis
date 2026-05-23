from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = ROOT / "dashboard" / "data" / "open_data_review_evidence_pack.json"
OUTPUT_PATH = ROOT / "dashboard" / "data" / "open_data_manual_review_result_template.json"
TAIPEI_TZ = timezone(timedelta(hours=8))

EVIDENCE_SUMMARY_TEMPLATE = "\n".join(
    [
        "- 來源頁標題：",
        "- 官方來源確認：",
        "- 授權或條款摘要：",
        "- 可用格式：",
        "- 更新頻率觀察：",
        "- 個資風險：",
        "- 私人陳情全文風險：",
        "- 審核者補充：",
    ]
)

RESULT_CHECKLIST = [
    "source_url 已人工開啟",
    "官方來源已人工確認",
    "授權或條款已人工記錄",
    "格式已人工確認",
    "更新頻率已人工記錄",
    "個資風險已人工確認",
    "私人陳情全文風險已人工確認",
    "reviewer_notes 已完成",
    "crawler_execution_allowed 仍為 false",
    "engineering_review_allowed 仍為 false",
]


def now_iso() -> str:
    return datetime.now(TAIPEI_TZ).isoformat(timespec="seconds")


def load_source(path: Path = SOURCE_PATH) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_evidence_pack(payload: dict) -> list[dict]:
    evidence_packs = payload.get("evidence_packs", [])
    if not isinstance(evidence_packs, list):
        raise ValueError("Review evidence pack must contain an evidence_packs list")
    if int(payload.get("total_count", 0)) != len(evidence_packs):
        raise ValueError("Review evidence pack total_count does not match evidence_packs length")
    if int(payload.get("source_session_count", 0)) != len(evidence_packs):
        raise ValueError("Review evidence pack source_session_count does not match evidence_packs length")
    if len(evidence_packs) != 10:
        raise ValueError("Review evidence pack should currently contain 10 records")
    return evidence_packs


def safety_notes() -> str:
    return " / ".join(
        [
            "no live crawler",
            "no personal data",
            "no private complaint full text",
            "no auto publish",
            "manual review result template only",
        ]
    )


def build_result(index: int, pack: dict) -> dict:
    return {
        "result_id": f"open-data-manual-review-result-{index + 1:02d}",
        "evidence_pack_id": pack["evidence_pack_id"],
        "session_task_id": pack["session_task_id"],
        "checklist_id": pack["checklist_id"],
        "review_id": pack["review_id"],
        "spec_id": pack["spec_id"],
        "task_id": pack["task_id"],
        "inventory_id": pack["inventory_id"],
        "title": pack["title"],
        "topic_group": pack["topic_group"],
        "source_owner": pack["source_owner"],
        "source_url": pack["source_url"],
        "review_day": pack["review_day"],
        "review_batch": pack["review_batch"],
        "result_status": "not_started",
        "reviewer_name": "",
        "reviewed_at": "",
        "source_opened_result": "not_checked",
        "official_source_result": "not_checked",
        "license_terms_result": "not_checked",
        "format_result": "not_checked",
        "update_cadence_result": "not_checked",
        "personal_data_result": "not_checked",
        "private_complaint_result": "not_checked",
        "evidence_summary": "",
        "evidence_summary_template": EVIDENCE_SUMMARY_TEMPLATE,
        "reviewer_decision": "not_decided",
        "reviewer_notes": "",
        "follow_up_required": False,
        "follow_up_reason": "",
        "recommended_next_action": "collect_missing_evidence",
        "result_checklist": list(RESULT_CHECKLIST),
        "crawler_execution_allowed": False,
        "engineering_review_allowed": False,
        "human_approval_required": True,
        "no_live_crawler": True,
        "manual_review_required": True,
        "no_auto_publish": True,
        "no_personal_data": True,
        "safety_notes": safety_notes(),
    }


def build_open_data_manual_review_result_template(
    source_path: Path = SOURCE_PATH,
    output_path: Path = OUTPUT_PATH,
) -> dict:
    payload = load_source(source_path)
    evidence_packs = validate_evidence_pack(payload)
    results = [build_result(index, pack) for index, pack in enumerate(evidence_packs)]

    if any(item["crawler_execution_allowed"] for item in results):
        raise ValueError("Manual review result template must never enable crawler execution")
    if any(item["engineering_review_allowed"] for item in results):
        raise ValueError("Manual review result template must not enable engineering review")
    if any(item["reviewer_decision"] == "approved_for_crawling" for item in results):
        raise ValueError("approved_for_crawling is not allowed")
    if any(item.get("live_crawler") for item in results):
        raise ValueError("live_crawler is not allowed")
    if any(len(item["result_checklist"]) < 10 for item in results):
        raise ValueError("Each manual review result template must contain at least 10 checklist items")
    if any(len(item["evidence_summary_template"].splitlines()) < 8 for item in results):
        raise ValueError("Each manual review result template must contain at least 8 summary template lines")

    review_days = Counter(item["review_day"] for item in results)
    review_batches = Counter(item["review_batch"] for item in results)
    topic_groups = Counter(item["topic_group"] for item in results)
    result_status_counts = Counter(item["result_status"] for item in results)
    reviewer_decision_counts = Counter(item["reviewer_decision"] for item in results)
    engineering_review_allowed_count = sum(1 for item in results if item["engineering_review_allowed"])

    result = {
        "generated_at": now_iso(),
        "public_use_status": "internal_manual_review_result_template",
        "source_evidence_pack_count": len(evidence_packs),
        "total_count": len(results),
        "review_days": dict(sorted(review_days.items())),
        "review_batches": dict(sorted(review_batches.items())),
        "topic_groups": dict(sorted(topic_groups.items())),
        "result_status_counts": dict(sorted(result_status_counts.items())),
        "reviewer_decision_counts": dict(sorted(reviewer_decision_counts.items())),
        "crawler_execution_allowed": False,
        "engineering_review_allowed_count": engineering_review_allowed_count,
        "no_live_crawler": True,
        "manual_review_required": True,
        "no_auto_publish": True,
        "no_personal_data": True,
        "results": results,
    }

    if result["total_count"] != 10:
        raise ValueError("Manual review result template should currently contain 10 records")
    if result["source_evidence_pack_count"] != 10:
        raise ValueError("Manual review result template should currently come from 10 evidence packs")
    if result["result_status_counts"].get("not_started") != 10:
        raise ValueError("Manual review result template should keep all results at not_started")
    if result["reviewer_decision_counts"].get("not_decided") != 10:
        raise ValueError("Manual review result template should keep all reviewer decisions at not_decided")
    if result["engineering_review_allowed_count"] != 0:
        raise ValueError("Manual review result template must keep engineering_review_allowed_count at 0")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> dict:
    return build_open_data_manual_review_result_template()


if __name__ == "__main__":
    main()

from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PATCH_DRAFTS_PATH = ROOT / "dashboard" / "data" / "open_data_manual_review_result_patch_drafts.json"
OUTPUT_PATH = ROOT / "dashboard" / "data" / "open_data_day1_sample_manual_review_results.json"
DOCS_DIR = ROOT / "docs" / "open_data_day1_sample_results"
DOC_PATH = DOCS_DIR / "day_1_sample_manual_review_results.md"
TAIPEI_TZ = timezone(timedelta(hours=8))

SOURCE_PATCH_DRAFT_FILE = "dashboard/data/open_data_manual_review_result_patch_drafts.json"
FIELDS_NOT_CHANGED = [
    "crawler_execution_allowed",
    "engineering_review_allowed",
    "approved_for_crawling",
    "live_crawler",
    "review_status",
    "approval_gate_status",
    "engineering_review_status",
]
BLOCKED_FIELDS = [
    "crawler_execution_allowed",
    "engineering_review_allowed",
    "approved_for_crawling",
    "live_crawler",
    "reviewer_decision_ready_for_engineering_review",
    "review_status_completed",
    "official_source_verified_without_manual_review",
]


def now_iso() -> str:
    return datetime.now(TAIPEI_TZ).isoformat(timespec="seconds")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_sample(index: int, patch: dict) -> dict:
    return {
        "sample_id": f"open-data-day1-sample-{index + 1:02d}",
        "patch_id": patch["patch_id"],
        "result_id": patch["result_id"],
        "title": patch["title"],
        "topic_group": patch["topic_group"],
        "source_owner": patch["source_owner"],
        "source_url": patch["source_url"],
        "review_day": patch["review_day"],
        "sample_status": "sample_not_actual_review",
        "sample_source_opened_result": "sample_only_not_checked",
        "sample_official_source_result": "sample_only_not_verified",
        "sample_license_terms_result": "sample_only_not_reviewed",
        "sample_format_result": "sample_only_not_checked",
        "sample_update_cadence_result": "sample_only_not_checked",
        "sample_personal_data_result": "sample_only_not_checked",
        "sample_private_complaint_result": "sample_only_not_checked",
        "sample_evidence_summary": "這是填寫範例，不代表已完成實際人工審核。",
        "sample_reviewer_decision": "not_decided",
        "sample_reviewer_notes": "範例：請在實際人工審核後，填入來源頁標題、授權摘要、格式觀察、個資風險與私人陳情全文風險。",
        "sample_follow_up_required": False,
        "sample_follow_up_reason": "",
        "sample_recommended_next_action": "collect_missing_evidence",
        "fields_not_changed": list(FIELDS_NOT_CHANGED),
        "blocked_fields": list(BLOCKED_FIELDS),
        "safety_notes": "sample only / not actual review result / no live crawler / no request to source_url / no personal data / no private complaint full text / no auto publish",
        "crawler_execution_allowed": False,
        "engineering_review_allowed": False,
        "human_approval_required": True,
        "no_live_crawler": True,
        "manual_review_required": True,
        "no_auto_publish": True,
        "no_personal_data": True,
        "sample_only": True,
        "not_actual_review_result": True,
    }


def render_markdown(samples: list[dict]) -> str:
    lines = [
        "# Day 1 人工審核填寫範例",
        "",
        "- 這是 sample，不是實際審核結果",
        "- 這不是 crawler",
        "- 不啟動 live crawler",
        "- 不對 source_url 發出自動請求",
        "- 不抓個資",
        "- 不抓私人陳情全文",
        "- 不自動發布",
        "- crawler_execution_allowed 永遠 false",
        "- engineering_review_allowed 預設 false",
        "- sample 不代表批准爬取",
        "- sample 不代表實際人工審核完成",
        "",
        f"- day_1 任務數：{len(samples)}",
        "",
    ]
    for index, sample in enumerate(samples, start=1):
        lines.extend(
            [
                f"## Sample {index}：{sample['title']}",
                "",
                f"- source_url：{sample['source_url']}",
                f"- sample_evidence_summary：{sample['sample_evidence_summary']}",
                f"- sample_reviewer_notes：{sample['sample_reviewer_notes']}",
                f"- fields_not_changed：{', '.join(sample['fields_not_changed'])}",
                f"- blocked_fields：{', '.join(sample['blocked_fields'])}",
                "",
            ]
        )
    lines.extend(
        [
            "## completion reminder",
            "",
            "- 這份文件只示範欄位如何填寫",
            "- 不可據此視為真實人工審核完成",
            "- crawler_execution_allowed 必須維持 false",
            "- engineering_review_allowed 必須維持 false",
        ]
    )
    return "\n".join(lines)


def write_doc(samples: list[dict], doc_path: Path = DOC_PATH) -> None:
    doc_path.parent.mkdir(parents=True, exist_ok=True)
    doc_path.write_text(render_markdown(samples) + "\n", encoding="utf-8")


def build_open_data_day1_sample_manual_review_results(
    patch_drafts_path: Path = PATCH_DRAFTS_PATH,
    output_path: Path = OUTPUT_PATH,
    doc_path: Path = DOC_PATH,
) -> dict:
    payload = load_json(patch_drafts_path)
    patches = payload.get("patches", [])
    if payload.get("total_count") != 10 or len(patches) != 10:
        raise ValueError("Manual review patch drafts must contain 10 patches")

    day_1_patches = [patch for patch in patches if patch.get("review_day") == "day_1"]
    if len(day_1_patches) != 3:
        raise ValueError("Day 1 sample results must use exactly 3 day_1 patches")

    samples = [build_sample(index, patch) for index, patch in enumerate(day_1_patches)]
    topic_groups = Counter(sample["topic_group"] for sample in samples)
    sample_status_counts = Counter(sample["sample_status"] for sample in samples)
    engineering_review_allowed_count = sum(1 for sample in samples if sample["engineering_review_allowed"])

    result = {
        "generated_at": now_iso(),
        "public_use_status": "internal_day1_sample_manual_review_results",
        "sample_only": True,
        "not_actual_review_result": True,
        "source_patch_draft_count": len(patches),
        "source_patch_draft_file": SOURCE_PATCH_DRAFT_FILE,
        "total_count": len(samples),
        "review_day": "day_1",
        "topic_groups": dict(sorted(topic_groups.items())),
        "sample_status_counts": dict(sorted(sample_status_counts.items())),
        "crawler_execution_allowed": False,
        "engineering_review_allowed_count": engineering_review_allowed_count,
        "no_live_crawler": True,
        "manual_review_required": True,
        "no_auto_publish": True,
        "no_personal_data": True,
        "samples": samples,
    }

    if result["total_count"] != 3:
        raise ValueError("Day 1 sample results total_count must be 3")
    if result["source_patch_draft_count"] != 10:
        raise ValueError("Day 1 sample results source_patch_draft_count must be 10")
    if result["review_day"] != "day_1":
        raise ValueError("Day 1 sample results review_day must stay day_1")
    if result["sample_only"] is not True or result["not_actual_review_result"] is not True:
        raise ValueError("Day 1 sample results must stay sample-only and not actual review result")
    if result["sample_status_counts"].get("sample_not_actual_review") != 3:
        raise ValueError("Day 1 sample results must start with 3 sample_not_actual_review items")
    if result["engineering_review_allowed_count"] != 0 or result["crawler_execution_allowed"] is not False:
        raise ValueError("Day 1 sample results must keep engineering review and crawler disabled")
    for sample in samples:
        if sample["crawler_execution_allowed"] or sample["engineering_review_allowed"]:
            raise ValueError("Sample rows must keep crawler and engineering review disabled")
        if sample["sample_reviewer_decision"] != "not_decided":
            raise ValueError("Sample reviewer decision must remain not_decided")
        if "approved_for_crawling" not in sample["blocked_fields"] or "live_crawler" not in sample["blocked_fields"]:
            raise ValueError("Blocked fields must include approved_for_crawling and live_crawler")
    serialized = json.dumps(result, ensure_ascii=False)
    if '"approved_for_crawling": true' in serialized:
        raise ValueError("approved_for_crawling true is not allowed")
    if '"live_crawler": true' in serialized:
        raise ValueError("live_crawler true is not allowed")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_doc(samples, doc_path)
    return result


def main() -> dict:
    return build_open_data_day1_sample_manual_review_results()


if __name__ == "__main__":
    main()

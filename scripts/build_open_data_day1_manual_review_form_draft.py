from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = ROOT / "dashboard" / "data" / "open_data_day1_sample_manual_review_results.json"
OUTPUT_PATH = ROOT / "dashboard" / "data" / "open_data_day1_manual_review_form_draft.json"
DOC_PATH = ROOT / "docs" / "open_data_day1_manual_review_forms" / "day_1_manual_review_form_draft.md"
TAIPEI_TZ = timezone(timedelta(hours=8))

SOURCE_SAMPLE_FILE = "dashboard/data/open_data_day1_sample_manual_review_results.json"
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


def build_form(index: int, sample: dict) -> dict:
    return {
        "form_id": f"open-data-day1-form-{index + 1:02d}",
        "sample_id": sample["sample_id"],
        "patch_id": sample["patch_id"],
        "result_id": sample["result_id"],
        "title": sample["title"],
        "topic_group": sample["topic_group"],
        "source_owner": sample["source_owner"],
        "source_url": sample["source_url"],
        "review_day": sample["review_day"],
        "form_status": "draft_not_started",
        "reviewer_fields": {
            "reviewer_name": "",
            "reviewed_at": "",
            "reviewer_notes": "",
            "evidence_summary": "",
            "reviewer_decision": "not_decided",
            "follow_up_required": False,
            "follow_up_reason": "",
            "recommended_next_action": "collect_missing_evidence",
        },
        "source_identity_section": {
            "source_url": sample["source_url"],
            "page_title_or_dataset_title": "",
            "official_owner": sample["source_owner"],
            "source_owner_matches": "",
            "source_identity_notes": "",
        },
        "license_terms_section": {
            "license_or_terms_found": "",
            "license_or_terms_summary": "",
            "license_terms_result": "",
            "license_terms_notes": "",
        },
        "format_section": {
            "available_format": "",
            "format_result": "",
            "downloadable_file_observed": "",
            "format_notes": "",
        },
        "update_cadence_section": {
            "update_cadence_observed": "",
            "update_cadence_result": "",
            "last_updated_observed": "",
            "update_notes": "",
        },
        "risk_review_section": {
            "personal_data_result": "",
            "personal_data_risk_observed": "",
            "private_complaint_result": "",
            "private_complaint_risk_observed": "",
            "risk_notes": "",
        },
        "evidence_summary_section": {
            "evidence_summary": "",
            "source_page_screenshot_note": "",
            "license_terms_screenshot_note": "",
            "format_or_download_link_note": "",
            "risk_review_note": "",
        },
        "reviewer_decision_section": {
            "reviewer_decision": "not_decided",
            "allowed_values": [
                "not_decided",
                "source_verified_but_not_engineering_ready",
                "needs_follow_up",
                "not_suitable",
            ],
            "disallowed_values": [
                "ready_for_engineering_review_later",
                "approved_for_crawling",
            ],
        },
        "follow_up_section": {
            "follow_up_required": False,
            "follow_up_reason": "",
            "recommended_next_action": "collect_missing_evidence",
        },
        "blocked_fields": list(BLOCKED_FIELDS),
        "safety_notes": "form draft only / not actual review result / no live crawler / no request to source_url / no personal data / no private complaint full text / no auto publish",
        "crawler_execution_allowed": False,
        "engineering_review_allowed": False,
        "human_approval_required": True,
        "no_live_crawler": True,
        "manual_review_required": True,
        "no_auto_publish": True,
        "no_personal_data": True,
        "form_draft_only": True,
        "not_actual_review_result": True,
    }


def render_markdown(forms: list[dict]) -> str:
    lines = [
        "# Day 1 人工審核表單草稿",
        "",
        "- 這是 form draft，不是實際審核結果",
        "- 這不是 crawler",
        "- 不啟動 live crawler",
        "- 不對 source_url 發出自動請求",
        "- 不抓個資",
        "- 不抓私人陳情全文",
        "- 不自動發布",
        "- crawler_execution_allowed 永遠 false",
        "- engineering_review_allowed 預設 false",
        "- form draft 不代表批准爬取",
        "- form draft 不代表實際人工審核完成",
        "",
        f"- day_1 表單數：{len(forms)}",
        "",
    ]
    for index, form in enumerate(forms, start=1):
        lines.extend(
            [
                f"## Form {index}：{form['title']}",
                "",
                f"- source_url：{form['source_url']}",
                "",
                "### reviewer_fields",
                "",
            ]
        )
        for key in form["reviewer_fields"].keys():
            lines.append(f"- {key}")
        lines.extend(["", "### source_identity_section", ""])
        for key in form["source_identity_section"].keys():
            lines.append(f"- {key}")
        lines.extend(["", "### license_terms_section", ""])
        for key in form["license_terms_section"].keys():
            lines.append(f"- {key}")
        lines.extend(["", "### format_section", ""])
        for key in form["format_section"].keys():
            lines.append(f"- {key}")
        lines.extend(["", "### update_cadence_section", ""])
        for key in form["update_cadence_section"].keys():
            lines.append(f"- {key}")
        lines.extend(["", "### risk_review_section", ""])
        for key in form["risk_review_section"].keys():
            lines.append(f"- {key}")
        lines.extend(["", "### evidence_summary_section", ""])
        for key in form["evidence_summary_section"].keys():
            lines.append(f"- {key}")
        lines.extend(["", "### reviewer_decision_section", ""])
        for key, value in form["reviewer_decision_section"].items():
            lines.append(f"- {key}：{value}")
        lines.extend(["", "### follow_up_section", ""])
        for key, value in form["follow_up_section"].items():
            lines.append(f"- {key}：{value}")
        lines.extend(
            [
                "",
                f"- blocked_fields：{', '.join(form['blocked_fields'])}",
                "",
            ]
        )
    lines.extend(
        [
            "## completion reminder",
            "",
            "- 這份文件只示範人工審核表單欄位",
            "- 不可據此視為真實人工審核完成",
            "- crawler_execution_allowed 必須維持 false",
            "- engineering_review_allowed 必須維持 false",
        ]
    )
    return "\n".join(lines)


def write_doc(forms: list[dict], doc_path: Path = DOC_PATH) -> None:
    doc_path.parent.mkdir(parents=True, exist_ok=True)
    doc_path.write_text(render_markdown(forms) + "\n", encoding="utf-8")


def build_open_data_day1_manual_review_form_draft(
    source_path: Path = SOURCE_PATH,
    output_path: Path = OUTPUT_PATH,
    doc_path: Path = DOC_PATH,
) -> dict:
    payload = load_json(source_path)
    samples = payload.get("samples", [])
    if payload.get("total_count") != 3 or len(samples) != 3:
        raise ValueError("Day 1 sample manual review results must contain 3 samples")
    if payload.get("review_day") != "day_1":
        raise ValueError("Day 1 sample manual review results review_day must be day_1")

    forms = [build_form(index, sample) for index, sample in enumerate(samples)]
    topic_groups = Counter(form["topic_group"] for form in forms)
    form_status_counts = Counter(form["form_status"] for form in forms)
    engineering_review_allowed_count = sum(1 for form in forms if form["engineering_review_allowed"])

    result = {
        "generated_at": now_iso(),
        "public_use_status": "internal_day1_manual_review_form_draft",
        "form_draft_only": True,
        "not_actual_review_result": True,
        "source_sample_count": len(samples),
        "source_sample_file": SOURCE_SAMPLE_FILE,
        "total_count": len(forms),
        "review_day": "day_1",
        "topic_groups": dict(sorted(topic_groups.items())),
        "form_status_counts": dict(sorted(form_status_counts.items())),
        "crawler_execution_allowed": False,
        "engineering_review_allowed_count": engineering_review_allowed_count,
        "no_live_crawler": True,
        "manual_review_required": True,
        "no_auto_publish": True,
        "no_personal_data": True,
        "forms": forms,
    }

    if result["total_count"] != 3:
        raise ValueError("Day 1 manual review form draft total_count must be 3")
    if result["source_sample_count"] != 3:
        raise ValueError("Day 1 manual review form draft source_sample_count must be 3")
    if result["review_day"] != "day_1":
        raise ValueError("Day 1 manual review form draft review_day must stay day_1")
    if result["form_draft_only"] is not True or result["not_actual_review_result"] is not True:
        raise ValueError("Day 1 manual review form draft must stay form-only and not actual review result")
    if result["form_status_counts"].get("draft_not_started") != 3:
        raise ValueError("Day 1 manual review form draft must start with 3 draft_not_started items")
    if result["engineering_review_allowed_count"] != 0 or result["crawler_execution_allowed"] is not False:
        raise ValueError("Day 1 manual review form draft must keep engineering review and crawler disabled")
    for form in forms:
        if form["crawler_execution_allowed"] or form["engineering_review_allowed"]:
            raise ValueError("Form rows must keep crawler and engineering review disabled")
        if form["reviewer_decision_section"]["reviewer_decision"] != "not_decided":
            raise ValueError("Reviewer decision must remain not_decided")
        if "approved_for_crawling" not in form["blocked_fields"] or "live_crawler" not in form["blocked_fields"]:
            raise ValueError("Blocked fields must include approved_for_crawling and live_crawler")
    serialized = json.dumps(result, ensure_ascii=False)
    if '"approved_for_crawling": true' in serialized:
        raise ValueError("approved_for_crawling true is not allowed")
    if '"live_crawler": true' in serialized:
        raise ValueError("live_crawler true is not allowed")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_doc(forms, doc_path)
    return result


def main() -> dict:
    return build_open_data_day1_manual_review_form_draft()


if __name__ == "__main__":
    main()

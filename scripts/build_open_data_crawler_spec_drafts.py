from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TOP10_TASKS_PATH = ROOT / "dashboard" / "data" / "open_data_top10_review_tasks.json"
OUTPUT_PATH = ROOT / "dashboard" / "data" / "open_data_crawler_spec_drafts.json"
TAIPEI_TZ = timezone(timedelta(hours=8))


def now_iso() -> str:
    return datetime.now(TAIPEI_TZ).isoformat(timespec="seconds")


def load_top10_tasks(path: Path = TOP10_TASKS_PATH) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_top10_tasks(payload: dict) -> list[dict]:
    tasks = payload.get("tasks", [])
    if not isinstance(tasks, list):
        raise ValueError("Top 10 review tasks must be a list")
    if int(payload.get("total_count", 0)) != len(tasks):
        raise ValueError("Top 10 review tasks total_count does not match tasks length")
    if int(payload.get("source_report_count", 0)) != 29:
        raise ValueError("Top 10 review tasks should currently come from 29 source report items")
    if len(tasks) != 10:
        raise ValueError("Top 10 review tasks should currently contain 10 tasks")
    return tasks


def proposed_fetch_method(task: dict) -> str:
    topic_group = str(task.get("topic_group", ""))
    expected_format = str(task.get("expected_format", "")).lower()
    source_url = str(task.get("source_url", "")).lower()

    if topic_group == "complaints_service":
        return "not_recommended"
    if "csv" in expected_format:
        return "csv_download_later"
    if "json" in expected_format or "api" in expected_format:
        return "json_api_later"
    if "xml" in expected_format:
        return "manual_download_later"
    if "html table" in expected_format:
        return "html_table_parse_later"
    if "html" in expected_format:
        if any(token in source_url for token in ("service", "form", "apply", "mailbox", "entry")):
            return "not_recommended"
        return "html_page_parse_later"
    return "manual_download_later"


def proposed_parser_type(task: dict) -> str:
    expected_format = str(task.get("expected_format", "")).lower()
    if "csv" in expected_format:
        return "csv"
    if "json" in expected_format or "api" in expected_format:
        return "json"
    if "xml" in expected_format:
        return "xml"
    if "html table" in expected_format:
        return "html_table"
    if "html" in expected_format:
        return "html_document"
    return "unknown"


def expected_output_dataset(task: dict) -> str:
    return f"open_data_{task['inventory_id']}_draft"


def output_fields_draft(task: dict) -> list[str]:
    fields = [
        "source_title",
        "source_url",
        "topic_group",
        "source_owner",
        "retrieved_at",
        "original_record_id",
        "raw_payload_reference",
        "review_status",
    ]
    group = str(task.get("topic_group", ""))
    if group == "traffic_parking":
        fields.extend(["location_name", "address", "district", "capacity", "fee_rule"])
    elif group == "social_welfare":
        fields.extend(["facility_name", "service_type", "address", "contact_unit", "district"])
    elif group == "public_works_environment":
        fields.extend(["project_name", "location", "responsible_unit", "update_date", "status"])
    elif group == "culture_events":
        fields.extend(["event_name", "venue", "start_date", "end_date", "organizer"])
    return fields


def refresh_strategy(task: dict) -> str:
    cadence = str(task.get("update_cadence", ""))
    if cadence:
        return f"先人工記錄 {cadence} 更新節奏，再決定是否需要後續工程化。"
    return "先人工確認更新節奏，再決定是否需要後續工程化。"


def rate_limit_notes(task: dict) -> str:
    method = proposed_fetch_method(task)
    if method in {"csv_download_later", "json_api_later"}:
        return "僅能在未來人工批准後，以低頻率單次抓取驗證，不可批次連續請求。"
    if method in {"html_page_parse_later", "html_table_parse_later"}:
        return "未來若人工批准，只能低頻率讀取公開頁，先確認 robots 與條款。"
    return "目前只允許人工閱讀，不進行任何自動請求。"


def robots_or_terms_review_status(task: dict) -> str:
    if proposed_fetch_method(task) == "not_recommended":
        return "blocked_pending_manual_policy_review"
    return "not_reviewed"


def personal_data_risk(task: dict) -> str:
    topic_group = str(task.get("topic_group", ""))
    method = proposed_fetch_method(task)
    if topic_group == "complaints_service":
        return "high"
    if method in {"html_page_parse_later", "html_table_parse_later"}:
        return "medium"
    return "low"


def private_complaint_risk(task: dict) -> str:
    if str(task.get("topic_group")) == "complaints_service":
        return "high"
    return "low"


def crawler_spec_status(task: dict) -> str:
    if proposed_fetch_method(task) == "not_recommended":
        return "blocked"
    if "review_needed" in str(task.get("license_status", "")).lower():
        return "license_review_required"
    if task.get("review_status") != "not_started":
        return "source_review_required"
    return "draft_not_reviewed"


def blockers(task: dict) -> list[str]:
    results = [
        "尚未完成人工來源驗證",
        "尚未完成人工授權條款確認",
        "尚未完成人工格式可讀性檢查",
    ]
    if proposed_fetch_method(task) == "not_recommended":
        results.append("來源頁型或風險屬性不適合自動爬取")
    if str(task.get("topic_group")) == "complaints_service":
        results.append("涉及私人陳情風險，必須維持人工審核")
    return results


def safety_notes(task: dict) -> str:
    notes = [
        "no live crawler",
        "no personal data",
        "no private complaint full text",
        "no auto publish",
        "crawler spec draft only",
    ]
    if str(task.get("topic_group")) == "complaints_service":
        notes.append("complaints_service requires stricter manual review")
    return " / ".join(notes)


def build_spec(index: int, task: dict) -> dict:
    return {
        "spec_id": f"open-data-crawler-spec-{index + 1:02d}",
        "task_id": task["task_id"],
        "inventory_id": task["inventory_id"],
        "title": task["title"],
        "topic_group": task["topic_group"],
        "source_owner": task["source_owner"],
        "source_url": task["source_url"],
        "expected_format": task["expected_format"],
        "license_status": task["license_status"],
        "update_cadence": task["update_cadence"],
        "readiness_score": task["readiness_score"],
        "review_priority": task["review_priority"],
        "source_review_status": "not_started",
        "crawler_spec_status": crawler_spec_status(task),
        "crawler_execution_allowed": False,
        "proposed_fetch_method": proposed_fetch_method(task),
        "proposed_parser_type": proposed_parser_type(task),
        "expected_output_dataset": expected_output_dataset(task),
        "output_fields_draft": output_fields_draft(task),
        "refresh_strategy": refresh_strategy(task),
        "rate_limit_notes": rate_limit_notes(task),
        "robots_or_terms_review_status": robots_or_terms_review_status(task),
        "personal_data_risk": personal_data_risk(task),
        "private_complaint_risk": private_complaint_risk(task),
        "safety_notes": safety_notes(task),
        "human_approval_required": True,
        "blockers": blockers(task),
        "next_action": task["next_action"],
        "no_live_crawler": True,
        "manual_review_required": True,
        "no_auto_publish": True,
        "no_personal_data": True,
    }


def build_open_data_crawler_spec_drafts(
    top10_tasks_path: Path = TOP10_TASKS_PATH,
    output_path: Path = OUTPUT_PATH,
) -> dict:
    payload = load_top10_tasks(top10_tasks_path)
    tasks = validate_top10_tasks(payload)
    specs = [build_spec(index, task) for index, task in enumerate(tasks)]

    if any(spec["crawler_execution_allowed"] for spec in specs):
        raise ValueError("Crawler spec drafts must never enable execution")

    topic_groups = Counter(spec["topic_group"] for spec in specs)
    fetch_methods = Counter(spec["proposed_fetch_method"] for spec in specs)
    parser_types = Counter(spec["proposed_parser_type"] for spec in specs)

    result = {
        "generated_at": now_iso(),
        "public_use_status": "internal_crawler_spec_drafts",
        "source_task_count": len(tasks),
        "total_count": len(specs),
        "topic_groups": dict(sorted(topic_groups.items())),
        "proposed_fetch_methods": dict(sorted(fetch_methods.items())),
        "parser_types": dict(sorted(parser_types.items())),
        "crawler_execution_allowed": False,
        "no_live_crawler": True,
        "manual_review_required": True,
        "no_auto_publish": True,
        "no_personal_data": True,
        "specs": specs,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> dict:
    return build_open_data_crawler_spec_drafts()


if __name__ == "__main__":
    main()

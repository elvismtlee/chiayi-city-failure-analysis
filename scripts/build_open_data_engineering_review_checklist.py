from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = ROOT / "dashboard" / "data" / "open_data_human_review_workbook.json"
OUTPUT_PATH = ROOT / "dashboard" / "data" / "open_data_engineering_review_checklist.json"
TAIPEI_TZ = timezone(timedelta(hours=8))


def now_iso() -> str:
    return datetime.now(TAIPEI_TZ).isoformat(timespec="seconds")


def load_source(path: Path = SOURCE_PATH) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_workbook(payload: dict) -> list[dict]:
    records = payload.get("records", [])
    if not isinstance(records, list):
        raise ValueError("Human review workbook must contain a records list")
    if int(payload.get("total_count", 0)) != len(records):
        raise ValueError("Human review workbook total_count does not match records length")
    if int(payload.get("source_spec_count", 0)) != len(records):
        raise ValueError("Human review workbook source_spec_count does not match records length")
    if len(records) != 10:
        raise ValueError("Human review workbook should currently contain 10 records")
    return records


def engineering_review_status(record: dict) -> str:
    approval_gate = str(record.get("approval_gate_status", ""))
    if approval_gate == "ready_for_engineering_review":
        return "ready_for_engineering_review"
    if approval_gate in {"blocked", "needs_risk_review"}:
        return "blocked_by_source_review"
    return "waiting_for_human_review"


def default_gate() -> str:
    return "not_checked"


def private_complaint_gate(record: dict) -> str:
    if str(record.get("topic_group", "")) == "complaints_service":
        return "needs_review"
    return "not_checked"


def engineering_blockers(record: dict) -> list[str]:
    blockers = ["尚未完成人工審核，不能進入 engineering review"]
    if str(record.get("topic_group", "")) == "complaints_service":
        blockers.append("complaints_service 需額外人工風險審查")
    return blockers


def next_action(record: dict) -> str:
    if str(record.get("topic_group", "")) == "complaints_service":
        return "verify_risk_review_result"
    return "wait_for_human_review"


def safety_notes(record: dict) -> str:
    notes = [
        "no live crawler",
        "no personal data",
        "no private complaint full text",
        "no auto publish",
        "engineering review checklist only",
    ]
    if str(record.get("topic_group", "")) == "complaints_service":
        notes.append("complaints_service requires extra human risk review")
    return " / ".join(notes)


def build_checklist(index: int, record: dict) -> dict:
    status = engineering_review_status(record)
    return {
        "checklist_id": f"open-data-engineering-review-{index + 1:02d}",
        "review_id": record["review_id"],
        "spec_id": record["spec_id"],
        "task_id": record["task_id"],
        "inventory_id": record["inventory_id"],
        "title": record["title"],
        "topic_group": record["topic_group"],
        "source_owner": record["source_owner"],
        "source_url": record["source_url"],
        "proposed_fetch_method": record["proposed_fetch_method"],
        "proposed_parser_type": record["proposed_parser_type"],
        "engineering_review_status": status,
        "engineering_review_allowed": False,
        "crawler_execution_allowed": False,
        "source_review_gate": default_gate(),
        "license_review_gate": default_gate(),
        "format_review_gate": default_gate(),
        "personal_data_gate": default_gate(),
        "private_complaint_gate": private_complaint_gate(record),
        "terms_gate": default_gate(),
        "parser_design_gate": default_gate(),
        "output_schema_gate": default_gate(),
        "rate_limit_gate": default_gate(),
        "rollback_plan_gate": default_gate(),
        "logging_plan_gate": default_gate(),
        "human_approval_gate": default_gate(),
        "engineering_blockers": engineering_blockers(record),
        "engineering_notes": "",
        "next_action": next_action(record),
        "safety_notes": safety_notes(record),
        "human_approval_required": True,
        "no_live_crawler": True,
        "manual_review_required": True,
        "no_auto_publish": True,
        "no_personal_data": True,
    }


def build_open_data_engineering_review_checklist(
    source_path: Path = SOURCE_PATH,
    output_path: Path = OUTPUT_PATH,
) -> dict:
    payload = load_source(source_path)
    records = validate_workbook(payload)
    checklists = [build_checklist(index, record) for index, record in enumerate(records)]

    if any(item["crawler_execution_allowed"] for item in checklists):
        raise ValueError("Engineering review checklist must never enable crawler execution")
    if any(item["engineering_review_allowed"] for item in checklists):
        raise ValueError("Engineering review checklist must not allow engineering review by default")
    if any(item["engineering_review_status"] == "approved_for_crawling" for item in checklists):
        raise ValueError("approved_for_crawling is not allowed")
    if any(item["proposed_fetch_method"] == "live_crawler" for item in checklists):
        raise ValueError("live_crawler is not allowed")
    if any(len([key for key in item if key.endswith("_gate")]) < 10 for item in checklists):
        raise ValueError("Each checklist item must contain at least 10 gate fields")

    topic_groups = Counter(item["topic_group"] for item in checklists)
    status_counts = Counter(item["engineering_review_status"] for item in checklists)
    engineering_allowed_count = sum(1 for item in checklists if item["engineering_review_allowed"])

    result = {
        "generated_at": now_iso(),
        "public_use_status": "internal_engineering_review_checklist",
        "source_workbook_count": len(records),
        "total_count": len(checklists),
        "topic_groups": dict(sorted(topic_groups.items())),
        "engineering_review_status_counts": dict(sorted(status_counts.items())),
        "engineering_review_allowed_count": engineering_allowed_count,
        "crawler_execution_allowed": False,
        "no_live_crawler": True,
        "manual_review_required": True,
        "no_auto_publish": True,
        "no_personal_data": True,
        "checklists": checklists,
    }

    if result["total_count"] != 10:
        raise ValueError("Engineering review checklist should currently contain 10 records")
    if result["source_workbook_count"] != 10:
        raise ValueError("Engineering review checklist should currently come from 10 human review records")
    if result["engineering_review_allowed_count"] != 0:
        raise ValueError("Engineering review checklist should not allow engineering review by default")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> dict:
    return build_open_data_engineering_review_checklist()


if __name__ == "__main__":
    main()

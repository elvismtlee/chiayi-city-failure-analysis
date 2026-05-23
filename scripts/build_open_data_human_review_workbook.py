from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = ROOT / "dashboard" / "data" / "open_data_crawler_spec_drafts.json"
OUTPUT_PATH = ROOT / "dashboard" / "data" / "open_data_human_review_workbook.json"
TAIPEI_TZ = timezone(timedelta(hours=8))


def now_iso() -> str:
    return datetime.now(TAIPEI_TZ).isoformat(timespec="seconds")


def load_source(path: Path = SOURCE_PATH) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_specs(payload: dict) -> list[dict]:
    specs = payload.get("specs", [])
    if not isinstance(specs, list):
        raise ValueError("Crawler spec drafts must contain a specs list")
    if int(payload.get("total_count", 0)) != len(specs):
        raise ValueError("Crawler spec drafts total_count does not match specs length")
    if int(payload.get("source_task_count", 0)) != len(specs):
        raise ValueError("Crawler spec drafts source_task_count does not match specs length")
    if len(specs) != 10:
        raise ValueError("Crawler spec drafts should currently contain 10 records")
    return specs


def approval_gate_status(spec: dict) -> str:
    if str(spec.get("topic_group", "")) == "complaints_service":
        return "needs_risk_review"
    return "pending_manual_review"


def blockers(spec: dict) -> list[str]:
    items = ["尚未完成人工審核"]
    if str(spec.get("topic_group", "")) == "complaints_service":
        items.append("complaints_service 需要更嚴格的私人陳情風險確認")
    return items


def safety_notes(spec: dict) -> str:
    notes = [
        "no live crawler",
        "no personal data",
        "no private complaint full text",
        "no auto publish",
        "human review workbook only",
    ]
    if str(spec.get("topic_group", "")) == "complaints_service":
        notes.append("complaints_service requires strict private complaint review")
    return " / ".join(notes)


def build_record(index: int, spec: dict) -> dict:
    return {
        "review_id": f"open-data-human-review-{index + 1:02d}",
        "spec_id": spec["spec_id"],
        "task_id": spec["task_id"],
        "inventory_id": spec["inventory_id"],
        "title": spec["title"],
        "topic_group": spec["topic_group"],
        "source_owner": spec["source_owner"],
        "source_url": spec["source_url"],
        "proposed_fetch_method": spec["proposed_fetch_method"],
        "proposed_parser_type": spec["proposed_parser_type"],
        "source_opened": False,
        "official_source_verified": False,
        "license_reviewed": False,
        "terms_reviewed": False,
        "format_checked": False,
        "sample_download_checked": False,
        "personal_data_checked": False,
        "private_complaint_checked": False,
        "robots_or_terms_checked": False,
        "reviewer": "",
        "reviewed_at": "",
        "review_status": "not_started",
        "approval_gate_status": approval_gate_status(spec),
        "engineering_review_allowed": False,
        "crawler_execution_allowed": False,
        "blockers": blockers(spec),
        "reviewer_notes": "",
        "next_action": "open_source_url",
        "safety_notes": safety_notes(spec),
        "human_approval_required": True,
        "no_live_crawler": True,
        "manual_review_required": True,
        "no_auto_publish": True,
        "no_personal_data": True,
    }


def build_open_data_human_review_workbook(
    source_path: Path = SOURCE_PATH,
    output_path: Path = OUTPUT_PATH,
) -> dict:
    payload = load_source(source_path)
    specs = validate_specs(payload)
    records = [build_record(index, spec) for index, spec in enumerate(specs)]

    if any(record["crawler_execution_allowed"] for record in records):
        raise ValueError("Human review workbook must never enable crawler execution")
    if any(record["engineering_review_allowed"] for record in records):
        raise ValueError("Human review workbook must not allow engineering review by default")
    if any("private_complaint_checked" not in record for record in records):
        raise ValueError("Human review workbook records must include private_complaint_checked")
    if any("personal_data_checked" not in record for record in records):
        raise ValueError("Human review workbook records must include personal_data_checked")
    for record in records:
        if record["topic_group"] == "complaints_service" and record["approval_gate_status"] not in {"needs_risk_review", "blocked"}:
            raise ValueError("complaints_service records must stay in risk review or blocked")

    topic_groups = Counter(record["topic_group"] for record in records)
    review_status_counts = Counter(record["review_status"] for record in records)
    gate_counts = Counter(record["approval_gate_status"] for record in records)
    engineering_count = sum(1 for record in records if record["engineering_review_allowed"])

    result = {
        "generated_at": now_iso(),
        "public_use_status": "internal_human_review_workbook",
        "source_spec_count": len(specs),
        "total_count": len(records),
        "topic_groups": dict(sorted(topic_groups.items())),
        "review_status_counts": dict(sorted(review_status_counts.items())),
        "approval_gate_status_counts": dict(sorted(gate_counts.items())),
        "engineering_review_allowed_count": engineering_count,
        "crawler_execution_allowed": False,
        "no_live_crawler": True,
        "manual_review_required": True,
        "no_auto_publish": True,
        "no_personal_data": True,
        "records": records,
    }

    if result["total_count"] != 10:
        raise ValueError("Human review workbook should currently contain 10 records")
    if result["source_spec_count"] != 10:
        raise ValueError("Human review workbook should currently come from 10 crawler spec drafts")
    if result["engineering_review_allowed_count"] != 0:
        raise ValueError("Human review workbook should not allow engineering review by default")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> dict:
    return build_open_data_human_review_workbook()


if __name__ == "__main__":
    main()

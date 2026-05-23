from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PACKETS_PATH = ROOT / "dashboard" / "data" / "open_data_manual_review_execution_packets.json"
RESULT_TEMPLATE_PATH = ROOT / "dashboard" / "data" / "open_data_manual_review_result_template.json"
OUTPUT_PATH = ROOT / "dashboard" / "data" / "open_data_manual_review_result_patch_drafts.json"
DOCS_DIR = ROOT / "docs" / "open_data_manual_review_patch_drafts"
TAIPEI_TZ = timezone(timedelta(hours=8))

SOURCE_EXECUTION_FILE = "dashboard/data/open_data_manual_review_execution_packets.json"
SOURCE_RESULT_TEMPLATE_FILE = "dashboard/data/open_data_manual_review_result_template.json"

FIELDS_REQUIRING_MANUAL_INPUT = [
    "source_opened_result",
    "official_source_result",
    "license_terms_result",
    "format_result",
    "update_cadence_result",
    "personal_data_result",
    "private_complaint_result",
    "evidence_summary",
    "reviewer_decision",
    "reviewer_notes",
    "reviewed_at",
]

BLOCKED_FIELDS = [
    "crawler_execution_allowed",
    "engineering_review_allowed",
    "approved_for_crawling",
    "live_crawler",
]


def now_iso() -> str:
    return datetime.now(TAIPEI_TZ).isoformat(timespec="seconds")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_inputs(packet_payload: dict, result_payload: dict) -> tuple[list[dict], list[dict]]:
    packets = packet_payload.get("packets", [])
    results = result_payload.get("results", [])
    if not isinstance(packets, list) or len(packets) != 3:
        raise ValueError("Manual review execution packets must contain 3 packets")
    if not isinstance(results, list) or len(results) != 10:
        raise ValueError("Manual review result template must contain 10 results")
    if int(packet_payload.get("total_tasks", 0)) != 10:
        raise ValueError("Manual review execution packets total_tasks must be 10")
    if int(result_payload.get("total_count", 0)) != 10:
        raise ValueError("Manual review result template total_count must be 10")
    return packets, results


def packet_task_map(packets: list[dict]) -> dict[str, dict]:
    mapping: dict[str, dict] = {}
    for packet in packets:
        for task in packet.get("task_cards", []):
            mapping[task["result_id"]] = {
                "review_day": packet["review_day"],
                "review_batch": task.get("review_batch", packet.get("review_batch", "待補")),
                "source_url": task["source_url"],
                "title": task["title"],
                "topic_group": task["topic_group"],
                "source_owner": task["source_owner"],
                "result_status": task["result_status"],
                "reviewer_decision": task["reviewer_decision"],
            }
    if len(mapping) != 10:
        raise ValueError("Execution packets task cards should cover exactly 10 result ids")
    return mapping


def build_source_result_patch(result: dict) -> dict:
    return {
        "source_opened_result": result["source_opened_result"],
        "official_source_result": result["official_source_result"],
        "license_terms_result": result["license_terms_result"],
        "format_result": result["format_result"],
        "update_cadence_result": result["update_cadence_result"],
        "personal_data_result": result["personal_data_result"],
        "private_complaint_result": result["private_complaint_result"],
        "evidence_summary": result["evidence_summary"],
        "reviewer_decision": result["reviewer_decision"],
        "reviewer_notes": result["reviewer_notes"],
        "follow_up_required": result["follow_up_required"],
        "follow_up_reason": result["follow_up_reason"],
        "recommended_next_action": result["recommended_next_action"],
    }


def build_patch(index: int, result: dict, packet_task: dict) -> dict:
    return {
        "patch_id": f"open-data-manual-review-patch-{index + 1:02d}",
        "result_id": result["result_id"],
        "evidence_pack_id": result["evidence_pack_id"],
        "session_task_id": result["session_task_id"],
        "checklist_id": result["checklist_id"],
        "review_id": result["review_id"],
        "spec_id": result["spec_id"],
        "task_id": result["task_id"],
        "inventory_id": result["inventory_id"],
        "title": result["title"],
        "topic_group": result["topic_group"],
        "source_owner": result["source_owner"],
        "source_url": result["source_url"],
        "review_day": packet_task["review_day"],
        "review_batch": packet_task["review_batch"],
        "patch_status": "draft_not_started",
        "source_result_patch": build_source_result_patch(result),
        "evidence_patch": {
            "evidence_pack_id": result["evidence_pack_id"],
            "required_evidence_items_completed": False,
            "evidence_summary_completed": False,
            "missing_evidence_items": [],
            "evidence_notes": "",
        },
        "human_review_workbook_patch": {
            "source_opened": False,
            "official_source_verified": False,
            "license_reviewed": False,
            "terms_reviewed": False,
            "format_checked": False,
            "sample_download_checked": False,
            "personal_data_checked": False,
            "private_complaint_checked": False,
            "robots_or_terms_checked": False,
            "review_status": "not_started",
            "approval_gate_status": "pending_manual_review",
            "engineering_review_allowed": False,
            "crawler_execution_allowed": False,
        },
        "engineering_checklist_patch": {
            "source_review_gate": "not_checked",
            "license_review_gate": "not_checked",
            "format_review_gate": "not_checked",
            "personal_data_gate": "not_checked",
            "private_complaint_gate": "not_checked",
            "terms_gate": "not_checked",
            "parser_design_gate": "not_checked",
            "output_schema_gate": "not_checked",
            "rate_limit_gate": "not_checked",
            "rollback_plan_gate": "not_checked",
            "logging_plan_gate": "not_checked",
            "human_approval_gate": "not_checked",
            "engineering_review_status": "waiting_for_human_review",
            "engineering_review_allowed": False,
            "crawler_execution_allowed": False,
        },
        "fields_requiring_manual_input": list(FIELDS_REQUIRING_MANUAL_INPUT),
        "blocked_fields": list(BLOCKED_FIELDS),
        "reviewer_notes_required": True,
        "human_approval_required": True,
        "no_live_crawler": True,
        "manual_review_required": True,
        "no_auto_publish": True,
        "no_personal_data": True,
        "crawler_execution_allowed": False,
        "engineering_review_allowed": False,
        "safety_notes": "patch draft only / no live crawler / no request to source_url / no personal data / no private complaint full text / no auto publish",
        "next_action": "wait_for_manual_review",
    }


def render_patch_markdown(review_day: str, patches: list[dict]) -> str:
    lines = [
        f"# 人工審核結果回填 Patch 草稿 {review_day}",
        "",
        f"- 今日 patch 數：{len(patches)}",
        "- 這不是 crawler",
        "- 不啟動 live crawler",
        "- 不對 source_url 發出自動請求",
        "- 不抓個資",
        "- 不抓私人陳情全文",
        "- 不自動發布",
        "- crawler_execution_allowed 永遠 false",
        "- engineering_review_allowed 預設 false",
        "- patch draft 不代表批准爬取",
        "",
    ]
    for index, patch in enumerate(patches, start=1):
        lines.extend(
            [
                f"## Patch {index}：{patch['title']}",
                "",
                f"- result_id：{patch['result_id']}",
                f"- source_url：{patch['source_url']}",
                f"- fields_requiring_manual_input：{', '.join(patch['fields_requiring_manual_input'])}",
                f"- blocked_fields：{', '.join(patch['blocked_fields'])}",
                "",
                "### source_result_patch 摘要",
                "",
            ]
        )
        for key, value in patch["source_result_patch"].items():
            lines.append(f"- {key}：{value}")
        lines.extend(["", "### human_review_workbook_patch 摘要", ""])
        for key, value in patch["human_review_workbook_patch"].items():
            lines.append(f"- {key}：{value}")
        lines.extend(["", "### engineering_checklist_patch 摘要", ""])
        for key, value in patch["engineering_checklist_patch"].items():
            lines.append(f"- {key}：{value}")
        lines.extend(["", "### completion reminder", "", "- 完成後仍需人工另開 PR 回填相關欄位", "- crawler_execution_allowed 仍須維持 false", "- engineering_review_allowed 仍須維持 false", ""])
    return "\n".join(lines)


def write_docs(patches: list[dict], docs_dir: Path = DOCS_DIR) -> None:
    docs_dir.mkdir(parents=True, exist_ok=True)
    for review_day in ["day_1", "day_2", "day_3"]:
        day_patches = [patch for patch in patches if patch["review_day"] == review_day]
        path = docs_dir / f"{review_day}_patch_drafts.md"
        path.write_text(render_patch_markdown(review_day, day_patches) + "\n", encoding="utf-8")


def build_open_data_manual_review_result_patch_drafts(
    packets_path: Path = PACKETS_PATH,
    result_template_path: Path = RESULT_TEMPLATE_PATH,
    output_path: Path = OUTPUT_PATH,
    docs_dir: Path = DOCS_DIR,
) -> dict:
    packet_payload = load_json(packets_path)
    result_payload = load_json(result_template_path)
    packets, results = validate_inputs(packet_payload, result_payload)
    tasks_by_result = packet_task_map(packets)
    patches = [build_patch(index, result, tasks_by_result[result["result_id"]]) for index, result in enumerate(results)]

    review_days = Counter(patch["review_day"] for patch in patches)
    review_batches = Counter(patch["review_batch"] for patch in patches)
    topic_groups = Counter(patch["topic_group"] for patch in patches)
    patch_status_counts = Counter(patch["patch_status"] for patch in patches)
    engineering_review_allowed_count = sum(1 for patch in patches if patch["engineering_review_allowed"])

    result = {
        "generated_at": now_iso(),
        "public_use_status": "internal_manual_review_result_patch_drafts",
        "source_execution_packet_count": len(tasks_by_result),
        "source_result_template_count": len(results),
        "source_execution_packet_file": SOURCE_EXECUTION_FILE,
        "source_result_template_file": SOURCE_RESULT_TEMPLATE_FILE,
        "total_count": len(patches),
        "review_days": dict(sorted(review_days.items())),
        "review_batches": dict(sorted(review_batches.items())),
        "topic_groups": dict(sorted(topic_groups.items())),
        "patch_status_counts": dict(sorted(patch_status_counts.items())),
        "crawler_execution_allowed": False,
        "engineering_review_allowed_count": engineering_review_allowed_count,
        "no_live_crawler": True,
        "manual_review_required": True,
        "no_auto_publish": True,
        "no_personal_data": True,
        "patches": patches,
    }

    if result["total_count"] != 10:
        raise ValueError("Manual review result patch drafts total_count must be 10")
    if result["source_result_template_count"] != 10:
        raise ValueError("Manual review result patch drafts source_result_template_count must be 10")
    if result["patch_status_counts"].get("draft_not_started") != 10:
        raise ValueError("Manual review result patch drafts must start with 10 draft_not_started items")
    if result["review_days"].get("day_1") != 3 or result["review_days"].get("day_2") != 4 or result["review_days"].get("day_3") != 3:
        raise ValueError("Manual review result patch drafts review day counts must be 3 / 4 / 3")
    if result["engineering_review_allowed_count"] != 0:
        raise ValueError("Manual review result patch drafts engineering_review_allowed_count must stay 0")
    for patch in patches:
        if patch["crawler_execution_allowed"] or patch["engineering_review_allowed"]:
            raise ValueError("Patch draft level crawler or engineering review must stay false")
        if "approved_for_crawling" not in patch["blocked_fields"] or "live_crawler" not in patch["blocked_fields"]:
            raise ValueError("Patch draft blocked_fields must include approved_for_crawling and live_crawler")
    serialized = json.dumps(result, ensure_ascii=False)
    if '"approved_for_crawling": true' in serialized:
        raise ValueError("approved_for_crawling true is not allowed")
    if '"live_crawler": true' in serialized:
        raise ValueError("live_crawler true is not allowed")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_docs(patches, docs_dir)
    return result


def main() -> dict:
    return build_open_data_manual_review_result_patch_drafts()


if __name__ == "__main__":
    main()

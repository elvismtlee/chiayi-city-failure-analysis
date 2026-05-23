from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOP_PATH = ROOT / "dashboard" / "data" / "open_data_manual_review_sop.json"
RESULT_PATH = ROOT / "dashboard" / "data" / "open_data_manual_review_result_template.json"
OUTPUT_PATH = ROOT / "dashboard" / "data" / "open_data_manual_review_execution_packets.json"
DOCS_DIR = ROOT / "docs" / "open_data_manual_review_packets"
TAIPEI_TZ = timezone(timedelta(hours=8))

SOURCE_SOP_FILE = "dashboard/data/open_data_manual_review_sop.json"
SOURCE_RESULT_TEMPLATE_FILE = "dashboard/data/open_data_manual_review_result_template.json"

CHECKLIST_BEFORE_START = [
    "確認今天只做人工審核",
    "不執行 crawler",
    "不下載私人陳情全文",
    "不記錄姓名、電話、email、地址等個資",
    "開啟 Evidence Pack 頁",
    "開啟人工審核結果輸入表",
    "準備截圖或文字紀錄工具",
    "確認每筆 source_url 只人工開啟檢查",
]

EVIDENCE_FIELDS_TO_FILL = [
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

RESULT_FIELDS_TO_FILL = [
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
    "follow_up_required",
    "follow_up_reason",
    "recommended_next_action",
]

COMPLETION_CHECKLIST = [
    "每筆 source_url 已人工開啟",
    "每筆官方來源已人工確認",
    "每筆授權或條款已人工記錄",
    "每筆格式已人工確認",
    "每筆更新頻率已人工記錄",
    "每筆個資風險已人工確認",
    "每筆私人陳情全文風險已人工確認",
    "每筆 reviewer_notes 已完成",
    "crawler_execution_allowed 仍為 false",
    "engineering_review_allowed 仍為 false",
]

HANDOFF_AFTER_COMPLETION = [
    "update_human_review_workbook_later",
    "update_engineering_checklist_later",
    "prepare_manual_review_summary_later",
    "request_follow_up_if_license_unclear",
    "block_item_if_risk_found",
]

REVIEWER_NOTES_TEMPLATE = "\n".join(
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

SAFETY_NOTES = "manual review only / no live crawler / no request to source_url / no personal data / no private complaint full text / no auto publish"


def now_iso() -> str:
    return datetime.now(TAIPEI_TZ).isoformat(timespec="seconds")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_inputs(sop_payload: dict, result_payload: dict) -> tuple[dict, list[dict]]:
    sop = sop_payload.get("sop", {})
    daily_batches = sop.get("daily_batches", [])
    results = result_payload.get("results", [])
    if not isinstance(daily_batches, list) or len(daily_batches) != 3:
        raise ValueError("Manual review SOP must contain 3 daily batches")
    if not isinstance(results, list) or len(results) != 10:
        raise ValueError("Manual review result template must contain 10 results")
    if int(sop_payload.get("total_tasks", 0)) != 10:
        raise ValueError("Manual review SOP total_tasks must be 10")
    if int(result_payload.get("total_count", 0)) != 10:
        raise ValueError("Manual review result template total_count must be 10")
    return sop, results


def result_map(results: list[dict]) -> dict[str, dict]:
    return {item["result_id"]: item for item in results}


def build_task_card(result: dict, review_batch: str) -> dict:
    return {
        "result_id": result["result_id"],
        "title": result["title"],
        "topic_group": result["topic_group"],
        "source_owner": result["source_owner"],
        "source_url": result["source_url"],
        "review_batch": review_batch,
        "recommended_next_action": result["recommended_next_action"],
        "result_status": result["result_status"],
        "reviewer_decision": result["reviewer_decision"],
        "evidence_summary_template": result["evidence_summary_template"],
        "result_checklist": list(result["result_checklist"]),
        "reviewer_notes_template": REVIEWER_NOTES_TEMPLATE,
        "crawler_execution_allowed": False,
        "engineering_review_allowed": False,
    }


def build_packet(batch: dict, results_by_id: dict[str, dict]) -> dict:
    task_cards = []
    review_batch = "待補"
    for item in batch.get("items", []):
        result = results_by_id.get(item["result_id"])
        if not result:
            raise ValueError(f"Missing result template for {item['result_id']}")
        review_batch = item.get("review_batch", review_batch)
        task_cards.append(build_task_card(result, review_batch))

    return {
        "day_packet_id": f"open-data-manual-review-{batch['review_day']}",
        "review_day": batch["review_day"],
        "review_batch": review_batch,
        "task_count": len(task_cards),
        "estimated_minutes_total": int(batch.get("estimated_minutes_total", 0)),
        "packet_status": "not_started",
        "checklist_before_start": list(CHECKLIST_BEFORE_START),
        "task_cards": task_cards,
        "evidence_fields_to_fill": list(EVIDENCE_FIELDS_TO_FILL),
        "result_fields_to_fill": list(RESULT_FIELDS_TO_FILL),
        "reviewer_notes_template": REVIEWER_NOTES_TEMPLATE,
        "completion_checklist": list(COMPLETION_CHECKLIST),
        "handoff_after_completion": list(HANDOFF_AFTER_COMPLETION),
        "safety_notes": SAFETY_NOTES,
        "crawler_execution_allowed": False,
        "engineering_review_allowed": False,
    }


def render_packet_markdown(packet: dict) -> str:
    lines = [
        f"# 官方資料人工審核工作包 {packet['review_day']}",
        "",
        f"- 今日任務數：{packet['task_count']}",
        f"- 預估時間：{packet['estimated_minutes_total']} 分鐘",
        f"- review_batch：{packet['review_batch']}",
        "",
        "## 安全提醒",
        "",
        "- 這不是 crawler",
        "- 不啟動 live crawler",
        "- 不對 source_url 發出自動請求",
        "- 不抓個資",
        "- 不抓私人陳情全文",
        "- 不自動發布",
        "- crawler_execution_allowed 永遠 false",
        "- engineering_review_allowed 預設 false",
        "",
        "## 今日每筆任務卡",
        "",
    ]
    for index, task in enumerate(packet["task_cards"], start=1):
        lines.extend(
            [
                f"### 任務 {index}：{task['title']}",
                "",
                f"- topic_group：{task['topic_group']}",
                f"- source_owner：{task['source_owner']}",
                f"- source_url：{task['source_url']}",
                f"- recommended_next_action：{task['recommended_next_action']}",
                "",
                "#### 應填 evidence 欄位",
                "",
            ]
        )
        lines.extend([f"- {field}" for field in EVIDENCE_FIELDS_TO_FILL])
        lines.extend(["", "#### 應填 result 欄位", ""])
        lines.extend([f"- {field}" for field in RESULT_FIELDS_TO_FILL])
        lines.append("")
    lines.extend(["## completion checklist", "", "## 完成檢查清單", ""])
    lines.extend([f"- {item}" for item in packet["completion_checklist"]])
    lines.extend(["", "## handoff next actions", ""])
    lines.extend([f"- {item}" for item in packet["handoff_after_completion"]])
    lines.append("")
    return "\n".join(lines)


def write_docs(packets: list[dict], docs_dir: Path = DOCS_DIR) -> None:
    docs_dir.mkdir(parents=True, exist_ok=True)
    for packet in packets:
        path = docs_dir / f"{packet['review_day']}_packet.md"
        path.write_text(render_packet_markdown(packet) + "\n", encoding="utf-8")


def build_open_data_manual_review_execution_packets(
    sop_path: Path = SOP_PATH,
    result_path: Path = RESULT_PATH,
    output_path: Path = OUTPUT_PATH,
    docs_dir: Path = DOCS_DIR,
) -> dict:
    sop_payload = load_json(sop_path)
    result_payload = load_json(result_path)
    sop, results = validate_inputs(sop_payload, result_payload)
    results_by_id = result_map(results)
    packets = [build_packet(batch, results_by_id) for batch in sop["daily_batches"]]

    packet_count = len(packets)
    review_days = Counter(packet["review_day"] for packet in packets for _ in range(packet["task_count"]))
    review_batches = Counter(packet["review_batch"] for packet in packets for _ in range(packet["task_count"]))
    topic_groups = Counter(
        task["topic_group"]
        for packet in packets
        for task in packet["task_cards"]
    )
    packet_status_counts = Counter(packet["packet_status"] for packet in packets)
    estimated_total_minutes = sum(packet["estimated_minutes_total"] for packet in packets)

    result = {
        "generated_at": now_iso(),
        "public_use_status": "internal_manual_review_execution_packets",
        "packet_id": "open-data-manual-review-execution-packets-001",
        "packet_title": "官方資料人工審核工作包",
        "source_sop_file": SOURCE_SOP_FILE,
        "source_result_template_file": SOURCE_RESULT_TEMPLATE_FILE,
        "total_tasks": sum(packet["task_count"] for packet in packets),
        "packet_count": packet_count,
        "review_days": dict(sorted(review_days.items())),
        "review_batches": dict(sorted(review_batches.items())),
        "topic_groups": dict(sorted(topic_groups.items())),
        "estimated_total_minutes": estimated_total_minutes,
        "packet_status_counts": dict(sorted(packet_status_counts.items())),
        "crawler_execution_allowed": False,
        "engineering_review_allowed_count": 0,
        "no_live_crawler": True,
        "manual_review_required": True,
        "no_auto_publish": True,
        "no_personal_data": True,
        "packets": packets,
    }

    if result["total_tasks"] != 10:
        raise ValueError("Execution packets total_tasks must be 10")
    if result["packet_count"] != 3:
        raise ValueError("Execution packets must contain 3 packets")
    if result["review_days"].get("day_1") != 3 or result["review_days"].get("day_2") != 4 or result["review_days"].get("day_3") != 3:
        raise ValueError("Execution packets review day counts must be 3 / 4 / 3")
    if result["estimated_total_minutes"] != 285:
        raise ValueError("Execution packets estimated_total_minutes must be 285")
    if result["engineering_review_allowed_count"] != 0:
        raise ValueError("Execution packets engineering_review_allowed_count must stay 0")
    for packet in packets:
        if packet["crawler_execution_allowed"] or packet["engineering_review_allowed"]:
            raise ValueError("Packet level crawler or engineering review must stay false")
        if len(packet["task_cards"]) < 1:
            raise ValueError("Each packet must contain at least one task card")
        for task in packet["task_cards"]:
            if task["crawler_execution_allowed"] or task["engineering_review_allowed"]:
                raise ValueError("Task card level crawler or engineering review must stay false")
    serialized = json.dumps(result, ensure_ascii=False)
    if '"approved_for_crawling"' in serialized:
        raise ValueError("approved_for_crawling is not allowed")
    if '"live_crawler"' in serialized:
        raise ValueError("live_crawler is not allowed")

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    write_docs(packets, docs_dir)
    return result


def main() -> dict:
    return build_open_data_manual_review_execution_packets()


if __name__ == "__main__":
    main()

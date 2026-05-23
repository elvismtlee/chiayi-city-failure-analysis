from __future__ import annotations

import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TAIPEI_TZ = timezone(timedelta(hours=8))
SOURCE_EXECUTION_PACKETS = ROOT / "dashboard" / "data" / "open_data_manual_review_execution_packets.json"
SOURCE_PATCH_DRAFTS = ROOT / "dashboard" / "data" / "open_data_manual_review_result_patch_drafts.json"
SOURCE_SAMPLE_RESULTS = ROOT / "dashboard" / "data" / "open_data_day1_sample_manual_review_results.json"
SOURCE_FORM_DRAFT = ROOT / "dashboard" / "data" / "open_data_day1_manual_review_form_draft.json"
OUTPUT_PATH = ROOT / "dashboard" / "data" / "open_data_day1_manual_review_operation_board.json"

MASTER_BLOCKED_FIELDS = [
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


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def sample_count(payload: dict[str, Any], key: str) -> int:
    items = payload.get(key, [])
    return len(items) if isinstance(items, list) else 0


def build_task_card(
    task_number: int,
    packet_reference: str,
    packet_task: dict[str, Any],
    patch: dict[str, Any],
    sample: dict[str, Any],
    form: dict[str, Any],
    estimated_minutes: int,
) -> dict[str, Any]:
    return {
        "task_number": task_number,
        "title": packet_task["title"],
        "topic_group": packet_task["topic_group"],
        "source_owner": packet_task["source_owner"],
        "source_url": packet_task["source_url"],
        "estimated_minutes": estimated_minutes,
        "packet_reference": packet_reference,
        "patch_reference": patch["patch_id"],
        "sample_reference": sample["sample_id"],
        "form_reference": form["form_id"],
        "current_status": "draft_not_started",
        "reviewer_decision": form["reviewer_decision_section"]["reviewer_decision"],
        "recommended_next_action": form["follow_up_section"]["recommended_next_action"],
        "manual_steps": [
            "人工開啟 source_url",
            "記錄 page_title_or_dataset_title",
            "確認 official_owner",
            "檢查 license_or_terms_summary",
            "檢查 available_format",
            "記錄 update_cadence_observed",
            "檢查 personal_data_risk_observed",
            "檢查 private_complaint_risk_observed",
            "填寫 reviewer_notes",
            "不執行 crawler",
        ],
        "form_sections_to_fill": [
            "reviewer_fields",
            "source_identity_section",
            "license_terms_section",
            "format_section",
            "update_cadence_section",
            "risk_review_section",
            "evidence_summary_section",
            "reviewer_decision_section",
            "follow_up_section",
        ],
        "blocked_fields": list(MASTER_BLOCKED_FIELDS),
        "safety_notes": form["safety_notes"],
        "crawler_execution_allowed": False,
        "engineering_review_allowed": False,
    }


def build_open_data_day1_manual_review_operation_board(
    execution_packets_path: Path = SOURCE_EXECUTION_PACKETS,
    patch_drafts_path: Path = SOURCE_PATCH_DRAFTS,
    sample_results_path: Path = SOURCE_SAMPLE_RESULTS,
    form_draft_path: Path = SOURCE_FORM_DRAFT,
    output_path: Path = OUTPUT_PATH,
) -> dict[str, Any]:
    execution_packets = load_json(execution_packets_path)
    patch_drafts = load_json(patch_drafts_path)
    sample_results = load_json(sample_results_path)
    form_draft = load_json(form_draft_path)

    assert execution_packets["total_tasks"] == 10
    assert patch_drafts["total_count"] == 10
    assert sample_results["review_day"] == "day_1"
    assert sample_results["total_count"] == 3
    assert form_draft["review_day"] == "day_1"
    assert form_draft["total_count"] == 3

    day_packet = next(packet for packet in execution_packets["packets"] if packet["review_day"] == "day_1")
    day1_patches = [item for item in patch_drafts["patches"] if item["review_day"] == "day_1"]
    day1_samples = list(sample_results["samples"])
    day1_forms = list(form_draft["forms"])

    patch_by_result = {item["result_id"]: item for item in day1_patches}
    sample_by_result = {item["result_id"]: item for item in day1_samples}
    form_by_result = {item["result_id"]: item for item in day1_forms}

    assert len(day_packet["task_cards"]) == 3
    assert len(day1_patches) == 3
    assert len(day1_samples) == 3
    assert len(day1_forms) == 3

    task_cards: list[dict[str, Any]] = []
    total_estimated_minutes = 0
    for index, packet_task in enumerate(day_packet["task_cards"], start=1):
        result_id = packet_task["result_id"]
        patch = patch_by_result[result_id]
        sample = sample_by_result[result_id]
        form = form_by_result[result_id]
        estimated_minutes = 30
        total_estimated_minutes += estimated_minutes
        task_cards.append(
            build_task_card(
                task_number=index,
                packet_reference=day_packet["day_packet_id"],
                packet_task=packet_task,
                patch=patch,
                sample=sample,
                form=form,
                estimated_minutes=estimated_minutes,
            )
        )

    result = {
        "generated_at": now_iso(),
        "public_use_status": "internal_day1_manual_review_operation_board",
        "operation_board_only": True,
        "not_actual_review_result": True,
        "board_id": "open-data-day1-manual-review-operation-board",
        "board_title": "Day 1 人工審核操作看板",
        "review_day": "day_1",
        "source_execution_packets_file": "dashboard/data/open_data_manual_review_execution_packets.json",
        "source_patch_drafts_file": "dashboard/data/open_data_manual_review_result_patch_drafts.json",
        "source_sample_results_file": "dashboard/data/open_data_day1_sample_manual_review_results.json",
        "source_form_draft_file": "dashboard/data/open_data_day1_manual_review_form_draft.json",
        "total_tasks": 3,
        "board_status": "draft_not_started",
        "kpi_cards": [
            {"label": "今日任務數", "value": 3, "unit": "tasks"},
            {"label": "預估時間", "value": 90, "unit": "分鐘"},
            {"label": "表單草稿數", "value": 3, "unit": "forms"},
            {"label": "sample_only", "value": True, "unit": "flag"},
            {"label": "crawler_execution_allowed", "value": False, "unit": "flag"},
            {"label": "engineering_review_allowed_count", "value": 0, "unit": "count"},
        ],
        "workflow_steps": [
            "打開 Day 1 工作包",
            "逐筆人工開啟 source_url",
            "記錄來源頁標題",
            "確認是否官方來源",
            "記錄授權或使用條款",
            "記錄格式與更新頻率",
            "檢查是否有個資或私人陳情全文",
            "填寫 Day 1 審核表單草稿",
            "保持 crawler_execution_allowed false",
            "另開 PR 回填人工審核結果",
        ],
        "safety_checklist": [
            "這是操作看板，不是實際審核結果",
            "這不是 crawler",
            "不啟動 live crawler",
            "不對 source_url 發出網路請求",
            "不抓個資",
            "不抓私人陳情全文",
            "不自動發布",
            "crawler_execution_allowed 永遠 false",
            "engineering_review_allowed 預設 false",
        ],
        "task_cards": task_cards,
        "blocked_fields": list(MASTER_BLOCKED_FIELDS),
        "operation_notes": [
            "本頁只整理 day_1 的 3 筆人工審核任務。",
            "所有結果仍是草稿，僅示範今天要做什麼、要填什麼。",
            "source_url 只允許人工點開查看，不做任何自動請求。",
        ],
        "next_actions": [
            "先開啟 Day 1 工作包與 Day 1 審核表單草稿並排查看。",
            "逐筆記錄來源頁標題、授權條款、格式、更新頻率與風險觀察。",
            "完成後再另開 PR 回填人工審核結果，不直接改成完成狀態。",
        ],
        "crawler_execution_allowed": False,
        "engineering_review_allowed_count": 0,
        "no_live_crawler": True,
        "manual_review_required": True,
        "no_auto_publish": True,
        "no_personal_data": True,
    }

    assert result["total_tasks"] == 3
    assert result["review_day"] == "day_1"
    assert result["board_status"] == "draft_not_started"
    assert result["operation_board_only"] is True
    assert result["not_actual_review_result"] is True
    assert result["crawler_execution_allowed"] is False
    assert result["engineering_review_allowed_count"] == 0
    assert total_estimated_minutes == 90
    assert len(result["workflow_steps"]) >= 10
    assert len(result["task_cards"]) == 3

    for task_card in result["task_cards"]:
        assert task_card["crawler_execution_allowed"] is False
        assert task_card["engineering_review_allowed"] is False
        assert "approved_for_crawling" in task_card["blocked_fields"]
        assert "live_crawler" in task_card["blocked_fields"]

    serialized = json.dumps(result, ensure_ascii=False)
    assert '"approved_for_crawling": true' not in serialized
    assert '"live_crawler": true' not in serialized

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return result


def main() -> dict[str, Any]:
    return build_open_data_day1_manual_review_operation_board()


if __name__ == "__main__":
    main()

import json
from pathlib import Path

from scripts import build_open_data_day1_manual_review_operation_board as builder


ROOT = Path(__file__).resolve().parents[1]
PACKETS_PATH = ROOT / "dashboard" / "data" / "open_data_manual_review_execution_packets.json"
PATCH_DRAFTS_PATH = ROOT / "dashboard" / "data" / "open_data_manual_review_result_patch_drafts.json"
SAMPLE_RESULTS_PATH = ROOT / "dashboard" / "data" / "open_data_day1_sample_manual_review_results.json"
FORM_DRAFT_PATH = ROOT / "dashboard" / "data" / "open_data_day1_manual_review_form_draft.json"


def test_build_open_data_day1_manual_review_operation_board_writes_dashboard_json(tmp_path: Path) -> None:
    output_path = tmp_path / "open_data_day1_manual_review_operation_board.json"
    payload = builder.build_open_data_day1_manual_review_operation_board(
        PACKETS_PATH,
        PATCH_DRAFTS_PATH,
        SAMPLE_RESULTS_PATH,
        FORM_DRAFT_PATH,
        output_path,
    )

    assert output_path.exists()
    data = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["public_use_status"] == "internal_day1_manual_review_operation_board"
    assert data["public_use_status"] == "internal_day1_manual_review_operation_board"
    assert data["total_tasks"] == 3
    assert data["review_day"] == "day_1"
    assert data["operation_board_only"] is True
    assert data["not_actual_review_result"] is True
    assert data["board_status"] == "draft_not_started"
    assert data["engineering_review_allowed_count"] == 0
    assert data["crawler_execution_allowed"] is False
    assert data["no_live_crawler"] is True
    assert data["manual_review_required"] is True
    assert data["no_auto_publish"] is True
    assert data["no_personal_data"] is True


def test_build_open_data_day1_manual_review_operation_board_defaults_and_safety(tmp_path: Path) -> None:
    output_path = tmp_path / "open_data_day1_manual_review_operation_board.json"
    data = builder.build_open_data_day1_manual_review_operation_board(
        PACKETS_PATH,
        PATCH_DRAFTS_PATH,
        SAMPLE_RESULTS_PATH,
        FORM_DRAFT_PATH,
        output_path,
    )

    assert len(data["workflow_steps"]) >= 10
    assert len(data["task_cards"]) == 3
    for task_card in data["task_cards"]:
        assert task_card["crawler_execution_allowed"] is False
        assert task_card["engineering_review_allowed"] is False
        assert "approved_for_crawling" in task_card["blocked_fields"]
        assert "live_crawler" in task_card["blocked_fields"]
        assert task_card.get("approved_for_crawling") is None
        assert task_card.get("live_crawler") is None

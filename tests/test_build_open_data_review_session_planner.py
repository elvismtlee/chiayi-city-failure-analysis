import json
from pathlib import Path

from scripts import build_open_data_review_session_planner as builder


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "dashboard" / "data" / "open_data_engineering_review_checklist.json"


def test_build_open_data_review_session_planner_writes_dashboard_json(tmp_path: Path) -> None:
    output_path = tmp_path / "open_data_review_session_planner.json"
    payload = builder.build_open_data_review_session_planner(SOURCE, output_path)

    assert output_path.exists()
    data = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["public_use_status"] == "internal_review_session_planner"
    assert data["public_use_status"] == "internal_review_session_planner"
    assert data["total_count"] == 10
    assert data["source_checklist_count"] == 10
    assert data["engineering_review_allowed_count"] == 0
    assert data["crawler_execution_allowed"] is False
    assert data["no_live_crawler"] is True
    assert data["manual_review_required"] is True
    assert data["no_auto_publish"] is True
    assert data["no_personal_data"] is True


def test_build_open_data_review_session_planner_item_defaults_and_safety(tmp_path: Path) -> None:
    output_path = tmp_path / "open_data_review_session_planner.json"
    data = builder.build_open_data_review_session_planner(SOURCE, output_path)

    for item in data["session_tasks"]:
        assert item["crawler_execution_allowed"] is False
        assert item["engineering_review_allowed"] is False
        assert item["human_approval_required"] is True
        assert len(item["reviewer_action_items"]) >= 8
        assert len(item["evidence_to_record"]) >= 8
        assert len(item["completion_criteria"]) >= 7
        assert item["session_status"] != "approved_for_crawling"
        assert item["proposed_fetch_method"] != "live_crawler"

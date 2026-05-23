import json
from pathlib import Path

from scripts import build_open_data_engineering_review_checklist as builder


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "dashboard" / "data" / "open_data_human_review_workbook.json"


def test_build_open_data_engineering_review_checklist_writes_dashboard_json(tmp_path: Path) -> None:
    output_path = tmp_path / "open_data_engineering_review_checklist.json"
    payload = builder.build_open_data_engineering_review_checklist(SOURCE, output_path)

    assert output_path.exists()
    data = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["public_use_status"] == "internal_engineering_review_checklist"
    assert data["public_use_status"] == "internal_engineering_review_checklist"
    assert data["total_count"] == 10
    assert data["source_workbook_count"] == 10
    assert data["engineering_review_allowed_count"] == 0
    assert data["crawler_execution_allowed"] is False
    assert data["no_live_crawler"] is True
    assert data["manual_review_required"] is True
    assert data["no_auto_publish"] is True
    assert data["no_personal_data"] is True


def test_build_open_data_engineering_review_checklist_item_defaults_and_safety(tmp_path: Path) -> None:
    output_path = tmp_path / "open_data_engineering_review_checklist.json"
    data = builder.build_open_data_engineering_review_checklist(SOURCE, output_path)

    for item in data["checklists"]:
        assert item["crawler_execution_allowed"] is False
        assert item["engineering_review_allowed"] is False
        assert item["human_approval_required"] is True
        assert "source_review_gate" in item
        assert "human_approval_gate" in item
        assert item["engineering_review_status"] != "approved_for_crawling"
        assert item["proposed_fetch_method"] != "live_crawler"

import json
from pathlib import Path

from scripts import build_open_data_human_review_workbook as builder


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "dashboard" / "data" / "open_data_crawler_spec_drafts.json"


def test_build_open_data_human_review_workbook_writes_dashboard_json(tmp_path: Path) -> None:
    output_path = tmp_path / "open_data_human_review_workbook.json"
    payload = builder.build_open_data_human_review_workbook(SOURCE, output_path)

    assert output_path.exists()
    data = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["public_use_status"] == "internal_human_review_workbook"
    assert data["public_use_status"] == "internal_human_review_workbook"
    assert data["total_count"] == 10
    assert data["source_spec_count"] == 10
    assert data["engineering_review_allowed_count"] == 0
    assert data["crawler_execution_allowed"] is False
    assert data["no_live_crawler"] is True
    assert data["manual_review_required"] is True
    assert data["no_auto_publish"] is True
    assert data["no_personal_data"] is True


def test_build_open_data_human_review_workbook_item_defaults_and_safety(tmp_path: Path) -> None:
    output_path = tmp_path / "open_data_human_review_workbook.json"
    data = builder.build_open_data_human_review_workbook(SOURCE, output_path)

    for record in data["records"]:
        assert record["crawler_execution_allowed"] is False
        assert record["engineering_review_allowed"] is False
        assert record["human_approval_required"] is True
        assert "private_complaint_checked" in record
        assert "personal_data_checked" in record
        assert record["review_status"] != "approved_for_crawling"

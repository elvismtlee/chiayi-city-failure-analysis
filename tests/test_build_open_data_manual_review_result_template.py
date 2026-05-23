import json
from pathlib import Path

from scripts import build_open_data_manual_review_result_template as builder


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "dashboard" / "data" / "open_data_review_evidence_pack.json"


def test_build_open_data_manual_review_result_template_writes_dashboard_json(tmp_path: Path) -> None:
    output_path = tmp_path / "open_data_manual_review_result_template.json"
    payload = builder.build_open_data_manual_review_result_template(SOURCE, output_path)

    assert output_path.exists()
    data = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["public_use_status"] == "internal_manual_review_result_template"
    assert data["public_use_status"] == "internal_manual_review_result_template"
    assert data["total_count"] == 10
    assert data["source_evidence_pack_count"] == 10
    assert data["result_status_counts"]["not_started"] == 10
    assert data["reviewer_decision_counts"]["not_decided"] == 10
    assert data["engineering_review_allowed_count"] == 0
    assert data["crawler_execution_allowed"] is False
    assert data["no_live_crawler"] is True
    assert data["manual_review_required"] is True
    assert data["no_auto_publish"] is True
    assert data["no_personal_data"] is True


def test_build_open_data_manual_review_result_template_item_defaults_and_safety(tmp_path: Path) -> None:
    output_path = tmp_path / "open_data_manual_review_result_template.json"
    data = builder.build_open_data_manual_review_result_template(SOURCE, output_path)

    for item in data["results"]:
        assert item["crawler_execution_allowed"] is False
        assert item["engineering_review_allowed"] is False
        assert item["human_approval_required"] is True
        assert len(item["result_checklist"]) >= 10
        assert item["reviewer_decision"] != "approved_for_crawling"
        assert item.get("live_crawler") is None

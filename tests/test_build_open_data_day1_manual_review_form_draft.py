import json
from pathlib import Path

from scripts import build_open_data_day1_manual_review_form_draft as builder


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SAMPLE_RESULTS = ROOT / "dashboard" / "data" / "open_data_day1_sample_manual_review_results.json"


def test_build_open_data_day1_manual_review_form_draft_writes_dashboard_json(tmp_path: Path) -> None:
    output_path = tmp_path / "open_data_day1_manual_review_form_draft.json"
    doc_path = tmp_path / "day_1_manual_review_form_draft.md"
    payload = builder.build_open_data_day1_manual_review_form_draft(SOURCE_SAMPLE_RESULTS, output_path, doc_path)

    assert output_path.exists()
    data = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["public_use_status"] == "internal_day1_manual_review_form_draft"
    assert data["public_use_status"] == "internal_day1_manual_review_form_draft"
    assert data["total_count"] == 3
    assert data["source_sample_count"] == 3
    assert data["review_day"] == "day_1"
    assert data["form_draft_only"] is True
    assert data["not_actual_review_result"] is True
    assert data["form_status_counts"]["draft_not_started"] == 3
    assert data["engineering_review_allowed_count"] == 0
    assert data["crawler_execution_allowed"] is False
    assert data["no_live_crawler"] is True
    assert data["manual_review_required"] is True
    assert data["no_auto_publish"] is True
    assert data["no_personal_data"] is True


def test_build_open_data_day1_manual_review_form_draft_defaults_and_safety(tmp_path: Path) -> None:
    output_path = tmp_path / "open_data_day1_manual_review_form_draft.json"
    doc_path = tmp_path / "day_1_manual_review_form_draft.md"
    data = builder.build_open_data_day1_manual_review_form_draft(SOURCE_SAMPLE_RESULTS, output_path, doc_path)

    for form in data["forms"]:
        assert form["crawler_execution_allowed"] is False
        assert form["engineering_review_allowed"] is False
        assert form["reviewer_decision_section"]["reviewer_decision"] == "not_decided"
        assert "approved_for_crawling" in form["blocked_fields"]
        assert "live_crawler" in form["blocked_fields"]
        assert form.get("approved_for_crawling") is None
        assert form.get("live_crawler") is None

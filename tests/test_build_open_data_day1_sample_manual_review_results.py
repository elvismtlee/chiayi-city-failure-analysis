import json
from pathlib import Path

from scripts import build_open_data_day1_sample_manual_review_results as builder


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATCH_DRAFTS = ROOT / "dashboard" / "data" / "open_data_manual_review_result_patch_drafts.json"


def test_build_open_data_day1_sample_manual_review_results_writes_dashboard_json(tmp_path: Path) -> None:
    output_path = tmp_path / "open_data_day1_sample_manual_review_results.json"
    doc_path = tmp_path / "day_1_sample_manual_review_results.md"
    payload = builder.build_open_data_day1_sample_manual_review_results(SOURCE_PATCH_DRAFTS, output_path, doc_path)

    assert output_path.exists()
    data = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["public_use_status"] == "internal_day1_sample_manual_review_results"
    assert data["public_use_status"] == "internal_day1_sample_manual_review_results"
    assert data["total_count"] == 3
    assert data["source_patch_draft_count"] == 10
    assert data["review_day"] == "day_1"
    assert data["sample_only"] is True
    assert data["not_actual_review_result"] is True
    assert data["sample_status_counts"]["sample_not_actual_review"] == 3
    assert data["engineering_review_allowed_count"] == 0
    assert data["crawler_execution_allowed"] is False
    assert data["no_live_crawler"] is True
    assert data["manual_review_required"] is True
    assert data["no_auto_publish"] is True
    assert data["no_personal_data"] is True


def test_build_open_data_day1_sample_manual_review_results_defaults_and_safety(tmp_path: Path) -> None:
    output_path = tmp_path / "open_data_day1_sample_manual_review_results.json"
    doc_path = tmp_path / "day_1_sample_manual_review_results.md"
    data = builder.build_open_data_day1_sample_manual_review_results(SOURCE_PATCH_DRAFTS, output_path, doc_path)

    for sample in data["samples"]:
        assert sample["crawler_execution_allowed"] is False
        assert sample["engineering_review_allowed"] is False
        assert sample["human_approval_required"] is True
        assert sample["sample_reviewer_decision"] == "not_decided"
        assert "approved_for_crawling" in sample["blocked_fields"]
        assert "live_crawler" in sample["blocked_fields"]
        assert sample.get("approved_for_crawling") is None
        assert sample.get("live_crawler") is None

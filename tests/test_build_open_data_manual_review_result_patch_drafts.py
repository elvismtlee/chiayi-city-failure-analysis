import json
from pathlib import Path

from scripts import build_open_data_manual_review_result_patch_drafts as builder


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PACKETS = ROOT / "dashboard" / "data" / "open_data_manual_review_execution_packets.json"
SOURCE_RESULTS = ROOT / "dashboard" / "data" / "open_data_manual_review_result_template.json"


def test_build_open_data_manual_review_result_patch_drafts_writes_dashboard_json(tmp_path: Path) -> None:
    output_path = tmp_path / "open_data_manual_review_result_patch_drafts.json"
    docs_dir = tmp_path / "docs"
    payload = builder.build_open_data_manual_review_result_patch_drafts(SOURCE_PACKETS, SOURCE_RESULTS, output_path, docs_dir)

    assert output_path.exists()
    data = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["public_use_status"] == "internal_manual_review_result_patch_drafts"
    assert data["public_use_status"] == "internal_manual_review_result_patch_drafts"
    assert data["total_count"] == 10
    assert data["source_result_template_count"] == 10
    assert data["patch_status_counts"]["draft_not_started"] == 10
    assert data["review_days"]["day_1"] == 3
    assert data["review_days"]["day_2"] == 4
    assert data["review_days"]["day_3"] == 3
    assert data["engineering_review_allowed_count"] == 0
    assert data["crawler_execution_allowed"] is False
    assert data["no_live_crawler"] is True
    assert data["manual_review_required"] is True
    assert data["no_auto_publish"] is True
    assert data["no_personal_data"] is True


def test_build_open_data_manual_review_result_patch_drafts_defaults_and_safety(tmp_path: Path) -> None:
    output_path = tmp_path / "open_data_manual_review_result_patch_drafts.json"
    docs_dir = tmp_path / "docs"
    data = builder.build_open_data_manual_review_result_patch_drafts(SOURCE_PACKETS, SOURCE_RESULTS, output_path, docs_dir)

    for patch in data["patches"]:
        assert patch["crawler_execution_allowed"] is False
        assert patch["engineering_review_allowed"] is False
        assert patch["human_approval_required"] is True
        assert "approved_for_crawling" in patch["blocked_fields"]
        assert "live_crawler" in patch["blocked_fields"]
        assert patch.get("approved_for_crawling") is None
        assert patch.get("live_crawler") is None

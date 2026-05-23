import json
from pathlib import Path

from scripts import build_open_data_review_evidence_pack as builder


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "dashboard" / "data" / "open_data_review_session_planner.json"


def test_build_open_data_review_evidence_pack_writes_dashboard_json(tmp_path: Path) -> None:
    output_path = tmp_path / "open_data_review_evidence_pack.json"
    payload = builder.build_open_data_review_evidence_pack(SOURCE, output_path)

    assert output_path.exists()
    data = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["public_use_status"] == "internal_review_evidence_pack"
    assert data["public_use_status"] == "internal_review_evidence_pack"
    assert data["total_count"] == 10
    assert data["source_session_count"] == 10
    assert data["engineering_review_allowed_count"] == 0
    assert data["crawler_execution_allowed"] is False
    assert data["no_live_crawler"] is True
    assert data["manual_review_required"] is True
    assert data["no_auto_publish"] is True
    assert data["no_personal_data"] is True


def test_build_open_data_review_evidence_pack_item_defaults_and_safety(tmp_path: Path) -> None:
    output_path = tmp_path / "open_data_review_evidence_pack.json"
    data = builder.build_open_data_review_evidence_pack(SOURCE, output_path)

    for item in data["evidence_packs"]:
        assert item["crawler_execution_allowed"] is False
        assert item["engineering_review_allowed"] is False
        assert item["human_approval_required"] is True
        assert len(item["required_evidence_items"]) >= 10
        assert len(item["evidence_file_placeholders"]) >= 5
        assert len(item["acceptance_criteria"]) >= 8
        assert item["evidence_status"] != "approved_for_crawling"
        assert item.get("live_crawler") is None

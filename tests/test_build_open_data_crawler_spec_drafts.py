import json
from pathlib import Path

from scripts import build_open_data_crawler_spec_drafts as builder


ROOT = Path(__file__).resolve().parents[1]
TOP10 = ROOT / "dashboard" / "data" / "open_data_top10_review_tasks.json"


def test_build_open_data_crawler_spec_drafts_writes_dashboard_json(tmp_path: Path) -> None:
    output_path = tmp_path / "open_data_crawler_spec_drafts.json"
    payload = builder.build_open_data_crawler_spec_drafts(TOP10, output_path)

    assert output_path.exists()
    data = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["public_use_status"] == "internal_crawler_spec_drafts"
    assert data["public_use_status"] == "internal_crawler_spec_drafts"
    assert data["total_count"] == 10
    assert data["source_task_count"] == 10
    assert data["crawler_execution_allowed"] is False
    assert data["no_live_crawler"] is True
    assert data["manual_review_required"] is True
    assert data["no_auto_publish"] is True
    assert data["no_personal_data"] is True


def test_build_open_data_crawler_spec_drafts_item_defaults_and_safety(tmp_path: Path) -> None:
    output_path = tmp_path / "open_data_crawler_spec_drafts.json"
    data = builder.build_open_data_crawler_spec_drafts(TOP10, output_path)

    for spec in data["specs"]:
        assert spec["crawler_execution_allowed"] is False
        assert spec["human_approval_required"] is True
        assert spec["no_live_crawler"] is True
        assert len(spec["output_fields_draft"]) >= 7
        assert "no live crawler" in spec["safety_notes"]
        assert spec["proposed_fetch_method"] != "live_crawler"

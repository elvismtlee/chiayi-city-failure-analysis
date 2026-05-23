import json
from pathlib import Path

from scripts import build_open_data_readiness_report as builder


ROOT = Path(__file__).resolve().parents[1]
QUEUE = ROOT / "dashboard" / "data" / "open_data_url_review_queue.json"


def test_build_open_data_readiness_report_writes_dashboard_json(tmp_path: Path) -> None:
    output_path = tmp_path / "open_data_readiness_report.json"
    payload = builder.build_open_data_readiness_report(QUEUE, output_path)

    assert output_path.exists()
    data = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["public_use_status"] == "internal_readiness_report"
    assert data["public_use_status"] == "internal_readiness_report"
    assert data["total_count"] == 29
    assert data["source_queue_count"] == 29
    assert data["no_live_crawler"] is True
    assert data["manual_review_required"] is True
    assert data["no_auto_publish"] is True
    assert data["no_personal_data"] is True


def test_build_open_data_readiness_report_item_ranges_and_stage_rules(tmp_path: Path) -> None:
    output_path = tmp_path / "open_data_readiness_report.json"
    data = builder.build_open_data_readiness_report(QUEUE, output_path)

    valid_levels = {"high", "medium", "low", "blocked"}
    for item in data["items"]:
        assert 0 <= item["readiness_score"] <= 30
        assert item["readiness_level"] in valid_levels
        assert item["crawler_stage"] != "live_crawler"

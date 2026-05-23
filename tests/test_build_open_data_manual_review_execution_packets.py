import json
from pathlib import Path

from scripts import build_open_data_manual_review_execution_packets as builder


ROOT = Path(__file__).resolve().parents[1]
SOURCE_SOP = ROOT / "dashboard" / "data" / "open_data_manual_review_sop.json"
SOURCE_RESULTS = ROOT / "dashboard" / "data" / "open_data_manual_review_result_template.json"


def test_build_open_data_manual_review_execution_packets_writes_dashboard_json(tmp_path: Path) -> None:
    output_path = tmp_path / "open_data_manual_review_execution_packets.json"
    docs_dir = tmp_path / "docs"
    payload = builder.build_open_data_manual_review_execution_packets(SOURCE_SOP, SOURCE_RESULTS, output_path, docs_dir)

    assert output_path.exists()
    data = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["public_use_status"] == "internal_manual_review_execution_packets"
    assert data["public_use_status"] == "internal_manual_review_execution_packets"
    assert data["total_tasks"] == 10
    assert data["packet_count"] == 3
    assert data["review_days"]["day_1"] == 3
    assert data["review_days"]["day_2"] == 4
    assert data["review_days"]["day_3"] == 3
    assert data["estimated_total_minutes"] == 285
    assert data["engineering_review_allowed_count"] == 0
    assert data["crawler_execution_allowed"] is False
    assert data["no_live_crawler"] is True
    assert data["manual_review_required"] is True
    assert data["no_auto_publish"] is True
    assert data["no_personal_data"] is True


def test_build_open_data_manual_review_execution_packets_packet_defaults_and_safety(tmp_path: Path) -> None:
    output_path = tmp_path / "open_data_manual_review_execution_packets.json"
    docs_dir = tmp_path / "docs"
    data = builder.build_open_data_manual_review_execution_packets(SOURCE_SOP, SOURCE_RESULTS, output_path, docs_dir)

    for packet in data["packets"]:
        assert packet["task_cards"]
        assert packet["crawler_execution_allowed"] is False
        assert packet["engineering_review_allowed"] is False
        for task_card in packet["task_cards"]:
            assert task_card["crawler_execution_allowed"] is False
            assert task_card["engineering_review_allowed"] is False
            assert task_card["result_status"] != "approved_for_crawling"
            assert task_card.get("live_crawler") is None

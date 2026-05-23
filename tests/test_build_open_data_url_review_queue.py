import json
from pathlib import Path

from scripts import build_open_data_url_review_queue as builder


ROOT = Path(__file__).resolve().parents[1]
INVENTORY = ROOT / "dashboard" / "data" / "open_data_url_inventory.json"


def test_build_open_data_url_review_queue_writes_dashboard_json(tmp_path: Path) -> None:
    output_path = tmp_path / "open_data_url_review_queue.json"
    payload = builder.build_open_data_url_review_queue(INVENTORY, output_path)

    assert output_path.exists()
    data = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["public_use_status"] == "internal_url_review_queue"
    assert data["public_use_status"] == "internal_url_review_queue"
    assert data["total_count"] == 29
    assert data["source_inventory_count"] == 29
    assert data["no_live_crawler"] is True


def test_build_open_data_url_review_queue_default_review_fields_are_locked(tmp_path: Path) -> None:
    output_path = tmp_path / "open_data_url_review_queue.json"
    data = builder.build_open_data_url_review_queue(INVENTORY, output_path)

    assert data["total_count"] >= 20
    for item in data["items"]:
        assert item["url_review_status"] == "needs_manual_url_review"
        assert item["crawler_candidate"] is False
        assert item["crawler_priority"] == "none"

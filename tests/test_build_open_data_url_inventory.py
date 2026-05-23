import json
from pathlib import Path

from scripts import build_open_data_url_inventory as builder


ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "chiayi_open_data_url_inventory.yml"
REQUIRED_GROUPS = {
    "traffic_parking",
    "social_welfare",
    "culture_events",
    "public_works_environment",
    "complaints_service",
}


def test_build_open_data_url_inventory_writes_dashboard_json(tmp_path: Path) -> None:
    output_path = tmp_path / "open_data_url_inventory.json"
    payload = builder.build_open_data_url_inventory(CONFIG, output_path)

    assert output_path.exists()
    data = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["total_count"] == data["total_count"]
    assert data["public_use_status"] == "internal_url_inventory"
    assert data["total_count"] >= 20


def test_build_open_data_url_inventory_topic_groups_are_complete(tmp_path: Path) -> None:
    output_path = tmp_path / "open_data_url_inventory.json"
    data = builder.build_open_data_url_inventory(CONFIG, output_path)

    assert set(data["topic_groups"].keys()) == REQUIRED_GROUPS
    assert sum(data["topic_groups"].values()) == data["total_count"]

from pathlib import Path

from scripts.build_open_data_url_inventory import load_config as load_inventory_config

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "chiayi_open_data_url_inventory.yml"
REQUIRED_GROUPS = {
    "traffic_parking",
    "social_welfare",
    "culture_events",
    "public_works_environment",
    "complaints_service",
}


def load_config() -> dict:
    return load_config_from_builder()


def load_config_from_builder() -> dict:
    return load_inventory_config(CONFIG)


def test_open_data_url_inventory_config_exists_and_has_minimum_items() -> None:
    data = load_config()
    items = data["items"]
    assert CONFIG.exists()
    assert len(items) >= 20


def test_open_data_url_inventory_covers_required_topic_groups() -> None:
    items = load_config()["items"]
    topic_groups = {item["topic_group"] for item in items}
    assert REQUIRED_GROUPS <= topic_groups


def test_open_data_url_inventory_items_keep_required_safety_flags() -> None:
    items = load_config()["items"]
    for item in items:
        assert item["source_url"]
        assert item["source_owner"]
        assert item["review_status"] == "needs_manual_url_review"
        assert item["manual_review_required"] is True
        assert item["no_auto_publish"] is True
        assert item["no_personal_data"] is True

from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "chiayi_open_data_inventory.yml"
DOC = ROOT / "docs" / "chiayi_open_data_inventory.md"


def test_open_data_inventory_config_is_internal_and_safe() -> None:
    data = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    assert data["public_use_status"] == "internal_open_data_inventory"
    assert data["manual_review_required"] is True
    assert data["no_auto_publish"] is True
    assert data["no_personal_data"] is True
    assert data["timezone"] == "Asia/Taipei"


def test_open_data_inventory_has_priority_topics() -> None:
    data = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    inventory = data["inventory"]
    ids = {item["id"] for item in inventory}
    assert "chiayi_transport_parking" in ids
    assert "chiayi_social_welfare" in ids
    assert "chiayi_culture_events" in ids
    assert "chiayi_public_works_environment" in ids
    for item in inventory:
        assert item["review_status"] == "needs_dataset_url_review"
        assert item["expected_topics"]
        assert item["next_action"]


def test_open_data_inventory_doc_exists() -> None:
    content = DOC.read_text(encoding="utf-8")
    assert "嘉義市政府開放資料 Inventory" in content
    assert "交通與停車" in content
    assert "長照、兒少與社福" in content
    assert "文化活動與場館" in content
    assert "公共工程、環境與城市維護" in content

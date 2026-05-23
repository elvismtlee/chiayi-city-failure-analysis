from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
INVENTORY_PATH = ROOT / "dashboard" / "data" / "open_data_url_inventory.json"
OUTPUT_PATH = ROOT / "dashboard" / "data" / "open_data_url_review_queue.json"
TAIPEI_TZ = timezone(timedelta(hours=8))
REQUIRED_GROUPS = {
    "traffic_parking",
    "social_welfare",
    "culture_events",
    "public_works_environment",
    "complaints_service",
}


def now_iso() -> str:
    return datetime.now(TAIPEI_TZ).isoformat(timespec="seconds")


def load_inventory(path: Path = INVENTORY_PATH) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def build_queue_item(item: dict) -> dict:
    return {
        "id": item["id"],
        "inventory_id": item["id"],
        "title": item["title"],
        "topic_group": item["topic_group"],
        "source_owner": item["source_owner"],
        "source_url": item["source_url"],
        "official_domain": item["official_domain"],
        "source_type": item["source_type"],
        "expected_format": item["expected_format"],
        "license_status": item["license_status"],
        "update_cadence": item["update_cadence"],
        "west_district_relevance": item.get("west_district_relevance", ""),
        "dashboard_use": item["dashboard_use"],
        "url_review_status": "needs_manual_url_review",
        "source_reachability": "unknown",
        "official_source_verified": False,
        "license_reviewed": False,
        "crawler_candidate": False,
        "crawler_priority": "none",
        "crawler_blockers": [],
        "reviewed_by": "",
        "reviewed_at": "",
        "review_notes": "",
        "safety_notes": "no personal data / no auto publish / no live crawler",
    }


def validate_inventory(inventory: dict) -> list[dict]:
    items = inventory.get("items", [])
    total_count = int(inventory.get("total_count", 0))
    if not isinstance(items, list):
        raise ValueError("Inventory items must be a list")
    if len(items) < 20:
        raise ValueError("Open data URL inventory must contain at least 20 items")
    if len(items) != total_count:
        raise ValueError("Inventory total_count does not match items length")
    if len(items) != 29:
        raise ValueError("Open data URL inventory should currently contain 29 items")

    topic_groups = {item.get("topic_group") for item in items}
    missing_groups = REQUIRED_GROUPS - topic_groups
    if missing_groups:
        raise ValueError(f"Missing required topic groups: {', '.join(sorted(missing_groups))}")

    return items


def build_payload(inventory: dict) -> dict:
    items = validate_inventory(inventory)
    queue_items = [build_queue_item(item) for item in items]

    for item in queue_items:
        if item["url_review_status"] != "needs_manual_url_review":
            raise ValueError("Every queue item must start as needs_manual_url_review")
        if item["crawler_candidate"] is not False:
            raise ValueError("Every queue item must start with crawler_candidate false")
        if item["crawler_priority"] != "none":
            raise ValueError("Every queue item must start with crawler_priority none")

    topic_groups = Counter(item["topic_group"] for item in queue_items)
    topic_counts = {group: topic_groups.get(group, 0) for group in sorted(REQUIRED_GROUPS)}

    payload = {
        "generated_at": now_iso(),
        "public_use_status": "internal_url_review_queue",
        "source_inventory_count": inventory["total_count"],
        "total_count": len(queue_items),
        "topic_groups": topic_counts,
        "items": queue_items,
        "no_live_crawler": True,
        "manual_review_required": True,
        "no_auto_publish": True,
        "no_personal_data": True,
    }

    if payload["total_count"] != payload["source_inventory_count"]:
        raise ValueError("Review queue total_count must match source inventory count")

    return payload


def build_open_data_url_review_queue(
    inventory_path: Path = INVENTORY_PATH,
    output_path: Path = OUTPUT_PATH,
) -> dict:
    inventory = load_inventory(inventory_path)
    payload = build_payload(inventory)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload


def main() -> dict:
    return build_open_data_url_review_queue()


if __name__ == "__main__":
    main()

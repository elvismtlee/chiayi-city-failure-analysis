from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timezone, timedelta
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONFIG = ROOT / "config" / "chiayi_open_data_url_inventory.yml"
OUTPUT = ROOT / "dashboard" / "data" / "open_data_url_inventory.json"
GROUPS = {"traffic_parking", "social_welfare", "culture_events", "public_works_environment", "complaints_service"}


def build_open_data_url_inventory() -> dict:
    data = yaml.safe_load(CONFIG.read_text(encoding="utf-8"))
    items = data.get("items", [])
    if len(items) < 20:
        raise ValueError("inventory must contain at least 20 items")
    seen = {item.get("topic_group") for item in items}
    if GROUPS - seen:
        raise ValueError("missing required topic group")
    required = ["source_url", "source_owner", "review_status", "manual_review_required", "no_auto_publish", "no_personal_data"]
    for item in items:
        for key in required:
            if key not in item:
                raise ValueError(f"missing {key}")
        if item["review_status"] != "needs_manual_url_review":
            raise ValueError("bad review status")
        if not (item["manual_review_required"] and item["no_auto_publish"] and item["no_personal_data"]):
            raise ValueError("safety flags must be true")
    counts = Counter(item["topic_group"] for item in items)
    payload = {
        "generated_at": datetime.now(timezone(timedelta(hours=8))).isoformat(timespec="seconds"),
        "public_use_status": "internal_url_inventory",
        "total_count": len(items),
        "topic_groups": {group: counts.get(group, 0) for group in sorted(GROUPS)},
        "items": items,
    }
    OUTPUT.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload


if __name__ == "__main__":
    build_open_data_url_inventory()

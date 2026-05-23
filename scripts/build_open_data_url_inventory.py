from __future__ import annotations

import json
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlparse

try:
    import yaml
except Exception:  # pragma: no cover - local runtime fallback
    yaml = None


ROOT = Path(__file__).resolve().parents[1]
CONFIG_PATH = ROOT / "config" / "chiayi_open_data_url_inventory.yml"
OUTPUT_PATH = ROOT / "dashboard" / "data" / "open_data_url_inventory.json"
TAIPEI_TZ = timezone(timedelta(hours=8))
REQUIRED_GROUPS = {
    "traffic_parking",
    "social_welfare",
    "culture_events",
    "public_works_environment",
    "complaints_service",
}
REQUIRED_FIELDS = {
    "id",
    "title",
    "topic_group",
    "source_owner",
    "source_type",
    "source_url",
    "official_domain",
    "expected_format",
    "license_status",
    "update_cadence",
    "west_district_relevance",
    "dashboard_use",
    "review_status",
    "no_personal_data",
    "no_auto_publish",
    "manual_review_required",
    "notes",
}
BLOCKED_HOSTS = {
    "wikipedia.org",
    "facebook.com",
    "threads.net",
    "line.me",
    "youtube.com",
    "tiktok.com",
}


def now_iso() -> str:
    return datetime.now(TAIPEI_TZ).isoformat(timespec="seconds")


def _parse_scalar(value: str):
    text = value.strip()
    if text == "true":
        return True
    if text == "false":
        return False
    return text


def _load_simple_yaml(text: str) -> dict:
    data: dict = {}
    items: list[dict] = []
    current_item: dict | None = None

    for raw_line in text.splitlines():
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue

        indent = len(raw_line) - len(raw_line.lstrip(" "))
        line = raw_line.strip()

        if indent == 0:
            key, value = line.split(":", 1)
            key = key.strip()
            if value.strip():
                data[key] = _parse_scalar(value)
            elif key == "items":
                data[key] = items
            else:
                data[key] = {}
            continue

        if indent == 2 and line.startswith("- "):
            current_item = {}
            items.append(current_item)
            remainder = line[2:]
            if remainder:
                key, value = remainder.split(":", 1)
                current_item[key.strip()] = _parse_scalar(value)
            continue

        if indent == 4 and current_item is not None:
            key, value = line.split(":", 1)
            current_item[key.strip()] = _parse_scalar(value)

    return data


def load_config(path: Path = CONFIG_PATH) -> dict:
    text = path.read_text(encoding="utf-8")
    if yaml is not None and hasattr(yaml, "safe_load"):
        return yaml.safe_load(text)
    return _load_simple_yaml(text)


def _validate_item(item: dict, index: int) -> None:
    missing_fields = [field for field in REQUIRED_FIELDS if field not in item]
    if missing_fields:
        raise ValueError(f"Item #{index} missing fields: {', '.join(sorted(missing_fields))}")

    empty_fields = [
        field for field in REQUIRED_FIELDS
        if field not in {"no_personal_data", "no_auto_publish", "manual_review_required"}
        and not str(item.get(field, "")).strip()
    ]
    if empty_fields:
        raise ValueError(f"Item #{index} has empty required fields: {', '.join(sorted(empty_fields))}")

    if item["review_status"] != "needs_manual_url_review":
        raise ValueError(f"Item #{index} review_status must be needs_manual_url_review")

    for field in ("manual_review_required", "no_auto_publish", "no_personal_data"):
        if item[field] is not True:
            raise ValueError(f"Item #{index} field {field} must be true")

    parsed = urlparse(item["source_url"])
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError(f"Item #{index} has invalid source_url: {item['source_url']}")

    hostname = parsed.netloc.lower()
    if any(blocked in hostname for blocked in BLOCKED_HOSTS):
        raise ValueError(f"Item #{index} uses blocked non-official host: {hostname}")

    official_domain = str(item["official_domain"]).lower()
    if official_domain not in hostname:
        raise ValueError(
            f"Item #{index} source_url host {hostname} does not match official_domain {official_domain}"
        )


def validate_inventory(config: dict) -> list[dict]:
    items = config.get("items")
    if not isinstance(items, list):
        raise ValueError("Config items must be a list")
    if len(items) < 20:
        raise ValueError("Open data URL inventory must contain at least 20 items")

    topic_groups = set()
    for index, item in enumerate(items, start=1):
        if not isinstance(item, dict):
            raise ValueError(f"Item #{index} must be an object")
        _validate_item(item, index)
        topic_groups.add(item["topic_group"])

    missing_groups = REQUIRED_GROUPS - topic_groups
    if missing_groups:
        raise ValueError(f"Missing required topic groups: {', '.join(sorted(missing_groups))}")

    return items


def build_output(items: list[dict]) -> dict:
    counts = Counter(item["topic_group"] for item in items)
    ordered_counts = {group: counts.get(group, 0) for group in sorted(REQUIRED_GROUPS)}
    return {
        "generated_at": now_iso(),
        "public_use_status": "internal_url_inventory",
        "total_count": len(items),
        "topic_groups": ordered_counts,
        "items": items,
        "notes": [
            "第二批真實資料來源盤點，先審核官方 URL，不啟動 crawler。",
            "internal dashboard / manual review required / no auto publish",
            "不抓個資、不抓私人陳情、不抓私人案件全文。",
        ],
    }


def build_open_data_url_inventory(
    config_path: Path = CONFIG_PATH,
    output_path: Path = OUTPUT_PATH,
) -> dict:
    config = load_config(config_path)
    items = validate_inventory(config)
    payload = build_output(items)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return payload


def main() -> dict:
    return build_open_data_url_inventory()


if __name__ == "__main__":
    main()

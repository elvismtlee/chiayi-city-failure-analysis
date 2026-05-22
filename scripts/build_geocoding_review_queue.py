from __future__ import annotations

import json
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "dashboard" / "data"
HOTSPOTS_JSON = DATA_DIR / "hotspots.json"
HOTSPOTS_GEOJSON = DATA_DIR / "hotspots.geojson"
LOCAL_PLACE_DICTIONARY = DATA_DIR / "local_place_dictionary.json"
OUTPUT_JSON = DATA_DIR / "geocoding_review_queue.json"

REVIEW_GEO_PRECISION = {"prototype", "unknown", "uncertain"}
REVIEW_STATUS = {"prototype", "uncertain", "unreviewed"}
PLACE_NAME_REPLACEMENTS = {
    "文化路夜市": "文化路商圈",
}
SENSITIVE_KEYS = {
    "phone",
    "mobile",
    "email",
    "national_id",
    "id_number",
    "address",
    "full_address",
    "name_of_reporter",
}


def load_json(path: Path, fallback: Any) -> Any:
    if not path.exists():
        return fallback
    return json.loads(path.read_text(encoding="utf-8"))


def load_place_dictionary() -> dict[str, dict[str, Any]]:
    records = load_json(LOCAL_PLACE_DICTIONARY, [])
    if not isinstance(records, list):
        return {}
    return {
        str(item.get("place_id")): item
        for item in records
        if isinstance(item, dict) and item.get("place_id")
    }


def score_priority(score: Any) -> str:
    try:
        numeric = float(score)
    except (TypeError, ValueError):
        numeric = 0
    if numeric >= 85:
        return "high"
    if numeric >= 70:
        return "medium"
    return "low"


def sanitize_query_part(value: Any) -> str:
    return " ".join(str(value or "").split())


def normalize_place_name(value: Any) -> str:
    place_name = sanitize_query_part(value)
    for banned_term, preferred_term in PLACE_NAME_REPLACEMENTS.items():
        place_name = place_name.replace(banned_term, preferred_term)
    return place_name


def build_suggested_query(district: str, place_name: str) -> str:
    parts = ["嘉義市", sanitize_query_part(district), normalize_place_name(place_name)]
    return " ".join(part for part in parts if part)


def feature_needs_review(properties: dict[str, Any]) -> bool:
    geo_precision = str(properties.get("geo_precision") or "unknown")
    review_status = str(properties.get("review_status") or "unreviewed")
    return geo_precision in REVIEW_GEO_PRECISION or review_status in REVIEW_STATUS


def geojson_feature_lookup(geojson: dict[str, Any]) -> dict[str, dict[str, Any]]:
    features = geojson.get("features") if isinstance(geojson, dict) else []
    lookup: dict[str, dict[str, Any]] = {}
    if not isinstance(features, list):
        return lookup

    for index, feature in enumerate(features):
        if not isinstance(feature, dict):
            continue
        properties = feature.get("properties") or {}
        if not isinstance(properties, dict):
            properties = {}
        key = str(properties.get("place_id") or feature.get("id") or f"hotspot-{index + 1}")
        lookup[key] = feature
    return lookup


def get_coordinates(feature: dict[str, Any]) -> tuple[float | None, float | None]:
    coordinates = ((feature.get("geometry") or {}).get("coordinates") or [])
    if not isinstance(coordinates, list) or len(coordinates) != 2:
        return None, None
    try:
        lng = float(coordinates[0])
        lat = float(coordinates[1])
    except (TypeError, ValueError):
        return None, None
    return lng, lat


def safe_queue_item(item: dict[str, Any]) -> dict[str, Any]:
    lowered = {str(key).lower() for key in item.keys()}
    blocked = lowered & SENSITIVE_KEYS
    if blocked:
        raise ValueError(f"Queue item contains sensitive fields: {sorted(blocked)}")
    return item


def build_queue() -> list[dict[str, Any]]:
    hotspots = load_json(HOTSPOTS_JSON, [])
    geojson = load_json(HOTSPOTS_GEOJSON, {"features": []})
    place_dictionary = load_place_dictionary()
    feature_lookup = geojson_feature_lookup(geojson)

    if not isinstance(hotspots, list):
        return []

    queue: list[dict[str, Any]] = []
    for index, hotspot in enumerate(hotspots):
        if not isinstance(hotspot, dict):
            continue
        fallback_id = f"hotspot-{index + 1}"
        candidate_id = str(hotspot.get("place_id") or fallback_id)
        feature = feature_lookup.get(candidate_id) or feature_lookup.get(fallback_id) or {}
        properties = feature.get("properties") or {}
        if not isinstance(properties, dict):
            properties = {}

        if not feature_needs_review(properties):
            continue

        lng, lat = get_coordinates(feature)
        place_record = place_dictionary.get(candidate_id, {})
        place_name = normalize_place_name(
            properties.get("name")
            or place_record.get("display_name")
            or hotspot.get("name")
            or candidate_id
        )
        district = str(properties.get("district") or hotspot.get("district") or "嘉義市")
        score = properties.get("score", hotspot.get("score", 0))

        queue_item = {
            "candidate_id": candidate_id,
            "place_name": place_name,
            "district": district,
            "category": str(properties.get("category") or hotspot.get("category") or "待分類"),
            "department": str(properties.get("department") or hotspot.get("department") or "待確認"),
            "score": float(score or 0),
            "current_lng": lng,
            "current_lat": lat,
            "geo_precision": str(properties.get("geo_precision") or "unknown"),
            "review_status": str(properties.get("review_status") or "unreviewed"),
            "suggested_query": build_suggested_query(district, place_name),
            "suggested_review_method": "manual_review_with_public_map",
            "priority": score_priority(score),
            "source": "dashboard/data/hotspots.geojson",
            "notes": "目前不是正式精準座標；需要人工確認後，才能標示為 reviewed 或 verified。",
        }
        queue.append(safe_queue_item(queue_item))

    priority_order = {"high": 0, "medium": 1, "low": 2}
    return sorted(queue, key=lambda item: (priority_order[item["priority"]], item["candidate_id"]))


def write_queue(output_path: Path = OUTPUT_JSON) -> list[dict[str, Any]]:
    queue = build_queue()
    output_path.write_text(json.dumps(queue, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return queue


if __name__ == "__main__":
    queue = write_queue()
    print(f"Wrote {OUTPUT_JSON.relative_to(ROOT)} with {len(queue)} candidates")

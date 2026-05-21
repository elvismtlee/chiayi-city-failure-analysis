from __future__ import annotations

import json
from datetime import date
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
HOTSPOTS_JSON = ROOT / "dashboard" / "data" / "hotspots.json"
HOTSPOTS_GEOJSON = ROOT / "dashboard" / "data" / "hotspots.geojson"

FALLBACK_COORDS = [
    (120.4497, 23.4808),
    (120.4456, 23.4787),
    (120.4528, 23.4758),
]

ISSUE_TAG_RULES = {
    "停車": ["traffic", "parking"],
    "交通": ["traffic"],
    "人行": ["pedestrian"],
    "垃圾": ["environment"],
    "環境": ["environment"],
    "市場": ["market"],
    "商圈": ["market"],
    "動線": ["market"],
    "通學": ["school"],
    "學校": ["school"],
    "排水": ["drainage"],
    "公共安全": ["safety"],
    "安全": ["safety"],
}

VALID_GEO_PRECISION = {
    "exact",
    "road_segment",
    "landmark",
    "village",
    "district",
    "prototype",
    "unknown",
}
VALID_REVIEW_STATUS = {"verified", "reviewed", "prototype", "uncertain", "rejected"}
SENSITIVE_KEYS = {
    "phone",
    "mobile",
    "email",
    "national_id",
    "id_number",
    "full_address",
    "address",
    "name_of_reporter",
}


def load_hotspots(path: Path = HOTSPOTS_JSON) -> list[dict[str, Any]]:
    return json.loads(path.read_text(encoding="utf-8"))


def _number(value: Any) -> float | None:
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return float(value)
    try:
        return float(str(value).strip())
    except (TypeError, ValueError):
        return None


def get_coordinates(hotspot: dict[str, Any], index: int) -> tuple[list[float], str, str]:
    lat = _number(hotspot.get("lat"))
    lng = _number(hotspot.get("lng"))
    if lat is not None and lng is not None:
        return [lng, lat], "exact", "reviewed"

    fallback_lng, fallback_lat = FALLBACK_COORDS[index % len(FALLBACK_COORDS)]
    return [fallback_lng, fallback_lat], "prototype", "prototype"


def infer_issue_tags(hotspot: dict[str, Any]) -> list[str]:
    text = " ".join(
        str(hotspot.get(field, ""))
        for field in ("name", "category", "department", "action")
    )
    tags: list[str] = []
    for keyword, keyword_tags in ISSUE_TAG_RULES.items():
        if keyword in text:
            for tag in keyword_tags:
                if tag not in tags:
                    tags.append(tag)
    return tags


def safe_score(value: Any) -> float:
    score = _number(value)
    if score is None:
        return 0
    return max(0, min(score, 100))


def hotspot_to_feature(hotspot: dict[str, Any], index: int) -> dict[str, Any]:
    coordinates, geo_precision, review_status = get_coordinates(hotspot, index)
    name = str(hotspot.get("name") or f"hotspot-{index + 1}")
    feature_id = str(hotspot.get("place_id") or f"hotspot-{index + 1}")

    properties = {
        "name": name,
        "district": str(hotspot.get("district") or "待確認"),
        "category": str(hotspot.get("category") or "待分類"),
        "department": str(hotspot.get("department") or "待確認"),
        "score": safe_score(hotspot.get("score")),
        "action": str(hotspot.get("action") or "待研擬"),
        "issue_tags": infer_issue_tags(hotspot),
        "source_count": int(hotspot.get("source_count") or 0),
        "geo_precision": geo_precision,
        "review_status": review_status,
    }
    if hotspot.get("place_id"):
        properties["place_id"] = str(hotspot["place_id"])

    return {
        "type": "Feature",
        "id": feature_id,
        "geometry": {
            "type": "Point",
            "coordinates": coordinates,
        },
        "properties": properties,
    }


def validate_feature(feature: dict[str, Any]) -> None:
    if feature.get("type") != "Feature":
        raise ValueError("GeoJSON feature must use type=Feature")
    geometry = feature.get("geometry") or {}
    if geometry.get("type") != "Point":
        raise ValueError("First phase hotspot geometry must use Point")
    coordinates = geometry.get("coordinates")
    if not isinstance(coordinates, list) or len(coordinates) != 2:
        raise ValueError("Feature coordinates must be [lng, lat]")
    lng, lat = coordinates
    if _number(lng) is None or _number(lat) is None:
        raise ValueError("Feature coordinates must be numeric")

    properties = feature.get("properties") or {}
    if properties.get("geo_precision") not in VALID_GEO_PRECISION:
        raise ValueError("Invalid geo_precision")
    if properties.get("review_status") not in VALID_REVIEW_STATUS:
        raise ValueError("Invalid review_status")
    score = _number(properties.get("score"))
    if score is None or score < 0 or score > 100:
        raise ValueError("Score must be between 0 and 100")

    lowered_keys = {str(key).lower() for key in properties.keys()}
    if lowered_keys & SENSITIVE_KEYS:
        raise ValueError("GeoJSON properties must not contain sensitive fields")


def build_geojson(hotspots: list[dict[str, Any]]) -> dict[str, Any]:
    features = [hotspot_to_feature(hotspot, index) for index, hotspot in enumerate(hotspots)]
    for feature in features:
        validate_feature(feature)

    return {
        "type": "FeatureCollection",
        "metadata": {
            "updated_at": date.today().isoformat(),
            "source": "dashboard/data/hotspots.json",
            "status": "prototype",
            "geo_precision_note": "部分座標為 prototype fallback，待正式 geocoding 更新。",
        },
        "features": features,
    }


def write_geojson(output_path: Path = HOTSPOTS_GEOJSON) -> dict[str, Any]:
    geojson = build_geojson(load_hotspots())
    output_path.write_text(
        json.dumps(geojson, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    return geojson


if __name__ == "__main__":
    write_geojson()
    print(f"Wrote {HOTSPOTS_GEOJSON.relative_to(ROOT)}")

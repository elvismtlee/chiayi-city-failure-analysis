import json
from pathlib import Path

from scripts.build_hotspots_geojson import build_geojson, get_coordinates, infer_issue_tags


ROOT = Path(__file__).resolve().parents[1]
GEOJSON = ROOT / "dashboard" / "data" / "hotspots.geojson"
HOTSPOTS = ROOT / "dashboard" / "data" / "hotspots.json"


def test_generated_hotspots_geojson_exists_and_parses() -> None:
    assert GEOJSON.exists()
    data = json.loads(GEOJSON.read_text(encoding="utf-8"))
    assert data["type"] == "FeatureCollection"
    assert isinstance(data["features"], list)
    assert data["features"]


def test_geojson_feature_count_matches_hotspots_json() -> None:
    geojson = json.loads(GEOJSON.read_text(encoding="utf-8"))
    hotspots = json.loads(HOTSPOTS.read_text(encoding="utf-8"))
    assert len(geojson["features"]) == len(hotspots)


def test_geojson_coordinates_use_lng_lat_order() -> None:
    geojson = json.loads(GEOJSON.read_text(encoding="utf-8"))
    for feature in geojson["features"]:
        lng, lat = feature["geometry"]["coordinates"]
        assert 120 <= lng <= 121
        assert 23 <= lat <= 24


def test_prototype_fallback_marks_geo_precision() -> None:
    coordinates, geo_precision, review_status = get_coordinates({}, 0)
    assert coordinates == [120.4497, 23.4808]
    assert geo_precision == "prototype"
    assert review_status == "prototype"


def test_build_geojson_marks_prototype_metadata() -> None:
    geojson = build_geojson([
        {
            "name": "測試熱點",
            "district": "西區",
            "category": "停車",
            "department": "交通處",
            "score": 80,
            "action": "測試改善行動",
        }
    ])
    assert geojson["metadata"]["status"] == "prototype"
    feature = geojson["features"][0]
    assert feature["properties"]["geo_precision"] == "prototype"
    assert feature["properties"]["review_status"] == "prototype"


def test_infer_issue_tags_from_hotspot_text() -> None:
    tags = infer_issue_tags({"category": "停車 / 人行", "action": "商圈動線改善"})
    assert "traffic" in tags
    assert "parking" in tags
    assert "pedestrian" in tags
    assert "market" in tags


def test_geojson_scores_are_bounded() -> None:
    geojson = build_geojson([
        {"name": "高分", "score": 999},
        {"name": "低分", "score": -20},
    ])
    scores = [feature["properties"]["score"] for feature in geojson["features"]]
    assert scores == [100, 0]

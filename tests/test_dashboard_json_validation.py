import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DASHBOARD_DATA_DIR = ROOT / "dashboard" / "data"

REQUIRED_JSON_FILES = [
    "dashboard_summary.json",
    "issue_ranking.json",
    "issue_trends.json",
    "hotspots.json",
    "hotspots.geojson",
    "geocoding_review_queue.json",
    "transcript_review_queue.json",
    "local_place_dictionary.json",
    "open_data_url_inventory.json",
    "open_data_url_review_queue.json",
    "open_data_readiness_report.json",
    "open_data_top10_review_tasks.json",
    "open_data_crawler_spec_drafts.json",
    "open_data_human_review_workbook.json",
    "site_map.json",
]

SENSITIVE_FIELD_NAMES = {
    "phone",
    "mobile",
    "email",
    "national_id",
    "id_number",
    "address",
    "full_address",
}

VALID_TRENDS = {"up", "down", "stable", "spike"}
VALID_TREND_REVIEW_STATUS = {"prototype", "uncertain", "unreviewed", "reviewed"}
VALID_GEO_PRECISION = {"exact", "road_segment", "landmark", "village", "district", "prototype", "unknown", "uncertain"}
VALID_GEO_REVIEW_STATUS = {"verified", "reviewed", "prototype", "uncertain", "unreviewed", "rejected"}
VALID_GEOCODING_PRIORITY = {"high", "medium", "low"}
VALID_TRANSCRIPT_STATUS = {"not_started", "queued", "transcribed", "reviewed", "rejected"}
VALID_TRANSCRIPT_REVIEW_STATUS = {"unreviewed", "needs_metadata_review", "reviewed", "rejected"}
VALID_TRANSCRIPT_PRIORITY = {"needs_metadata_review", "medium", "normal"}


def load_json(filename: str):
    path = DASHBOARD_DATA_DIR / filename
    return json.loads(path.read_text(encoding="utf-8"))


def walk_json(value):
    if isinstance(value, dict):
        yield value
        for child in value.values():
            yield from walk_json(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_json(child)


def assert_number(value, field_name: str) -> None:
    assert isinstance(value, (int, float)) and not isinstance(value, bool), (
        f"{field_name} must be a number"
    )


def test_dashboard_json_files_exist_and_parse() -> None:
    for filename in REQUIRED_JSON_FILES:
        path = DASHBOARD_DATA_DIR / filename
        assert path.exists(), f"Missing dashboard JSON file: {filename}"
        load_json(filename)


def test_dashboard_summary_required_fields() -> None:
    summary = load_json("dashboard_summary.json")

    for field in ["updated_at", "total_cases", "top_issue", "total_hotspots", "total_questions"]:
        assert field in summary

    assert isinstance(summary["updated_at"], str)
    assert isinstance(summary["top_issue"], str)
    for field in ["total_cases", "total_hotspots", "total_questions"]:
        assert_number(summary[field], field)
        assert summary[field] >= 0


def test_issue_ranking_schema() -> None:
    issue_ranking = load_json("issue_ranking.json")
    assert isinstance(issue_ranking, list)
    assert issue_ranking

    for index, item in enumerate(issue_ranking):
        assert isinstance(item, dict), f"issue_ranking item #{index} must be an object"
        assert isinstance(item.get("issue"), str)
        assert "count" in item or "score" in item
        if "count" in item:
            assert_number(item["count"], "count")
            assert item["count"] >= 0
        if "score" in item:
            assert_number(item["score"], "score")
            assert 0 <= item["score"] <= 100
        if "percent" in item:
            assert_number(item["percent"], "percent")
            assert 0 <= item["percent"] <= 100
        if "trend" in item:
            assert item["trend"] in VALID_TRENDS


def test_hotspots_schema_and_score_range() -> None:
    hotspots = load_json("hotspots.json")
    assert isinstance(hotspots, list)
    assert hotspots

    required_fields = ["name", "district", "category", "score", "action"]
    for index, item in enumerate(hotspots):
        assert isinstance(item, dict), f"hotspots item #{index} must be an object"
        for field in required_fields:
            assert field in item, f"hotspots item #{index} missing {field}"
        for field in ["name", "district", "category", "action"]:
            assert isinstance(item[field], str)
            assert item[field].strip()
        assert_number(item["score"], "score")
        assert 0 <= item["score"] <= 100
        for field in ["lat", "lng", "x", "y"]:
            if field in item and item[field] is not None:
                assert_number(item[field], field)


def test_hotspots_geojson_schema() -> None:
    geojson = load_json("hotspots.geojson")
    assert geojson["type"] == "FeatureCollection"
    assert isinstance(geojson.get("metadata"), dict)
    assert geojson["metadata"].get("source") == "dashboard/data/hotspots.json"
    assert isinstance(geojson.get("features"), list)
    assert geojson["features"]

    for index, feature in enumerate(geojson["features"]):
        assert feature.get("type") == "Feature", f"feature #{index} must be a Feature"
        geometry = feature.get("geometry") or {}
        assert geometry.get("type") == "Point", f"feature #{index} must be a Point"
        coordinates = geometry.get("coordinates")
        assert isinstance(coordinates, list) and len(coordinates) == 2
        lng, lat = coordinates
        assert_number(lng, "lng")
        assert_number(lat, "lat")
        assert 120 <= lng <= 121
        assert 23 <= lat <= 24

        properties = feature.get("properties") or {}
        for field in ["name", "district", "category", "department", "score", "action", "issue_tags", "source_count", "geo_precision", "review_status"]:
            assert field in properties, f"feature #{index} missing {field}"
        assert_number(properties["score"], "score")
        assert 0 <= properties["score"] <= 100
        assert isinstance(properties["issue_tags"], list)
        assert_number(properties["source_count"], "source_count")
        assert properties["geo_precision"] in VALID_GEO_PRECISION
        assert properties["review_status"] in VALID_GEO_REVIEW_STATUS


def test_hotspots_geojson_feature_count_matches_hotspots_json() -> None:
    hotspots = load_json("hotspots.json")
    geojson = load_json("hotspots.geojson")
    assert len(geojson["features"]) == len(hotspots)


def test_geocoding_review_queue_schema() -> None:
    queue = load_json("geocoding_review_queue.json")
    assert isinstance(queue, list)
    assert queue
    required_fields = [
        "candidate_id",
        "place_name",
        "district",
        "category",
        "department",
        "score",
        "current_lng",
        "current_lat",
        "geo_precision",
        "review_status",
        "suggested_query",
        "suggested_review_method",
        "priority",
        "source",
        "notes",
    ]
    for index, item in enumerate(queue):
        assert isinstance(item, dict), f"queue item #{index} must be an object"
        for field in required_fields:
            assert field in item, f"queue item #{index} missing {field}"
        for field in ["candidate_id", "place_name", "district", "category", "department", "suggested_query", "suggested_review_method", "priority", "source", "notes"]:
            assert isinstance(item[field], str)
            assert item[field].strip()
        assert "嘉義市" in item["suggested_query"]
        assert item["suggested_review_method"] == "manual_review_with_public_map"
        assert item["priority"] in VALID_GEOCODING_PRIORITY
        assert_number(item["score"], "score")
        assert 0 <= item["score"] <= 100
        assert_number(item["current_lng"], "current_lng")
        assert_number(item["current_lat"], "current_lat")
        assert item["geo_precision"] in VALID_GEO_PRECISION
        assert item["review_status"] in VALID_GEO_REVIEW_STATUS
        if item["geo_precision"] == "prototype":
            assert item["review_status"] != "verified"


def test_transcript_review_queue_schema() -> None:
    queue = load_json("transcript_review_queue.json")
    assert isinstance(queue, list)
    assert queue
    required_fields = [
        "queue_id",
        "source_id",
        "councilor_name",
        "council_term",
        "session_name",
        "video_title",
        "video_url",
        "video_platform",
        "video_id",
        "meeting_date",
        "topic_guess",
        "raw_hash",
        "transcript_status",
        "review_status",
        "priority",
        "needs_metadata_review",
        "recommended_action",
        "notes",
    ]
    for index, item in enumerate(queue):
        assert isinstance(item, dict), f"transcript queue item #{index} must be an object"
        for field in required_fields:
            assert field in item, f"transcript queue item #{index} missing {field}"
        assert item["queue_id"].startswith("cycc-transcript-")
        assert item["source_id"] == "CYCC_QUESTION_VIDEO"
        assert isinstance(item["needs_metadata_review"], bool)
        assert item["transcript_status"] in VALID_TRANSCRIPT_STATUS
        assert item["review_status"] in VALID_TRANSCRIPT_REVIEW_STATUS
        assert item["priority"] in VALID_TRANSCRIPT_PRIORITY
        assert item["recommended_action"] == "manual_transcript_or_asr_review"
        assert "不呼叫 Whisper" in item["notes"]


def test_issue_trends_schema() -> None:
    issue_trends = load_json("issue_trends.json")
    assert isinstance(issue_trends, list)
    assert issue_trends

    required_fields = [
        "issue",
        "current_count",
        "previous_count",
        "change_percent",
        "trend",
        "window_days",
        "confidence",
        "summary",
        "review_status",
    ]
    window_days = set()
    for index, item in enumerate(issue_trends):
        assert isinstance(item, dict), f"issue_trends item #{index} must be an object"
        for field in required_fields:
            assert field in item, f"issue_trends item #{index} missing {field}"
        assert isinstance(item["issue"], str)
        for field in ["current_count", "previous_count", "change_percent", "window_days", "confidence"]:
            assert_number(item[field], field)
        assert item["current_count"] >= 0
        assert item["previous_count"] >= 0
        assert item["window_days"] in {7, 30, 90}
        assert 0 <= item["confidence"] <= 1
        assert item["trend"] in VALID_TRENDS
        assert isinstance(item["summary"], str)
        assert item["summary"].strip()
        assert item["review_status"] in VALID_TREND_REVIEW_STATUS
        window_days.add(item["window_days"])

    assert window_days == {7, 30, 90}


def test_site_map_schema() -> None:
    site_map = load_json("site_map.json")
    assert isinstance(site_map, list)
    assert site_map

    for index, item in enumerate(site_map):
        assert isinstance(item, dict), f"site_map item #{index} must be an object"
        for field in ["title", "path", "level", "description"]:
            assert field in item, f"site_map item #{index} missing {field}"
        assert isinstance(item["title"], str)
        assert isinstance(item["path"], str)
        assert item["path"].endswith(".html")
        assert_number(item["level"], "level")
        assert isinstance(item["description"], str)


def test_site_map_includes_hotspot_map_page() -> None:
    site_map = load_json("site_map.json")
    paths = {item["path"] for item in site_map}
    assert "./map.html" in paths


def test_open_data_inventory_and_review_queue_statuses() -> None:
    inventory = load_json("open_data_url_inventory.json")
    review_queue = load_json("open_data_url_review_queue.json")
    readiness = load_json("open_data_readiness_report.json")
    top10 = load_json("open_data_top10_review_tasks.json")
    crawler_specs = load_json("open_data_crawler_spec_drafts.json")
    human_review = load_json("open_data_human_review_workbook.json")
    assert inventory["public_use_status"] == "internal_url_inventory"
    assert review_queue["public_use_status"] == "internal_url_review_queue"
    assert readiness["public_use_status"] == "internal_readiness_report"
    assert top10["public_use_status"] == "internal_top10_review_tasks"
    assert crawler_specs["public_use_status"] == "internal_crawler_spec_drafts"
    assert human_review["public_use_status"] == "internal_human_review_workbook"


def test_no_sensitive_field_names_in_dashboard_json() -> None:
    violations = []
    for path in DASHBOARD_DATA_DIR.glob("*.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        for item in walk_json(data):
            for key in item.keys():
                if str(key).lower() in SENSITIVE_FIELD_NAMES:
                    violations.append(f"{path.relative_to(ROOT)} contains sensitive field: {key}")

    assert not violations, "\n".join(violations)


def test_optional_trend_values_are_valid() -> None:
    violations = []
    for path in DASHBOARD_DATA_DIR.glob("*.json"):
        data = json.loads(path.read_text(encoding="utf-8"))
        for item in walk_json(data):
            if "trend" in item and item["trend"] not in VALID_TRENDS:
                violations.append(
                    f"{path.relative_to(ROOT)} has invalid trend value: {item['trend']}"
                )

    assert not violations, "\n".join(violations)

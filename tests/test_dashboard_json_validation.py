import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DASHBOARD_DATA_DIR = ROOT / "dashboard" / "data"

REQUIRED_JSON_FILES = [
    "dashboard_summary.json",
    "issue_ranking.json",
    "hotspots.json",
    "local_place_dictionary.json",
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

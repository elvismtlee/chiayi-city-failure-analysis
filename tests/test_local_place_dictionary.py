import json
from pathlib import Path


DICTIONARY_PATH = Path("dashboard/data/local_place_dictionary.json")

REQUIRED_FIELDS = {
    "place_id",
    "display_name",
    "local_name",
    "formal_name",
    "aliases",
    "avoid_terms",
    "district",
    "place_type",
    "issue_tags",
    "geo_precision",
    "public_note",
    "updated_at",
}

BANNED_DISPLAY_TERMS = {
    "文化路夜市",
    "嘉義市中心夜市區",
    "嘉義著名夜市觀光區",
}

VALID_GEO_PRECISIONS = {
    "exact_address",
    "intersection",
    "road_segment",
    "landmark",
    "village",
    "district",
    "city",
    "unknown",
}


def load_dictionary():
    repo_root = Path(__file__).resolve().parents[1]
    dictionary_file = repo_root / DICTIONARY_PATH
    return json.loads(dictionary_file.read_text(encoding="utf-8"))


def test_local_place_dictionary_is_list():
    data = load_dictionary()
    assert isinstance(data, list)
    assert data, "local_place_dictionary.json should not be empty"


def test_local_place_dictionary_required_fields():
    data = load_dictionary()
    violations = []

    for index, item in enumerate(data):
        missing = REQUIRED_FIELDS - set(item.keys())
        if missing:
            violations.append(f"item #{index} missing fields: {sorted(missing)}")

    assert not violations, "\n".join(violations)


def test_local_place_dictionary_unique_place_ids():
    data = load_dictionary()
    place_ids = [item["place_id"] for item in data]
    duplicated = sorted({place_id for place_id in place_ids if place_ids.count(place_id) > 1})
    assert not duplicated, f"Duplicated place_id values: {duplicated}"


def test_local_place_dictionary_display_names_do_not_use_banned_terms():
    data = load_dictionary()
    violations = []

    for item in data:
        display_name = item.get("display_name", "")
        local_name = item.get("local_name", "")
        formal_name = item.get("formal_name", "") or ""
        for banned in BANNED_DISPLAY_TERMS:
            if banned in display_name or banned in local_name or banned in formal_name:
                violations.append(
                    f"{item.get('place_id')} uses banned term '{banned}' in display/local/formal name"
                )

    assert not violations, "\n".join(violations)


def test_local_place_dictionary_list_fields_are_lists():
    data = load_dictionary()
    violations = []

    for item in data:
        for field in ("aliases", "avoid_terms", "issue_tags"):
            if not isinstance(item.get(field), list):
                violations.append(f"{item.get('place_id')} field '{field}' must be a list")

    assert not violations, "\n".join(violations)


def test_local_place_dictionary_geo_precision_is_valid():
    data = load_dictionary()
    violations = []

    for item in data:
        geo_precision = item.get("geo_precision")
        if geo_precision not in VALID_GEO_PRECISIONS:
            violations.append(
                f"{item.get('place_id')} has invalid geo_precision: {geo_precision}"
            )

    assert not violations, "\n".join(violations)


def test_wenhua_road_entry_uses_local_name():
    data = load_dictionary()
    matching = [item for item in data if item.get("place_id") == "place-wenhua-road-business-district"]
    assert matching, "Missing Wenhua Road business district entry"

    item = matching[0]
    assert item["display_name"] == "文化路商圈"
    assert item["local_name"] == "文化路"
    assert "文化路夜市" in item["avoid_terms"]

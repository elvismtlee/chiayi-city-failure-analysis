import csv
from pathlib import Path


CSV_PATH = Path("data/reference/place_name_review_sample.csv")

REQUIRED_COLUMNS = {
    "review_id",
    "raw_name",
    "suggested_display_name",
    "local_name",
    "formal_name",
    "district",
    "place_type",
    "aliases",
    "avoid_terms",
    "issue_tags",
    "geo_precision",
    "source",
    "review_status",
    "reviewer",
    "reviewed_at",
    "notes",
}

VALID_REVIEW_STATUS = {"pending", "reviewed", "approved", "rejected"}
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
VALID_PLACE_TYPES = {
    "business_district",
    "market",
    "station",
    "road_segment",
    "school_area",
    "park",
    "public_space",
    "other",
}
BANNED_DISPLAY_TERMS = {
    "文化路夜市",
    "嘉義市中心夜市區",
    "嘉義著名夜市觀光區",
}


def load_rows():
    repo_root = Path(__file__).resolve().parents[1]
    csv_file = repo_root / CSV_PATH
    with csv_file.open("r", encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def test_place_name_review_sample_has_required_columns():
    repo_root = Path(__file__).resolve().parents[1]
    csv_file = repo_root / CSV_PATH
    with csv_file.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        columns = set(reader.fieldnames or [])

    missing = REQUIRED_COLUMNS - columns
    assert not missing, f"Missing required columns: {sorted(missing)}"


def test_place_name_review_sample_has_rows():
    rows = load_rows()
    assert rows, "place_name_review_sample.csv should not be empty"


def test_review_ids_are_unique():
    rows = load_rows()
    review_ids = [row["review_id"] for row in rows]
    duplicated = sorted({rid for rid in review_ids if review_ids.count(rid) > 1})
    assert not duplicated, f"Duplicated review_id values: {duplicated}"


def test_review_status_values_are_valid():
    rows = load_rows()
    violations = []
    for row in rows:
        status = row.get("review_status", "")
        if status not in VALID_REVIEW_STATUS:
            violations.append(f"{row.get('review_id')} invalid review_status: {status}")
    assert not violations, "\n".join(violations)


def test_geo_precision_values_are_valid():
    rows = load_rows()
    violations = []
    for row in rows:
        geo_precision = row.get("geo_precision", "")
        if geo_precision not in VALID_GEO_PRECISIONS:
            violations.append(f"{row.get('review_id')} invalid geo_precision: {geo_precision}")
    assert not violations, "\n".join(violations)


def test_place_type_values_are_valid():
    rows = load_rows()
    violations = []
    for row in rows:
        place_type = row.get("place_type", "")
        if place_type not in VALID_PLACE_TYPES:
            violations.append(f"{row.get('review_id')} invalid place_type: {place_type}")
    assert not violations, "\n".join(violations)


def test_suggested_display_name_does_not_use_banned_terms():
    rows = load_rows()
    violations = []
    for row in rows:
        display_name = row.get("suggested_display_name", "")
        for banned in BANNED_DISPLAY_TERMS:
            if banned in display_name:
                violations.append(
                    f"{row.get('review_id')} suggested_display_name contains banned term: {banned}"
                )
    assert not violations, "\n".join(violations)


def test_approved_rows_have_reviewer_and_reviewed_at():
    rows = load_rows()
    violations = []
    for row in rows:
        if row.get("review_status") == "approved":
            if not row.get("reviewer") or not row.get("reviewed_at"):
                violations.append(
                    f"{row.get('review_id')} approved row must include reviewer and reviewed_at"
                )
    assert not violations, "\n".join(violations)

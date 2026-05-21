import argparse
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = ROOT / "data" / "reference" / "place_name_review_sample.csv"
DEFAULT_OUTPUT = ROOT / "dashboard" / "data" / "local_place_dictionary.json"

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


def split_list(value: str) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def make_place_id(row: dict[str, str]) -> str:
    review_id = row.get("review_id", "").strip()
    return f"place-{review_id.replace('review-', '')}"


def validate_columns(fieldnames: list[str] | None) -> None:
    if not fieldnames:
        raise ValueError("CSV file has no header")
    missing = REQUIRED_COLUMNS - set(fieldnames)
    if missing:
        raise ValueError(f"Missing required columns: {sorted(missing)}")


def validate_approved_row(row: dict[str, str]) -> None:
    display_name = row.get("suggested_display_name", "").strip()
    if not display_name:
        raise ValueError(f"{row.get('review_id')} missing suggested_display_name")
    for banned in BANNED_DISPLAY_TERMS:
        if banned in display_name:
            raise ValueError(
                f"{row.get('review_id')} suggested_display_name contains banned term: {banned}"
            )
    if not row.get("district", "").strip():
        raise ValueError(f"{row.get('review_id')} missing district")
    if not row.get("place_type", "").strip():
        raise ValueError(f"{row.get('review_id')} missing place_type")
    geo_precision = row.get("geo_precision", "").strip()
    if geo_precision not in VALID_GEO_PRECISIONS:
        raise ValueError(f"{row.get('review_id')} invalid geo_precision: {geo_precision}")


def row_to_dictionary_entry(row: dict[str, str]) -> dict:
    validate_approved_row(row)
    display_name = row["suggested_display_name"].strip()
    local_name = row.get("local_name", "").strip() or display_name
    formal_name = row.get("formal_name", "").strip() or display_name
    reviewed_at = row.get("reviewed_at", "").strip()

    return {
        "place_id": make_place_id(row),
        "display_name": display_name,
        "local_name": local_name,
        "formal_name": formal_name,
        "aliases": split_list(row.get("aliases", "")),
        "avoid_terms": split_list(row.get("avoid_terms", "")),
        "district": row["district"].strip(),
        "place_type": row["place_type"].strip(),
        "issue_tags": split_list(row.get("issue_tags", "")),
        "geo_precision": row["geo_precision"].strip(),
        "public_note": row.get("notes", "").strip(),
        "updated_at": reviewed_at or "unknown",
    }


def load_existing_dictionary(path: Path) -> list[dict]:
    if not path.exists():
        return []
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        raise ValueError(f"Existing dictionary must be a list: {path}")
    return data


def merge_entries(existing: list[dict], imported: list[dict]) -> list[dict]:
    merged = {item["place_id"]: item for item in existing}
    for item in imported:
        merged[item["place_id"]] = item
    result = list(merged.values())
    place_ids = [item["place_id"] for item in result]
    duplicated = sorted({place_id for place_id in place_ids if place_ids.count(place_id) > 1})
    if duplicated:
        raise ValueError(f"Duplicated place_id values: {duplicated}")
    return result


def import_review_csv(source: Path, existing_dictionary_path: Path | None = None) -> list[dict]:
    with source.open("r", encoding="utf-8-sig", newline="") as csv_file:
        reader = csv.DictReader(csv_file)
        validate_columns(reader.fieldnames)
        imported = [
            row_to_dictionary_entry(row)
            for row in reader
            if row.get("review_status", "").strip() == "approved"
        ]

    existing = load_existing_dictionary(existing_dictionary_path) if existing_dictionary_path else []
    return merge_entries(existing, imported)


def write_dictionary(path: Path, data: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Import approved place-name review CSV rows.")
    parser.add_argument("--source", type=Path, default=DEFAULT_SOURCE)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    parser.add_argument("--replace", action="store_true", help="Replace output instead of merging existing dictionary.")
    args = parser.parse_args()

    existing_path = None if args.replace else args.output
    data = import_review_csv(args.source, existing_path)
    write_dictionary(args.output, data)
    print(f"Imported {len(data)} place dictionary entries to {args.output}")


if __name__ == "__main__":
    main()

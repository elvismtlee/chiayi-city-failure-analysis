import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts.import_place_name_review import import_review_csv


FIELDNAMES = [
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
]


def write_review_csv(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8-sig", newline="") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def base_row(**overrides) -> dict[str, str]:
    row = {
        "review_id": "review-9001",
        "raw_name": "測試地名附近",
        "suggested_display_name": "測試地名周邊",
        "local_name": "測試地名",
        "formal_name": "測試地名",
        "district": "西區",
        "place_type": "landmark",
        "aliases": "測試地名附近,測試地名一帶",
        "avoid_terms": "外地錯誤名稱",
        "issue_tags": "traffic,parking",
        "geo_precision": "landmark",
        "source": "人工",
        "review_status": "approved",
        "reviewer": "在地確認",
        "reviewed_at": "2026-05-21",
        "notes": "測試備註",
    }
    row.update(overrides)
    return row


def test_import_review_csv_imports_only_approved_rows(tmp_path: Path) -> None:
    source = tmp_path / "review.csv"
    write_review_csv(
        source,
        [
            base_row(review_id="review-9001", suggested_display_name="核准地名"),
            base_row(review_id="review-9002", suggested_display_name="待確認地名", review_status="pending"),
        ],
    )

    data = import_review_csv(source)

    assert [item["display_name"] for item in data] == ["核准地名"]
    assert data[0]["place_id"] == "place-9001"


def test_import_review_csv_converts_csv_lists_to_arrays(tmp_path: Path) -> None:
    source = tmp_path / "review.csv"
    write_review_csv(source, [base_row()])

    data = import_review_csv(source)
    item = data[0]

    assert item["aliases"] == ["測試地名附近", "測試地名一帶"]
    assert item["avoid_terms"] == ["外地錯誤名稱"]
    assert item["issue_tags"] == ["traffic", "parking"]


def test_import_review_csv_rejects_banned_display_name(tmp_path: Path) -> None:
    source = tmp_path / "review.csv"
    banned = "\u6587\u5316\u8def\u591c\u5e02"
    write_review_csv(source, [base_row(suggested_display_name=banned)])

    try:
        import_review_csv(source)
    except ValueError as exc:
        assert "suggested_display_name contains banned term" in str(exc)
    else:
        raise AssertionError("Expected ValueError for banned display name")


def test_import_review_csv_requires_valid_geo_precision(tmp_path: Path) -> None:
    source = tmp_path / "review.csv"
    write_review_csv(source, [base_row(geo_precision="too_precise")])

    try:
        import_review_csv(source)
    except ValueError as exc:
        assert "invalid geo_precision" in str(exc)
    else:
        raise AssertionError("Expected ValueError for invalid geo_precision")

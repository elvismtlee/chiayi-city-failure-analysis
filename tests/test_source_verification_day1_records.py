from pathlib import Path
import json


ROOT = Path(__file__).resolve().parents[1]
DATA_FILE = ROOT / "dashboard" / "data" / "source_verification_day1_records.json"
DOC_FILE = ROOT / "docs" / "source_verification_day1_records.md"
PAGE = ROOT / "dashboard" / "source-verification-workspace.html"

MAIN_FIELDS = [
    "source_title",
    "source_owner",
    "source_url",
    "is_official_source",
    "data_format",
    "visible_fields",
    "privacy_risk",
    "recommended_next_action",
]


def test_source_verification_day1_records_exist_and_have_three_records() -> None:
    assert DATA_FILE.exists()
    payload = json.loads(DATA_FILE.read_text(encoding="utf-8"))
    records = payload.get("records", [])
    assert len(records) >= 3

    for record in records:
        for field in MAIN_FIELDS:
            assert field in record
        assert record["crawler_execution_allowed"] is False
        assert record["engineering_review_allowed"] is False
        assert record["approved_for_crawling"] is False


def test_source_verification_day1_docs_exist() -> None:
    assert DOC_FILE.exists()
    content = DOC_FILE.read_text(encoding="utf-8")
    assert "今天要看哪 3 筆" in content
    assert "不把任何資料標成 `approved_for_crawling`" in content


def test_source_verification_workspace_links_day1_records() -> None:
    content = PAGE.read_text(encoding="utf-8")
    assert "Day 1 第一批 3 筆資料源" in content
    assert "./data/source_verification_day1_records.json" in content
    assert "../docs/source_verification_day1_records.md" in content

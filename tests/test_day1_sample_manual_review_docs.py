from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DOC = ROOT / "docs" / "open_data_day1_sample_results" / "day_1_sample_manual_review_results.md"


def test_day1_sample_manual_review_doc_exists() -> None:
    assert DOC.exists()


def test_day1_sample_manual_review_doc_contains_required_text() -> None:
    content = DOC.read_text(encoding="utf-8")
    assert "這是 sample" in content
    assert "不是實際審核結果" in content
    assert "不是 crawler" in content
    assert "不啟動 live crawler" in content
    assert "crawler_execution_allowed" in content
    assert "source_url" in content
    assert "blocked_fields" in content

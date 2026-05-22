from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RUNBOOK = ROOT / "docs" / "cycc_crawler_runbook.md"


def test_cycc_crawler_runbook_exists_and_has_commands() -> None:
    content = RUNBOOK.read_text(encoding="utf-8")
    assert "Crawler 執行手冊" in content
    assert "python scripts/crawl_cycc_public_records.py" in content
    assert "data/raw/cycc_minutes_metadata.csv" in content
    assert "data/raw/cycc_question_video_metadata.csv" in content
    assert "data/processed/cycc_public_records_crawl_report.json" in content
    assert "python -m json.tool" in content

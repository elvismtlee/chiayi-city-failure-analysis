from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PAGE = ROOT / "dashboard" / "cycc-review.html"
SITE_JS = ROOT / "dashboard" / "site-pages.js"


def test_cycc_review_page_exists_with_safety_labels() -> None:
    content = PAGE.read_text(encoding="utf-8")
    assert "CYCC 公開資料審核" in content
    assert "internal metadata" in content
    assert "manual review required" in content
    assert "data-page=\"cycc-review\"" in content
    assert "data-cycc=\"minutes\"" in content
    assert "data-cycc=\"videos\"" in content
    assert "data-cycc=\"total\"" in content


def test_cycc_review_page_is_summary_first() -> None:
    content = PAGE.read_text(encoding="utf-8")
    assert "summary report" in content
    assert "raw CSV" in content
    assert "不自動產生競選文案" in content
    assert "141 筆逐筆 metadata" in content


def test_site_pages_renders_cycc_review_report() -> None:
    content = SITE_JS.read_text(encoding="utf-8")
    assert "renderCyccReview" in content
    assert "cycc_minutes_metadata.csv" in content
    assert "cycc_question_video_metadata.csv" in content
    assert "./data/cycc_public_records_crawl_report.json" in content
    assert "data-cycc=\"total\"" in content
